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

	def prepare_args(self, parser, plotData):
		super(ConvertToTGraphErrors, self).prepare_args(parser, plotData)
		if plotData.plotdict['convert_nicks'] is None:
			plotData.plotdict['convert_nicks'] = plotData.plotdict['nicks']

	def run(self, plotData=None):
		super(ConvertToTGraphErrors, self).run(plotData)
		for nick in plotData.plotdict['convert_nicks']:
			hist = plotData.plotdict["root_objects"][nick]
			tgraph = ROOT.TGraphErrors(hist)
			plotData.plotdict["root_objects"][nick] = tgraph
