#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jec_comparisons

def comparison_CHS_Puppi(args=None, additional_dictionary={}, mpf_substract_muons=False):
	""" Do full comparison for CHS and Puppi ntuples """
	plotting_jobs = []

	d = {
		'y_subplot_label': 'Puppi / CHS'
	}
	if additional_dictionary is not None:
		d.update(additional_dictionary)

	basic_comparison_jobs = jec_comparisons.basic_comparisons(args, d, data_quantities=False)
	for plotdict in basic_comparison_jobs[0].plots:
		if plotdict['x_expressions'][0] == 'njets':
			plotdict['x_lims'] = [0, 100]
			plotdict['x_bins'] = "100,0,100"
			del plotdict['analysis_modules']
		if plotdict['x_expressions'][0] == 'zpt':
			plotdict['y_lims'] = [5000000, 70000000000]
			plotdict['y_subplot_lims'] = [0, 10]
		if plotdict['x_expressions'][0] == 'alpha':
			plotdict['y_subplot_lims'] = [0, 10]
			plotdict['plot_modules'] =['PlotMplZJet', 'PlotMplRectangle']
			plotdict['rectangle_x'] = [0.3,1.0]
			plotdict['rectangle_alpha'] = [0.2]
			plotdict['rectangle_color'] = ["red"]
		if plotdict['x_expressions'][0] == 'mpf' and mpf_substract_muons:
			plotdict['x_expressions'] = ['(mpf-1)', 'mpf']
			plotdict['x_label'] = 'MPF Response'
	plotting_jobs += basic_comparison_jobs
	plotting_jobs += jec_comparisons.basic_profile_comparisons(args, d)
	plotting_jobs += jec_comparisons.pf_fractions(args, d)
	response_comparisons_jobs = jec_comparisons.response_comparisons(args, additional_dictionary=d, data_quantities=False)
	for plotdict in response_comparisons_jobs[0].plots:
		if plotdict['y_expressions'][0] == 'trueresponse':
			plotdict['y_lims'] = [0.839, 1.10]
			plotdict['y_subplot_lims'] = [0.65, 1.25]
		if plotdict['y_expressions'][0] == 'ptbalance':
			plotdict['y_lims'] = [0.75, 1.1]
			plotdict['y_subplot_lims'] = [0.8, 1.1]
		if plotdict['y_expressions'][0] == 'mpf' and mpf_substract_muons:
			if mpf_substract_muons:
				plotdict['y_expressions'] = ['(mpf-1)', 'mpf']
			plotdict['y_lims'] = [0.75, 1.1]
			plotdict['y_subplot_lims'] = [0.8, 1.1]
			plotdict['y_label'] = 'MPF Response'
	plotting_jobs += response_comparisons_jobs
	plotting_jobs += jec_comparisons.jet_resolution(args, additional_dictionary=d)
	response_extrapolation_jobs = jec_comparisons.response_extrapolation(args, additional_dictionary=d)
	if mpf_substract_muons:
		response_extrapolation_jobs[0].plots[0]['y_expressions'][2] = '(mpf-1)'
	response_extrapolation_jobs[0].plots[0]['legend'] = 'upper left'
	response_extrapolation_jobs[0].plots[0]['legend_cols'] = 2
	response_extrapolation_jobs[0].plots[0]['y_lims'] = [0.79, 1.2]
	response_extrapolation_jobs[0].plots[0]['y_subplot_lims'] = [0.82, 1.07]
	response_extrapolation_jobs[0].plots[0]['subplot_legend'] = 'lower left'
	response_extrapolation_jobs[0].plots[0]['extrapolation_text_position'] = [0.18, 0.9]
	response_extrapolation_jobs[0].plots[0]['line_styles'].pop(11)
	for property in [
		'y_expressions', 'nicks', 'labels', 'colors', 'markers', 'marker_fill_styles',
		'line_styles', 'function_fit', 'function_nicknames', 'files', 'algorithms'
	]:
		response_extrapolation_jobs[0].plots[0][property].pop(4)

	plotting_jobs += response_extrapolation_jobs
	cutflow_jobs = jec_comparisons.cutflow(args, d)
	for plotdict in cutflow_jobs[0].plots:
		plotdict['folders'] = [
			'finalcuts_ak4PFJetsPuppiL1L2L3',
			'finalcuts_ak4PFJetsCHSL1L2L3'
		]
	cutflow_jobs[0].plots[1]['y_log'] = True
	cutflow_jobs[0].plots[1]['y_lims'] = [0.01, 1.00]
	plotting_jobs += cutflow_jobs
	return plotting_jobs

