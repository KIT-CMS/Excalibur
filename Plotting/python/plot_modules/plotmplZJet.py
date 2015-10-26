# -*- coding: utf-8 -*-

"""
"""

import matplotlib
import os
import datetime

import Artus.HarryPlotter.plot_modules.plotmpl as plotmpl
import Artus.Utility.tools as tools
import Excalibur.Plotting.utility.matplotlib_rc as matplotlib_rc
import Excalibur.Plotting.utility.labelsZJet as labelsZJet
import Excalibur.Plotting.utility.colors as colors

class PlotMplZJet(plotmpl.PlotMpl):

	def __init__(self):
		super(PlotMplZJet, self).__init__()
		self.nicelabels = labelsZJet.LabelsDictZJet()
		self.default_bar_colors = [
			colors.histo_colors[color] for color in [
				'blue',
				'yellow',
				'green',
				'brown',
				'violet',
				'grey',
				'red',
				'teal',
				'salmon',
			]
		]
		self.cutlabeldict = {
			"CutAlphaMax": r"$\mathit{\alpha}<@VALUE@$",
			"CutLeadingJetEtaMax": r"|$\mathit{\eta}^{\mathrm{Leading \ jet}}$|$<@VALUE@$",
			"CutZPtMin": "$\mathit{p}_\mathrm{T}^\mathrm{Z}>@VALUE@ \ GeV$",
		}
		self.cutvaluedict = {
			'CutAlphaMax': '0.2',
			'CutLeadingJetEtaMax': '1.3',
			'CutZPtMin': '30',
		}

	def modify_argument_parser(self, parser, args):
		super(PlotMplZJet, self).modify_argument_parser(parser, args)

		self.formatting_options.set_defaults(x_errors=[False])
		self.formatting_options.set_defaults(y_errors=[True])
		self.formatting_options.set_defaults(legloc='center right')
		self.formatting_options.set_defaults(colormap="Blues")
		self.formatting_options.set_defaults(texts_x=0.03)
		self.formatting_options.set_defaults(texts_y=0.97)

		self.output_options.set_defaults(output_dir="plots/%s/" % datetime.date.today().strftime('%Y_%m_%d'))

		self.formatting_options.add_argument('--layout', type=str,
			default=None, choices=['poster'],
			help="layout for the plots. E.g. 'poster': bigger font. Default is %(default)s")
		self.formatting_options.add_argument('--cutlabel', action='store_true', default=False,
			help="Add a label with the cuts (ZpT. alpha, jet eta) for the used Artus-pipeline. [Defaut: %(default)s]")
		self.formatting_options.add_argument("--marker-colors", type=str, nargs="+",
			help="Specify only the colors for markers.")
		self.formatting_options.add_argument("--bar-colors", type=str, nargs="+",
			help="Specify only the colors for histogram bars.")
		self.formatting_options.add_argument('--no-energy-label', action='store_true', default=False,
			help="Dont add an energy (sqrt(s)=X TeV) label.")


	def prepare_args(self, parser, plotData):
		matplotlib.rcParams.update(matplotlib_rc.getstyle(plotData.plotdict['layout']))

		if plotData.plotdict['y_label'] in [None, ""] and not all([i==None for i in plotData.plotdict['y_expressions']]):
			plotData.plotdict['y_label'] = plotData.plotdict['y_expressions'][0]

		if plotData.plotdict['www'] is not None:
			plotData.plotdict['live'] = None
		elif plotData.plotdict['live'] is not None:
			plotData.plotdict['output_dir'] = 'plots/live/'
			plotData.plotdict['filename'] = 'plot'

		# automatically set labels to filenames if labels are not specified
		if (
			plotData.plotdict['labels'] == None and
			'files' in plotData.plotdict and
			plotData.plotdict['files'] != None and
			len(plotData.plotdict['nicks']) == len(plotData.plotdict['files']) and  # check that the different nicks correspond to different files
			len(set([i[0] for i in plotData.plotdict['files']])) == len(plotData.plotdict['files'])  # check that file(name)s are unique
		):
			plotData.plotdict['labels'] = [os.path.splitext(os.path.basename(i[0]))[0] for i in plotData.plotdict['files']]

		# marker and bar colors
		if plotData.plotdict['marker_colors'] is not None:
			self.default_marker_colors = plotData.plotdict['marker_colors']
		if plotData.plotdict['bar_colors'] is not None:
			self.default_bar_colors = plotData.plotdict['bar_colors']

		# auto determine lumi and energy
		if all(['Energy' in d for d in plotData.input_json_dicts]):
			energies = [d['Energy'] for d in plotData.input_json_dicts]
			if len(set(energies)) == 1:
				plotData.plotdict['energies'] = [energies[0]]
		if plotData.plotdict['no_energy_label']:
			plotData.plotdict['energies'] = []

		super(PlotMplZJet, self).prepare_args(parser, plotData)
		if 'ratio' in plotData.plotdict['nicks']:
			plotData.plotdict['colors'][plotData.plotdict['nicks'].index('ratio')] = 'black'

		# iterate over keys in cutvaluedict and input_json_dicts to replace
		# the default cut values with the ones actually used in the input files
		for key in self.cutvaluedict.keys():
			valuelist = []
			for input_dict in plotData.input_json_dicts:
				if key in input_dict:
					valuelist.append(input_dict[key])
			if len(set(valuelist)) == 1 and len(valuelist)>0:
				self.cutvaluedict[key] = (str(int(valuelist[0])) if key == 'CutZPtMin' else str(valuelist[0]))

	def add_labels(self, plotData):
		super(PlotMplZJet, self).add_labels(plotData)
		folder_cutlabel = {
			'nocuts': [],
			'finalcuts': ['CutAlphaMax', 'CutLeadingJetEtaMax', 'CutZPtMin'],
			'zcuts': ['CutZPtMin'],
			'noalphacuts': ['CutLeadingJetEtaMax', 'CutZPtMin'],
			'noetacuts': ['CutAlphaMax', 'CutZPtMin'],
			'noalphanoetacuts': ['CutZPtMin'],
		}

		# put the cut values into the labels
		for key in self.cutlabeldict.keys():
			self.cutlabeldict[key] = self.cutlabeldict[key].replace('@VALUE@', self.cutvaluedict[key])

		for ax in [plotData.plot.axes[0]]:
			if plotData.plotdict['cutlabel'] == True:
				texts = folder_cutlabel.get(plotData.plotdict['zjetfolders'][0], [])
				texts = [self.cutlabeldict.get(text, text) for text in texts]
				text = "\n".join(texts)
				ax.text(0.03, 0.97, text, va='top', ha='left', color='black', transform=ax.transAxes, size='large')


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

		matplotlib.rcParams['legend.frameon'] = False

