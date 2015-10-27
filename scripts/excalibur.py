#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is the main analysis program"""

import argparse
import glob
import imp
import json
import os, errno
import shutil
import subprocess
import sys
import time
import socket
import logging

import Artus.Utility.tools as tools

wrapper_logger = logging.getLogger("CORE")
print "Python version:", sys.version_info


class ArtusJSONEncoder(json.JSONEncoder):
	"""
	JSON serializer to convert complex objects for Artus configs

	Any object may provide a representation for use in Artus configs by
	defining an `artus_value` attribute or property.
	"""
	def default(self, obj):
		try:
			return obj.artus_value
		except AttributeError as aerr:
			# reraise any error happening inside the method
			if aerr.message.endswith("object has no attribute 'artus_value'"):
				return json.JSONEncoder.default(self, obj)
			raise

# ZJet Runner

def ZJet():
	"""ZJet modifies and runs the configs"""
	aborted = False
	artus_returncode = 0
	gctime = 0
	options = getoptions()
	if not options.nologo:
		print logo()

	if options.delete:
		try:
			subprocess.call(['go.py', options.work + "/" + options.out + ".conf", "-d all"])
		except Exception as err:
			print "Could not delete currently running jobs"
			print "%s: %s" % (err.__class__.__name__, err)
			sys.exit(1)
		try:
			shutil.rmtree(options.work)
			print "Directory %s deleted." % options.work
		except Exception as err:
			print "Could not delete output directory %s" % options.work
			print "%s: %s" % (err.__class__.__name__, err)
		sys.exit(0)

	# always make json config unless we resume existing one
	if not options.isjson and not options.resume:
		conf = import_config(options.cfg, options.config_mods)
		conf["InputFiles"] = createFileList(conf["InputFiles"], options.fast)
		if conf["OutputPath"] == "out":
			conf["OutputPath"] = options.out + '.root'
		if options.skip:
			conf['FirstEvent'] = options.skip
		if options.nevents:
			conf['ProcessNEvents'] = options.nevents
		writeJson(conf, options.json)
		wrapper_logger.info("%d pipelines configured, written to %s", len(conf["Pipelines"]), options.json)
	# get an existing one
	else:
		with open(options.json) as config_json:
			conf = json.load(config_json)
		cli_conf_options = ("skip", "nevents")
		if any(getattr(options, attr, False) for attr in cli_conf_options):
			print "Resuming run, ignoring CLI options:", ", ".join(getattr(options, attr) for attr in cli_conf_options if getattr(options, attr, False))

	if options.printconfig:
		print "json config:"
		print json.dumps(conf, sort_keys=True, indent=4, separators=(',', ': '), cls=ArtusJSONEncoder)
	# exit here if json config was the only aim
	if options.config:
		sys.exit(0)

	if not options.isjson and not options.resume:
		Kappacompiled = False

	# Now the config .json is ready and we can run zjet
	if options.batch:
		if not options.resume:
			prepare_wkdir_parent(options.work, options.out, options.clean)
			writeDBS(conf["InputFiles"], options.out, options.work + "/files.dbs")
			populate_workdir(artus_json=options.json, workdir_path=options.work)
			outpath = createGridControlConfig(conf, options.work + "/" + options.out + ".conf", timestamp = options.timestamp, batch=options.batch, jobs=options.jobs, files_per_job=options.files_per_job)

		outpath = options.work + "out/*.root"

		print "go.py %s/%s.conf" % (options.work, options.out)
		gctime = time.time()
		try:
			subprocess.check_call(['go.py', options.work + "/" + options.out + ".conf"])
		except OSError:
			print "Could not start grid-control! Do you have the grid-control directory in you PATH?"
			sys.exit(1)
		except KeyboardInterrupt:
			sys.exit(0)
		except subprocess.CalledProcessError:
			print "grid-control run failed"
			sys.exit(1)
		gctime = time.time() - gctime

		if glob.glob(outpath):
			subprocess.call(['hadd', options.work + 'out.root'] + glob.glob(outpath))
		else:
			print "Batch job did not produce output %s. Exit." % outpath
			sys.exit(1)

		try:
			print "Symlink to output file created: ", "%s/work/%s.root" % (getEnv(), options.out)
			if not os.path.exists(getEnv() + "/work/"):
				os.makedirs(getEnv() + "/work/")
			os.symlink(options.work + "out.root", "%s/work/%s.root" % (getEnv(), options.out))
		except OSError, e:
			if e.errno == errno.EEXIST:
				os.remove("%s/work/%s.root" % (getEnv(), options.out))
				os.symlink(options.work + "out.root", "%s/work/%s.root" % (getEnv(), options.out))
		except:
			print "Could not create symlink."

	else:  # local
		if not options.fast and len(conf["InputFiles"])>100:
			print "Warning: The full run as a single job will take a while.",
			print "Are you sure? [Y/n]"
			try:
				if raw_input() == "n":
					sys.exit(0)
			except KeyboardInterrupt:
				sys.exit(0)
		try:
			child = subprocess.Popen(["artus", options.json] + (["--log-level", options.artus_log_level] if options.artus_log_level is not None else []))
			streamdata = child.communicate()[0]
			artus_returncode = child.returncode
		except KeyboardInterrupt:
			aborted = True
			print '\33[31m%s\033[0m' % "zjet run was aborted prematurely."

	# show message and optionally open root file
	if artus_returncode != 0:
		showMessage("Excalibur", "zjet run with config " + options.out + " FAILED!", fail=True)
	elif aborted:
		showMessage("Excalibur", "zjet run with config " + options.out + " aborted.")
	else:
		showMessage("Excalibur", "zjet run with config " + options.out + " done.")
	if options.root and not aborted:
		print "\nOpen output file in TBrowser:"
		try:
			subprocess.call(["rot",
				"%s/%s.root" % (options.base, options.out)])
		except:
			pass
	return gctime