def comparison_CHS_Puppi_all(args=None):
	""" Do full comparison for CHS and Puppi ntuples for finalcuts, noalphacuts and betacuts """
	plotting_jobs = []
	for met in ['NoMuNoHF']:
		for corrections in ['', 'L1L2L3']:
			for zjetfolder in ['finalcuts', 'noalphacuts']:
				d = {
					'files': [
						'work/mc15Puppi' + met + '.root',
						'work/mc15.root',
					],
					"algorithms": ["ak4PFJetsPuppi", "ak4PFJetsCHS"],
					'corrections': [corrections],
					'labels': ['Puppi', 'CHS']
				}

				if corrections == '':
					d['title'] = 'No corrections'
					d['www'] = 'comparison_CHS_Puppi' + met + '_' + zjetfolder + '_None'
				else:
					d['title'] = corrections
					d['www'] = 'comparison_CHS_Puppi' + met + '_' + zjetfolder + '_' + corrections

				if zjetfolder != "finalcuts":
					d['zjetfolders'] = zjetfolder

				plotting_jobs += comparison_CHS_Puppi(args, d)

				#if met == 'NoMuNoHF':
				#	if corrections == '':
				#		d['www'] = 'comparison_CHS_Puppi' + met + '_mpf_corrected_' + zjetfolder + '_None'
				#	else:
				#		d['www'] = 'comparison_CHS_Puppi' + met + '_mpf_corrected_' + zjetfolder + '_' + corrections
				#	plotting_jobs += comparison_CHS_Puppi(args, d, mpf_substract_muons=True)

				if corrections == '':
					d['www'] = 'comparison_CHS_Puppi' + met + '_bins_' + zjetfolder + '_None'
				else:
					d['www'] = 'comparison_CHS_Puppi' + met + '_bins_' + zjetfolder + '_' + corrections

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

def comparison_CHS_PuppiNoMuons(args=None):

	d = {
		'files': [
			'work/mc15PuppiNoMuNoHF_NoMuons.root',
			'work/mc15.root',
		],
		"algorithms": ["ak4PFJetsPuppi", "ak4PFJetsCHS"],
		'corrections': ['L1L2L3'],
		'labels': ['Puppi', 'CHS'],
	}

	return jec_comparisons.response_bin_comparisons(args, d, data_quantities=False)


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

