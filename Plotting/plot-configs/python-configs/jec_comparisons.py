#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface
import Excalibur.Plotting.utility.colors as colors

import argparse
import copy
import jec_factors
import jec_files


# TODO to more general location
def get_list_slice(lists, arg):
	if arg is False:
		return lists
	else:
		return [[l[arg]] for l in lists]


# TODO to more general location
def get_special_parser(args):
	parser = argparse.ArgumentParser()
	# if these arguments are set true the function will not iterate over the respective quantities
	#	by default, argument ist False -> whole list is taken and iterated over
	#	if set without arguments: first item of list is taken, no iteration
	#	if set with arguments N: N-th item of list is taken, no iteration
	parser.add_argument('--no-quantities', type=int, nargs='?', default=False, const=0)
	parser.add_argument('--no-methods', type=int, nargs='?', default=False, const=0)
	if args is None:
		known_args, args = parser.parse_known_args()
	else:
		known_args, args = parser.parse_known_args(args)
	return known_args, args

def response_extrapolation(args=None, additional_dictionary=None):
	d = {
		'filename': 'extrapolation',
		'files': ['ntuples/MC_RD1_8TeV_53X_E2_50ns_2015-05-20.root', 'ntuples/Data_8TeV_53X_E2_50ns_2015-05-20.root'],
		'labels': [r'$\\mathit{p}_{T}$ balance (MC)', r'$\\mathit{p}_{T}$ balance (Data)', 'MPF (MC)', 'MPF (Data)', r'$p_T^\\mathrm{reco}$/$p_T^\\mathrm{ptcl}$', r'$\\mathit{p}_{T}$ balance', 'MPF', '', '', '', '', '', '', '', '', ''],
		'algorithms': ["AK5PFJetsCHS",],
		'corrections': ['L1L2L3', 'L1L2L3Res'],
		'zjetfolders': 'noalphacuts',
		'lines': [1.0],
		'legend': 'lower left',
		'x_expressions': 'alpha',
		'x_bins': '6,0,0.3',
		'x_lims': [0,0.3],
		'y_expressions': ['ptbalance', 'ptbalance', 'mpf', 'mpf', "jet1pt/matchedgenjet1pt"],
		'y_label': 'Jet Response',
		'y_lims': [0.88,1.03],
		'nicks': ['ptbalance_mc', 'ptbalance_data', 'mpf_mc', 'mpf_data', 'reco_gen_jet'],
		'colors': ['orange', 'darkred', 'royalblue', 'darkblue', 'darkgreen', 'darkred', 'darkblue'],
		'markers': ['s', 'o', 's', 'o', '*', 'o', 'o'],
		'marker_fill_styles': ['none', 'none', 'full', 'full', 'full', 'none', 'full'],
		'line_styles': [None, None, None, None, None, None, None, '--', '--', '--', '--', '--', '--', '--'],
		'line_widths': ['1'],
		'tree_draw_options': 'prof',
		'analysis_modules': ['Ratio', 'FunctionPlot'],
		'plot_modules': ['PlotMplZJet', 'PlotExtrapolationText'],
		'functions': ['[0]+[1]*x'],
		'function_fit': ['ptbalance_mc', 'ptbalance_data', 'mpf_mc', 'mpf_data', 'reco_gen_jet', 'ptbalance_ratio', 'mpf_ratio'],
		'function_parameters': ['1,1'],
		'function_ranges': ['0,0.3'],
		'function_nicknames': ['ptbalance_mc_fit', 'ptbalance_data_fit', 'mpf_mc_fit', 'mpf_data_fit', 'reco_gen_jet_fit', 'ptbalance_ratio_fit', 'mpf_ratio_fit'],
		'ratio_numerator_nicks': ['ptbalance_data', 'mpf_data'],
		'ratio_denominator_nicks': ['ptbalance_mc', 'mpf_mc'],
		'ratio_result_nicks': ['ptbalance_ratio', 'mpf_ratio'],
		'y_subplot_lims': [0.966, 1.015],
		'y_subplot_label': 'Data / MC',
		'subplot_fraction': 40,
		'subplot_legend': 'lower left',
	}

	if additional_dictionary != None:
		d.update(additional_dictionary)
	harryinterface.harry_interface([d], args)

