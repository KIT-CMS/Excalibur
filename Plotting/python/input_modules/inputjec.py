# -*- coding: utf-8 -*-

"""
	This module evaluates jec txt files and plots the correction factors vs pT, eta
	
	Usage:
		merlin.py --input-modules InputJEC -i jecfile.txt
	The binning in eta (x) is usually fixed, the binning in pT (y) is needed and configurable.
	For L1 or RC files, the values for rho and jet area (for which the corrections are evaluated) can be configured.
		merlin.py  --input-modules InputJEC -i L1jecfile.txt --area 0.5 --rho 10 --y-bins "20,0,200"

"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.input_modules.inputfile as inputfile
import Excalibur.Plotting.utility.toolsZJet as toolsZJet


class InputJEC(inputfile.InputFile):
	def __init__(self):
		super(InputJEC, self).__init__()
	
	def modify_argument_parser(self, parser, args):
		super(InputJEC, self).modify_argument_parser(parser, args)
		self.input_options.add_argument("--area", type=float, default=0.78, help="For L1 or RC files: fixed value for jet area.")
		self.input_options.add_argument("--rho", type=float, default=15., help="For L1 or RC files: fixed value for rho.")
		self.input_options.set_defaults(y_bins="20,0,100")


	def prepare_args(self, parser, plotData):
		super(InputJEC, self).prepare_args(parser, plotData)
		plotData.plotdict["x_label"] = "jeteta"
		plotData.plotdict["y_label"] = "jetpt"
		plotData.plotdict["z_label"] = "JEC Correction factor"

	def run(self, plotData):
		"""Iterate over files, create JECfile object, get histo and put into plotdict."""
		for file in plotData.plotdict["files"]:
			jec_file = toolsZJet.JECfile(file[0])
			histo = jec_file.get_corr_histo(plotData.plotdict["y_bins"], fixed_values=[plotData.plotdict["area"], plotData.plotdict["rho"]])
			plotData.plotdict.setdefault("nicks", []).append("nick0")
			plotData.plotdict.setdefault("root_objects", {})["nick0"] = histo
		plotData.plotdict["nicks"].pop(0)
