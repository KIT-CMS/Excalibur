# -*- coding: utf-8 -*-

"""
"""

import Artus.HarryPlotter.plot_modules.plotmpl as plotmpl

class PlotMplZJet(plotmpl.PlotMpl):

	def __init__(self):
		super(PlotMplZJet, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(PlotMplZJet, self).modify_argument_parser(parser, args)
		self.other_options.set_defaults(userpc=True)