def import_config(config_file, config_mods):
	"""
	Import a configuration from file
	"""
	config_module = imp.load_source("config", config_file)
	config = config_module.config()
	for mod_idx, mod_file in enumerate(config_mods):
		mod_module = imp.load_source("config_mod%s" % mod_idx, mod_file)
		config = mod_module.modify_config(config)
	return config


# ZJet Options


def getoptions(configdir=None, name='excalibur'):
	"""Set standard options and read command line arguments. """
	if configdir is None:
		configdir = tools.get_environment_variable("EXCALIBURCONFIGS")
	config_dirs = configdir.split(':')
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="%(prog)s is the main analysis program.",
		epilog="""
Config files must provide a function
	`config() -> dict`.
Config mod files must provide a function
	`modify_config(config: dict) -> dict`.

Have fun. ;)
"""
	)
	# config file
	parser.add_argument('cfg', metavar='cfg', type=str, nargs='?', default=None,
		help="config file (.py or .py.json)" +
			 " - path: %s and .py can be omitted. No config implies mc -f" % configdir)
	parser.add_argument('config_mods', metavar='cfg_mod', type=str, nargs='*', default=[],
		help="config modifier")
	# options
	parser.add_argument('-c', '--config', action='store_true',
		help="produce json config only")
	parser.add_argument('-C', '--clean', action='store_true',
		help="delete old outputs but one with the same name")
	parser.add_argument('-f', '--fast', type=int, nargs='*', default=None,
		help="limit number of input files. 3=files[-3:], 5 6=files[5:6].")
	parser.add_argument('-l', '--nologo', action='store_true',
		help="do not print the logo")
	parser.add_argument('-o', '--out', type=str, default=None,
		help="specify custom output name (default: config name)")
	parser.add_argument('-p', '--printconfig', action='store_true',
		help="print json config (long output)")
	parser.add_argument('-s', '--skip', type=int, default=None,
		help="skip the first n events.")
	parser.add_argument('-n', '--nevents', type=int, default=None,
		help="process only n events.")
	parser.add_argument('-v', '--verbose', action='store_true',
		help="verbosity")
	parser.add_argument('-r', '--root', action='store_true',
		help="open output file in ROOT TBrowser after completion")
	parser.add_argument('--log-level', metavar="{artus|core|conf|cache}:{debug,info,warning,error,critical}",
		default=["cache:critical", "core:info", "conf:info"],
		help="Verbosity of logging. Category is optional and defaults to artus.", nargs='+')

	batch_parser = parser.add_argument_group("batch processing arguments", "Deploy analysis to a cluster using grid-control.")
	batch_parser.add_argument('-b', '--batch', type=str, nargs='?', default=False,
		const=('naf' if 'naf' in socket.gethostname() else 'ekpsg'),
		help="use batch mode with optional base config "
			 "'ekpcluster', 'ekpsg', 'ekpcloud', 'naf' or 'local' [Default: %(const)s]")
	batch_parser.add_argument('-R', '--resume', action='store_true',
		help="resume the grid-control run and hadd after interrupting it.")
	batch_parser.add_argument('-d', '--delete', action='store_true',
		help="delete the latest output and jobs still running")
	batch_parser.add_argument('-w', '--work', type=str, nargs=1, default=None,
		help="specify custom work path (default from $EXCALIBUR_WORK variable")
	batch_parser.add_argument('-j', '--jobs', type=int, default=None,
		help="set the number of jobs to use")
	batch_parser.add_argument('--files-per-job', type=int, default=None,
		help="set the number of files per job (overwrites -j|--jobs)")

	opt = parser.parse_args()

	# logging
	logging.basicConfig(level=logging.WARNING, stream=sys.stderr, format="%(name)5s: %(message)s")
	opt.artus_log_level = None
	for log_str in opt.log_level:
		logger, _, level = log_str.upper().rpartition(":")
		assert level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], "valid python/c++ log level required"
		logging.getLogger(logger).level = getattr(logging, level)
		if logger in ("", "ARTUS"):
			opt.artus_log_level = level.lower()
	# test mode
	if opt.cfg is None:
		opt.cfg = 'mc'
		if not opt.fast and not opt.batch and not opt.config:
			opt.fast = [3]
	# derive config file names
	opt.cfg = resolve_config(opt.cfg, config_dirs)
	opt.config_mods = [resolve_config(config_mod, config_dirs) for config_mod in opt.config_mods]
	# set paths for libraries and outputs
	if not opt.out:
		opt.out = get_config_nick(opt.cfg, opt.config_mods)
	# derive json config file name
	opt.isjson = (opt.cfg[-8:] == '.py.json')
	opt.json = os.path.join(os.path.dirname(opt.cfg), opt.out + '.py.json')
	if opt.isjson:
		opt.cfg = opt.cfg[:-8]

	# derive omitted values for fast and skip
	if opt.fast == []:
		opt.fast = [3]
	if opt.fast and len(opt.fast) == 1:
		opt.fast = [-opt.fast[0], None]

	# workdirs
	if not opt.work:
		opt.work = getEnv('EXCALIBUR_WORK', True) or getEnv()
	opt.work = os.path.join(opt.work, name, opt.out)
	if not opt.resume and not opt.delete:
		opt.timestamp = time.strftime("_%Y-%m-%d_%H-%M")
	else:
		paths = glob.glob(opt.work + "_20*")
		paths.sort()
		try:
			opt.timestamp = paths[-1][-17:]
		except:
			print "No existing output directory available!"
			sys.exit(1)
	opt.work += opt.timestamp + '/'
	if opt.verbose:
		print "Options:"
		print opt
	return opt


