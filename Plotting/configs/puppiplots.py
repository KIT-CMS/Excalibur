#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jec_comparisons

def comparison_CHS_Puppi_test(args=None):
	""" Do full comparison for E1 and E2 ntuples """
	plotting_jobs = []
	for corrections in ['L1L2L3']:
		for zjetfolder in ['finalcuts']:
			d = {
				'files': [
					'work/mc15Puppi.root',
					'work/mc15.root',
				],
				"algorithms": ["ak4PFJetsPuppi", "ak4PFJetsCHS"],
				'corrections': [corrections],
				'labels': ['Puppi', 'CHS']
			}

			if corrections == '':
				d['title'] = 'No corrections'
				d['www'] = 'comparison_CHS_Puppi_' + zjetfolder + '_None'
			else:
				d['title'] = corrections
				d['www'] = 'comparison_CHS_Puppi_' + zjetfolder + '_' + corrections

			if zjetfolder != "finalcuts":
				d['zjetfolders'] = zjetfolder

			plotting_jobs += jec_comparisons.response_bin_comparisons(args, d, data_quantities=False)

	return plotting_jobs

def comparison_CHS_Puppi(args=None, additional_dictionary={}):
	""" Do full comparison for CHS and Puppi ntuples """
	plotting_jobs = []

	#plotting_jobs += response_bin_comparisons(args, d, data_quantities=False)
	basic_comparison_jobs = jec_comparisons.basic_comparisons(args, additional_dictionary, data_quantities=False)
	for plotdict in basic_comparison_jobs[0].plots:
		if plotdict['x_expressions'][0] == 'njets':
			plotdict['x_lims'] = [0, 100]
			plotdict['x_bins'] = "100,0,100"
			del plotdict['analysis_modules']
		if plotdict['x_expressions'][0] == 'zpt':
			plotdict['y_lims'] = [5000000, 70000000000]
		if plotdict['x_expressions'][0] == 'alpha':
			plotdict['plot_modules'] =['PlotMplZJet', 'PlotMplRectangle']
			plotdict['rectangle_x'] = [0.3,1.0]
			plotdict['rectangle_alpha'] = [0.2]
			plotdict['rectangle_color'] = ["red"]
	plotting_jobs += basic_comparison_jobs
	plotting_jobs += jec_comparisons.basic_profile_comparisons(args, additional_dictionary)
	plotting_jobs += jec_comparisons.pf_fractions(args, additional_dictionary)
	response_comparisons_jobs = jec_comparisons.response_comparisons(args, additional_dictionary=additional_dictionary, data_quantities=False)
	for plotdict in response_comparisons_jobs[0].plots:
		if plotdict['y_expressions'][0] == 'trueresponse':
			plotdict['y_lims'] = [0.839, 1.10]
			plotdict['y_subplot_lims'] = [0.65, 1.25]
		if plotdict['y_expressions'][0] == 'ptbalance':
			plotdict['y_lims'] = [0.69, 1.15]
			plotdict['y_subplot_lims'] = [0.76, 1.14]
	plotting_jobs += response_comparisons_jobs
	plotting_jobs += jec_comparisons.jet_resolution(args, additional_dictionary=additional_dictionary)
	response_extrapolation_jobs = jec_comparisons.response_extrapolation(args, additional_dictionary=additional_dictionary)
	response_extrapolation_jobs[0].plots[0]['legend'] = 'upper left'
	response_extrapolation_jobs[0].plots[0]['legend_cols'] = 2
	response_extrapolation_jobs[0].plots[0]['y_lims'] = [0.79, 1.2]
	response_extrapolation_jobs[0].plots[0]['y_subplot_lims'] = [0.82, 1.07]
	response_extrapolation_jobs[0].plots[0]['y_subplot_label'] = 'Puppi / CHS'
	response_extrapolation_jobs[0].plots[0]['subplot_legend'] = 'lower left'
	response_extrapolation_jobs[0].plots[0]['extrapolation_text_position'] = [0.18, 0.9]
	response_extrapolation_jobs[0].plots[0]['line_styles'].pop(11)
	for property in [
		'y_expressions', 'nicks', 'labels', 'colors', 'markers', 'marker_fill_styles',
		'line_styles', 'function_fit', 'function_nicknames'
	]:
		response_extrapolation_jobs[0].plots[0][property].pop(4)

	plotting_jobs += response_extrapolation_jobs
	cutflow_jobs = jec_comparisons.cutflow(args, additional_dictionary)
	for plotdict in cutflow_jobs[0].plots:
		plotdict['folders'] = [
			'finalcuts_ak4PFJetsPuppiL1L2L3',
			'finalcuts_ak4PFJetsCHSL1L2L3'
		]
	cutflow_jobs[0].plots[1]['y_log'] = True
	cutflow_jobs[0].plots[1]['y_lims'] = [0.001, 1.00]
	plotting_jobs += cutflow_jobs
	return plotting_jobs

def comparison_CHS_Puppi_all(args=None):
	""" Do full comparison for CHS and Puppi ntuples for finalcuts, noalphacuts and betacuts """
	plotting_jobs = []
	for corrections in ['', 'L1', 'L1L2L3']:
		for zjetfolder in ['finalcuts', 'noalphacuts', 'betacuts']:
			d = {
				'files': [
					'work/mc15Puppi.root',
					'work/mc15.root',
				],
				"algorithms": ["ak4PFJetsPuppi", "ak4PFJetsCHS"],
				'corrections': [corrections],
				'labels': ['Puppi', 'CHS']
			}

			if corrections == '':
				d['title'] = 'No corrections'
				d['www'] = 'comparison_CHS_Puppi_' + zjetfolder + '_None'
			else:
				d['title'] = corrections
				d['www'] = 'comparison_CHS_Puppi_' + zjetfolder + '_' + corrections

			if zjetfolder != "finalcuts":
				d['zjetfolders'] = zjetfolder

			plotting_jobs += jec_comparisons.comparison_CHS_Puppi(args, d)

			if corrections == '':
				d['www'] = 'comparison_CHS_Puppi_bins_' + zjetfolder + '_None'
			else:
				d['www'] = 'comparison_CHS_Puppi_bins_' + zjetfolder + '_' + corrections

			plotting_jobs += jec_comparisons.response_bin_comparisons(args, d, data_quantities=False)
	return plotting_jobs

def comparison_CHS_Puppi_matched(args=None):
	"""comparison between CHS and Puppi in a eventmatcher output file"""
	d = {
		'files': ['eventmatching.root'],
		'folders': ['common2', 'common1'],
		'labels': ['Puppi', 'CHS'],
		'www': 'comparison_CHS_Puppi_matched',
	}

	return comparison_CHS_Puppi(args, d)

def comparison_Puppi(args=None):
	""" Do full comparison for E1 and E2 ntuples """
	plotting_jobs = []
	d = {
		'files': [
			'work/mc15Puppi.root',
		],
		"algorithms": ["ak4PFJetsPuppi"],
		'corrections': ['L1L2L3', ""],
		'labels': ['L1L2L3', 'No corrections'],
	}
	return comparison_CHS_Puppi(args, d)



if __name__ == '__main__':
	comparison_CHS_Puppi_all()
