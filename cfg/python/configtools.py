#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

configtools provides the tools to make a valid artus config.

The most used functions are:

- BaseConfig to generate a default configuration
- CreateFileList to create a list of input files
- Run to acutally call artus and run it
"""
import copy
import socket
import os
import json
import sys
import defaultconfig
import hashlib
import base64
import subprocess

from configutils import config_logger, cache_logger, env_logger
from configutils import get_excalibur_env, getPath, get_cachepath, download_tarball, get_relsubpath, cached_query


def getConfig(inputtype, year, channel, **kwargs):
	"""
	Main function to get a basic config.

	According to the three main categories (type, year, channel), the config
	is modified according to whats specified in ZJetConfigFunctions.
	All combinations of the categories are considered, if config functions are available.
	"""

	# python class/function names cant start with a number -> add '_' to year
	l = [channel, inputtype, '_' + str(year)]
	print "Getting cfg for", channel, inputtype, year
	cfg = defaultconfig.getBaseConfig(**kwargs)

	# iterate over all combinations and call updateConfig(single-entry tuples first):
	for i in l:
		updateConfig(cfg, (i), **kwargs)
	for i in l:
		for j in l:
			updateConfig(cfg, (i, j), **kwargs)
	for i in l:
		for j in l:
			for k in l:
				updateConfig(cfg, (i, j, k), **kwargs)

	# Adjust met input if CHS jets are requested
	if "CHS" in cfg['TaggedJets'] or "Puppi" in cfg['TaggedJets']:
		cfg['Met'] = cfg['Met'] + 'CHS'

	return cfg


def updateConfig(conf, tupl, **kwargs):
	string = "".join(tupl)
	if string in dir(defaultconfig):
		getattr(defaultconfig, string)(conf, **kwargs)


def setInputFiles(ekppath=None, nafpath=None):
	"""Return ekppath if you're at EKP, nafpath if at NAF. """
	d = {'ekp': ekppath, 'naf': nafpath}
	host = socket.gethostname()[:3]
	if host in d:
		if d[host] in [None, '']:
			sys.exit("ERROR: You're at %s, but the path for this skim is not set here!" % host.upper())
		else:
			return d[host]
	else:
		sys.exit("ERROR: Cant determine input file location!")


def changeNamingScheme(cfg, old=True):
	"""Switch back to the old naming scheme or enforce the new one"""
	cfg['TaggedJets'] = 'AK5PFTaggedJetsCHS' if old else 'ak5PFJetsCHS'
	cfg['PileupDensity'] = 'KT6Area' if old else 'pileupDensity'


def expand(config, cutModes, corrLevels, default="default"):
	"""create pipelines for each cut mode and correction level"""
	pipelines = config['Pipelines']
	p = config['Pipelines'][default]
	# define cut variations and copy default pipeline for different cut variations
	# ATTENTION: the modes dictionary contains the cuts which are REMOVED for a certain pipeline
	modes = {
		'nocuts': ['ZPt', 'MuonPt', 'MuonEta', 'ElectronPt', 'ElectronEta', 'LeadingJetPt','BackToBack', 'LeadingJetEta', 'Alpha', 'Beta'],
		'leptoncuts': ['ZPt', 'LeadingJetPt', 'BackToBack', 'LeadingJetEta', 'Alpha', 'Beta'],
		'zcuts': ['LeadingJetPt', 'BackToBack', 'LeadingJetEta', 'Alpha', 'Beta'],
		'noalphanoetacuts': ['LeadingJetEta', 'Alpha', 'Beta'],
		'noalphacuts': ['Alpha', 'Beta'],
		'noetacuts': ['LeadingJetEta', 'Beta'],
		'finalcuts': ['Beta'],
		'betacuts': ['Alpha']
	}
	for cutMode in cutModes:
		if cutMode not in modes:
			print "cutMode", cutMode, "not defined!"
			sys.exit(1)
		pipelines[cutMode] = copy.deepcopy(p)
		for cut in ["filter:%sCut" % m for m in modes[cutMode]]:
			if cut in pipelines[cutMode]['Processors']:
				pipelines[cutMode]['Processors'].remove(cut)
	# remove template pipeline
	pipelines.pop(default)
	# copy pipelines with different correction levels, naming scheme: cut_AlgoName + CorrectionLevel
	for name, p in pipelines.items():
		for corrLevel in corrLevels:
			pipelinename = name + "_" + config['TaggedJets'].replace('Tagged', '').replace('ak','AK') + corrLevel.replace('None','')
			pipelines[pipelinename] = copy.deepcopy(p)
			pipelines[pipelinename]['CorrectionLevel'] = corrLevel
		del pipelines[name]
	return config


def pipelinediff(config, to=None):
	print "Comparing", len(config['Pipelines']), "pipelines:"
	if to == None:
		to = filter(lambda x: 'finalcuts' in x, config['Pipelines'].keys())[0]
	for name, p in config['Pipelines'].items():
		if name != to:
			print "- Compare", name, "to", to
			pipelinediff2(p, config['Pipelines'][to])
	print


def pipelinediff2(p1=None, p2=None):
	for k, v in p1.items():
		if k in p2.keys():
			if p1[k] != p2[k]:
				print "    different %s: %s != %s" % (k, str(p1[k]), str(p2[k]))


def remove_quantities(cfg, quantities):
	for pipeline in cfg['Pipelines']:
		for quantity in quantities:
			try:
				cfg['Pipelines'][pipeline]['Quantities'].remove(quantity)
			except IndexError:
				pass


def add_quantities(cfg, quantities):
	for pipeline in cfg['Pipelines']:
		cfg['Pipelines'][pipeline]['Quantities'].extend(quantities)


