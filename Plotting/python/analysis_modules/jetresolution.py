# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
from pprint import pprint
import ROOT

log = logging.getLogger(__name__)

import numpy as np

import Artus.HarryPlotter.analysisbase as analysisbase


class JetResolution(analysisbase.AnalysisBase):

	def modify_argument_parser(self, parser, args):
		super(JetResolution, self).modify_argument_parser(parser, args)

		self.jetresolution_options = parser.add_argument_group("{} options".format(self.name()))
		self.jetresolution_options.add_argument("--response-nicks", type=list, nargs="+",
				help="help.")
		self.jetresolution_options.add_argument("--resolution-nicks", type=list, nargs="+",
				help="help.")


	def prepare_args(self, parser, plotData):
		super(JetResolution, self).prepare_args(parser, plotData)

	def run(self, plotData=None):
		super(JetResolution, self).run(plotData)

		for response_nick, resolution_nick in zip(plotData.plotdict['response_nicks'], plotData.plotdict['resolution_nicks']):
			response_hist = plotData.plotdict["root_objects"][response_nick]
			response_hist.SetErrorOption("s")

			plotData.plotdict["root_objects"][resolution_nick] = ROOT.TGraphErrors()
			plotData.plotdict["nicks"].append(resolution_nick)
			plotData.plotdict["nicks_whitelist"].append(resolution_nick)

			for x_bin in xrange(1, response_hist.GetNbinsX()+1):
				global_bin = response_hist.GetBin(x_bin)
				x_value = response_hist.GetBinCenter(global_bin)
				y_value = response_hist.GetBinError(global_bin)
				plotData.plotdict["root_objects"][resolution_nick].SetPoint(x_bin, x_value, y_value)
				plotData.plotdict["root_objects"][resolution_nick].SetPointError(x_bin, 0, 0)





