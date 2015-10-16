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
from Excalibur.Plotting.utility.expressionsZJet import ExpressionsDictZJet
from Excalibur.Plotting.utility.binningsZJet import BinningsDictZJet


class InputRootZJet(inputroot.InputRoot):

	def __init__(self):
		super(InputRootZJet, self).__init__()
		self.expressions = ExpressionsDictZJet()
		self.binnings = BinningsDictZJet()

	def modify_argument_parser(self, parser, args):
		super(InputRootZJet, self).modify_argument_parser(parser, args)

		# special arguments for custom zjet folder naming conventions
		self.zjet_input_options = parser.add_argument_group("ZJet input options")
		self.zjet_input_options.add_argument("--zjetfolders", type=str, nargs='*', default=['finalcuts'],
		                                help="'zjetfolders'/cutlevels for the input folder names (nocuts, finalcuts....) [Default: %(default)s]")
		self.zjet_input_options.add_argument("--algorithms", type=str, nargs='*', default=["AK5PFJetsCHS"],
		                                help="Jet algorithms for the input folder names. [Default: %(default)s]")
		self.zjet_input_options.add_argument("--corrections", type=str, nargs='*', default=["L1L2L3Res"],
		                                help="correction levels for the input folder names. [Default: %(default)s]")
		self.zjet_input_options.add_argument("--no-weight", action="store_true", default=False,
		                                help="Dont apply 'weight' by default when plotting from a TTree/TNtuple.")

		self.input_options.set_defaults(read_config=True)

	def prepare_args(self, parser, plotData):
		# this is needed so one can put together the folder name like in the old
		# merlin plotting
		zjetlist =  ["algorithms", "corrections", "zjetfolders"]
		self.prepare_list_args(plotData, zjetlist)
		if plotData.plotdict['folders'] is None:
			folders = []
			if all( [plotData.plotdict[i] != [None] for i in zjetlist]):
				for algo, corr, folder in zip(*[plotData.plotdict[i] for i in zjetlist]):
					folders.append("%s_%s%s/ntuple" % (folder, algo, corr))
			plotData.plotdict['folders'] = folders

		# automatically set nicks, x-expressions if not explicitly given
		if plotData.plotdict['nicks'] == None and plotData.plotdict['files'] != None and len(set(plotData.plotdict['files'])) > 1:
			plotData.plotdict['nicks'] = [os.path.splitext(os.path.basename(i))[0] for i in plotData.plotdict['files']]

		super(InputRootZJet, self).prepare_args(parser, plotData)

		# add 'weight' by default to weights
		if not plotData.plotdict['no_weight'] and not any(bool(json) is False for json in plotData.input_json_dicts):
			plotData.plotdict['weights'] = ["(weight * ({0}))".format(weight) for weight in plotData.plotdict['weights']]

		# get int. lumi from input dicts
		if plotData.plotdict['lumis'] is None:
			lumis = [input_json_dict.get('Lumi', None) for input_json_dict in plotData.input_json_dicts if input_json_dict.get('Lumi', None) is not None]
		else:
			lumis = plotData.plotdict['lumis']

		if len(set(lumis)) == 1:
			plotData.plotdict['lumis'] = lumis
			# add lumi as weight for mc files:
			for i, rootfile in enumerate(plotData.plotdict['files']):
				if plotData.input_json_dicts[i] is not None and not plotData.input_json_dicts[i].get('InputIsData', True):
					log.info("Scaling sample {0} by lumi: {1}".format(rootfile[0], plotData.plotdict['lumis'][0]))
					plotData.plotdict['weights'][i] = "(({1}) * ({0}))".format(plotData.plotdict['weights'][i], plotData.plotdict['lumis'][0])