def resolve_config(config_name, config_dirs):
	if config_name is None:
		return None
	if os.path.isfile(config_name):
		return config_name
	if '/' not in config_name:
		add_ext = '' if os.path.splitext(config_name)[1] else '.py'
		for cdir in config_dirs:
			candidate_file = os.path.join(cdir, config_name + add_ext)
			if os.path.isfile(candidate_file):
				return candidate_file
	raise ValueError("Config '%s' does not exist." % config_name)


def get_config_nick(config, modifiers=()):
	return "".join(
		os.path.splitext(os.path.basename(name))[0] for name in
		([config] + list(modifiers))
	)


# ZJet Tools


def getEnv(variable='EXCALIBURPATH', nofail=False):
	try:
		return os.environ[variable]
	except:
		print variable, "is not in shell variables:", os.environ.keys()
		print "Please source scripts/ini_excalibur.sh and CMSSW!"
		if nofail:
			return None
		sys.exit(1)


def writeJson(settings, filename):
	with open(filename, 'w') as f:
		json.dump(settings, f, sort_keys=True, indent=4, separators=(',', ': '), cls=ArtusJSONEncoder)


def copyFile(source, target, replace={}):
	with open(source) as f:
		text = f.read()
	for a, b in replace.items():
		text = text.replace(a, b)
	with open(target, 'wb') as f:
		f.write(text)
	return text


def writeDBS(input_files, nickname, dbsfile_name):
	"""
	Create a DBS file of all input files

	:param input_files: files to process
	:type input_files: list[str]
	:param nickname: name of the run
	:type nickname: str
	:param dbsfile_name: name (and path) to write DBS information to
	:type dbsfile_name: str
	"""
	file_prefix = os.path.dirname(os.path.commonprefix(input_files))
	# ordering is important in the .dbs file format
	with open(dbsfile_name, 'wb') as f:
		f.write("[" + nickname + "]\n")
		f.write("nickname = " + nickname + "\n")
		f.write("events = " + str(-len(input_files)) + "\n")
		f.write("prefix = " + file_prefix + "\n")
		for input_file in input_files:
			f.write(os.path.relpath(input_file, file_prefix) + " = -1\n")