# Queries to external data
def get_jec(nickname):
	"""
	Get a specific corrections folder

	:param nickname: name of the JEC, such as `Summer15_25nsV5_MC`
	:type nickname: str
	:returns: JEC string as understood by Artus (`<path/nickname>`)
	"""
	jec_cache_folder = os.path.join(get_cachepath(), "data", "jec", nickname)
	jec_base = cached_query(func=get_jec_force, func_kwargs={"nickname": nickname, "jec_folder": jec_cache_folder}, dependency_folders=[jec_cache_folder])
	config_logger.info("Using JEC %s", jec_base)
	return jec_base


def get_jec_force(nickname, jec_folder=None):
	"""
	Get a specific corrections folder from source

	:param nickname: name of the JEC, such as `Summer15_25nsV5_MC`
	:type nickname: str
	:param jec_folder: folder in which to store JECs
	:type jec_folder: str
	:returns: JEC string as understood by Artus (`<path/nickname>`)

	Supported sources:

	**GitHub JEC Database**
	  https://github.com/cms-jet/JECDatabase/
	"""
	if jec_folder is None:
		jec_folder = os.path.join(getPath(), "data", "jec", nickname)
	config_logger.warning("Fetching JEC %s from %s", nickname, "JECDatabase")
	jec_files = download_tarball("https://github.com/cms-jet/JECDatabase/blob/master/tarballs/%s.tar.gz?raw=true"%nickname, jec_folder)
	config_logger.warning("Retrieved JEC %s", len(jec_files))
	return os.path.join(jec_folder, nickname)


def get_lumi(json_source, min_run=float("-inf"), max_run=float("inf"), normtag="/afs/cern.ch/user/c/cmsbril/public/normtag_json/OfflineNormtagV1.json"):
	"""
	Get the lumi in /pb for a specific set of runs from CMS run JSON
	"""
	cache_key = _lumi_cache_key(json_sources=[json_source], min_run=min_run, max_run=max_run, normtag=normtag)
	cache_dep = [get_relsubpath(path) for path in [json_source] if path is not None]
	lumi = cached_query(
		func=get_lumi_force,
		func_kwargs={"json_source": json_source, "min_run": min_run, "max_run": max_run, "normtag": normtag},
		dependency_files=cache_dep,
		cache_dir=os.path.join(getPath(), "data", "lumi"),
		cache_key=cache_key,
	)
	config_logger.info("Using lumi %.3f/fb", lumi)


def _lumi_cache_key(json_sources, min_run, max_run, normtag):
	"""
	Constructs a verbose key for lumi caches to allow identifying committed data
	"""
	key = "lumi"
	for json_source in json_sources:
		if json_source.endswith(".json") or json_source.endswith(".txt"):
			key += "_jfile-" + os.path.splitext(os.path.basename(json_source))[0]
		else:
			key += "_jstr-" + base64.b32encode(hashlib.sha1(str(json_source)).digest())
	if min_run > float("-inf"):
		key += "_min-" + str(min_run)
	if max_run < float("inf"):
		key += "_max-" + str(max_run)
	if normtag is not None:
		key += "_nt-" + os.path.splitext(os.path.basename(normtag))[0]
	return key


def get_lumi_force(json_source, bril_ssh=None, min_run=float("-inf"), max_run=float("inf"), normtag="/afs/cern.ch/user/c/cmsbril/public/normtag_json/OfflineNormtagV1.json"):
	"""
	Get the integrated luminosity for runs specified in JSONs from `brilcalc`

	:param json_sources: CMS run JSON file or string
	:type json_sources: str
	:param bril_ssh: SSH connection string to a host capable of running `brilcalc`
	:type bril_ssh: str
	:param min_run: minimum run to use
	:type min_run: int
	:param max_run: maximum run to use
	:type max_run: int
	:param normtag: `brilcalc` normtag file
	:type normtag: str
	:returns: integrated luminosity for run ranges in /fb

	:note: the requirement for specifying `bril_ssh` may be dropped in the future
	       if the CMS database becomes externally accessible. Until then, use of
	       SSH is required; a loopback (e.g. `"localhost"`) can be used if `brilcalc`
	       is available locally.
	"""
	if bril_ssh is None:
		bril_ssh = get_excalibur_env("EXCALIBURBRILSSH", default="lxplus.cern.ch")
	# parse jsons so that we can send any file and string input over SSH as run string
	try:
		json_data = json.loads(json_source)
	except ValueError:
		with open(json_source) as json_file:
			json_data = json.load(json_file)
	for run in json_data.keys():
		if not min_run < int(run) < max_run:
			del json_data[run]
	json_string = json.dumps(json_data).replace(r'"', r'')
	if json_string == "{}":
		return 0.0
	# execute brilcalc on a remote host
	config_logger.warning("Querying brilcalc for lumi (via %s)", bril_ssh)
	with open(os.path.join(getPath(), "scripts", "get_lumi.py")) as get_lumi_raw:
		lumi_json_raw = subprocess.check_output([
				"ssh", bril_ssh,
				# stream script directly to remote python interpreter via CLI
				'python -c "%(get_lumi)s" "%(json_string)s" '
				'--lumi-unit "/pb" %(normtag)s' % {
					"get_lumi": get_lumi_raw.read().replace(r'"', r'\"'),
					"json_string": json_string,
					"normtag": "" if normtag is None else ('--normtag "%s"' % normtag),
				}
			])
	lumi_dict = json.loads(lumi_json_raw)
	# query /pb for precision, convert to /fb
	return lumi_dict["totrecorded"]/1000.0
