# -*- coding: utf-8 -*-

"""
	plot run ranges and labels as dashed vertical lines on the plot
"""

import Artus.HarryPlotter.plotbase as plotbase

class PlotRunRanges(plotbase.PlotBase):

	def run(self, plotData):
		runs = [['2012A', 190456.], ['2012B', 193834.], ['2012C', 197770.], ['2012D', 203773.]]
		for [runlabel, runnumber] in runs:
			plotData.plot.axes[0].text(
				(runnumber - plotData.plot.axes[0].dataLim.min[0]) / (plotData.plot.axes[0].dataLim.max[0] - plotData.plot.axes[0].dataLim.min[0]),
				0.92, runlabel, transform=plotData.plot.axes[0].transAxes, va='top',
				ha='left', color='gray', alpha=0.7, size='medium'
			)
			for ax in plotData.plot.axes:
				ax.axvline(runnumber, color='gray', linestyle='--', alpha=0.2)
