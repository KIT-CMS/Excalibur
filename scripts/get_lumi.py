#!/usr/bin/python
# standard library imports
import os
import sys
import json
import subprocess
import argparse
import errno

# third party imports

# application/library imports

CLI = argparse.ArgumentParser(
	description="Get/Calculate integrated luminosity for given runs",
	epilog="This tool uses the brilcalc suite to extract luminosity information,"
	"\nautomating the queries and environment setup."
	"\n"
	"\nThe brilcalc documentation can be found at"
	"\nhttp://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html",
	formatter_class=argparse.RawDescriptionHelpFormatter,
)
CLI_runs = CLI.add_argument_group("run definition")
CLI_runs.add_argument(
	"runs",
	help="runs in CMS JSON file format; either a file path (quoted runs) or raw string (unquoted runs)"
)
CLI_bril = CLI.add_argument_group("brilsw/brilcalc settings")
CLI_bril.add_argument(
	"--brilconda-path",
	default="/afs/cern.ch/cms/lumi/brilconda-1.0.3",
	help="path to the brilconda suite (contains bin and lib directories)"
)
CLI_bril.add_argument(
	"--brilws-path",
	default="~/.local",
	help="pip virtual env of brilws"
)
CLI_bril.add_argument(
	"--lumi-unit",
	default="/pb",
	help="unit of lumi output, e.g. /fb, /pb or 1e39/cm2"
)


def get_bril_env(brilconda_path, brilws_path):
	"""
	Create the env for running bril commands

	:param brilconda_path: path of the brilconda suite (contains bin and lib directories)
	:type brilconda_path: str
	:param brilws_path: pip virtual env of brilws
	:type brilws_path: str
	:returns: env for processes using brilws to run in
	:rtype: dict
	"""
	# construct dedicated env for bril commands
	bril_env = os.environ.copy()
	bril_env["PATH"] = ":".join((
		os.path.join(os.path.expanduser(brilws_path), "bin"),
		os.path.join(os.path.expanduser(brilconda_path), "bin"),
		bril_env["PATH"],
	))
	# make sure brilws is available
	get_proc_output(
		['pip', 'install', '--install-option=--prefix=$HOME/.local', 'brilws'],
		env=bril_env,
	)
	return bril_env


def get_lumi(run_str, bril_env, unit="/pb"):
	"""
	Get the lumi for a specific run string from brilcalc
	"""
	# use CSV output for easier parsing
	bril_out, bril_err = get_proc_output(
		[
			"brilcalc",
			"lumi", "-i", run_str,
			"--output-style", "csv",
			"-u", unit,
		],
		env=bril_env,
	)
	bril_iter, header, values = iter(bril_out.splitlines()), None, None
	while True:
		line = bril_iter.next()
		# we only care about the summary for the runs
		if not line.startswith('#Summary:'):
			continue
		header = bril_iter.next()
		values = bril_iter.next()
		break
	header = header.replace("(%s)" % unit, "")
	header = header[1:].split(",")
	values = [
		float(value) if "." in value else int(value)
		for value in values[1:].split(",")
	]
	return dict(zip(header, values))


def main():
	opts = CLI.parse_args()
	# all bril commands execute with brilws suite
	bril_env = get_bril_env(
		brilconda_path=opts.brilconda_path,
		brilws_path=opts.brilws_path
	)
	lumi_dict = get_lumi(
		run_str=opts.runs,
		bril_env=bril_env,
		unit=opts.lumi_unit,
	)
	print json.dumps(lumi_dict)

# -- Helpers -------------------------------------------------------------------


class CalledProcessError(Exception):
	def __init__(self, returncode, cmd="<unknown>", output=None):
		self.returncode, self.cmd, self.output = returncode, cmd, output

	def __str__(self):
		return "Command '%s' returned non-zero exit status %d" % (self.cmd, self.returncode)


def get_proc_output(*popenargs, **kwargs):
	"""
	Tweaked version of subprocess.check_output (which is not in py2.6 anyways)

	:param popenargs: arguments to Popen
	:param kwargs: keyword arguments to Popen
	:returns: stdout and stderr of the process
	"""
	if 'stdout' in kwargs:
		raise ValueError('stdout argument not allowed, it will be overridden.')
	try:
		process = subprocess.Popen(stdout=subprocess.PIPE, stderr=subprocess.PIPE, *popenargs, **kwargs)
	except OSError as oserr:
		if oserr.errno == errno.ENOENT:
			raise EnvironmentError(
				"Executable for '%s' not found" % kwargs.get("args", popenargs[0])
			)
		else:
			raise
	stdout, stderr = process.communicate()
	if process.poll():  # check retcode != 0
		print stdout, stderr
		raise CalledProcessError(
			returncode=process.poll(),
			cmd=kwargs.get("args", popenargs[0]),
			output=stdout,
		)
	return stdout, stderr

if __name__ == "__main__":
	main()
