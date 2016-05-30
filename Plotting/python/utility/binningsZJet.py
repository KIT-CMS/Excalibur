
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

from Artus.HarryPlotter.utility.binnings import BinningsDict

"""
	This module contains a dictionary for binnings.
"""
class BinningsDictZJet(BinningsDict):

	def __init__(self):
		super(BinningsDictZJet, self).__init__()

		absetabins = "0 0.783 1.305 1.93 2.5 2.964 3.139 5.191"
		self.binnings_dict.update({
			'zpt': "30 40 50 60 85 105 130 175 230 300 400 500 700 1000 1500",
		'npv':"-0.5 4.5 6.5 8.5 10.5 12.5 21.5",
			'eta':" ".join([str(y) for y in [-i for i in [float(x) for x in absetabins.split(" ")][7:0:-1]]+[float(x) for x in absetabins.split(" ")]]),
			'abseta': absetabins,
			'jet1abseta': absetabins,

			'phi': '20,-3.14159,3.14159',

			'jet2eta': '50,-5,5',
			'jet2pt': '25,0,50',

			'deltaphijet1jet2': '25,-0,3.14159',
			'deltaetajet1jet2': '20,0,5',
			'deltarjet1jet2': '40,0,7'
		})
