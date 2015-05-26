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
import Excalibur.Plotting.utility.quantities as quantities
from Excalibur.Plotting.utility.binnings import binnings


class InputRootZJet(inputroot.InputRoot):

	def __init__(self):
		super(InputRootZJet, self).__init__()
		# TODO: put this dict in dedicated module
		self.quantities_replace_dict = quantities.quantities_dict

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

		# if x_bins is e.g. 'zpt', replace string with the values from the binning dictionary
		for axis in ['x', 'y', 'z']:
			if len(plotData.plotdict[axis+'_bins']) == 1 and plotData.plotdict[axis+'_bins'][0] in binnings.keys():
				plotData.plotdict[axis+'_bins'][0] = binnings[plotData.plotdict[axis+'_bins'][0]]

		super(InputRootZJet, self).prepare_args(parser, plotData)

		# add 'weight' by default to weights
		plotData.plotdict['weights'] = ["(weight * {0})".format(weight) for weight in plotData.plotdict['weights']]

		# add lumi as weight for mc files
		if any([d.get('InputIsData', False) for d in plotData.input_json_dicts]):
			for i, rootfile in enumerate(plotData.plotdict['files']):
				if plotData.input_json_dicts[i] is not None and not plotData.input_json_dicts[i].get('InputIsData', True):
					log.info("Scaling sample by lumi: {0}".format(plotData.plotdict['lumis'][0]))
					plotData.plotdict['weights'][i] = "(({1}) * ({0}))".format(plotData.plotdict['weights'][i], plotData.plotdict['lumis'][0])

		# automatically replace quantity names, eg. ptbalance->jet1pt/zpt
		for axis in ['x', 'y', 'z']:
			for i, item in enumerate(plotData.plotdict['{0}_expressions'.format(axis)]):
				for key, value in self.quantities_replace_dict.iteritems():
					if item != None and key in item:
						if plotData.plotdict.get(axis+"_label", None) is None and len(set(plotData.plotdict[axis+"_expressions"]))==1:
							plotData.plotdict[axis+"_label"] = plotData.plotdict[axis+"_expressions"][0]
						plotData.plotdict['{0}_expressions'.format(axis)][i] = plotData.plotdict['{0}_expressions'.format(axis)][i].replace(key, value)
