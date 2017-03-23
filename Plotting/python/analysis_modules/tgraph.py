# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
from pprint import pprint
import ROOT

log = logging.getLogger(__name__)

import ROOT
import Artus.HarryPlotter.analysisbase as analysisbase


class ConvertToTGraphErrors(analysisbase.AnalysisBase):

	def modify_argument_parser(self, parser, args):
		super(ConvertToTGraphErrors, self).modify_argument_parser(parser, args)

		self.convert_options = parser.add_argument_group("{} options".format(self.name()))
		self.convert_options.add_argument(
				"--convert-nicks", nargs="+", default=None,
				help="Nick names of the objects to be converted to ROOT histos"
		)
		self.convert_options.add_argument(
                                "--convert-error-limit", nargs="+", default=False,
                                help="limit errors to one"
		)

	def prepare_args(self, parser, plotData):
		super(ConvertToTGraphErrors, self).prepare_args(parser, plotData)
		if plotData.plotdict['convert_nicks'] is None:
			plotData.plotdict['convert_nicks'] = plotData.plotdict['nicks']

	def run(self, plotData=None):
		super(ConvertToTGraphErrors, self).run(plotData)
		for nick in plotData.plotdict['convert_nicks']:
			hist = plotData.plotdict["root_objects"][nick]
			if(plotData.plotdict['convert_error_limit']):
				tgraph = ROOT.TGraphAsymmErrors(hist)
				for i in range(0,hist.GetNbinsX()):
					if((hist.GetBinContent(i+1)+hist.GetBinError(i+1))>1):
						tgraph.SetPointEYhigh(i,1-hist.GetBinContent(i+1))
						tgraph.SetPointEYlow(i,2*hist.GetBinError(i+1)+hist.GetBinContent(i+1)-1)
					print(hist.GetBinError(i+1), tgraph.GetErrorYhigh(i), tgraph.GetErrorYlow(i))
			else:
				tgraph = ROOT.TGraphErrors(hist)
			plotData.plotdict["root_objects"][nick] = tgraph
