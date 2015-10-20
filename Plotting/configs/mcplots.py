# -*- coding: utf-8 -*-

"""
	This module contains some functions for MC-only plots
"""

from Excalibur.Plotting.utility.toolsZJet import PlottingJob


def vertex_reco_efficiency(args=None, additional_dictionary=None):
	"""Vertex reconstruction efficiency: Number of reconstructed vertices (npv) as a function of true vertices"""
	lims = [-0.5, 40.5]
	binning = ",".join([str(i) for i in [(lims[1]-lims[0])]+lims])
	d = {
		# input
		'zjetfolders': ['nocuts'],
		'x_expressions': 'npu+1',
		'y_expressions': 'npv',
		'x_bins': binning,
		'tree_draw_options': 'prof',
		'x_lims': lims,
		'y_lims': lims,
		# fit
		'analysis_modules': ['FunctionPlot'],
		'functions': ['[0]+[1]*x'],
		'function_fit': ['nick0'],
		'function_parameters': ['1,1'],
		'function_ranges': ['-0.5,40.5'],
		'function_nicknames': [' '],
		'function_display_result': True,
		'function_fit_parameter_names': [r'y-intercept', r'Slope'+r'\\ '*11],
		# formatting
		'line_styles': [None, '-'],
		'labels': ["None"],
		'x_label': '$n_{PV}^{Gen}$',
		'y_label': '$n_{PV}^{Reco}$',
		# output
		'filename': 'npv_reco_gen',
	}
	if additional_dictionary:
		d.update(additional_dictionary)
	return [PlottingJob(plots=[d], args=args)]


def z_response(args=None, additional_dictionary=None):
	"""Z response (pT reco/gen) as function of gen pT"""
	d = {
		# input
		'x_expressions': ['genzpt'],
		'y_expressions': ['zpt/genzpt'],
		'x_bins': 'zpt',
		'tree_draw_options': 'prof',
		# formatting
		'lines': [1.00],
		'y_lims': [0.99, 1.01],
		'x_log': True,
		'x_lims': [30, 1000],
		'x_errors': [True],
		'x_ticks':  [30, 50, 70, 100, 200, 400, 1000],
		# output
		'filename': 'z_response',
	}
	if additional_dictionary != None:
		d.update(additional_dictionary)
	return [PlottingJob(plots=[d], args=args)]


def z_pt_resolution(args=None, additional_dictionary=None):
	"""Z resolution (pT reco/gen) as function of gen pT"""
	d = {
		# input
		'x_expressions': ['genzpt'],
		'y_expressions': ['zpt/genzpt'],
		'x_bins': 'zpt',
		'tree_draw_options': 'profs',
		'analysis_modules': ['ConvertToHistogram', 'StatisticalErrors'],
		'convert_nicks': ['nick0'],
		'stat_error_nicks': ['nick0'],
		# formatting
		'x_log': True,
		'y_label': r'Z $\\mathit{p}_T$ resolution',
		'markers': ['o'],
		'x_lims': [30, 1000],
		'x_errors': [True],
		'y_errors': [False],
		'x_ticks':  [30, 50, 70, 100, 200, 400, 1000],
		# output
		'filename': 'z_pt_resolution',
	}
	if additional_dictionary != None:
		d.update(additional_dictionary)
	return [PlottingJob(plots=[d], args=args)]


def response_rms(args=None, additional_dictionary=None):
	"""2D response-RMS plots vs ZpT and nPV. Same as Fig19 in the 2016 JEC paper."""
	plots = []
	for method, label in zip(['ptbalance', 'mpf'], ['balance', 'MPF']):
		d = {
			# input
			"tree_draw_options": ["prof"],
			"x_bins": ["30,30,330"],
			"x_expressions": ["zpt"],
			"y_bins": ["40,5,45"],
			"y_expressions": ["npumean"],
			"z_expressions": ["(((trueresponse-{})/trueresponse)**2)".format(method)],
			# analysis
			"analysis_modules": ["ConvertToHistogram","SquareRootBinContent"],
			"convert_nicks": ["nick0"],
			"square_root_nicks": ["nick0"],
			# formatting and output
			"z_label": r"$RMS((R_{Sim} - R_{"+label+r"}) \/ R_{Sim})$",
			"z_lims": [0.0, 0.25],
			"y_lims": [5, 40],
			"filename": "rms_" + method,
		}
		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]


def response_correlations(args=None, additional_dictionary=None):
	"""2D plots for response method correlations (+ correlation factor)."""
	plots = []
	methods = [('ptbalance', 'trueresponse'), ('mpf', 'trueresponse'), ('ptbalance', 'mpf'),]
	bins = '30,0.7,1.3'
	lims = [float(f) for f in bins.split(',')[1:]]

	for method1, method2 in methods:
		d = {
			'x_expressions': [method2],
			'y_expressions': [method1],
			'x_bins': [bins],
			'y_bins': [bins],
			'analysis_modules': ['GetCorrelationFactor'],
			'x_lims': lims,
			'y_lims': lims,
			'filename': '_'.join(['correlation', method1, method2]),
		}
		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
