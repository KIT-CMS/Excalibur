#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import combinations

import Artus.HarryPlotter.harry as harry
import Excalibur.Plotting.harryinterface as harryinterface


def rivet_fastnlo(args=None):
	""" compare rivet with fastnlo and MC-gen"""

	plots = []
	# normalized or not:
	for title, norm_modules, y_label_suffix, filename_norm_suffix in zip(
		['', "shape comparison"],
		[[], ["NormalizeToUnity"]],
		['', " (normalized)"],
		['', '_normalizes'],
	):
		# pT or y:
		for quantity, x, xlabel, upper_limit in zip(['pT', 'y'], ["d01-x01-y01", "d02-x01-y01"], ['zpt', 'abs(zy)'], [100, 3]):
			# all combinations of the 
			for files, labels, filename_suffixes, paths, weights in zip(
				combinations([
					"/usr/users/dhaitz/home/qcd/sherivf/rivet-results/Rivet.root",
					"/usr/users/dhaitz/home/artus/Excalibur/plots/genz{0}.root".format(quantity.lower()),
					"/usr/users/dhaitz/home/qcd/sherivf/fnlo-results/fnlo_{0}Z.root".format(quantity)], 2),
				combinations(["Sherpa+Rivet", "Madgraph+Pythia", "Sherpa+fastNLO"], 2),
				combinations(["Riv", "MG", "Fnlo"], 2),
				combinations([x, '4', '0'], 2),
				combinations(['1', '19.789', '1'], 2)
			):
				d = {
					"analysis_modules": norm_modules + ["Ratio"],
					"files": files,
					"folders": [""],
					"labels": labels,
					"markers": ["o", "fill","o"],
					"filename": quantity + "_riv-" + "_".join(filename_suffixes) + filename_norm_suffix,
					"title": title,
					"scale_factors": weights,
					"x_expressions": paths,
					"x_label": xlabel,
					"x_lims": [0.0, upper_limit],
					"y_label": "Events" + y_label_suffix,
					"y_subplot_lims": [0.5, 1.5],
				}
				plots.append(d)
	harryinterface.harry_interface(plots, args)


def genz_root(args=None):
	base_root(
		"/storage/a/dhaitz/excalibur/mc_ee_corr.root",
		"genz",
		args
	)

def z_root(args=None):
	base_root(
		"/storage/a/dhaitz/excalibur/artus/data_ee_corr_2015-02-18_10-34/out.root",
		"z",
		args
	)

def base_root(rootfile, quantityprefix, args=None):
	""" Create the root files from data for the Sherpa-Madgraph comparison."""
	plots = []
	for quantity, binning in zip(["pt", "y"], ["10,0,100", "25,0,2.5"]):
		d = {
			"files": [rootfile],
			"plot_modules": ["ExportRoot"],
			"x_bins": [binning],
			"x_expressions": [quantityprefix + quantity],
			"folders": ["all_AK5PFJetsCHSL1L2L3"],
			"weights": [],
			"nicks": [],
		}
		for njets in range(5):
			d['weights'].append("({})".format(
				" && ".join(["epluspt>25", "eminuspt>25", "abs(epluseta)<2.5",
				"abs(eminuseta)<2.5", "zmass>81", "zmass<101", "njets30<={0}".format(njets)])
			))
			d["nicks"].append(str(njets))

		plots.append(d)
	harryinterface.harry_interface(plots, args)


if __name__ == '__main__':
	rivet_fastnlo()
