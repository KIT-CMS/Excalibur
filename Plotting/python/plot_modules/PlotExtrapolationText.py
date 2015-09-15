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
		self.plot_extrapolation_text_options.add_argument("--extrapolation-text-size", type=int, nargs="?",
				help="Size of the text")
		self.plot_extrapolation_text_options.add_argument("--extrapolation-text-position", type=float, nargs="?",
				help="Position of the text in x/y-coordinates")


	def prepare_args(self, parser, plotData):
		super(PlotExtrapolationText, self).prepare_args(parser, plotData)
		# arguments are now available in the plotdict, can be modified if necessary
		# plotData.plotdict['argument']
		self.prepare_list_args(
				plotData,
				["extrapolation_text_colors"],
				n_items = max([len(plotData.plotdict[l]) for l in ["extrapolation_text_nicks"] if plotData.plotdict[l] is not None]
		))

		if plotData.plotdict["extrapolation_text_size"] == None:
			plotData.plotdict["extrapolation_text_size"] = 14

	def run(self, plotData):
		size = plotData.plotdict["extrapolation_text_size"]
		for ax in [plotData.plot.axes[1]]:

			if plotData.plotdict["extrapolation_text_position"] == None:
				xlim = ax.get_xlim()
				ylim = ax.get_ylim()
				pos = [xlim[0] + 0.03 * (xlim[1] - xlim[0]), ylim[1] - 0.15 * (ylim[1] - ylim[0])]
			else:
				pos = plotData.plotdict["extrapolation_text_position"]

			transform = ax.transData
			for nick, color, in zip(
					plotData.plotdict["extrapolation_text_nicks"],
					plotData.plotdict["extrapolation_text_colors"],
			):
				fit = plotData.plotdict["root_objects"][nick]
				fit_result = plotData.fit_results[nick]

				first_text = ax.text(pos[0],
						pos[1],
						"$\mathit{R}_0$ = %.4f $\pm$ %.4f" % (fit.GetParameter(0), fit.GetParError(0)),
						color=color,
						size=size,
						transform=transform)

				first_text.draw(plotData.plot.fig.canvas.get_renderer())
				ex = first_text.get_window_extent()
				t = transforms.offset_copy(first_text._transform, y=-(ex.height+10), units='dots')

				second_text = ax.text(pos[0],
						pos[1],
						"$\chi^2 / \mathit{n.d.f}$ = %.2f / %d" % (fit_result.Chi2(), fit_result.Ndf()),
						color=color,
						size=size,
						transform=t)

				second_text.draw(plotData.plot.fig.canvas.get_renderer())
				ex = second_text.get_window_extent()
				transform = transforms.offset_copy(second_text._transform, y=-(ex.height+10), units='dots')


