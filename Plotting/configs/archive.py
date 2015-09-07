#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface
import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob

import argparse
import copy
import jec_factors
import jec_files



def comparison_1215(args=None):
	"""comparison between 2012 (8TeV) and 2015 (13TeV) MC"""
	plotting_jobs = []
	d = {
		'files': [
			'ntuples/MC_13TeV_72X_E2_50ns_algo_2015-06-16.root',
			'ntuples/MC_RD1_8TeV_53X_E2_50ns_algo_2015-05-21.root',
		],
		'labels': ['13 TeV', '8 TeV'],
		'corrections': ['L1L2L3'],
		'y_subplot_label' : "13/8",
	}
	plotting_jobs += full_comparison(args, d, data_quantities=False)
	return plotting_jobs


def comparison_121515(args=None):
	"""comparison between 2012 (8TeV) and 2015 (13TeV) MC"""
	plotting_jobs = []
	d = {
		'files': [
			'ntuples/MC_13TeV_72X_E2_50ns_algo_ak5fake_2015-06-19.root',
			'ntuples/MC_13TeV_72X_E2_25ns_algo_2015-06-18.root',
			'ntuples/MC_RD1_8TeV_53X_E2_50ns_2015-06-17.root',
		],
		'labels': ['13 TeV (50ns)', '13 TeV (25ns)', '8 TeV'],
		'corrections': [''],
		'y_subplot_label' : "13/8",
		'y_errors' : [True, True, True, False, False],
		'markers': ['o', 'd', 'fill'],
		'zorder': [30, 20, 10],
		'nicks': ['13b', '13a', '8'],
#		'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'lumis': [0.309],
		'energies': None,
		"ratio_numerator_nicks": ['13b', '13a'],
		"ratio_denominator_nicks": ['8', '8'],
		"x_errors": False,
		"colors": ['red','black', colors.histo_colors['blue'], 'red', 'black'],
	}
	plotting_jobs += basic_comparisons(args, d, data_quantities=False)
	plotting_jobs += basic_profile_comparisons(args, d)
	d['markers'] = ['o', 'd', '^']
	plotting_jobs += response_comparisons(args, d)
	del d['colors']
	del d['markers']
	plotting_jobs += pf_fractions(args, d)
	return plotting_jobs

def comparison_53742(args=None):
	"""Comparison between 2012 rereco (22Jan) and 2015 742 rereco of 8TeV DoubleMu."""
	plotting_jobs = []
	d = {
		'files': [
			'ntuples/Data_8TeV_742_E2_50ns_noHlt_2015-05-21.root',
			'ntuples/Data_8TeV_53X_E2_50ns_noHlt_2015-05-20.root',
		],
		'nicks': ['742','53'],
		'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'y_subplot_label' : "742/53",
		'lumis': [0.309],
	}
	plotting_jobs += full_comparison(args, d)
	return plotting_jobs


def comparison_53742_event_matched(args=None):
	"""Comparison between 2012 rereco (22Jan) and 2015 742 rereco of 8TeV DoubleMu."""
	plotting_jobs = []
	d = {
		'files': [
			'output.root',
			'output.root',
		],
		'folders': [
			'common2',
			'common1',
		],
		'nicks': ['742','53'],
		'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'y_subplot_label': "742/53",
		'lumis': [0.309],
		'energies': [8],
		'y_errors': [True, True, False],
		'x_errors': False,
		'ratio_result_nicks': ['742vs53'],
	}
	plotting_jobs += full_comparison(args, d)
	return plotting_jobs


def comparison_740742(args=None):
	"""Comparison between 740 and 2015 742 rereco of 8TeV DoubleMu."""
	plotting_jobs = []
	d = {
		'files': [
			'ntuples/Data_8TeV_742_E2_50ns_noHlt_2015-05-21.root',
			'ntuples/Data_8TeV_74X_E2_50ns_noHlt_2015-05-20.root',
		],
		'nicks': ['742','740'],
		#'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'y_subplot_label' : "742/740",
		'lumis': [0.309],
	}
	plotting_jobs += full_comparison(args, d)
	return plotting_jobs


