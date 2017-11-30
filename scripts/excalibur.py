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
import itertools
import ast
import shlex

wrapper_logger = logging.getLogger("CORE")


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


def group_iter(iterable, n):
	"s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
	return itertools.izip(*[iter(iterable)]*n)


def pair_iter(iterable):
	"""Return pairs from the iterable: s -> (s0,s1), (s2,s3), ..."""
	return group_iter(iterable, 2)


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
		if options.skip:
			conf['FirstEvent'] = options.skip
		if options.nevents:
			conf['ProcessNEvents'] = options.nevents
		for key, value in options.set_opts:
			conf[key] = value
		conf["InputFiles"] = createFileList(conf["InputFiles"], options.fast)
		if options.lfn:
			conf["InputFiles"] = change_lfn(options.lfn, conf["InputFiles"])
		if conf["OutputPath"] == "out":
			conf["OutputPath"] = options.out + '.root'
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
		dump_json(settings=conf, file_obj=sys.stdout)
	# exit here if json config was the only aim
	if options.config:
		sys.exit(0)

	if not options.isjson and not options.resume:
		Kappacompiled = False

	# Now the config .json is ready and we can run zjet
	if options.batch:
		config_path = options.work + "/" + options.out + ".conf"
		if not options.resume:
			prepare_wkdir_parent(options.work, options.out, options.clean)
			lfn_modi = writeDBS(conf["InputFiles"], options.out, options.work + "/files.dbs")
			if options.lfn:
				lfn_modi = options.lfn
			
			populate_workdir(artus_json=options.json, workdir_path=options.work)
			createGridControlConfig(conf, config_path, 
						 timestamp = options.timestamp, 
						 batch=options.batch, 
						 jobs=options.jobs, 
						 files_per_job=options.files_per_job,
						 partition_lfn_modifier=lfn_modi,
						 excalibur_json = os.path.basename(options.json),
						 workdir_path=options.work
						 )
		#output_glob = options.work + "out/*.root"
		output_glob = options.work + "out/"
		if options.parallel_merge is None:
			gctime = run_gc(config_path=config_path, output_glob=output_glob, workdir_path=options.work)
		else:
			gctime = run_gc_pmerge(config_path=config_path, output_glob=output_glob, workdir_path=options.work, mergers=options.parallel_merge)

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
			child = subprocess.Popen(["excalibur", options.json] + (["--log-level", options.artus_log_level] if options.artus_log_level is not None else []))
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


def run_gc(config_path, output_glob, workdir_path):
	"""
	Run a GC job and merge the output

	:param config_path: path to GC config file
	:type config_path: str
	:param output_glob: glob for output files of jobs
	:type output_glob: str
	:param workdir_path: path to Artus workdir
	:type workdir_path: str
	"""
	wrapper_logger.info("running: go.py %s", config_path)
	gctime = time.time()
	try:
		subprocess.check_call(['go.py', config_path])
	except OSError:
		print "Could not start grid-control! Do you have the grid-control directory in $PATH?"
		sys.exit(1)
	except KeyboardInterrupt:
		sys.exit(0)
	except subprocess.CalledProcessError:
		print "grid-control run failed"
		sys.exit(1)
	try: 
		downloadFromSE = False
	  	with open(config_path) as cfg_file:
		  for line in cfg_file:
		    if 'se path =' in line  and 'srm' in line:
		      downloadFromSE = True
		if downloadFromSE:
		  subprocess.check_call(['downloadFromSE.py', config_path,'-o',output_glob,'-s'])
	except KeyboardInterrupt:
		sys.exit(0)
	except subprocess.CalledProcessError:
		print "downloadFromSE.py failed"
		sys.exit(1)	
	
	
	gctime = time.time() - gctime
	print output_glob
	print glob.glob(output_glob+"*.root")
	
	if glob.glob(output_glob):
		wrapper_logger.info("Merging output files")
		subprocess.call(['hadd', workdir_path + 'out.root'] + glob.glob(output_glob+"*.root"))
	else:
		print "Batch job failed to produce any output (%s)" % output_glob
		sys.exit(1)
	return gctime