def comparison_Puppi_datamc(args=None):
	plotting_jobs = []
	pilup_weights='((npv==1)*3.31995+(npv==2)*2.09524+(npv==3)*1.97961+(npv==4)*2.06361+(npv==5)*2.11363+(npv==6)*2.09933+(npv==7)*2.02487+(npv==8)*1.88725+(npv==9)*1.7323+(npv==10)*1.50607+(npv==11)*1.27733+(npv==12)*1.03614+(npv==13)*0.822112+(npv==14)*0.628461+(npv==15)*0.491918+(npv==16)*0.367429+(npv==17)*0.265498+(npv==18)*0.193309+(npv==19)*0.139352+(npv==20)*0.10778+(npv==21)*0.0777005+(npv==22)*0.0561054+(npv==23)*0.0434616+(npv==24)*0.0266506+(npv==25)*0.0234651+(npv==26)*0.0187798+(npv==27)*0.00811271+(npv==28)*0.006758+(npv==29)*0.00540069+(npv==30)*0.0090498)'
	d = {
		'files': [
			'work/data15PuppiNoMuNoHF_25ns.root',
			'work/mc15PuppiNoMuNoHF_25ns.root',
		],
		"algorithms": ["AK4PFJetsPuppiNoMu", "AK4PFJetsPuppi"],
		'corrections': ['L1L2L3Res', "L1L2L3"],
		'labels': ['Data', 'MC'],
	}

	basic_comparisons_jobs = jec_comparisons.basic_comparisons(args, d, data_quantities=True, only_normalized=True)
	for plotdict in basic_comparisons_jobs[0].plots:
		plotdict['weights'] = ['1', pilup_weights]
		if plotdict['x_expressions'][0] == 'zmass':
			plotdict['x_bins'] = ['40,71,111']
			plotdict["nicks"] = ["nick1", "nick2"]
			#plotdict["colors"] = ["red", "blue", "black"]
			plotdict["line_styles"] = [None, None, None, '-', '-']
			plotdict["markers"] = ['fill', 'o', '.', None, None]
			plotdict["analysis_modules"] = ["NormalizeToFirstHisto", "Ratio", "FunctionPlot"]
			plotdict["function_fit"] = ["nick1", "nick2"]
			plotdict["function_nicknames"] = ["nick1_fit", "nick2_fit"]
			plotdict["function_parameters"] = ["1,91,1"]
			plotdict["function_ranges"] = ["71,110"]
			plotdict["functions"] = ["[0]*exp(-0.5*((x-[1])/[2])**2)"]
	plotting_jobs += basic_comparisons_jobs
	pf_fractions_jobs = jec_comparisons.pf_fractions(args, d)
	for plotdict in pf_fractions_jobs[0].plots:
		plotdict['weights'] = ['1', pilup_weights]
	#plotting_jobs += pf_fractions_jobs
	response_jobs = jec_comparisons.response_comparisons(args, additional_dictionary=d, data_quantities=True)
	for plotdict in response_jobs[0].plots:
		if plotdict['y_expressions'][0] == 'trueresponse':
			plotdict['weights'] = [plotdict['weights'], "(" + plotdict['weights'] + ")*"+pilup_weights]
		else:
			plotdict['weights'] = ['1', pilup_weights]

	#plotting_jobs += response_jobs
	resolution_jobs = jec_comparisons.jet_resolution(args, additional_dictionary=d)
	for plotdict in resolution_jobs[0].plots:
		if plotdict['y_expressions'] == 'trueresponse':
			plotdict['weights'] = [plotdict['weights'][0], "(" + plotdict['weights'][0] + ")*"+pilup_weights]
		else:
			plotdict['weights'] = ['1', pilup_weights]
	#plotting_jobs += resolution_jobs
	response_extrapolation_jobs = jec_comparisons.response_extrapolation(args, additional_dictionary=d)
	response_extrapolation_jobs[0].plots[0]['legend'] = 'upper left'
	response_extrapolation_jobs[0].plots[0]['legend_cols'] = 2
	response_extrapolation_jobs[0].plots[0]['weights'] = ['1', pilup_weights, '1', pilup_weights, pilup_weights]
	response_extrapolation_jobs[0].plots[0]['y_lims'] = [0.79, 1.2]
	response_extrapolation_jobs[0].plots[0]['y_subplot_lims'] = [0.82, 1.07]
	response_extrapolation_jobs[0].plots[0]['subplot_legend'] = 'lower left'
	response_extrapolation_jobs[0].plots[0]['extrapolation_text_position'] = [0.18, 0.9]
	#plotting_jobs += response_extrapolation_jobs
	d.update({'folders': ['finalcuts_' + d['algorithms'][0] +  d['corrections'][0], 'finalcuts_' + d['algorithms'][1] +  d['corrections'][1]]})
	#plotting_jobs += jec_comparisons.cutflow(args, d)

	return plotting_jobs

