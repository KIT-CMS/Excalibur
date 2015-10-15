# -*- coding: utf-8 -*-

"""
	This module contains some functions for data-only plots
"""

from Excalibur.Plotting.utility.toolsZJet import PlottingJob
import Excalibur.Plotting.utility.binningsZJet as binningsZJet


def response_time_dependence(args=None, additional_dictionary=None):
	""" Plot the response vs time (run-number) for different eta regions"""
	plots = []
	etabins = binningsZJet.BinningsDictZJet().binnings_dict["abseta"].split(" ")
	weights = ["{}<abs(jet1eta)&&{}>abs(jet1eta)".format(lower, upper) for lower, upper in zip(etabins, etabins[1:])]
	labels = [r"{:.2f}<|$\\eta_{{jet}}$|<{:.2f}".format(float(lower), float(upper)) for lower, upper in zip(etabins, etabins[1:])]
	for response in ['mpf', 'ptbalance']:
		d = {
			# input
			'zjetfolders': ['noetacuts'],
			'x_expressions': 'run',
			'y_expressions': response,
			'weights': weights,
			'tree_draw_options': 'prof',
			# analysis
			'analysis_modules': ['FunctionPlot'],
			'functions': ['[0]+[1]*x'],
			'function_fit': ['nick{}'.format(i) for i in range(len(weights))],
			'function_parameters': ['1,1'],
			'function_nicknames': ['fnick{}'.format(i) for i in range(len(weights))],
			# formatting
			'y_lims': [0.8, 1.1],
			'alphas': [0.3],
			'colors': ['black', 'red', 'blue', 'green', 'purple', 'orange', 'cyan'][:len(weights)]*2,  # TODO take color names directly from plotmpl.py
			# TODO improve x-axis ticks and ticklabels
			'labels': labels + [None]*len(labels),
			'legend_cols': 2,
			# output
			'filename': 'time_dependence_' + response,
		}
		if response == 'mpf':
			d['legend'] = 'lower left'
		if additional_dictionary:
			d.update(additional_dictionary)
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]


def response_time_dependence_2012(args=None, additional_dictionary=None):
	"""Time dependence plot for 2012

		binning determined with
		../Artus/HarryPlotter/scripts/get_binning_with_equal_entries.py work/data.root  noetacuts_AK5PFJetsCHSL1L2L3Res/ntuple run --n-bins 10
	"""
	d = {
		'plot_modules': ['PlotMplZJet', 'PlotMplRunRanges'],
		'x_bins': '190645 194480 195647 198230 199752 200992 202088 204564 206210 207231 208686',
		'x_lims': [190456, 208686],
	}
	if additional_dictionary:
		d.update(additional_dictionary)
	return response_time_dependence(args, d)


def response_time_dependence_2015(args=None, additional_dictionary=None):
	"""
	Time dependence plot for 2015
	"""
	d = {
		'plot_modules': ['PlotMplZJet', 'PlotMplRunRanges'],
		'x_bins': '50,248000,258000',
		'x_lims': [248000, 258000],
		'y_lims': [0.5, 1.5],
		'run_range_year': 2015,
		'algorithms': 'ak4PFJetsCHS',
	}
	if additional_dictionary:
		d.update(additional_dictionary)
	return response_time_dependence(args, d)
