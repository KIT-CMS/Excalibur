#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface
from Excalibur.Plotting.utility.colors import histo_colors
import Artus.Utility.logger as logger
import argparse

def alpha(args=None, additional_dictionary=None):
	plots = []

	parser = argparse.ArgumentParser()
	parser.add_argument('--fraction', type=bool, nargs='?', default=None)

	if args is None:
		known_args, args = parser.parse_known_args()
	else:
		known_args, args = parser.parse_known_args(args)


	for zjetfolder in [None, 'noalphacuts']:
		for fraction in [False,True]:
			if known_args.fraction is not None and fraction != known_args.fraction:
				continue

			for x_value, x_bins, x_lims, y_value, y_bins, y_lims, filename in zip(
				["jet2eta", 'jet2pt', 'jet2eta', 'deltaphijet1jet2', 'alpha', 'deltaphijet1jet2', 'deltaetajet1jet2', 'deltarjet1jet2'],
				['jet2eta', "jet2pt", "jet2eta", "deltaphijet1jet2", "25,0,1", "deltaphijet1jet2", 'deltaetajet1jet2', "deltarjet1jet2"],
				[[-5,5],[0,50],[-5,5],[0,3.14159], [0, 1], [0,3.14159], [0, 5], None],
				[None, None, 'jet2phi', 'deltaetajet1jet2', None, None, None, None],
				[None, None, "phi", 'deltaetajet1jet2', None, None, None, None],
				[None, None, [-3.2, 3.2], [0, 5], None, None, None, None],
				["jet2eta", "jet2pt", "jet2_eta_VS_phi", "jet1jet2_deltaphi_VS_deltaeta", "alpha", "deltaphijet1jet2", 'deltaetajet1jet2', 'deltarjet1jet2']):

				for weights, file_name_postfix, title in zip(
					["", '*(matchedgenjet2pt > 0)', '*(matchedgenjet2pt < 0)'],
					['all', 'genjet', 'pileup'],
					['All jets', 'Genjets', 'Pileup jets']):

					d = {
						"filename": filename + "_" + file_name_postfix,
						"x_expressions": [x_value],
						"x_bins": [x_bins],
						"x_lims": x_lims,
						"title": title,
						"cutlabel": True,
					}

					if y_value is not None:
						d['y_expressions'] = [y_value]
						d['y_bins'] = [y_bins]
						d['y_lims'] = y_lims
						d['colormap'] = "Blues"

					if fraction:
						if weights == "":
							continue

						d['filename'] += "_fraction"
						d['tree_draw_options'] = 'prof'
						axis = 'y'
						if y_value is not None:
							axis = 'z'
						d[axis + '_expressions'] = '(jet2pt > 0)' + weights
						d[axis + '_lims'] = [0, 1]
						d[axis + '_label'] = "Fraction of Events"
					elif weights is not None:
						d['weights'] = '(jet2pt > 0)' + weights

					if zjetfolder is not None:
						d['zjetfolders'] = [zjetfolder]
						d['filename'] += "_" + zjetfolder
						d['title'] += " " + zjetfolder

					if additional_dictionary is not None:
						d.update(additional_dictionary)
					plots.append(d)
	harryinterface.harry_interface(plots, args)


def pileup_studies(args=None):
	"""Plots all pileup studies plots"""
	d = {
		"files": [
			"ntuples/MC_RD1_8TeV_53X_E2_50ns_2015-05-20.root",
		],
		"algorithms": ["AK5PFJetsCHS",],
		"corrections": ["L1L2L3",]
	}

	alpha(args, d)