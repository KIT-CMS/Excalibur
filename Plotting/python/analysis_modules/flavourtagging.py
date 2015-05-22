# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
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

		# get the values from the root histograms
		# mean = plotData.plotdict["root_objects"][nick].GetMean()

		# put together the lists with the response and composition values
		#flavour_fractions = np.array(
		#[
		#	[uds(MC-Truth)_flavour_in_uds_zone, c(MC-Truth)_flavour_in_uds_zone, ... ],
		#	[uds(MC-Truth)_flavour_in_c_zone, c(MC-Truth)_flavour_in_c_zone, ... ],
		#	[..., ],
		#	[...],
		#)
		#mean_response_values = np.array([mean_mpf_response_in_uds_zone, mean_mpf_response_in_c_zone, ...])

		# solve the equation
		#response_for_flavour = np.linalg.solve(flavour_fractions, mean_response_values)

		# create ROOT histograms from values, push into plotdict
