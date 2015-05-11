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
		for quantity, x, xlabel, upper_limit in zip(['pT', 'y'], ["d01-x01-y01", "d02-x01-y01"], ['zpt', 'abs(zy)'], [100, 3]):
			for file1, label1, filename_suffix, path, weight in zip(
				["/usr/users/dhaitz/home/qcd/work/rivet-results/Rivet.root", "/usr/users/dhaitz/home/artus/Excalibur/plots/genz{}.root".format(quantity.lower())],
				["Sherpa+Rivet", 'Madgraph+Pythia'],
				["fnlo", "mg"],
				[x, '4'],
				['1', '19.789'],
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
					"scale_factors": ["1", weight],
					"x_expressions": ["0", path],
					"x_label": xlabel,
					"x_lims": [0.0, upper_limit],
					"y_label": "Events" + y_label_suffix,
					"y_subplot_lims": [0.5, 1.5],
				}
				plots.append(d)

	plotscript.plotscript(plots, args)

if __name__ == '__main__':
	rivet_fastnlo()
