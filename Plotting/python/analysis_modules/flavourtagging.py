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

		#self.flavourtagging_options = parser.add_argument_group("{} options".format(self.name()))
		#self.flavourtagging.add_argument("--flavour_tagging_zone_names", type=list, nargs="+",
		#		help="help.")
		#self.flavourtagging.add_argument("--flavour_tagging_zone_names", type=list, nargs="+",
		#		help="help.")

	def prepare_args(self, parser, plotData):
		super(FlavourTagging, self).prepare_args(parser, plotData)
		# arguments are now available in the plotdict, can be modified if necessary
		# plotData.plotdict['argument']

	def run(self, plotData=None):
		super(FlavourTagging, self).run(plotData)

		mc_mean_mpf_values = []
		mc_mean_mpf_values_up = []
		mc_mean_mpf_values_down = []
		list_of_fractions = []

		print plotData.plotdict["root_objects"].keys()

		for i in xrange(4):
			zone =  plotData.plotdict["flavour_tagging_zone_names"][i]
			mc_mean_mpf_values.append(plotData.plotdict["root_objects"][zone + "all"].GetMean())
			# vary mean error/up down (neede to determine errors on final response values)
			mc_mean_mpf_values_up.append(mc_mean_mpf_values[-1] + plotData.plotdict["root_objects"][zone + "all"].GetMeanError())
			mc_mean_mpf_values_down.append(mc_mean_mpf_values[-1] - plotData.plotdict["root_objects"][zone + "all"].GetMeanError())

			sum_g = plotData.plotdict["root_objects"][zone + "g"].Integral()
			sum_b = plotData.plotdict["root_objects"][zone + "b"].Integral()
			sum_c = plotData.plotdict["root_objects"][zone + "c"].Integral()
			sum_uds = plotData.plotdict["root_objects"][zone + "uds"].Integral()
			sum_all = plotData.plotdict["root_objects"][zone + "all"].Integral()

			list_of_fractions.append([
				sum_uds / sum_all,
				sum_c / sum_all,
				sum_b / sum_all,
				sum_g / sum_all,
			])

		for fractions in list_of_fractions:
			if sum(fractions) != 1.:
				log.warning("Flavour fractions do not sum up to 1!")

		flavour_fractions = np.array(list_of_fractions)
		mc_mean_response_values = np.array(mc_mean_mpf_values)
		mc_mean_response_values_up = np.array(mc_mean_mpf_values_up)
		mc_mean_response_values_down = np.array(mc_mean_mpf_values_down)

		mc_response_for_flavour = np.linalg.solve(flavour_fractions, mc_mean_response_values)
		mc_response_for_flavour_up = np.linalg.solve(flavour_fractions, mc_mean_response_values_up)
		mc_response_for_flavour_down = np.linalg.solve(flavour_fractions, mc_mean_response_values_down)

		# create ROOT histograms from values, push into plotdict
		plotData.plotdict["root_objects"]['mc_flavour_response'] = ROOT.TGraphAsymmErrors()
		plotData.plotdict["nicks"].append('mc_flavour_response')
		plotData.plotdict["nicks_whitelist"].append('mc_flavour_response')
		for i in xrange(4):
			plotData.plotdict["root_objects"]['mc_flavour_response'].SetPoint(i, i+1, mc_response_for_flavour[i])
			plotData.plotdict["root_objects"]['mc_flavour_response'].SetPointEYhigh(i, mc_response_for_flavour_up[i] - mc_response_for_flavour[i])
			plotData.plotdict["root_objects"]['mc_flavour_response'].SetPointEYlow(i, mc_response_for_flavour[i] - mc_response_for_flavour_down[i])

		for data_file in plotData.plotdict['flavour_tagging_data_files']:
			mean_mpf_values = []
			mean_mpf_values_up = []
			mean_mpf_values_down = []
			for i in xrange(4):
				zone =  plotData.plotdict["flavour_tagging_zone_names"][i]
				mean_mpf_values.append(plotData.plotdict["root_objects"][zone + data_file].GetMean())
				# vary mean error/up down (neede to determine errors on final response values)
				mean_mpf_values_up.append(mean_mpf_values[-1] + plotData.plotdict["root_objects"][zone + data_file].GetMeanError())
				mean_mpf_values_down.append(mean_mpf_values[-1] - plotData.plotdict["root_objects"][zone + data_file].GetMeanError())

			mean_response_values = np.array(mean_mpf_values)
			mean_response_values_up = np.array(mean_mpf_values_up)
			mean_response_values_down = np.array(mean_mpf_values_down)

			response_for_flavour = np.linalg.solve(flavour_fractions, mean_response_values)
			response_for_flavour_up = np.linalg.solve(flavour_fractions, mean_response_values_up)
			response_for_flavour_down = np.linalg.solve(flavour_fractions, mean_response_values_down)

			plotData.plotdict["root_objects"][data_file + '_flavour_response'] = ROOT.TGraphAsymmErrors()
			plotData.plotdict["nicks"].append(data_file + '_flavour_response')
			plotData.plotdict["nicks_whitelist"].append(data_file + '_flavour_response')
			for i in xrange(4):
				plotData.plotdict["root_objects"][data_file + '_flavour_response'].SetPoint(i, i+1, response_for_flavour[i])
				plotData.plotdict["root_objects"][data_file + '_flavour_response'].SetPointEYhigh(i, response_for_flavour_up[i] - response_for_flavour[i])
				plotData.plotdict["root_objects"][data_file + '_flavour_response'].SetPointEYlow(i, response_for_flavour[i] - response_for_flavour_down[i])
