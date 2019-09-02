# -*- coding: utf-8 -*-

"""
	plot fit labels to extrapolation plot
"""

import Artus.HarryPlotter.plotbase as plotbase
from matplotlib import transforms, pyplot


class PlotExtrapolationText(plotbase.PlotBase):

	def modify_argument_parser(self, parser, args):
		super(PlotExtrapolationText, self).modify_argument_parser(parser, args)

		self.plot_extrapolation_text_options = parser.add_argument_group("{} options".format(self.name()))
		self.plot_extrapolation_text_options.add_argument("--extrapolation-text-nicks", type=str, nargs="+",
				help="Nicks of the ratio fits in the subplot.")
		self.plot_extrapolation_text_options.add_argument("--extrapolation-text-colors", type=str, nargs="+",
				help="Colors of the text")
		self.plot_extrapolation_text_options.add_argument("--extrapolation-text-size", type=int, default=14,
				help="Size of the text")
		self.plot_extrapolation_text_options.add_argument("--extrapolation-text-position", type=float, nargs="?",
				help="Position of the text in x/y-coordinates")
		self.plot_extrapolation_text_options.add_argument("--extrapolation-text-label", type=str, default="$\mathit{R}_0$",
		#self.plot_extrapolation_text_options.add_argument("--extrapolation-text-label", type=str, default="$m^\mathrm{Z}$",
				help="Label of the extrapolation parameter. ")


	def prepare_args(self, parser, plotData):
		super(PlotExtrapolationText, self).prepare_args(parser, plotData)
		# arguments are now available in the plotdict, can be modified if necessary
		self.prepare_list_args(
				plotData,
				["extrapolation_text_colors"],
				n_items = max([len(plotData.plotdict[l]) for l in ["extrapolation_text_nicks"] if plotData.plotdict[l] is not None]
		))


	def run(self, plotData):
		size = plotData.plotdict["extrapolation_text_size"]
		name = plotData.plotdict["extrapolation_text_label"]
		ax = plotData.plot.axes[1]

		for index, (nick, color) in enumerate(zip(
				plotData.plotdict["extrapolation_text_nicks"],
				plotData.plotdict["extrapolation_text_colors"],
		)):
			fit_function = plotData.plotdict["root_objects"][nick]
			fit_result = plotData.fit_results[nick]

			# texts with y-intercept and chi^2
			#texts = ["$\mathit{R}_0$ = %.4f $\pm$ %.4f" % (fit_function.GetParameter(0), fit_function.GetParError(0)),
			texts = [name+" = %.4f $\pm$ %.4f" % (fit_function.GetParameter(0), fit_function.GetParError(0)),
					"$\chi^2 / \mathit{n.d.f}$ = %.2f / %d" % (fit_result.Chi2(), fit_result.Ndf())]

			for text, ypos in zip(texts, [0.95, 0.95-(size/150.)]):
				# x/y coords are chosen depending on font size to put the text in the upper right corner
				ax.text(1.-(size*0.03),
						ypos-0.015*size*index,
				#ax.text(0.03,#1.-(size*0.03),
				#		2.7-0.01*size*index,#ypos-0.015*size*index,
						text,
						color=color,
						size=size,
						va='top',
						transform=ax.transAxes)
