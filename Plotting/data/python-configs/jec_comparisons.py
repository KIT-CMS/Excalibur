#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.plotscript as plotscript

import argparse


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
				'x_errors': [1, 1],
				'tree_draw_options': 'prof',
				'markers': ['.', '*'],
				'legloc': 'best',

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
	for quantity in ['zpt', 'zy', 'zmass', 'zphi', 'jet1pt', 'jet1eta', 'jet1phi', 'npv']:
		# normal comparison
		d = {
			'x_expressions': [quantity],
		}
		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)

		# shape comparison
		d = {
			'x_expressions': [quantity],
			'analysis_modules': ['NormalizeToFirstHisto'],
			'filename': quantity+"_shapeComparison",
		}		
		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)

	plotscript.plotscript(plots, args)


def comparison_E1E2(args=None):
	""" Do response and basic comparison for E1 and E2 ntuples """
	d = {
		'files': [
			'ntuples/Data_8TeV_53X_E2_50ns_2015-04-16.root',
			'ntuples/Data_8TeV_53X_E1_50ns_2015-01-08.root', 
		],
		"algorithms": [
				"AK5PFTaggedJetsCHS",
				"AK5PFJetsCHS",
		],
		"corrections": [
				"L1L2L3/ntuple",
				"L1L2L3",
		],
		"zjetfolders": [
				"finalcuts",
				"incut",
		],
		'nicks': [
			'Ex2',
			'Ex1',
		]
	}
	response_comparisons(args, additional_dictionary=d)
	basic_comparisons(args, additional_dictionary=d)


if __name__ == '__main__':
	basic_comparisons()
