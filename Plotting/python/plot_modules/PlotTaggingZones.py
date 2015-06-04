# -*- coding: utf-8 -*-

"""
	plot run ranges and labels as dashed vertical lines on the plot
"""

import Artus.HarryPlotter.plotbase as plotbase

class PlotTaggingZones(plotbase.PlotBase):

	def run(self, plotData):
		super(PlotTaggingZones, self).run(plotData)

		color = "red"
		lw = 3.0
		text_size = 24.0
		font_weight = 'bold'

		for ax in plotData.plot.axes:

			if plotData.plotdict['plot_tagging_zones'] == 'g' or plotData.plotdict['plot_tagging_zones'] == 'all':
				ax.axvline(0.3, 0.0, 0.1, color=color, linestyle="-", alpha=1.0, lw=lw)
				ax.axhline(0.1, 0.0, 0.3, color=color, linestyle="-", alpha=1.0, lw=lw)
				ax.text(0.13, 0.04, "g", color=color, size=text_size, fontweight=font_weight)

			if plotData.plotdict['plot_tagging_zones'] == 'uds' or plotData.plotdict['plot_tagging_zones'] == 'all':
				ax.axvline(0.3, 0.9, 1.0, color=color, linestyle="-", alpha=1.0, lw=lw)
				ax.axhline(0.9, 0.0, 0.3, color=color, linestyle="-", alpha=1.0, lw=lw)
				ax.text(0.10, 0.93, "uds", color=color, size=text_size, fontweight=font_weight)

			if plotData.plotdict['plot_tagging_zones'] == 'c' or plotData.plotdict['plot_tagging_zones'] == 'all':
				ax.axvline(0.6, 0.6, 0.9, color=color, linestyle="-", alpha=1.0, lw=lw)
				ax.axvline(0.9, 0.6, 0.9, color=color, linestyle="-", alpha=1.0, lw=lw)
				ax.axhline(0.6, 0.6, 0.9, color=color, linestyle="-", alpha=1.0, lw=lw)
				ax.axhline(0.9, 0.6, 0.9, color=color, linestyle="-", alpha=1.0, lw=lw)
				ax.text(0.74, 0.73, "c", color=color, size=text_size, fontweight=font_weight)

			if plotData.plotdict['plot_tagging_zones'] == 'b' or plotData.plotdict['plot_tagging_zones'] == 'all':
				b_color = color
				if plotData.plotdict['plot_tagging_zones'] == 'b':
					b_color="blue"
				ax.axvline(0.9, color=b_color, linestyle="-", alpha=1.0, lw=lw)
				ax.text(0.93, 0.48, "b", color=b_color, size=text_size, fontweight=font_weight)

			if plotData.plotdict['plot_tagging_zones'] == 'all':
				ax.axhspan(0.1, 0.9, 0.0, 0.3, color=color, ec="none", alpha=0.1)
				ax.axhspan(0.6, 0.9, 0.3, 0.6, color=color, ec="none", alpha=0.1)
				ax.axhspan(0.9, 1.0, 0.3, 0.9, color=color, ec="none", alpha=0.1)
				ax.axhspan(0.0, 0.6, 0.3, 0.9, color=color, ec="none", alpha=0.1)















