# -*- coding: utf-8 -*-

"""
"""

import matplotlib
import datetime

import Artus.HarryPlotter.plot_modules.plotmpl as plotmpl
import Artus.Utility.tools as tools
import Excalibur.Plotting.utility.matplotlib_rc as matplotlib_rc
import Excalibur.Plotting.utility.labelsZJet as labelsZJet

class PlotMplZJet(plotmpl.PlotMpl):

	def __init__(self):
		super(PlotMplZJet, self).__init__()
		self.nicelabels = labelsZJet.LabelsDictZJet()
		self.default_bar_colors = [
				'#7293cb',  # light blue
				'#e1974c',  # mustard yellow
				'#808585',  # grey
				'#ab6857',  # brown
		]
		self.cutlabeldict = {
			"1": r"",
			"(abs(jet1eta)<1.3)": r"|$\eta^{\mathrm{Leading \ jet}}$|$<1.3$",
			"zpt>30": "$p_\mathrm{T}^\mathrm{Z}>30 \ GeV$",
			"(jet2pt/zpt<0.2)": r"$\alpha<0.2$"
		}


	def modify_argument_parser(self, parser, args):
		super(PlotMplZJet, self).modify_argument_parser(parser, args)

		self.formatting_options.set_defaults(x_errors=[False])
		self.formatting_options.set_defaults(y_errors=[True])
		self.formatting_options.set_defaults(legloc='center right')

		self.formatting_options.set_defaults(energy='8')
		self.formatting_options.set_defaults(lumi=19.789)

		self.formatting_options.set_defaults(texts_x=0.03)
		self.formatting_options.set_defaults(texts_y=0.97)

		self.output_options.set_defaults(output_dir="plots/%s/" % datetime.date.today().strftime('%Y_%m_%d'))

		self.formatting_options.add_argument('--layout', type=str,
			default='cmsstyle_JetMET',
			help="layout for the plots. E.g. 'document': serif, LaTeX, pdf; " +
				 "'slides': sans serif, big, png; 'generic': slides + pdf. " +
				 "Default is %(default)s")
		self.formatting_options.add_argument('--cutlabel', type=bool, default=False,
			help="Place a label with the current cuts on the plot. [Defaut: %(default)s]")


	def prepare_args(self, parser, plotData):
		#matplotlib.rcParams.update(matplotlib_rc.getstyle(plotData.plotdict['layout']))
		#matplotlib.rc('text.latex', preamble=r'\usepackage{helvet},\usepackage{sfmath}')

		if 'ekplx' in tools.get_environment_variable('USERPC'):
			plotData.plotdict['userpc'] = True

		if plotData.plotdict['y_label'] in [None, ""] and not all([i==None for i in plotData.plotdict['y_expressions']]):
			plotData.plotdict['y_label'] = plotData.plotdict['y_expressions'][0]

		if plotData.plotdict['www'] is not None:
			plotData.plotdict['formats'] = ['png']
			plotData.plotdict['live'] = None
		elif plotData.plotdict['live'] is not None:
			plotData.plotdict['formats'] = ['pdf']
			plotData.plotdict['output_dir'] = 'plots/live/'
			plotData.plotdict['filename'] = 'plot'

		if plotData.plotdict.get('nolumilabel', True):
			plotData.plotdict['lumi'] = None

		super(PlotMplZJet, self).prepare_args(parser, plotData)


	def add_labels(self, plotData):
		super(PlotMplZJet, self).add_labels(plotData)
		for ax in [plotData.plot.axes[0]]:
			if plotData.plotdict['cutlabel'] == True:
				texts = ["zpt>30", plotData.plotdict['allalpha'], plotData.plotdict['alleta']]
				texts = [self.cutlabeldict.get(*(text,)*2) for text in texts if self.cutlabeldict.get(*(text,)*2) != ""]
				ax.text(0.03, 0.97, "\n".join(texts), va='top', ha='left', color='black', transform=ax.transAxes, size='large')


	def set_matplotlib_defaults(self):
		super(PlotMplZJet, self).set_matplotlib_defaults()

		# set finer ticks
		matplotlib.rcParams['xtick.major.size'] = 6
		if self.mpl_version >= 121:
			matplotlib.rcParams['xtick.major.width'] = 0.8
		matplotlib.rcParams['xtick.minor.size'] = 4
		if self.mpl_version >= 121:
			matplotlib.rcParams['xtick.minor.width'] = 0.5
		if self.mpl_version >= 121:
			matplotlib.rcParams['ytick.major.width'] = 0.8
		matplotlib.rcParams['ytick.major.size'] = 6
		matplotlib.rcParams['ytick.minor.size'] = 3.5
		if self.mpl_version >= 121:
			matplotlib.rcParams['ytick.minor.width'] = 0.5