def response_comparisons(args2=None, additional_dictionary=None):
	"""Response (MPF/pTbal) vs zpt npv abs(jet1eta), with ratio"""

	known_args, args = get_special_parser(args2)

	plots = []
	# TODO put these default binning values somewhere more globally
	for quantity, bins in zip(*get_list_slice([
		['zpt', 'npv', 'abs(jet1eta)'],
		['zpt', 'npv','abseta']
	], known_args.no_quantities)):
		for method in get_list_slice([['ptbalance', 'mpf']], known_args.no_methods)[0]:
			d = {
				'y_expressions': [method],
				'x_expressions': [quantity],
				'x_bins': bins,
				'y_lims': [0.5, 1.5],
				'x_errors': [1],
				'tree_draw_options': 'prof',
				'markers': ['.', '*'],
				'legend': 'best',
				'cutlabel': True,
				'lines': [1.0],

				'analysis_modules': ['Ratio'],

				'filename': method + "_" + quantity.replace("(", "").replace(")", ""),
				
				'y_subplot_lims': [0.5, 1.5],
			}
			if quantity == 'abs(jet1eta)':
				d['zjetfolders'] = ["noetacuts"]
				d['y_lims'] = [0.6, 1.1],
			if quantity == 'zpt':
				d['x_log'] = True
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			if additional_dictionary != None:
				d.update(additional_dictionary)
			plots.append(d)
	harryinterface.harry_interface(plots, args)


def basic_comparisons(args=None, additional_dictionary=None, data_quantities=True):
	"""Comparison of: zpt zy zmass zphi jet1pt jet1eta jet1phi npv, both absolute and normalized"""
	
	plots = []
	# TODO move this to more general location
	x_dict = {
		'npv': ["31,-0.5,30.5"],
		'npu': ["31,-0.5,30.5"],
		'npumean': ["31,-0.5,30.5"],
		'mu1pt': ["20,0,150"],
		'mupluspt': ["20,0,150"],
		'muminuspt': ["20,0,150"],
		'met': ["20,0,125"],
		'rawmet': ["20,0,125"],
		'ptbalance': ["20,0,2"],
		'mpf': ["20,0,2"],
		'jet2pt': ["20,0,100"],
		'mu1phi': ["20,-3.1415,3.1415", "lower center"],
		'jet2phi': ["20,-3.1415,3.1415", "lower center"],
		'jet1phi': ["20,-3.1415,3.1415", "lower center"],
		'metphi': ["20,-3.1415,3.1415", "lower center"],
		'zphi': ["20,-3.1415,3.1415", "lower center"],
		'jet2eta': ["20,-5,5"],
		'jet1pt': ["20,0,400"],
		'zpt': ["20,0,400"],
		'zy': ["25,-2.5,2.5"],
		'alpha': ["20,0,1"],
	}
	for q in x_dict:
		if len(x_dict[q]) == 1:
			x_dict[q] += ['best']

	for quantity in ['zpt', 'zy', 'zmass', 'zphi', 'jet1pt', 'jet1eta', 'jet1phi', 'jet1area',
			 'npv', 'rho', 'met', 'metphi', 'rawmet', 'rawmetphi',
			 'mu1pt', 'mu1eta', 'mu1phi', 'mu2pt', 'mu2eta', 'mu2phi',
			 'ptbalance', 'mpf', 'jet2pt', 'jet2eta', 'jet2phi', 'alpha',
			 'muminusphi', 'muminuseta', 'muminuspt', 'muplusphi', 'mupluseta', 'mupluspt'] \
			 + (['run', 'lumi', 'event'] if data_quantities else ['npu', 'npumean']):
		# normal comparison
		d = {
			'x_expressions': [quantity],
			'cutlabel': True,
			'analysis_modules': ['Ratio'],
			'y_subplot_lims': [0, 2],
		}
		d["y_log"] = quantity in ['jet1pt', 'zpt']
		if quantity in x_dict:
			d["x_bins"] = [x_dict[quantity][0]]
			d["legend"] = x_dict[quantity][1]

		if additional_dictionary:
			d.update(additional_dictionary)
		plots.append(d)

		# shape comparison
		d2 = copy.deepcopy(d)
		d2.update({
			'analysis_modules': ['NormalizeToFirstHisto', 'Ratio'],
			'filename': quantity+"_shapeComparison",
			'title': "Shape Comparison",
		})
		if additional_dictionary:
			d2.update(additional_dictionary)
		plots.append(d2)

	harryinterface.harry_interface(plots, args)

