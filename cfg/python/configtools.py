#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""configtools provides the tools to make a valid artus config.

The most used functions are:
  - BaseConfig to generate a default configuration
  - CreateFileList to create a list of input files
  - Run to acutally call artus and run it
"""
import copy
import glob
import socket
import ConfigParser
import os
import stat
import getpass
import json
import sys
import ZJetConfigFunctions


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
	cfg = ZJetConfigFunctions.getBaseConfig(**kwargs)

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
	if string in dir(ZJetConfigFunctions):
		getattr(ZJetConfigFunctions, string)(conf, **kwargs)


def getPath(variable='EXCALIBURPATH', nofail=False):
	try:
		return os.environ[variable]
	except:
		print variable, "is not in shell variables:", os.environ.keys()
		print "Please source scripts/ini_excalibur.sh and CMSSW!"
		if nofail:
			return None
		exit(1)


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
		'nocuts': ['MuonPt', 'MuonEta', 'ElectronPt', 'ElectronEta', 'LeadingJetPt', 'ZPt', 'BackToBack', 'LeadingJetEta', 'Alpha'],
		'zcuts': ['LeadingJetPt', 'BackToBack', 'LeadingJetEta', 'Alpha'],
		'noalphanoetacuts': ['LeadingJetEta', 'Alpha'],
		'noalphacuts': ['Alpha'],
		'noetacuts': ['LeadingJetEta'],
		'finalcuts': [],
	}
	for cutMode in cutModes:
		if cutMode not in modes:
			print "cutMode", cutMode, "not defined!"
			exit(1)
		pipelines[cutMode] = copy.deepcopy(p)
		for cut in ["filter:%sCut" % m for m in modes[cutMode]]:
			if cut in pipelines[cutMode]['Processors']:
				pipelines[cutMode]['Processors'].remove(cut)

	# remove template pipeline
	pipelines.pop(default)

	# copy pipelines with different correction levels, naming scheme: cut_AlgoName + CorrectionLevel
	for name, p in pipelines.items():
		for corrLevel in corrLevels:
			if corrLevel == 'None':
				pipelines[name + "_" + config['TaggedJets'].replace('Tagged', '')] = copy.deepcopy(p)
				pipelines[name + "_" + config['TaggedJets'].replace('Tagged', '')]['CorrectionLevel'] = corrLevel
			else:
				pipelines[name + "_" + config['TaggedJets'].replace('Tagged', '') + corrLevel] = copy.deepcopy(p)
				pipelines[name + "_" + config['TaggedJets'].replace('Tagged', '') + corrLevel]['CorrectionLevel'] = corrLevel
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
			if quantity in cfg['Pipelines'][pipeline]['Quantities']:
				cfg['Pipelines'][pipeline]['Quantities'].remove(quantity)

