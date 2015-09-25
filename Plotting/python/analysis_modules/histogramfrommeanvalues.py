# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase


class HistogramFromMeanValues(analysisbase.AnalysisBase):
	"""Construct an histogram from root_objects mean values"""

	def run(self, plotData=None):
		super(HistogramFromMeanValues, self).run(plotData)

		hist = ROOT.TH1D(self.__class__.__name__, self.__class__.__name__, len(plotData.plotdict["nicks"]), 0, len(plotData.plotdict["nicks"]))

		# TODO make nicks configurable
		for index, nick in enumerate(plotData.plotdict['nicks']):
			hist.SetBinContent(index+1, plotData.plotdict['root_objects'][nick].GetMean())
			hist.SetBinError(index+1, plotData.plotdict['root_objects'][nick].GetRMS())
			hist.GetXaxis().SetBinLabel(index+1, nick)

		nick = "mean"  # TODO make this configurable
		plotData.plotdict['nicks'].append(nick)
		plotData.plotdict['root_objects'][nick] = hist