def basic_profile_comparisons(args=None, additional_dictionary=None):
	""" Plots Z mass as a function of pT """
	plots = []
	for xquantity, yquantity in zip(['zpt'], ['zmass']):
		d = {
			'x_expressions': [xquantity],
			'y_expressions': [yquantity],
			'analysis_modules': ['Ratio'],
			'tree_draw_options': 'prof',
			'cutlabel': True,
			'y_subplot_lims': [0.99, 1.01],
			'x_log': True,
			'y_lims': [90.19, 92.19],
			'x_bins': "30 40 50 60 75 95 125 180 300 1000",
		}
		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)

		d = {
			'x_expressions': ['npv'],
			'y_expressions': ['rho'],
			'analysis_modules': ['Ratio'],
			'tree_draw_options': 'prof',
			'cutlabel': True,
			'markers': ['o', 'd'],
			'y_subplot_lims': [0.5, 1.5],
			'x_bins': "25,0.5,25.5",
		}
		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)

	harryinterface.harry_interface(plots, args)

def pf_comparisons(args=None, additional_dictionary=None):
	"""Absolute contribution of PF fractions vs Z pT."""
	plots = []

	for pf in ['ch', 'm', 'nh', 'p']:
		d = {
			'y_expressions': ["(jet1{0}f*jet1pt)".format(pf)],
			'x_expressions': ['zpt'],
			'x_bins': ['zpt'],
			'x_log': True,
			'cutlabel': True,
			'markers': ['.', 'd'],
			'tree_draw_options':  'prof',
			'x_lims': [30, 1000],
			'analysis_modules': ['Ratio'],
		}
		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)
	harryinterface.harry_interface(plots, args)


