# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
import pprint
import ROOT

log = logging.getLogger(__name__)

import numpy as np

import Artus.HarryPlotter.analysisbase as analysisbase


class FlavourTagging(analysisbase.AnalysisBase):
	"""Extract the flavour reponse with 2D-tagging"""

	def modify_argument_parser(self, parser, args):
		super(FlavourTagging, self).modify_argument_parser(parser, args)

		self.flavourtagging_options = parser.add_argument_group("{} options".format(self.name()))
		#self.flavourtagging.add_argument("--argument", type=str, nargs="+",
		#		help="help.")

	def prepare_args(self, parser, plotData):
		super(FlavourTagging, self).prepare_args(parser, plotData)
		# arguments are now available in the plotdict, can be modified if necessary
		# plotData.plotdict['argument']

	def run(self, plotData=None):
		super(FlavourTagging, self).run(plotData)

		#print plotData.plotdict["root_objects"]



		mean_mpf_values = []
		fractions = []
		for i in xrange(4):
			zone =  plotData.plotdict["flavour_tagging_zone_names"][i]
			mean_mpf_values.append(plotData.plotdict["root_objects"][zone + "all"].GetMean())


			sum_g = plotData.plotdict["root_objects"][zone + "g"].Integral()
			sum_b = plotData.plotdict["root_objects"][zone + "b"].Integral()
			sum_c = plotData.plotdict["root_objects"][zone + "c"].Integral()
			sum_uds = plotData.plotdict["root_objects"][zone + "uds"].Integral()
			sum_all = plotData.plotdict["root_objects"][zone + "all"].Integral()

			fractions.append([
				sum_uds / sum_all,
				sum_c / sum_all,
				sum_b / sum_all,
				sum_g / sum_all,
			])

		flavour_fractions = np.array(fractions)
		mean_response_values = np.array(mean_mpf_values)

		response_for_flavour = np.linalg.solve(flavour_fractions, mean_response_values)

		print response_for_flavour

		# create ROOT histograms from values, push into plotdict
		plotData.plotdict["root_objects"]['test'] = ROOT.TGraphErrors()
		plotData.plotdict["nicks"].append("test")
		plotData.plotdict["nicks_whitelist"] = ["test"]
		for i in xrange(4):
			plotData.plotdict["root_objects"]['test'].SetPoint(i, i+1, response_for_flavour[i])