def createGridControlConfig(settings, filename, original=None, timestamp='', batch="", jobs=None, files_per_job=None):
	if original is None:
		original = getEnv() + '/cfg/gc/gc_{}.conf'.format(batch)
	# guess best job number
	if files_per_job is None:
		# avoid small jobs unless specifically requested
		min_files_per_job = 1 if jobs is not None else 8
		# guess for condor
		if jobs is None and batch == 'ekpsg':
			n_free_slots = get_n_free_slots_ekpsg()
			if n_free_slots >= 32:  # If enough slots available, use all of them. If not, its wiser to use the default number and queue them
				jobs = ( n_free_slots / 8) * 8  # use multiples-of-X for stable job counts (caching)
				print "%d free slots on ekpsg -> submit %d jobs" % (n_free_slots, jobs)

		jobdict = {False: 80, True: 40} # is_data => files per job
		n_jobs = (jobs if jobs is not None else jobdict.get(settings['InputIsData'], 70))
		files_per_job = max((len(settings['InputFiles']) / n_jobs) + 1, min_files_per_job)
	d = {
		'files per job = 100': 'files per job = %d' % files_per_job,
		'@NICK@': settings["OutputPath"][:-5],
		'@TIMESTAMP@': timestamp,
		'$EXCALIBURPATH': getEnv(),
		'$EXCALIBUR_WORK': getEnv('EXCALIBUR_WORK'),
	}

	copyFile(original, filename, d)


def create_runfile(configjson, filename='test.sh', original=None, workpath=None):
	"""
	Create the wrapper for executing excalibur/artus in grid-control

	:param configjson: Artus run json config
	:type configjson: str
	:param filename: path to write wrapper to
	:type filename: str
	:param original: path to template for the wrapper
	:type original: str
	:param workpath: path to GC work directory
	:type workpath: str
	"""
	if original is None:
		original = getEnv() + '/cfg/gc/run-excalibur.sh'
	with open(original) as f:
		text = f.read()
	text = text.replace('@ARTUS_CONFIG@', os.path.basename(configjson))
	text = text.replace('@SCRAM_ARCH@', getEnv('SCRAM_ARCH'))
	text = text.replace('@EXCALIBURPATH@', getEnv())
	text = text.replace('@CMSSW_BASE@', getEnv('CMSSW_BASE'))
	if workpath is not None:
		text = text.replace('@WORKPATH@/', workpath)
	with open(filename, 'wb') as f:
		f.write(text)


def populate_workdir(workdir_path, artus_json):
	"""
	Copy required resources to the working directory
	"""
	print "Populating workdir:", workdir_path
	create_runfile(artus_json, workdir_path + "/run-excalibur.sh", workpath = workdir_path)
	shutil.copy(artus_json, workdir_path)
	# files to transfer: wkdir_subdir => basedir => relpaths
	transfer_dict = {
		"": {
			getEnv(): [
				"cfg/gc/json_modifier.py", "cfg/gc/gc_base.conf",
				"scripts/ini_excalibur.sh", "scripts/artus"
			],
		},
		"lib": {
			getEnv('ARTUSPATH'): [
				"libartus_configuration.so", "libartus_consumer.so",
				"libartus_core.so", "libartus_externalcorr.so",
				"libartus_filter.so", "libartus_kappaanalysis.so",
				"libartus_provider.so", "libartus_utility.so",
				# these should probably be read from a 'KAPPAPATH' - MF@20151016
				"../Kappa/lib/libKappa.so", "../KappaTools/lib/libKPlotTools.so",
				"../KappaTools/lib/libKRootTools.so", "../KappaTools/lib/libKToolbox.so"
			],
			getEnv('BOOSTPATH'): [
				"libboost_regex.so." + getEnv('BOOSTVER').split('-')[0],
				"libboost_program_options.so." + getEnv('BOOSTVER').split('-')[0]
			],
		}
	}
	for wkdir_subdir in transfer_dict:
		if wkdir_subdir:
			os.makedirs(os.path.join(workdir_path, wkdir_subdir))
		for source_basedir in transfer_dict[wkdir_subdir]:
			for relpath in transfer_dict[wkdir_subdir][source_basedir]:
				shutil.copy(os.path.join(source_basedir, relpath), os.path.join(workdir_path, wkdir_subdir))


