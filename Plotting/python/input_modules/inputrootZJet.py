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
		self.zjet_input_options.add_argument("--zjetfolders", type=str, nargs='*', default=['incut'],
		                                help="zjet folders (all, incut....")
		self.zjet_input_options.add_argument("--algorithms", type=str, nargs='*', default=["AK5PFJetsCHS"],
		                                help="jet algorithms.")
		self.zjet_input_options.add_argument("--corrections", type=str, nargs='*', default=["L1L2L3"],
		                                help="correction levels.")
		self.zjet_input_options.set_defaults(files=[os.environ.get(x) for x in ['DATA', 'MC']])


	def prepare_args(self, parser, plotData):
		# this is needed so one can put together the folder name like in the old
		# merlin plotting
		zjetlist =  ["algorithms", "corrections", "zjetfolders"]
		self.prepare_list_args(plotData, zjetlist)
		if plotData.plotdict['folders'] is None:
			if all( [plotData.plotdict[i] != [None] for i in zjetlist]):
				folders = []
				for algo, corr, folder in zip(*[plotData.plotdict[i] for i in zjetlist]):
					folders.append("%s_%s%s" % (folder, algo, corr))
			plotData.plotdict['folders'] = folders

		# automatically set nicks, x-expressions if not explicitly given
		if plotData.plotdict['nicks'] == None and len(set(plotData.plotdict['files'])) > 1:
			plotData.plotdict['nicks'] = [os.path.splitext(os.path.basename(i))[0] for i in plotData.plotdict['files']]
		if plotData.plotdict['x_expressions'] == None:
			plotData.plotdict['x_expressions'] = plotData.plotdict['plot'].split("_")[-1]

		super(InputRootZJet, self).prepare_args(parser, plotData)


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
			if plotData.plotdict.get('lumi', None) == None:
				log.critical("'lumi' is not set, but needed for weights!")
				return weight
			mc_weight = mc_weight.replace('lumi', str(plotData.plotdict['lumi']))
			log.debug("Automatically add MC weights: %s" % mc_weight)
			return "((%s) * (%s))" % (weight, mc_weight)
		elif all([typ == 'data' for typ in types]):
			plotData.plotdict['nolumilabel'] = False
			if data_weight is not None:
				log.debug("Automatically add Data weights: %s" % data_weight)
				return "((%s) * (%s))" % (weight, data_weight)
		return weight
