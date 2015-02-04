# -*- coding: utf-8 -*-

"""
"""

import Artus.HarryPlotter.harryparser as harryparser

class HarryParserZJet(harryparser.HarryParser):

	def __init__(self, **kwargs):
		super(HarryParserZJet, self).__init__()

		self.set_defaults(plot_modules=["PlotMplZJet"])
		self.set_defaults(input_module="InputRootZJet")

		self.add_argument("plot", type=str, nargs='?', default='zmass',
                          help="""Name of the plot. x-/y-expressions and output filename 
                          are constructed from this, if not explicitly given. 
                          Default is '%(default)s'.""")
