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

def radiationjet(args=None, additional_dictionary=None):
	plots = []
	for zjetfolder in ['noalphacuts', 'nocuts']:
		for filename, x_values, x_bins, x_labels, labels, y_values, y_bins, y_lims in zip(
			[
				"compare_radiationjet_pt",
				"compare_radiationjet_phi",
				"compare_radiationjet_eta",
				"radiationjet1index",
				"radiationjet_eta_vs_phi",
				"deltarjet1radiationjet1",
				"ptbalance_vs_alpha_beta",
				"mpf_vs_alpha_beta",
				"mpf_improved_alpha",
				"zpt_improved_alpha"
			], [
				["genjet2pt", "radiationjet1pt", "jet2pt"],
				["genjet2phi", "radiationjet1phi", "jet2phi"],
				["genjet2eta", "radiationjet1eta", "jet2eta"],
				"radiationjet1index",
				"radiationjet1eta",
				"deltarjet1radiationjet1",
				["alpha", "(radiationjet1pt/zpt)"],
				["alpha", "(radiationjet1pt/zpt)"],
				"zpt",
				"zpt",
			], [
				"50,0,100",
				"phi",
				"jet2eta",
				"51,-0.5,50.5",
				"jet2eta",
				"20,0.4,1.0",
				"40,0.0,0.4",
				"40,0.0,0.4",
				"zpt",
				"zpt",
			], [
				r"Jet $\\mathit{p}_{T}$",
				r"Jet $\\phi$",
				r"Jet $\\eta$",
				None, None, None,
				r"$\\mathit{p}_{T}^{Radiation Jet 1}/\\mathit{p}_T^Z$, $\\mathit{p}_{T}^{Jet 2}/\\mathit{p}_T^Z$",
				r"$\\mathit{p}_{T}^{Radiation Jet 1}/\\mathit{p}_T^Z$, $\\mathit{p}_{T}^{Jet 2}/\\mathit{p}_T^Z$",
				None, None
			], [
				["GenJet2", "Radiation-Jet", "Jet2"],
				["GenJet2", "Radiation-Jet", "Jet2"],
				["GenJet2", "Radiation-Jet", "Jet2"],
				None, None, None,
				[r'$\\mathit{p}_{T}^{Radiation Jet 1}/\\mathit{p}_T^Z$', r'$\\mathit{p}_{T}^{Jet 2}/\\mathit{p}_T^Z$'],
				[r'$\\mathit{p}_{T}^{Radiation Jet 1}/\\mathit{p}_T^Z$', r'$\\mathit{p}_{T}^{Jet 2}/\\mathit{p}_T^Z$'],
				["default 2nd jet cut", "(radiation-)improved 2nd jet cut"],
				["(radiation-)improved 2nd jet cut", "default 2nd jet cut"],
			], [
				None, None, None, None,
				'radiationjet1phi',
				None,
				"ptbalance",
				"mpf",
				"ptbalance",
				None,
			], [
				None, None, None, None,
				"phi",
				None, None, None, None, None,
			], [
				None, None, None, None,
				[-3.14159, 3.14159],
				None,
				[0.8, 1.2],
				[0.8, 1.2],
				[0.92, 1.001],
				None,
			]
		):
			d = {
				"filename": filename + "_" + zjetfolder,
				"zjetfolders": zjetfolder,
				"x_expressions": x_values,
				"x_bins": x_bins,
				"labels": labels,
				"markers": ["fill", "o", "d"],
				"cutlabel": True,
			}

			if x_labels is not None:
				d['x_label'] = x_labels

			if x_values == "zpt":
				d['x_log'] = True
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
				if y_values is None:
					d['weights'] = ["jet2pt/zpt<0.4&&(radiationjet1pt/zpt)<0.1", "jet2pt/zpt<0.2"]
				else:
					d['weights'] = ["jet2pt/zpt<0.2", "jet2pt/zpt<0.4&&(radiationjet1pt/zpt)<0.1"]

			if y_values is not None:
				d['y_expressions'] = y_values

				if y_bins is not None:
					d['y_bins'] = "phi"
					d['colormap'] = "Blues"
				else:
					d['tree_draw_options'] = "prof"
					d['markers'] = ["o", "d"]

				if x_values == "zpt":
					d['lines'] = ["1"]

				if y_lims is not None:
					d['y_lims'] = y_lims
			#elif x_values != "zpt":
			#	d['line_styles'] = [None, '-', '-']

			if additional_dictionary is not None:
				d.update(additional_dictionary)
			plots.append(d)

	harryinterface.harry_interface(plots, args)

def pileup_studies(args=None):
	"""Plots all pileup studies plots"""
	d = {
		"files": [
			"ntuples/MC_13TeV_72X_E2_50ns_algo_2015-06-16.root",
#			"ntuples/MC_RD1_8TeV_53X_E2_50ns_algo_2015-06-17.root",
		],
		"algorithms": ["AK5PFJetsCHS",],
		"corrections": ["L1L2L3",]
	}

	alpha(args, d)
	radiationjet(args, d)