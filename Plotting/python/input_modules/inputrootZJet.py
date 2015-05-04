# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT
import os

import Artus.HarryPlotter.input_modules.inputroot as inputroot
import Artus.Utility.jsonTools as jsonTools
import Artus.HarryPlotter.utility.roottools as roottools

class InputRootZJet(inputroot.InputRoot):

	def __init__(self):
		super(InputRootZJet, self).__init__()
		self.quantities_replace_dict = {
			'ptbalance': '(jet1pt/zpt)',
			'deltaphizjet1' : '(abs(abs(abs(zphi-jet1phi)-TMath::Pi())-TMath::Pi()))',
			'deltaphizmet' : '(abs(abs(abs(zphi-metphi)-TMath::Pi())-TMath::Pi()))',
		}

	def modify_argument_parser(self, parser, args):
		super(InputRootZJet, self).modify_argument_parser(parser, args)

		# special arguments for custom zjet folder naming conventions
		self.zjet_input_options = parser.add_argument_group("ZJet input options")
		self.zjet_input_options.add_argument("--zjetfolders", type=str, nargs='*', default=['finalcuts'],
		                                help="zjet folders (nocuts, finalcuts....")
		self.zjet_input_options.add_argument("--algorithms", type=str, nargs='*', default=["AK5PFJetsCHS"],
		                                help="jet algorithms.")
		self.zjet_input_options.add_argument("--corrections", type=str, nargs='*', default=["L1L2L3Res"],
		                                help="correction levels.")

		# arguments to quickly switch to full alpha / eta range
		self.zjet_input_options.add_argument("--allalpha", type=str, nargs="?", default="(jet2pt/zpt<0.2)", const="1",
		                                help="If in finalcuts folder, dont apply alpha cut [Default: %(default)s]")
		self.zjet_input_options.add_argument("--alleta", type=str, nargs="?", default="(abs(jet1eta)<1.3)", const="1",
		                                help="If in finalcuts folder, dont apply eta cut [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		# this is needed so one can put together the folder name like in the old
		# merlin plotting
		zjetlist =  ["algorithms", "corrections", "zjetfolders"]
		self.prepare_list_args(plotData, zjetlist)
		if plotData.plotdict['folders'] is None:
			if all( [plotData.plotdict[i] != [None] for i in zjetlist]):
				folders = []
				for algo, corr, folder in zip(*[plotData.plotdict[i] for i in zjetlist]):
					folders.append("%s_%s%s/ntuple" % (folder, algo, corr))
			plotData.plotdict['folders'] = folders

		# automatically set nicks, x-expressions if not explicitly given
		if plotData.plotdict['nicks'] == None and len(set(plotData.plotdict['files'])) > 1:
			plotData.plotdict['nicks'] = [os.path.splitext(os.path.basename(i))[0] for i in plotData.plotdict['files']]
		if plotData.plotdict['x_expressions'] == None:
			plotData.plotdict['x_expressions'] = plotData.plotdict['plot'].split("_")[-1]

		super(InputRootZJet, self).prepare_args(parser, plotData)

		# apply alpha / eta cuts on the fly
		if all([any(key in folder[0] for key in ['incut', 'finalcuts']) for folder in plotData.plotdict['folders']]):
			zjet_cuts = " * ".join([plotData.plotdict['allalpha'], plotData.plotdict['alleta']])
			plotData.plotdict['weights'] = ["({}) * ({})".format(w, zjet_cuts) for w in plotData.plotdict['weights']]
			log.info("Applying default ZJet cuts: {}".format(zjet_cuts))

		# add 'weight' by default to weights by default
		plotData.plotdict['weights'] = ["(weight * {0})".format (weight) for weight in plotData.plotdict['weights']]

		# automatically replace quantity names, eg. ptbalance->jet1pt/zpt
		for axis in ['x', 'y', 'z']:
			for i, item in enumerate(plotData.plotdict['{0}_expressions'.format(axis)]):
				for key, value in self.quantities_replace_dict.iteritems():
					if item != None and key in item:
						plotData.plotdict['{0}_expressions'.format(axis)][i] = plotData.plotdict['{0}_expressions'.format(axis)][i].replace(key, value)

	def scale_histograms(self, plotData):

		# automatically scale mc samples by lumi
		for index, input_config_dict in enumerate(plotData.plotdict['input_json_dicts']):
			if not input_config_dict.get("InputIsData", True):
				plotData.plotdict['scale_factors'][index] *= plotData.plotdict['lumi']

		super(InputRootZJet, self).scale_histograms(plotData)

