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
import os
import sys
import defaultconfig

from configutils import config_logger, cache_logger, env_logger
from configutils import get_excalibur_env, getPath, get_cachepath
from configutils import download_tarball, get_relsubpath, cached_query, RunJSON, PUWeights, InputFiles, Lumi


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
	return InputFiles(ekppath=ekppath, nafpath=nafpath)


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
		'nocuts': ['ZPt', 'MuonPt', 'MuonEta', 'ElectronPt', 'ElectronEta', 'LeadingJetPt','BackToBack', 'LeadingJetEta', 'Alpha'],
		'leptoncuts': ['ZPt', 'LeadingJetPt', 'BackToBack', 'LeadingJetEta', 'Alpha'],
		'zcuts': ['LeadingJetPt', 'BackToBack', 'LeadingJetEta', 'Alpha'],
		'noalphanoetacuts': ['LeadingJetEta', 'Alpha'],
		'noalphacuts': ['Alpha'],
		'noetacuts': ['LeadingJetEta'],
		'finalcuts': [],
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
	# copy pipelines with different correction levels, naming scheme: cut + _CorrectionLevel
	for name, p in pipelines.items():
		for corrLevel in corrLevels:
			pipelinename = name + ('' if corrLevel == 'None' else "_" + corrLevel)
			pipelines[pipelinename] = copy.deepcopy(p)
			pipelines[pipelinename]['CorrectionLevel'] = corrLevel
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


# external and calculated data
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