def comparison_Puppi_weights(args=None):
	plotting_jobs = []
	pilup_weights='((npv==1)*3.31995+(npv==2)*2.09524+(npv==3)*1.97961+(npv==4)*2.06361+(npv==5)*2.11363+(npv==6)*2.09933+(npv==7)*2.02487+(npv==8)*1.88725+(npv==9)*1.7323+(npv==10)*1.50607+(npv==11)*1.27733+(npv==12)*1.03614+(npv==13)*0.822112+(npv==14)*0.628461+(npv==15)*0.491918+(npv==16)*0.367429+(npv==17)*0.265498+(npv==18)*0.193309+(npv==19)*0.139352+(npv==20)*0.10778+(npv==21)*0.0777005+(npv==22)*0.0561054+(npv==23)*0.0434616+(npv==24)*0.0266506+(npv==25)*0.0234651+(npv==26)*0.0187798+(npv==27)*0.00811271+(npv==28)*0.006758+(npv==29)*0.00540069+(npv==30)*0.0090498)'
	d = {
		'files': [
			'work/mc15PuppiNoMuNoHF_25ns.root',
			'work/mc15PuppiNoMuNoHF_25ns.root',
		],
		"algorithms": ["AK4PFJetsPuppi", "AK4PFJetsPuppi"],
		'corrections': ['L1L2L3', "L1L2L3"],
		'labels': ['No reweighting', 'Reweighted'],
	}

	basic_comparisons_jobs = jec_comparisons.basic_comparisons(args, d, data_quantities=False, only_normalized=True)
	for plotdict in basic_comparisons_jobs[0].plots:
		plotdict['weights'] = ['1', pilup_weights]
		plotdict['y_subplot_lims'] = [0.75,1.25]
		if plotdict['x_expressions'][0] == 'zmass':
			plotdict['x_bins'] = ['40,71,111']
			#plotdict["nicks"] = ["nick1", "nick2"]
			#plotdict["colors"] = ["red", "blue", "black"]
			#plotdict["line_styles"] = [None, None, None, '-', '-']
			#plotdict["markers"] = ['fill', 'o', '.', None, None]
			#plotdict["analysis_modules"] = ["NormalizeToFirstHisto", "Ratio", "FunctionPlot"]
			#plotdict["function_fit"] = ["nick1", "nick2"]
			#plotdict["function_nicknames"] = ["nick1_fit", "nick2_fit"]
			#plotdict["function_parameters"] = ["1,91,1"]
			#plotdict["function_ranges"] = ["0,110"]
			#plotdict["functions"] = ["[0]*exp(-0.5*((x-[1])/[2])**2)"]
	plotting_jobs += basic_comparisons_jobs
	pf_fractions_jobs = jec_comparisons.pf_fractions(args, d)
	for plotdict in pf_fractions_jobs[0].plots:
		plotdict['weights'] = ['1', pilup_weights]
	plotting_jobs += pf_fractions_jobs
	response_jobs = jec_comparisons.response_comparisons(args, additional_dictionary=d, data_quantities=False)
	for plotdict in response_jobs[0].plots:
		if plotdict['y_expressions'][0] == 'trueresponse':
			plotdict['weights'] = [plotdict['weights'], "(" + plotdict['weights'] + ")*"+pilup_weights]
		else:
			plotdict['weights'] = ['1', pilup_weights]

	plotting_jobs += response_jobs
	resolution_jobs = jec_comparisons.jet_resolution(args, additional_dictionary=d)
	for plotdict in resolution_jobs[0].plots:
		if plotdict['y_expressions'] == 'trueresponse':
			plotdict['weights'] = [plotdict['weights'][0], "(" + plotdict['weights'][0] + ")*"+pilup_weights]
		else:
			plotdict['weights'] = ['1', pilup_weights]
	plotting_jobs += resolution_jobs
	response_extrapolation_jobs = jec_comparisons.response_extrapolation(args, additional_dictionary=d)
	response_extrapolation_jobs[0].plots[0]['legend'] = 'upper left'
	response_extrapolation_jobs[0].plots[0]['legend_cols'] = 2
	response_extrapolation_jobs[0].plots[0]['weights'] = ['1', pilup_weights, '1', pilup_weights, pilup_weights]
	response_extrapolation_jobs[0].plots[0]['y_lims'] = [0.79, 1.2]
	response_extrapolation_jobs[0].plots[0]['y_subplot_lims'] = [0.82, 1.07]
	response_extrapolation_jobs[0].plots[0]['subplot_legend'] = 'lower left'
	response_extrapolation_jobs[0].plots[0]['extrapolation_text_position'] = [0.18, 0.9]
	plotting_jobs += response_extrapolation_jobs
	d.update({'folders': ['finalcuts_' + d['algorithms'][0] +  d['corrections'][0], 'finalcuts_' + d['algorithms'][1] +  d['corrections'][1]]})
	plotting_jobs += jec_comparisons.cutflow(args, d)

	return plotting_jobs