def comparison_740742_event_matched(args=None):
	"""Comparison between event matched 740 and 2015 742 rereco of 8TeV DoubleMu. Takes output.root from eventmatching.py as input."""
	plotting_jobs = []
	d = {
		'files': [
			'output.root',
			'output.root',
		],
		'folders': [
			'common1',
			'common2',
		],
		'nicks': ['742','740'],
		#'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'y_subplot_label' : "742/740",
		'lumis': [0.309],
	}
	plotting_jobs += full_comparison(args, d)

	return plotting_jobs


def comparison_53740742(args=None):
	"""Comparison between 53X, 740 and 742 rereco of 8TeV data."""
	plotting_jobs = []
	d = {
		'files': [
			'output.root',
			'output.root',
			'output.root',
		],
		'folders': [
			'common3',
			'common2',
			'common1',
		],
		'y_errors' : [True, True, True, False, False],
		'markers': ['.', '.', 'fill'],
		'zorder': [30, 20, 10],
		'nicks': ['740', '742', '53'],
		'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'lumis': [0.309],
		'energies': [8],
		"ratio_numerator_nicks": ['742', '740'],
		"ratio_denominator_nicks": ['53', '53'],
		"x_errors": False,
		"colors": ['black','red', colors.histo_colors['blue'], 'red', 'black'],
		'y_subplot_label' : "74X/53",
	}
	plotting_jobs += basic_comparisons(args, d, True)
	d['markers'] = ['o', 'o', 'd']
	plotting_jobs += response_comparisons(args, d)
	plotting_jobs += basic_profile_comparisons(args, d)
	return plotting_jobs


