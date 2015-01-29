# -*- coding: utf-8 -*-

"""
"""

import Artus.HarryPlotter.harryparser as harryparser

class HarryParserZJet(harryparser.HarryParser):

	def __init__(self, **kwargs):
		super(HarryParserZJet, self).__init__()
		self.module_options.add_argument("--plot-modules", default="PlotMplZJet", nargs="+",
		                                 help="Plot Modules. [Default: %(default)s]")
		self.module_options.set_defaults(plot_modules="PlotMplZJet")
		self.set_defaults(plot_modules=["PlotMplZJet"])

