# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT
import os

import Artus.HarryPlotter.input_modules.inputroot as inputroot

class InputRootZJet(inputroot.InputRoot):

	def modify_argument_parser(self, parser, args):
		super(InputRootZJet, self).modify_argument_parser(parser, args)

		# special arguemnts for custom zjet folder naming conventions
		self.zjet_input_options = parser.add_argument_group("ZJet input options")
		self.zjet_input_options.add_argument("--zjetfolders", type=str, nargs='*', default=None,
		                                help="zjet folders (all, incut....")
		self.zjet_input_options.add_argument("--algorithms", type=str, nargs='*', default=None,
		                                help="jet algorithms.")
		self.zjet_input_options.add_argument("--corrections", type=str, nargs='*', default=None,
		                                help="correction levels.")
		self.zjet_input_options.set_defaults(files=[os.environ.get(x) for x in ['DATA', 'MC']])


	def prepare_args(self, parser, plotData):
		super(InputRootZJet, self).prepare_args(parser, plotData)
		
		# this is needed so one can put together the folder name like in the old
		# merlin plotting
		zjetlist =  ["algorithms", "corrections", "zjetfolders"]
		self.prepare_list_args(plotData, zjetlist)
		if all( [plotData.plotdict[i] != [None] for i in zjetlist]):
			folders = []
			for algo, corr, folder in zip([plotData.plotdict[i] for i in zjetlist]):
				folders.append("%s_%s%s" % (folder, algo, corr))


	def auto_detect_type_and_modify_weight(self, weight, root_files, plotData,
								mc_weight="lumi * weight", data_weight=None):
		""" This function checks the type (data/MC) of the input file(s) and
			modifies the weights accordingly. Actual implementation is
			analysis-specific.
		"""
		types = []
		for root_file in root_files:
			f = ROOT.TFile(root_file)
			types.append(f.Get("Type"))

		if all([typ == 'mc' for typ in types]) and mc_weight is not None:
			if plotData.plotdict['lumi'] == None:
				log.critical("'lumi' is not set, but needed for weights!")
			mc_weight = mc_weight.replace('lumi', str(plotData.plotdict['lumi']))
			log.debug("Automatically add MC weights: %s" % mc_weight)
			return "((%s) * (%s))" % (weight, mc_weight)
		elif all([typ == 'data' for typ in types]) and data_weight is not None:
			log.debug("Automatically add Data weights: %s" % data_weight)
			return "((%s) * (%s))" % (weight, data_weight)
		else:
			return weight
