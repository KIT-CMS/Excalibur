# -*- coding: utf-8 -*-

"""
"""

import matplotlib

import Artus.HarryPlotter.plot_modules.plotmpl as plotmpl
import ZJet.Plotting.utility.matplotlib_rc as matplotlib_rc

class PlotMplZJet(plotmpl.PlotMpl):

	def __init__(self):
		super(PlotMplZJet, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(PlotMplZJet, self).modify_argument_parser(parser, args)
		self.other_options.set_defaults(userpc=True)
	
		self.formatting_options.add_argument('--layout', type=str,
			default='cmsstyle_JetMET',
			help="layout for the plots. E.g. 'document': serif, LaTeX, pdf; " +
				 "'slides': sans serif, big, png; 'generic': slides + pdf. " +
				 "Default is %(default)s")

	def prepare_args(self, parser, plotData):
		super(PlotMplZJet, self).prepare_args(parser, plotData)
		matplotlib.rcParams.update(matplotlib_rc.getstyle(plotData.plotdict['layout']))
		matplotlib.rc('text.latex', preamble=r'\usepackage{helvet},\usepackage{sfmath}')
