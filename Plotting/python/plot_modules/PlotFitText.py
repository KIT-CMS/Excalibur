# -*- coding: utf-8 -*-

"""
	plot fit labels to fit plot
"""

import Artus.HarryPlotter.plotbase as plotbase
from matplotlib import transforms, pyplot


class PlotFitText(plotbase.PlotBase):

	def modify_argument_parser(self, parser, args):
		super(PlotFitText, self).modify_argument_parser(parser, args)

		self.plot_fit_text_options = parser.add_argument_group("{} options".format(self.name()))
		self.plot_fit_text_options.add_argument("--fit-text-nicks", type=str, nargs="+",
				help="Nicks of the function fits.")
		self.plot_fit_text_options.add_argument("--fit-text-npar", type=int,
				help="Number of Parameters to plot.")
		self.plot_fit_text_options.add_argument("--fit-text-parameter-names", type=str, nargs="+",
				help="Name of the Parameters to plot")
		self.plot_fit_text_options.add_argument("--fit-text-colors", type=str, nargs="+",
				help="Colors of the text")
		self.plot_fit_text_options.add_argument("--fit-text-size", type=int, default=14,
				help="Size of the text")
		self.plot_fit_text_options.add_argument("--fit-text-position", type=float, nargs="?",
				help="Position of the text in x/y-coordinates")


	def prepare_args(self, parser, plotData):
		super(PlotFitText, self).prepare_args(parser, plotData)
		# arguments are now available in the plotdict, can be modified if necessary
		self.prepare_list_args(
				plotData,
				["fit_text_colors"],
				n_items = max([len(plotData.plotdict[l]) for l in ["fit_text_nicks"] if plotData.plotdict[l] is not None]
		))


	def run(self, plotData):
		size = plotData.plotdict["fit_text_size"]
		ax = plotData.plot.axes[0]
		npar = plotData.plotdict["fit_text_npar"]
		parameter_names = plotData.plotdict["fit_text_parameter_names"]
		name_length=len(max(parameter_names, key=len))

		for index, (nick, color) in enumerate(zip(
				plotData.plotdict["fit_text_nicks"],
				plotData.plotdict["fit_text_colors"],
		)):
			fit_function = plotData.plotdict["root_objects"][nick]
			fit_result = plotData.fit_results[nick]

			# texts with y-intercept and chi^2
			texts = []
			yposs = []
			for i in range(0,npar):
				texts.append("$\mathit{"+parameter_names[i]+"}$ = %.4f $\pm$ %.4f" % (fit_function.GetParameter(i), fit_function.GetParError(i)))
				yposs.append(0.95-(size*i/250.))
			for text, ypos in zip(texts,yposs):
				# x/y coords are chosen depending on font size to put the text in the upper right corner
				ax.text(1.-(size*0.036),
						ypos-(size*(i+1.)*(index)/250),
						text,
						color=color,
						size=size,
						va='top',
						transform=ax.transAxes)
