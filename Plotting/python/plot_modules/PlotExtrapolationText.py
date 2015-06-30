# -*- coding: utf-8 -*-

"""
	plot fit labels to extrapolation plot
"""

import Artus.HarryPlotter.plotbase as plotbase

class PlotExtrapolationText(plotbase.PlotBase):

	def run(self, plotData):

		for ax in [plotData.plot.axes[1]]:

			for nick, color, x_pos, y_pos in zip(
					['ptbalance_ratio_fit', 'mpf_ratio_fit'],
					['darkred', 'darkblue'],
					[0.15, 0.15],
					[0.985, 0.975],

			):
				fit = plotData.plotdict["root_objects"][nick]
				fit_result = plotData.fit_results[nick]

				ax.text(x_pos,
						y_pos,
						"$\mathit{R}_0$ = %.4f $\pm$ %.4f" % (fit.GetParameter(0), fit.GetParError(0)),
						color=color,
						size=16)
				ax.text(x_pos,
						(y_pos - 0.005),
						"$\chi^2 / \mathit{n.d.f}$ = %.2f / %d" % (fit_result.Chi2(), fit_result.Ndf()),
						color=color,
						size=16)