def run_gc_pmerge(config_path, output_glob, workdir_path, mergers):
	"""
	Run a GC job and merge the output in parallel

	:param config_path: path to GC config file
	:type config_path: str
	:param output_glob: glob for output files of jobs
	:type output_glob: str
	:param workdir_path: path to Artus workdir
	:type workdir_path: str
	:param mergers: number of parallel merge processes
	:type mergers: int
	"""
	wrapper_logger.info("running: go.py %s", config_path)
	gctime = time.time()
	try:
		gc_proc = subprocess.Popen(['go.py', config_path])
	except OSError:
		print "Could not start grid-control! Do you have the grid-control directory in $PATH?"
		sys.exit(1)
	try:
		merge_proc = subprocess.Popen(['auto_hadd.py', workdir_path + 'out.root', '--file-globs', output_glob, '--pid', str(gc_proc.pid), '--mergers', str(mergers)])
	except OSError:
		print "Could not start merger! Do you have the scripts directory in $PATH?"
		sys.exit(1)
	# wait with interruption to allow breaking
	while gc_proc.poll() is None:
		time.sleep(0.5)
	gctime = time.time() - gctime
	if gc_proc.poll() > 0:
		print "grid-control failed with %d", gc_proc.poll()
		sys.exit(gc_proc.poll())
	while merge_proc.poll() is None:
		time.sleep(0.5)
	return gctime
      
def change_lfn(new_lfn, input_files):
	print "Will change lfn (the very begining of the file path) to",new_lfn
	new_input_files = []
	for akt_file in input_files:
	    new_input_files.append(new_lfn+'/store/'+akt_file.split('/store/')[-1])    
	return new_input_files

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
		configdir = getEnv("EXCALIBURCONFIGS")
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
	parser.add_argument('-C', '--clean', action='store_true',
		help="delete old outputs but one with the same name")
	parser.add_argument('-f', '--fast', type=int, nargs='*', default=None,
		help="limit number of input files. 3=files[-3:], 5 6=files[5:6].")
	parser.add_argument('-l', '--nologo', action='store_true',
		help="do not print the logo")
	parser.add_argument('-o', '--out', type=str, default=None,
		help="specify custom output name (default: config name)")
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

	config_parser = parser.add_argument_group("configuration arguments", "Act on or modify the configuration.")
	config_parser.add_argument('-c', '--config', action='store_true',
		help="produce json config only")
	config_parser.add_argument('-p', '--printconfig', action='store_true',
		help="print json config (long output)")
	config_parser.add_argument('--set-opts', nargs='*', metavar="OPTION VALUE", default=[],
		help="Overwrite individual option. Parsed as python expression, falls back to string.")

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
	batch_parser.add_argument('-L', '--lfn', type=str, nargs='?', default=None,
		help="specify custom lfn modifier")
	batch_parser.add_argument('-j', '--jobs', type=int, default=None,
		help="set the number of jobs to use")
	batch_parser.add_argument('--files-per-job', type=int, default=None,
		help="set the number of files per job (overwrites -j|--jobs)")
	batch_parser.add_argument('--parallel-merge', metavar='MERGE_THREADS', type=int, default=None, nargs='?', const=2,
		help="Merge output in parallel while GC is running [Default: %(const)s threads]")

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
	# opt.cfg  : short config name, e.g. data15
	# opt.json : json file name, e.g. data15.py.json
	opt.isjson = (opt.cfg[-8:] == '.py.json')
	if opt.isjson:
		opt.json = opt.cfg
		opt.cfg = opt.cfg[:-8]
	else:
		opt.json = opt.cfg.rstrip('.json').rstrip('.py') + '.py.json'

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
		except IndexError:
			print "No existing output directory available!"
			sys.exit(1)
	opt.work += opt.timestamp + '/'

	# transform overwrite options to python types
	if not len(opt.set_opts) % 2 == 0:
		raise ValueError('Overwrite options must be specified as pairs of OPTION VALUE.')
	set_opts = []
	for option, value in pair_iter(opt.set_opts):
		try:
			set_opts.append((option, ast.literal_eval(value)))
		except (ValueError, SyntaxError):
			set_opts.append((option, value))
	opt.set_opts = set_opts

	if opt.verbose:
		print "Options:"
		key_len = max(map(len, vars(opt).iterkeys()))
		for key, value in vars(opt).iteritems():
			print key.ljust(key_len), "=", value
	return opt


def resolve_config(config_name, config_dirs):
	# return `None` is name is `None`
	if config_name is None:
		return None

	# return the filename directly if the path exists
	if os.path.isfile(config_name):
		return config_name

	# search the paths given in `config_dirs`
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
	with open(filename, 'w') as json_file:
		dump_json(settings, json_file)