def comparison_Puppi_25ns_oldnew(args=None):
	plotting_jobs = []
	d = {
		'files': [
			'work/mc15PuppiNoMuNoHF_25ns_old_muonadded.root',
			'work/mc15PuppiNoMuNoHF_25ns.root',
		],
		"algorithms": ["ak4PFJetsPuppi", "ak4PFJetsPuppi"],
		'corrections': ['L1L2L3', "L1L2L3"],
		'labels': ['Old-Muons-Added', 'New'],
	}

	basic_comparison_jobs = jec_comparisons.basic_comparisons(args, d, data_quantities=False)
	for plotdict in basic_comparison_jobs[0].plots:
		plotdict['weights'] = ['(mpf<0||mpf>3)']
		if plotdict['x_expressions'][0] == 'njets':
			plotdict['x_lims'] = [0, 100]
			plotdict['x_bins'] = "100,0,100"
			del plotdict['analysis_modules']
		if plotdict['x_expressions'][0] == 'zpt':
			plotdict['y_lims'] = [5000000, 70000000000]
			plotdict['y_subplot_lims'] = [0, 10]
		if plotdict['x_expressions'][0] == 'alpha':
			plotdict['y_subplot_lims'] = [0, 10]
			plotdict['plot_modules'] =['PlotMplZJet', 'PlotMplRectangle']
			plotdict['rectangle_x'] = [0.3,1.0]
			plotdict['rectangle_alpha'] = [0.2]
			plotdict['rectangle_color'] = ["red"]
		if plotdict['x_expressions'][0] == 'mpf':
			#plotdict['x_expressions'] = ['(mpf-1)', 'mpf']
			plotdict['x_label'] = 'MPF Response'
	plotting_jobs += basic_comparison_jobs
	plotting_jobs += jec_comparisons.pf_fractions(args, d)
	response_comparisons_jobs = jec_comparisons.response_comparisons(args, additional_dictionary=d, data_quantities=False)
	for plotdict in response_comparisons_jobs[0].plots:
		if plotdict['y_expressions'][0] == 'trueresponse':
			plotdict['y_lims'] = [0.839, 1.10]
			plotdict['y_subplot_lims'] = [0.65, 1.25]
		if plotdict['y_expressions'][0] == 'ptbalance':
			plotdict['y_lims'] = [0.75, 1.1]
			plotdict['y_subplot_lims'] = [0.8, 1.1]
		if plotdict['y_expressions'][0] == 'mpf':
			#plotdict['y_expressions'] = ['(mpf-1)', 'mpf']
			plotdict['y_lims'] = [0.75, 1.1]
			plotdict['y_subplot_lims'] = [0.8, 1.1]
			plotdict['y_label'] = 'MPF Response'
	plotting_jobs += response_comparisons_jobs
	plotting_jobs += jec_comparisons.jet_resolution(args, additional_dictionary=d)
	response_extrapolation_jobs = jec_comparisons.response_extrapolation(args, additional_dictionary=d)
	response_extrapolation_jobs[0].plots[0]['legend'] = 'upper left'
	response_extrapolation_jobs[0].plots[0]['legend_cols'] = 2
	response_extrapolation_jobs[0].plots[0]['y_lims'] = [0.79, 1.2]
	response_extrapolation_jobs[0].plots[0]['y_subplot_lims'] = [0.975, 1.01]
	#response_extrapolation_jobs[0].plots[0]['y_expressions'][2] = '(mpf-1)'
	response_extrapolation_jobs[0].plots[0]['subplot_legend'] = 'lower left'
	response_extrapolation_jobs[0].plots[0]['extrapolation_text_position'] = [0.18, 0.985]
	plotting_jobs += response_extrapolation_jobs

	response_bin_jobs = jec_comparisons.response_bin_comparisons(args, d, data_quantities=False)
	for plotdict in response_bin_jobs[0].plots:
		if plotdict['x_expressions'][0] == 'mpf':
			plotdict['weights'][0] = '(' + plotdict['weights'][0] + ')*(mpf<0||mpf>3)'
	plotting_jobs += response_bin_jobs
	#d.update({'folders': ['finalcuts_' + d['algorithms'][0] +  d['corrections'][0], 'finalcuts_' + d['algorithms'][1] +  d['corrections'][1]]})
	#plotting_jobs += jec_comparisons.cutflow(args, d)

	return plotting_jobs
