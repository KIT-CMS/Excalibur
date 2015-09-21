# -*- coding: utf-8 -*-

"""
	This module contains some functions for data-only plots
"""

from Excalibur.Plotting.utility.toolsZJet import PlottingJob
import Excalibur.Plotting.utility.binningsZJet as binningsZJet


def response_time_dependence(args=None, additional_dictionary=None):
	""" Plot the response vs time (run-number) for different eta regions"""
	plots= []
	#bindict =
	etabins = binningsZJet.BinningsDictZJet().binnings_dict["abseta"].split(" ")
	weights = ["{}<abs(jet1eta)&&{}>abs(jet1eta)".format(lower, upper) for lower, upper in zip(etabins, etabins[1:])]
	labels = [r"{:.1f}<|$\\eta_{{jet}}$|<{:.1f}".format(float(lower), float(upper)) for lower, upper in zip(etabins, etabins[1:])]
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
			'line_styles': ['-'],
			'colors': ['black', 'red', 'blue', 'green', 'purple', 'orange', 'cyan']*2,
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
	"""Time dependence plot for 2012"""
	d = {
		'plot_modules': ['PlotMplZJet', 'PlotMplRunRanges'],
		'x_bins': '5,190450,208535'
	}
	return response_time_dependence(args, d)
