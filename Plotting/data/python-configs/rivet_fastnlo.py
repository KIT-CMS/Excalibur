#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Artus.HarryPlotter.harry as harry
import Excalibur.Plotting.plotscript as plotscript


def rivet_fastnlo(args=None):
	""" compare rivet with fastnlo and MC-gen"""

	plots = []
	for quantity, x, xlabel, upper_limit in zip(['pt', 'y'], ["16", "50"], ['zpt', 'abs(zy)'], [100, 3]):
		for file1, label1, filename_suffix, xx in zip(
			["/usr/users/dhaitz/home/qcd/work/Rivet_10000.root", "/usr/users/dhaitz/home/artus/Excalibur/plots/genz{}.root".format(quantity)],
			["Sherpa+Rivet", 'Madgraph+Pythia'],
			["fnlo", "mg"],
			[x, 'nick0']
		):

			d = {
				"analysis_modules": [
					"NormalizeToFirstHisto", 
					"NormalizeToUnity", 
					"Ratio"
				], 
				"files": [
					"/usr/users/dhaitz/home/qcd/work/fnlo_{}.root".format(quantity),
					 file1,
				], 
				"folders": [
					""
				], 
				"labels": [
					"Sherpa+fastNLO",
					label1,
				], 
				"markers": [
					"o", 
					"fill", 
					"o"
				],
				"filename": quantity + "_riv-" + filename_suffix,
				"title": "shape comparison", 
				"x_expressions": [
					"0",
					xx,
				], 
				"x_label": xlabel, 
				"x_lims": [
					0.0, 
					upper_limit
				], 
				"y_label": "Events (normalized)", 
				"y_subplot_lims": [
					0.5, 
					1.5
				]
			}


			plots.append(d)
	plotscript.plotscript(plots, args)

if __name__ == '__main__':
	rivet_fastnlo()
