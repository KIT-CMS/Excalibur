# -*- coding: utf-8 -*-

"""
"""

import matplotlib

import Artus.HarryPlotter.plot_modules.plotmpl as plotmpl
import ZJet.Plotting.utility.matplotlib_rc as matplotlib_rc
import ZJet.Plotting.utility.labelsZJet as labelsZJet

class PlotMplZJet(plotmpl.PlotMpl):

	def __init__(self):
		super(PlotMplZJet, self).__init__()
		self.nicelabels = labelsZJet.LabelsDictZJet()

	def modify_argument_parser(self, parser, args):
		super(PlotMplZJet, self).modify_argument_parser(parser, args)
		self.other_options.set_defaults(userpc=True)

		self.formatting_options.set_defaults(markers=['o']+['fill']*8)
		self.formatting_options.set_defaults(colors=[
                    'black',
                    '#7293cb',  # light blue
                    '#e1974c',  # mustard yellow
                    '#808585',  # grey
                    '#d35e60',  # light red
                    '#9067a7',  # violet
                    '#ab6857',  # brown
                    '#84ba5b',  # green
                    '#ccc210',  # dirty yellow
                    'salmon',
                    'mediumaquamarine'
        ])
		self.formatting_options.set_defaults(x_errors=[False])
		self.formatting_options.set_defaults(y_errors=[True])
		self.formatting_options.set_defaults(legloc='center right')

		self.formatting_options.set_defaults(energy='8')
		self.formatting_options.set_defaults(lumi=19.789)
		self.formatting_options.set_defaults(live='evince')

		self.formatting_options.add_argument('--layout', type=str,
			default='cmsstyle_JetMET',
			help="layout for the plots. E.g. 'document': serif, LaTeX, pdf; " +
				 "'slides': sans serif, big, png; 'generic': slides + pdf. " +
				 "Default is %(default)s")

	def prepare_args(self, parser, plotData):
		super(PlotMplZJet, self).prepare_args(parser, plotData)
		#matplotlib.rcParams.update(matplotlib_rc.getstyle(plotData.plotdict['layout']))
		#matplotlib.rc('text.latex', preamble=r'\usepackage{helvet},\usepackage{sfmath}')

		if not all([i==None for i in plotData.plotdict['y_expressions']]):
			plotData.plotdict['y_label'] = plotData.plotdict['y_expressions'][0]

		if plotData.plotdict['live']:
			plotData.plotdict['formats'] = ['pdf']
		if plotData.plotdict['www']:
			plotData.plotdict['formats'] = ['png']
			plotData.plotdict['live'] = False
