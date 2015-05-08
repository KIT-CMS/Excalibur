#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Artus.HarryPlotter.harry as harry
import Excalibur.Plotting.plotscript as plotscript


def rivet_fastnlo(args=None):
	""" compare rivet with fastnlo and MC-gen"""

	plots = []
	# normalized or not
	for title, norm_modules, y_label_suffix, filename_norm_suffix in zip(
		['', "shape comparison"],
		[[], ["NormalizeToFirstHisto", "NormalizeToUnity"]],
		['', " (normalized)"],
		['', '_normalizes'],
	):
		for quantity, x, xlabel, upper_limit in zip(['pT', 'y'], ["256", "514"], ['zpt', 'abs(zy)'], [100, 3]):
			for file1, label1, filename_suffix, xx in zip(
				["/usr/users/dhaitz/home/qcd/work/rivet-results/Rivet.root", "/usr/users/dhaitz/home/artus/Excalibur/plots/genz{}.root".format(quantity.lower())],
				["Sherpa+Rivet", 'Madgraph+Pythia'],
				["fnlo", "mg"],
				[x, 'nick0']
			):
				d = {
					"analysis_modules": norm_modules + ["Ratio"],
					"files": [
						"/usr/users/dhaitz/home/qcd/work/fnlo-results/fnlo_{}Z.root".format(quantity),
						 file1,
					],
					"folders": [""],
					"labels": ["Sherpa+fastNLO", label1],
					"markers": ["o", "fill","o"],
					"filename": quantity + "_riv-" + filename_suffix + filename_norm_suffix,
					"title": title,
					"x_expressions": ["0", xx],
					"x_label": xlabel,
					"x_lims": [0.0, upper_limit],
					"y_label": "Events" + y_label_suffix,
					"y_subplot_lims": [0.5, 1.5],
				}
				plots.append(d)

	plotscript.plotscript(plots, args)

if __name__ == '__main__':
	rivet_fastnlo()
