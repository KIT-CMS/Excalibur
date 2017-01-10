
# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)
import collections
import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase


class GetErrorFromCovMat(analysisbase.AnalysisBase):
	'''Converts a 2D Covariance Matrix into a 1D Histogram showing statistical errors'''
	def run(self, plotData=None):
		for nick, root_object in plotData.plotdict["root_objects"].iteritems():
			if isinstance(root_object, ROOT.TH2):
				new_histo = root_object.ProjectionX()
				for x in xrange(1, root_object.GetNbinsX() + 1):
        				new_histo.SetBinContent(x, root_object.GetBinContent(x,x)**0.5) 
				plotData.plotdict["root_objects"][nick] = new_histo
			
			