def dump_json(settings, file_obj):
	"""Dump JSON to file-like object"""
	json.dump(settings, file_obj, sort_keys=True, indent=4, separators=(',', ': '), cls=ArtusJSONEncoder)


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
	lfn_modi = ''
	file_prefix = os.path.dirname(os.path.commonprefix(input_files))
	short_file_prefix = file_prefix
	if file_prefix.split(':')[0] == 'srm':
	  short_file_prefix = file_prefix[file_prefix.find("/store/"):]
	  lfn_modi = file_prefix[:file_prefix.find("store/")]
	# ordering is important in the .dbs file format
	with open(dbsfile_name, 'wb') as f:
		f.write("[" + nickname + "]\n")
		f.write("nickname = " + nickname + "\n")
		f.write("events = " + str(-len(input_files)) + "\n")
		f.write("prefix = " + short_file_prefix + "\n")
		for input_file in input_files:
			f.write(os.path.relpath(input_file, file_prefix) + " = -1\n")
	return lfn_modi


def createGridControlConfig(settings, filename, original=None, timestamp='', batch="", jobs=None, files_per_job=None, partition_lfn_modifier='', excalibur_json="", workdir_path=None):
	if original is None:
		original = getEnv() + '/cfg/gc/gc_{}.conf'.format(batch)
	# guess best job number
	if files_per_job is None:
		# avoid small jobs unless specifically requested
		min_files_per_job = 1 if jobs is not None else 8
		# guess for condor
		if jobs is None and batch == 'ekpsg':
			n_free_slots = get_n_free_slots_ekpsg()
			print n_free_slots
			if n_free_slots >= 32:  # If enough slots available, use all of them. If not, its wiser to use the default number and queue them
				jobs = n_free_slots  # use multiples-of-X for stable job counts (caching)
				print "%d free slots on ekpsg -> submit %d jobs" % (n_free_slots, jobs)

		jobdict = {False: 800, True: 400} # is_data => files per job
		n_jobs = (jobs if jobs is not None else jobdict.get(settings['InputIsData'], 70))
		files_per_job = max((len(settings['InputFiles']) / n_jobs) + 1, min_files_per_job)
	d = {
		'@FilesPerJob@': '%d' % files_per_job,
		'@PartitionLfnModifier@': "partition lfn modifier = %s " %partition_lfn_modifier,
		'@NICK@': settings["OutputPath"][:-5],
		'@TIMESTAMP@': timestamp,
		'@EXCALIBURJSON@' : excalibur_json,
		'@WORKPATH@' : workdir_path,
		'@EXCALIBUR_SE@' : getEnv('EXCALIBUR_SE'),
		'$EXCALIBURPATH': getEnv('EXCALIBURPATH'),
		'$EXCALIBUR_WORK': getEnv('EXCALIBUR_WORK'),
	}
	copyFile(original, filename, d)
	copyFile("cfg/gc/gc_base.conf", os.path.join(os.path.dirname(filename),"gc_base.conf"), d)

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
				"cfg/gc/json_modifier.py", "cfg/gc/gc_base_usermod.conf", ## usermod will die after all batch scripts have been updated
				"scripts/ini_excalibur.sh"  #, "scripts/artus"
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


def createFileList(infiles, fast=False):
	files_list = getattr(infiles, "artus_value", infiles)
	out_files = []	
	if type(files_list) != list:
		print "Not posilbe to resolve inputfiles format ",str(type(files_list))," must be a str"
	        sys.exit(1)
	for files in files_list:
	  if "*.root" in files:
		print "Creating file list from", files
		if files.split(':')[0] == 'srm':
		  print "Use grid ls tools (gfal2)"
		  gridpath = files.replace("*.root","")
		  import gfal2
		  ctxt = gfal2.creat_context()
		  listdir = ctxt.listdir(gridpath)
		  for f in listdir:
		    if f.endswith('.root'):
		      out_files.append(gridpath + f)
		else:
		  out_files.extend(glob.glob(files))
	  else:
		out_files.append(files)

	if not out_files:
		print "No input files found."
		sys.exit(1)
	if fast:
		out_files = out_files[fast[0]:fast[1]]
	return out_files


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
	condor_constraint = 'CloudSite == "ekpsupermachines"'
	constraint = "condor_status -constraint '%s' -af TotalSlots" % condor_constraint
	condor = subprocess.Popen(shlex.split(constraint), stdout=subprocess.PIPE)
	return int(subprocess.check_output(('wc', '-l'), stdin=condor.stdout))

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