def pf_fractions(args=None, additional_dictionary=None):
	"""PF fractions and contributions to leading jet vs. ZpT, NPV, jet |eta|"""
	plots = []

	# for 'incoming' labels, add them to the PFfraction-labels
	if additional_dictionary is not None:
		if 'labels' in additional_dictionary:
			labels = additional_dictionary['labels']
			additional_dictionary.pop('labels')
		elif 'nicks' in additional_dictionary:
			labels = additional_dictionary['nicks']
			additional_dictionary.pop('nicks')
		else:
			labels = ['', '']
	else:
		labels = ['', '']
	if labels != ['', '']:
		labels = ["({0})".format(l) for l in labels]

	for absolute_contribution in [False, True]:
		for x_quantity, x_binning in zip(['zpt', 'abs(jet1eta)', 'npv'],
			['zpt', 'abseta', 'npv'],
		):
			d = {
				"labels": [
					"CH {0}".format(labels[0]),
					"CH {0}".format(labels[1]),
					r"$\\gamma$ {0}".format(labels[0]),
					r"$\\gamma$ {0}".format(labels[1]),
					"NH {0}".format(labels[0]),
					"NH {0}".format(labels[1]),
					r"$e$ {0}".format(labels[0]),
					r"$e$ {0}".format(labels[1]),
					r"$\\mu$ {0}".format(labels[0]),
					r"$\\mu$ {0}".format(labels[1]),
				],
				"nicks": [
					"CHad1",
					"CHad2",
					"g1",
					"g2",
					"NHad1",
					"NHad2",
					"e1",
					"e2",
					"m1",
					"m2",
				],
				"colors":[
					'blue',
					colors.histo_colors['blue'],
					'orange',
					colors.histo_colors['yellow'],
					'green',
					colors.histo_colors['green'],
					'brown',
					colors.histo_colors['brown'],
					'purple',
					colors.histo_colors['violet'],
					'blue',
					'orange',
					'green',
					'brown',
					'purple',
				],
				"markers": ["o", "fill"]*5 + ["o"]*5,
				"stacks": ["a", "b"]*5,
				"tree_draw_options": ["prof"],
				"legend_cols": 2,
				"x_expressions": [x_quantity],
				"x_bins": [x_binning],
				"y_expressions": [i for i in ["jet1chf", "jet1pf", "jet1nhf", "jet1ef", "jet1mf"] for _ in (0,1)],
				"y_label": "Leading Jet PF Energy Fraction",
				"y_lims": [0.0, 1.0],
				"analysis_modules": ["Ratio"],
				"ratio_numerator_nicks": [
					"CHad1",
					"g1",
					"NHad1",
					"e1",
					"m1",
				],
				"ratio_denominator_nicks": [
					"CHad2",
					"g2",
					"NHad2",
					"e2",
					"m2",
				],
				'y_subplot_lims' : [0, 2],
				'filename': "PFfractions_{}".format(x_quantity),
				'legend': "None",
			}
			if x_quantity == 'zpt':
				d["x_log"] = True
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			elif x_quantity == 'abs(jet1eta)':
				d["zjetfolders"] = ["noetacuts"]
				d["save_legend"] = "PF_legend"
				# add HF fractions
				d["labels"] += [
					r"HFhad {0}".format(labels[0]),
					r"HFhad {0}".format(labels[1]),
					r"HFem {0}".format(labels[0]),
					r"HFem {0}".format(labels[1])]
				d["ratio_numerator_nicks"] += ["HFhad1", "HFem1"]
				d["ratio_denominator_nicks"] += ["HFhad2", "HFem2"]
				d["y_expressions"] += ["jet1hfhf", "jet1hfhf", "jet1hfemf", "jet1hfemf"]
				d["nicks"] += ["HFhad1","HFhad2", "HFem1", "HFem2"]
				d["colors"] = d["colors"][:10]+['black', 'grey', 'red', '#D35658']+d["colors"][10:]+['grey', 'red']
				d["markers"] = ["o", "fill"]*7 + ["o"]*7,
				d["stacks"] = ["a", "b"]*7,
			if absolute_contribution:
				d["y_expressions"] = ["{0}*jet1pt".format(i) for i in d["y_expressions"]]
				d.pop("y_lims")
				d["filename"] = "PFcontributions_{}".format(x_quantity)
				d["y_label"] = r"Leading Jet PF Energy / GeV"

			if additional_dictionary != None:
				d.update(additional_dictionary)
			plots.append(d)
	harryinterface.harry_interface(plots, args)

def jet_resolution_vs_pt(args=None, additional_dictionary=None):
	plots = []

	d = {
		'files': ['/storage/8/cmetzlaff//excalibur/data_2015-07-01_15-53/out.root', '/storage/8/cmetzlaff//excalibur/mc_2015-07-01_15-45/out.root'],
		'labels': ['data', 'mc'],
		'corrections': ['L1L2L3Res', 'L1L2L3'],
		'x_expressions': 'zpt',
		'x_bins': 'zpt',
		'x_lims': [30, 1000],
		'x_log': True,
		'y_expressions': 'ptbalance',
		'y_lims': [0.0, 0.5],
		'y_label': 'Jet response resolution',
		'nicks': ['data', 'mc'],
		'markers': ['o', 'o'],
		'marker_fill_styles': ['full', 'none'],
		'tree_draw_options': 'prof',
		'analysis_modules': ['JetResolution'],
		'response_nicks': ['data', 'mc'],
		'resolution_nicks': ['data_resolution', 'mc_resolution']
	}

	if additional_dictionary != None:
		d.update(additional_dictionary)
	plots.append(d)
	harryinterface.harry_interface(plots, args)

def cutflow(args=None, additional_dictionary=None):
	"""cutflow plots, relative and absolute """
	plots = []
	for rel in [True, False]:
		d = {
			'x_expressions': ['cutFlowWeighted'],
			'analysis_modules': ['Cutflow'],
			'rel_cuts': rel,
			'y_lims': [0, 1],
			'y_errors': [False],
			'filename': 'cutflow' + ('_relative' if rel else ''),
		}
		plots.append(d)
		if additional_dictionary != None:
			d.update(additional_dictionary)
	harryinterface.harry_interface(plots, args)


