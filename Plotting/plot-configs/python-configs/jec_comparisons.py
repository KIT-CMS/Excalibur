#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.plotscript as plotscript

import argparse
import copy


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


def response_comparisons(args2=None, additional_dictionary=None):
	"""Response (MPF/pTbal) vs zpt npv abs(jet1eta), with ratio"""

	known_args, args = get_special_parser(args2)

	plots = []
	# TODO put these default binning values somewhere more globally
	for quantity, bins in zip(*get_list_slice([
		['zpt', 'npv', 'abs(jet1eta)'],
		["30 40 50 60 75 95 125 180 300 1000", "-0.5 4.5 8.5 15.5 21.5 45.5",
				"0 0.783 1.305 1.93 2.5 2.964 3.139 5.191"]
	], known_args.no_quantities)):
		for method in get_list_slice([['ptbalance', 'mpf']], known_args.no_methods)[0]:
			d = {
				'y_expressions': [method],
				'x_expressions': [quantity],
				'x_bins': bins,
				'y_lims': [0.8, 1.1],
				'x_errors': [1],
				'tree_draw_options': 'prof',
				'markers': ['.', '*'],
				'legloc': 'best',
				'cutlabel': True,

				'analysis_modules': ['Ratio'],

				'filename': method + "_" + quantity.replace("(", "").replace(")", ""),
				
				'y_subplot_lims': [0.9, 1.1],
			}
			if quantity == 'abs(jet1eta)':
				d['alleta'] = "1"
				d['y_lims'] = [0.6, 1.1],
			if quantity == 'zpt':
				d['x_log'] = True
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			if additional_dictionary != None:
				d.update(additional_dictionary)
			plots.append(d)
	plotscript.plotscript(plots, args)


def basic_comparisons(args=None, additional_dictionary=None):
	"""Comparison of: zpt zy zmass zphi jet1pt jet1eta jet1phi npv, both absolute and normalized"""
	
	plots = []
	for quantity in ['zpt', 'zy', 'zmass', 'zphi', 'jet1pt', 'jet1eta', 'jet1phi',
			 'npv', 'metpt', 'metphi', 'run', 'mu1pt', 'mu1eta', 'mu1phi', 'lumi',
			 'event', 'ptbalance', 'mpf', 'jet2pt', 'jet2eta',
			 'muminusphi', 'muminuseta', 'muminuspt', 'muplusphi', 'mupluseta', 'mupluspt']:
		# normal comparison
		d = {
			'x_expressions': [quantity],
			'cutlabel': True,
			'analysis_modules': ['Ratio'],
			'y_subplot_lims': [0, 2],
		}
		if quantity in ['jet1pt', 'zpt']:
			d["y_log"] = True
			d["x_bins"] = ["25,0,400"]
		# TODO move this to more general location
		xbins_dict = {
			'mu1pt': ["25,0,150"],
			'metpt': ["25,0,125"],
			'ptbalance': ["25,0,2"],
			'mpf': ["25,0,2"],
			'jet2pt': ["25,0,100"],
			'jet2eta': ["20,-5,5"],
		}
		if quantity in xbins_dict:
			d.update({"x_bins": xbins_dict[quantity]})

		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)

		# shape comparison
		d2 = copy.deepcopy(d)
		d2.update({
			'analysis_modules': ['NormalizeToFirstHisto', 'Ratio'],
			'filename': quantity+"_shapeComparison",
			'title': "Shape Comparison",
		})
		if additional_dictionary != None:
			d2.update(additional_dictionary)
		plots.append(d2)

	plotscript.plotscript(plots, args)

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

	plotscript.plotscript(plots, args)

def pf_comparisons(args=None, additional_dictionary=None):
	"""Absolute contribution of PF fractions vs Z pT."""
	plots = []

	for pf in ['ch', 'm', 'nh', 'p']:
		d = {
			'y_expressions': ["(jet1{0}f*jet1pt)".format(pf)],
			'x_expressions': ['zpt'],
			'x_bins': ["30 40 50 60 75 95 125 180 300 1000"],
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
	plotscript.plotscript(plots, args)

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
		]
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
	response_comparisons(args, additional_dictionary=d)
	basic_comparisons(args, additional_dictionary=d)
	basic_profile_comparisons(args, additional_dictionary=d)
	pf_comparisons(args, additional_dictionary=d)

if __name__ == '__main__':
	basic_comparisons()
