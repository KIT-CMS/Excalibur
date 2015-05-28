# -*- coding: utf-8 -*-

"""
	plot run ranges and labels as dashed vertical lines on the plot
"""

import Artus.HarryPlotter.plotbase as plotbase

class PlotTaggingZones(plotbase.PlotBase):

	def run(self, plotData):
		super(PlotTaggingZones, self).run(plotData)

		for ax in plotData.plot.axes:
			ax.axhspan(0.1, 0.9, 0.0, 0.3, color="red", ec="none", alpha=0.1)
			ax.axhspan(0.6, 0.9, 0.3, 0.6, color="red", ec="none", alpha=0.1)
			ax.axhspan(0.9, 1.0, 0.3, 0.9, color="red", ec="none", alpha=0.1)
			ax.axhspan(0.0, 0.6, 0.3, 0.9, color="red", ec="none", alpha=0.1)

			ax.axvline(0.3, 0.0, 0.1, color="red", linestyle="-", alpha=1.0)
			ax.axvline(0.3, 0.9, 1.0, color="red", linestyle="-", alpha=1.0)
			ax.axvline(0.6, 0.6, 0.9, color="red", linestyle="-", alpha=1.0)
			ax.axvline(0.9, 0.6, 0.9, color="red", linestyle="-", alpha=1.0)
			ax.axvline(0.9, color="red", linestyle="-", alpha=1.0)

			ax.axhline(0.1, 0.0, 0.3, color="red", linestyle="-", alpha=1.0)
			ax.axhline(0.9, 0.0, 0.3, color="red", linestyle="-", alpha=1.0)
			ax.axhline(0.6, 0.6, 0.9, color="red", linestyle="-", alpha=1.0)
			ax.axhline(0.9, 0.6, 0.9, color="red", linestyle="-", alpha=1.0)

			ax.text(0.10, 0.93, "uds", color="red", size="xx-large")
			ax.text(0.13, 0.04, "g", color="red", size="xx-large")
			ax.text(0.74, 0.73, "c", color="red", size="xx-large")
			ax.text(0.93, 0.48, "b", color="red", size="xx-large")