def full_comparison(args=None, d=None, data_quantities=True):
	""" Do all comparison plots"""
	response_comparisons(args, d)
	basic_comparisons(args, d, data_quantities)
	basic_profile_comparisons(args, d)
	pf_fractions(args, d)


def comparison_E1E2(args=None):
	""" Do response and basic comparison for E1 and E2 ntuples """
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
	response_comparisons(args, additional_dictionary=d)
	basic_comparisons(args, additional_dictionary=d)
	basic_profile_comparisons(args, additional_dictionary=d)


def comparison_5374(args=None):
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
	full_comparison(args, d)


def comparison_datamc(args=None):
	"""full data mc comparisons for work/data.root and work/mc.root"""
	d = {
		'files': ['work/data.root', 'work/mc.root'],
		'labels': ['data', 'mc'],
		'corrections': ['L1L2L3Res', 'L1L2L3'],
	}
	pf_fractions(args, additional_dictionary=d)


def comparison_1215(args=None):
	"""comparison between 2012 (8TeV) and 2015 (13TeV) MC"""
	d = {
		'files': [
			'ntuples/MC_13TeV_72X_E2_50ns_algo_2015-06-16.root',
			'ntuples/MC_RD1_8TeV_53X_E2_50ns_algo_2015-05-21.root',
		],
		'labels': ['13 TeV', '8 TeV'],
		'corrections': ['L1L2L3'],
		'y_subplot_label' : "13/8",
	}
	full_comparison(args, d, data_quantities=False)


def comparison_121515(args=None):
	"""comparison between 2012 (8TeV) and 2015 (13TeV) MC"""
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
	basic_comparisons(args, d, data_quantities=False)
	basic_profile_comparisons(args, d)
	d['markers'] = ['o', 'd', '^']
	response_comparisons(args, d)
	del d['colors']
	del d['markers']
	pf_fractions(args, d)

def comparison_53742(args=None):
	"""Comparison between 2012 rereco (22Jan) and 2015 742 rereco of 8TeV DoubleMu."""
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
	full_comparison(args, d)


def comparison_53742_event_matched(args=None):
	"""Comparison between 2012 rereco (22Jan) and 2015 742 rereco of 8TeV DoubleMu."""
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
	full_comparison(args, d)


def comparison_740742(args=None):
	"""Comparison between 740 and 2015 742 rereco of 8TeV DoubleMu."""
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
	full_comparison(args, d)


def comparison_740742_event_matched(args=None):
	"""Comparison between event matched 740 and 2015 742 rereco of 8TeV DoubleMu. Takes output.root from eventmatching.py as input."""
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
	full_comparison(args, d)


def comparison_53740742(args=None):
	"""Comparison between 53X, 740 and 742 rereco of 8TeV data."""
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
	basic_comparisons(args, d, True)
	d['markers'] = ['o', 'o', 'd']
	response_comparisons(args, d)
	basic_profile_comparisons(args, d)


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


def comparison_run2(args=None):
	"""Comparison for run2 samples."""
	d = {
		'files': [
			'data15.root',
			'work/mc15.root',
		],
		'labels': ['Data','MC'],
		'y_subplot_label' : "Data/MC",
		'algorithms': ['ak4PFJetsCHS'],
		'corrections': ['L1L2L3'],
		'lumis': [0.00559],
	}
	full_comparison(args, d)

	d.update({'folders': ['finalcuts_ak4PFJetsCHSL1L2L3']})
	cutflow(args, d)

	jec_factors.jec_factors(args, {
		'files': ['work/mc15.root'],
		'algorithms': ['ak4PFJetsCHS'],
		'corrections': ['L1L2L3'],
	})

def comparison_run2_jec(args=None):
	""" evaluate the latest JEC files for RUn2"""
	jec_files.jec_files(args+[
		'--jec-dir','data/jec/PY8_RunIISpring15DR74_bx50',
		'--jec-algo', 'AK4PFchs',
	])


if __name__ == '__main__':
	basic_comparisons()