def rootfile_53742(args=None):
	"""
	Create a root file with zpt-jet1eta 2D histograms for 53 and 742. Matched events. Sent to Ia 18.06.2015
	Input file created with eventmatching tool:
	eventmatching.py /storage/a/dhaitz/zjet/excalibur/data742RC_2015-07-09_11-49/out.root /storage/a/dhaitz/zjet/excalibur/dataRC_2015-07-09_10-45/out.root  -t nocuts_AK5PFJetsCHSRC/ntuple finalcuts_AK5PFJetsCHSRC/ntuple -o -n 742 53 -f 53742_newRC_RConly_event_matched_finalcuts_nocuts.root
	eventmatching.py /storage/a/dhaitz/zjet/excalibur/data742RC_2015-07-09_11-49/out.root /storage/a/dhaitz/zjet/excalibur/dataRC_2015-07-09_10-45/out.root  -t nocuts_AK5PFJetsCHSRC/ntuple noetacuts_AK5PFJetsCHSRC/ntuple -o -n 742 53 -f 53742_newRC_RConly_event_matched_noetacuts_nocuts.root
	"""
	d = {
		'files': ['/storage/a/dhaitz/zjet/53742_newRC_RConly_fixedArea_event_matched_finalcuts_nocuts.root'],
		'folders': ['common742', 'common53'],
		'labels': ['742', '53'],
		'plot_modules': ['ExportRoot'],
	}
	d1 = {
		'x_expressions': ['zpt'],
		'y_expressions': ['jet1eta'],
		'x_bins': ["100,0,500"],
		'y_bins': ["26,-1.3,1.3"],
	}
	d2 = {
		'x_expressions': ['zpt'],
		'y_expressions': ['jet1pt'],
		'x_bins': ["100,0,500"],
		'y_bins': ["40,0,400"],
	}
	d3 = {
		'x_expressions': ['zpt'],
		'y_expressions': ['ptbalance'],
		'x_bins': ["100,0,500"],
		'y_bins': ["210,0.,2.1"],
	}
	harryinterface.harry_interface([dict(d,**d1)], args)
	harryinterface.harry_interface([dict(d,**d2)], args)
	harryinterface.harry_interface([dict(d,**d3)], args)

	# outer eta region: 1.3<|jet1eta|<2.5
	d = {
		'files': ['/storage/a/dhaitz/zjet/53742_newRC_RConly_fixedArea_event_matched_noetacuts_nocuts.root'],
		'folders': ['common742', 'common53'],
		'labels': ['742', '53'],
		'plot_modules': ['ExportRoot'],
		'weights' : ["(abs(jet1eta)<2.5&&abs(jet1eta)>1.3)"],
	}
	d1 = {
		'x_expressions': ['zpt'],
		'y_expressions': ['jet1eta'],
		'x_bins': ["100,0,500"],
		'y_bins': ["50,-2.5,2.5"],
		'filename': 'outereta_jet1eta_VS_zpt',
	}
	d2 = {
		'x_expressions': ['zpt'],
		'y_expressions': ['jet1pt'],
		'x_bins': ["100,0,500"],
		'y_bins': ["40,0,400"],
		'filename': 'outereta_jet1pt_VS_zpt',
	}
	d3 = {
		'x_expressions': ['zpt'],
		'y_expressions': ['ptbalance'],
		'x_bins': ["100,0,500"],
		'y_bins': ["210,0.,2.1"],
		'filename': 'outereta_ptbalance_VS_zpt',
	}
	harryinterface.harry_interface([dict(d,**d1)], args)
	harryinterface.harry_interface([dict(d,**d2)], args)
	harryinterface.harry_interface([dict(d,**d3)], args)

	# jet1pt_VS_zpt for 53 (only), where jet is corrected with Winter V8 JEC:
	d = {
		'files': ['ntuples/Data_8TeV_53X_E2_50ns_2015-05-20.root'],
		'algorithms': ['AK5PFJetsCHS'],
		'corrections': ['L1L2L3Res'],
		'labels': ['53'],
		'plot_modules': ['ExportRoot'],
		'x_expressions': ['zpt'],
		'y_expressions': ['jet1pt'],
		'x_bins': ["100,0,500"],
		'y_bins': ["40,0,400"],
		'filename': 'fully_corrected_jet1pt_VS_zpt',
	}
	harryinterface.harry_interface([d], args)


def comparison_E1E2(args=None):
	""" Do response and basic comparison for E1 and E2 ntuples """
	plotting_jobs = []
	d = {
		'files': [
			'ntuples/Data_8TeV_53X_E2_50ns_2015-04-21.root',
			'ntuples/Data_8TeV_53X_E1_50ns_2015-04-22.root',
		],
		"folders": [
				"finalcuts_AK5PFTaggedJetsCHSL1L2L3/ntuple",
				"incut_AK5PFJetsCHSL1L2L3",
		],
		'nicks': [
			'Ex2',
			'Ex1',
		],
		'y_subplot_lims' : [0.95, 1.05],
		'y_subplot_label' : "Ex2/Ex1",
		'y_errors' : [True, True, False],
	}
	plotting_jobs += response_comparisons(args, additional_dictionary=d)
	plotting_jobs += basic_comparisons(args, additional_dictionary=d)
	plotting_jobs += basic_profile_comparisons(args, additional_dictionary=d)
	return plotting_jobs


def comparison_5374(args=None):
	plotting_jobs = []
	d = {
		'files': [
			'ntuples/Data_8TeV_74X_E2_50ns_noHlt_2015-04-23.root',
			'ntuples/Data_8TeV_53X_E2_50ns_noHlt_2015-04-23.root',
		],
		"algorithms": ["AK5PFJetsCHS",],
		"corrections": ["L1L2L3Res",],
		'nicks': [
			'74',
			'53',
		],
		'weights': ['(run==208307||run==208339||run==208341||run==208351||run==208353)'],
		'y_subplot_label' : "74/53",
		'lumi': 0.309
	}
	plotting_jobs += full_comparison(args, d)
	return plotting_jobs