def showMessage(title, message, fail=False):
	userpc = "%s@%s" % (getEnv('USER'), getEnv('USERPC'))
	iconpath = '/usr/users/dhaitz/excalibur/excal_small{}.jpg'.format('_fail' if fail else '')
	try:
		if 'ekplx' in userpc:
			subprocess.call(['ssh', userpc,
				'DISPLAY=:0 notify-send "%s" "%s" -i %s' % (title, message, iconpath)])
	except:
		pass
	print message


def createFileList(files, fast=False):
	files = getattr(files, "artus_value", files)
	if type(files) == str:
		if "*.root" in files:
			print "Creating file list from", files
			files = glob.glob(files)
			# Direct access to /pnfs is buggy, prepend dcap to file paths
			if 'naf' in socket.gethostname():
				files = ["dcap://dcache-cms-dcap.desy.de/" + f for f in files]
		else:
			files = [files]
	if not files:
		print "No input files found."
		sys.exit(1)
	if fast:
		files = files[fast[0]:fast[1]]
	return files


def prepare_wkdir_parent(work_path, out_name, clean=False):
	"""
	Prepare the parent directory hosting GC work directories

	:param work_path: work directory path, e.g. `"/foo/bar/data15_25ns_2015-09-02_09-04"`
	:type work_path: str
	:param out_name: name of the run, e.g. `"data15_25ns"`
	:type out_name: str
	:param clean: remove old working directories
	:type clean: bool

	:note: The `work_path` can be specified in both `<config>` and
	       `<config>_<run_date>` notation.
	"""
	work_path = work_path if work_path[-1] != '/' else work_path[:-1]
	if "_20" in work_path:  # explicit run work dir path
		paths = sorted(glob.glob(work_path[:-17]+"_20*"))[1:]
	else:  # general task work dir path base
		paths = glob.glob(work_path + "_20*")
	if clean:
		for p in paths:
			if os.path.exists(p):
				print "removing", p
				shutil.rmtree(p)
	elif len(paths) > 1:
		print len(paths), "old output directories for this config. Clean-up recommended."
	print "Output directory:", work_path
	os.makedirs(work_path + "/work." + out_name)


def get_n_free_slots_ekpsg():
	"""Get number of free slots on sg machines."""
	condor = subprocess.Popen(('condor_status'), stdout=subprocess.PIPE)
	output = subprocess.Popen(('egrep', 'ekpsg.*Unclaimed'), stdin=condor.stdout, stdout=subprocess.PIPE)
	return int(subprocess.check_output(('wc', '-l'), stdin=output.stdout))

def format_time(seconds):
	# TODO is there already a built-in python function for this sort of thing?
	if seconds < 180.:
		return "{0:.0f} seconds".format(seconds)
	elif (seconds/60.) < 120.:
		return "{0:.0f} minutes".format(seconds/60.)
	else:
		return "{0:.0f} hours {1:.0f} minutes".format(int(seconds/3600.), (seconds/60. % 60))

def logo():
	return """\
  _______ ___   ___  ______      ___       __       __   ______    __    __   ______
 |   ____|\  \ /  / /      |    /   \     |  |     |  | |   _  \  |  |  |  | |   _  \ 
 |  |__    \  V  / |  ,----'   /  ^  \    |  |     |  | |  |_)  | |  |  |  | |  |_)  |
 |   __|    >   <  |  |       /  /_\  \   |  |     |  | |   _  <  |  |  |  | |      /
 |  |____  /  .  \ |  `----. /  _____  \  |  `----.|  | |  |_)  | |  `--'  | |  |\  \ 
 |_______|/__/ \__\ \______|/__/     \__\ |_______||__| |______/   \______/  | _| \__|
                                                                  (previously CalibFW)
                   (O)
                   <M       The mighty broadsword of cut-based jet studies
        o          <M
       /| ......  /:M\------------------------------------------------,,,,,,
     (O)[]XXXXXX[]I:K+}=====<{H}>================================------------>
       \| ^^^^^^  \:W/------------------------------------------------''''''
        o          <W
                   <W
                   (O)                 Calibrate like a king!
"""

if __name__ == "__main__":
	start_time = time.time()
	gctime = ZJet()
	print "---   Excalibur took {} ---".format(format_time(time.time() - start_time))
	if gctime > 0:
		print "--- GridControl took {} ---".format(format_time(gctime))
