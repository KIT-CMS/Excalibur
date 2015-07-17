# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
from pprint import pprint
import ROOT

log = logging.getLogger(__name__)

import ROOT
import Artus.HarryPlotter.analysisbase as analysisbase


class ConvertToTGraphErrors(analysisbase.AnalysisBase):

	def run(self, plotData=None):
		super(ConvertToTGraphErrors, self).run(plotData)
		#TODO make this configurable?
		for nick in plotData.plotdict['nicks']:
			hist = plotData.plotdict["root_objects"][nick]
			tgraph = ROOT.TGraphErrors(hist)
			plotData.plotdict["root_objects"][nick] = tgraph