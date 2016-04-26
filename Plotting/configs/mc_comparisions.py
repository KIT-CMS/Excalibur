#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files

import argparse
import copy
import jec_factors
import jec_files
import datetime


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

def response_extrapolation(args=None, additional_dictionary=None, inputtuple='datamc'):
	"""Do the extrapolation plot for balance and MPF, add Ratio, display fit parameters. Default is an input tuple of data, mc, also possible is datadata and mcmc."""
	additional_dictionary = additional_dictionary.copy() if additional_dictionary else {}
	input_files, other_args = get_input_files(args)
	if input_files: # CLI is expected to overwrite script, do it explicitly
		additional_dictionary['files'] = input_files
		args = other_args
	assert additional_dictionary['files'] >= 2, "extrapolation requires 2 files as input"
	# explicitly clone expansion parameters to position additional MC quantities
	for key, default in (('files', None), ('corrections', ['L1L2L3Res', 'L1L2L3', 'L1L2L3Res', 'L1L2L3', 'L1L2L3']), ('algorithms', ['AK5PFJetsCHS'])):
		if key in additional_dictionary:
			if len(additional_dictionary[key]) > 1:
				additional_dictionary[key] = list(additional_dictionary[key][:2]) * 2
				if inputtuple== 'datamc': additional_dictionary[key] += [additional_dictionary[key][1]]
				elif inputtuple== 'mcmc': additional_dictionary[key] += [additional_dictionary[key][0]] + [additional_dictionary[key][1]]
		else:
			additional_dictionary[key] = default
	try:
		labels = ["({0})".format(name) for name in additional_dictionary.pop('labels')]
	except KeyError:
		try:
			labels = ["({0})".format(name) for name in additional_dictionary.pop('nicks')]
		except KeyError:
			labels = ['Data', 'MC']
	labellist = [
			r"$\\mathit{p}_T$ balance" + " {0}".format(labels[0]),
			r"$\\mathit{p}_T$ balance" + " {0}".format(labels[1]),
			'MPF {0}'.format(labels[0]),
			'MPF {0}'.format(labels[1])]
	if inputtuple == 'datamc':
		labellist.extend([r'$\\mathit{p}_T^\\mathrm{reco}$/$\\mathit{p}_T^\\mathrm{ptcl}$'])
	elif inputtuple == 'mcmc':
		labellist.extend([r'$\\mathit{p}_T^\\mathrm{reco}$/$\\mathit{p}_T^\\mathrm{ptcl}$'+' {}'.format(labels[0].replace('MC',''))])
		labellist.extend([r'$\\mathit{p}_T^\\mathrm{reco}$/$\\mathit{p}_T^\\mathrm{ptcl}$'+' {}'.format(labels[1].replace('MC',''))])
	labellist.extend([r'$\\mathit{p}_T$ balance',
			'MPF',
			'', '', '', '', '', '', '', '', ''])
	yexpress=['ptbalance', 'ptbalance', 'mpf', 'mpf']
	if inputtuple == 'datamc':
		yexpress.extend(["jet1pt/matchedgenjet1pt"])
	elif inputtuple == 'mcmc':
		yexpress.extend(["jet1pt/matchedgenjet1pt","jet1pt/matchedgenjet1pt"])
	nicklist= {
		'datamc':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc','reco_gen_jet'],
		'mcmc':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc','reco_gen_jet', 'reco_gen_jet2'],
		'datadata':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc'],
	}
	markerlist= {
		'datamc':['s', 'o', 's', 'o', '*', 'o', 'o'],
		'mcmc':['s', 'o', 's', 'o', '^', '*', 'o', 'o'],
		'datadata':['s', 'o', 's', 'o', 'o', 'o'],
	}
	fitlist= {
		'datamc':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc','reco_gen_jet','ptbalance_ratio', 'mpf_ratio'],
		'mcmc':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc','reco_gen_jet', 'reco_gen_jet2', 'ptbalance_ratio', 'mpf_ratio'],
		'datadata':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc', 'ptbalance_ratio', 'mpf_ratio'],
	}
	fitnicklist= {
		'datamc':['ptbalance_data_fit', 'ptbalance_mc_fit', 'mpf_data_fit', 'mpf_mc_fit', 'reco_gen_jet_fit', 'ptbalance_ratio_fit', 'mpf_ratio_fit'],
		'mcmc':['ptbalance_data_fit', 'ptbalance_mc_fit', 'mpf_data_fit', 'mpf_mc_fit', 'reco_gen_jet_fit','reco_gen_jet_fit2', 'ptbalance_ratio_fit', 'mpf_ratio_fit'],
		'datadata':['ptbalance_data_fit', 'ptbalance_mc_fit', 'mpf_data_fit', 'mpf_mc_fit', 'ptbalance_ratio_fit', 'mpf_ratio_fit'],
	}
	colorlist= {
		'datamc':['orange', 'darkred', 'royalblue', 'darkblue', 'darkgreen', 'darkred', 'darkblue'],
		'mcmc':['orange', 'darkred', 'royalblue', 'darkblue', 'lightgreen', 'darkgreen', 'darkred', 'darkblue'],
		'datadata':['orange', 'darkred', 'royalblue', 'darkblue', 'darkred', 'darkblue'],
	}
	filllist= {
		'datamc':['none', 'none', 'full', 'full', 'full', 'none', 'full'],
		'mcmc':['none', 'none', 'full', 'full', 'full', 'full', 'none', 'full'],
		'datadata':['none', 'none', 'full', 'full', 'none', 'full'],
	}
	linelist= {
		'datamc':[None, None, None, None, None, None, None, '--', '--', '--', '--', '--', '--', '--'],
		'mcmc':[None, None, None, None, None, None, None, None, '--', '--', '--', '--', '--', '--', '--'],
		'datadata':[None, None, None, None, None, None, '--', '--', '--', '--', '--', '--', '--'],
	}
	d = {
		'filename': 'extrapolation',
		'labels': labellist,
		'alphas': [0.3],
		'zjetfolders': ['noalphacuts'],
		'lines': [1.0],
		'legend': 'lower left',
		'x_expressions': 'alpha',
		'x_bins': '6,0,0.3',
		'x_lims': [0,0.3],
		'y_expressions': yexpress,
		'y_label': 'Jet Response',
		'y_lims': [0.88,1.03],
		'nicks': nicklist[inputtuple],
		'colors': colorlist[inputtuple],
		'markers': markerlist[inputtuple],
		'marker_fill_styles': filllist[inputtuple],
		'line_styles': linelist[inputtuple],
		'line_widths': ['1'],
		'tree_draw_options': 'prof',
		'analysis_modules': ['Ratio', 'FunctionPlot'],
		'ratio_denominator_no_errors': False,
		'plot_modules': ['PlotMplZJet', 'PlotExtrapolationText'],
        	'output_dir' : "plots/%s/" % datetime.date.today().strftime('%Y_%m_%d'),
		'extrapolation_text_nicks': ['ptbalance_ratio_fit', 'mpf_ratio_fit'],
		'extrapolation_text_colors': ['darkred', 'darkblue'],
		'functions': ['[0]+[1]*x'],
		'function_fit': fitlist[inputtuple],
		'function_parameters': ['1,1'],
		'function_ranges': ['0,0.3'],
		'function_nicknames': fitnicklist[inputtuple],
		'ratio_numerator_nicks': ['ptbalance_data', 'mpf_data'],
		'ratio_denominator_nicks': ['ptbalance_mc', 'mpf_mc'],
		'ratio_result_nicks': ['ptbalance_ratio', 'mpf_ratio'],
		'y_subplot_lims': [0.966, 1.034],
		'extrapolation_text_position': [0.18, 1.025],
		'y_subplot_label': '{} / {}'.format(labels[0], labels[1]).replace('(','').replace(')',''),
		'subplot_fraction': 40,
		'subplot_legend': 'lower left',
	}
	if additional_dictionary != None:
		d.update(additional_dictionary)
	return [PlottingJob(plots=[d], args=args)]

def response_bin_comparisons(args=None, additional_dictionary=None, data_quantities=True):
	plots = []

	if additional_dictionary is not None:
		additional_dictionary = additional_dictionary.copy()
		if 'title' in additional_dictionary:
			additional_dictionary.pop('title')
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
		labels = ["{0}".format(l) for l in labels]

	for quantity, title_quantity, bins in zip(
		[
			'zpt',
			'alpha',
			#'npv',
			#'abs(jet1eta)'
		],
		[
			r"$\\mathit{p}_{T}^{Z}$",
			r"$\\alpha$"
			#'$\\mathit{n}_{PV}$',
			#'|$\\mathit{\eta}_{Leading \ Jet}$|'
		],
		[
			"30 40 50 60 75 95 125 180 300 1000",
			"0 0.05 0.1 0.15 0.2 0.25 0.3",
			#"-0.5 4.5 8.5 15.5 21.5 45.5",
			#"0 0.783 1.305 1.93 2.5 2.964 3.139 5.191"
		]
	):
		for method in ['ptbalance', 'mpf']:
			bin_edges = bins.split(" ")
			for i in xrange(len(bin_edges)-1):
				filename_postfix = "{0}-{1}".format(bin_edges[i], bin_edges[i+1])

				d = {
					'x_expressions': [method],
					'x_lims': [0, 2],
					'x_bins': "20,0,2",
					'weights': ["{0}>{1}&&{0}<{2}".format(quantity, bin_edges[i], bin_edges[i+1])],
					'title': "{1} < {0} < {2}".format(title_quantity, bin_edges[i], bin_edges[i+1]),
					'cutlabel': True,
					#'analysis_modules': ['Ratio'],
					'filename': method + "_" + quantity.replace("(", "").replace(")", "") + "_" + filename_postfix,
					#'y_subplot_lims': [0.5, 1.5],
					"nicks": ['nick1', 'nick2'],
					"markers": ['*', '.', None, None],
					"line_styles": [None, None, '-', '-'],
					"colors": ["red", "blue"],
					"labels": [labels[0], labels[1], labels[0] + " Fit", labels[1] + " Fit"],
					"analysis_modules": ["NormalizeToFirstHisto","FunctionPlot"],
					"function_fit": ["nick1", "nick2"],
					"function_nicknames": ["nick1_fit", "nick2_fit"],
					"function_parameters": ["1,1,1"],
					"function_ranges": ["0,2"],
					"functions": ["[0]*exp(-0.5*((x-[1])/[2])**2)"],
				}

				if additional_dictionary != None:
					d.update(additional_dictionary)
				plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def response_nevents(args=None, additional_dictionary=None, data_quantities=True):
	"""Number of Events per Response bin"""
	known_args, args = get_special_parser(args)
	plots = []
	# TODO put these default binning values somewhere more globally
	for quantity, bins in zip(*get_list_slice([
		['zpt', 'npv', 'abs(jet1eta)'],
		['zpt', 'npv','abseta']
	], known_args.no_quantities)):
		d = {
			'x_expressions': [quantity],
			'x_bins': bins,
			'lines': [1.0],
			'analysis_modules': ['Ratio'],
			'ratio_denominator_no_errors': False,
			'filename': "NEvents_" + quantity.replace("(", "").replace(")", ""),
			'y_subplot_lims': [0.0, 2.0],
			'legend': 'upper right',
			'no_weight': True,
		}
		if quantity == 'abs(jet1eta)':
			d['zjetfolders'] = ["noetacuts"]
		if quantity == 'zpt':
			d['x_log'] = True
			d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def response_comparisons(args2=None, additional_dictionary=None, data_quantities=True):
	"""Response (MPF/pTbal) vs zpt npv abs(jet1eta), with ratio"""
	known_args, args = get_special_parser(args2)

	plots = []
	# TODO put these default binning values somewhere more globally
	for quantity, bins in zip(*get_list_slice([
		['zpt', 'npv', 'abs(jet1eta)'],
		['zpt', 'npv','abseta']
	], known_args.no_quantities)):
		for method in get_list_slice([['ptbalance', 'mpf'] + (['trueresponse'] if not data_quantities else [])], known_args.no_methods)[0]:
			d = {
				'y_expressions': [method],
				'x_expressions': [quantity],
				'x_bins': bins,
				'y_lims': [0.6, 1.1],
				'x_errors': [1],
				'tree_draw_options': 'prof',
				'markers': ['.', '*'],
				'cutlabel': True,
				'lines': [1.0],
				'analysis_modules': ['Ratio'],
				'ratio_denominator_no_errors': False,
				'filename': method + "_" + quantity.replace("(", "").replace(")", ""),
				'y_subplot_lims': [0.9, 1.1],
				'legend': 'lower left',
			}
			if quantity == 'abs(jet1eta)':
				d['zjetfolders'] = ["noetacuts"]
			if quantity == 'zpt':
				d['x_log'] = True
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			if method == 'trueresponse':
				d['filename'] = "true_response__vs__" + quantity
				d['weights'] = "matchedgenjet1pt>0"
			if additional_dictionary != None:
				d.update(additional_dictionary)
			plots.append(d)
	return [PlottingJob(plots=plots, args=args)]


def basic_comparisons(args=None, additional_dictionary=None, data_quantities=True, only_normalized=False, channel="mm"):
	"""Comparison of: zpt zy zmass zphi jet1pt jet1eta jet1phi npv, both absolute and normalized"""
	plots = []
	# TODO move this to more general location
	x_dict = {
		'alpha': ['40,0,1'],
		'jet1area': ['40,0.3,0.9'],
		'jet1eta': ['30,-1.5,1.5'],
		'jet1phi': ['20,-3.1415,3.1415',],
		'jet1pt': ['40,0,400'],
		'jet2eta': ['20,-5,5'],
		'jet2phi': ['20,-3.1415,3.1415',],
		'jet2pt': ['30,0,75'],
		'met': ['40,0,100'],
		'metphi': ['20,-3.1415,3.1415',],
		'mpf': ['40,0,2'],
		'npu': ['31,-0.5,30.5'],
		'npumean': ['40,0,40'],
		'npv': ['31,-0.5,30.5'],
		'ptbalance': ['40,0,2'],
		'rawmet': ['40,0,100'],
		'zmass': ['40,71,111'],
		'zphi': ['20,-3.1415,3.1415',],
		'zpt': ['40,0,400'],
		'zy': ['25,-2.5,2.5'],
	}
	x_dict_zl={
		'%s1phi': ['20,-3.1415,3.1415',],
		'%s1pt': ['20,0,150'],
		'%s2pt': ['20,0,150'],
		'%sminuspt': ['20,0,150'],
		'%spluspt': ['20,0,150'],
	}

	quantity_list= ['zpt', 'zy', 'zmass', 'zphi', 'jet1pt', 'jet1eta', 'jet1phi', 'jet1area',
			 'npv', 'npumean', 'rho', 'met', 'metphi', 'rawmet', 'rawmetphi', 'njets',
			 'ptbalance', 'mpf', 'jet2pt', 'jet2eta', 'jet2phi', 'alpha',]
	quantity_list_zl=['%s1pt', '%s1eta', '%s1phi', '%s2pt', '%s2eta', '%s2phi','%sminusphi', '%sminuseta', '%sminuspt', '%splusphi', '%spluseta', '%spluspt']
	# apply channel specific settings
	zl_basenames = []
	if "mm" in channel:
		zl_basenames += ["mu"]
	if "ee" in channel:
		zl_basenames += ["e"]
	for zl_basename in zl_basenames:
		quantity_list.extend(quantity % zl_basename for quantity in quantity_list_zl)
		for key in x_dict_zl:
			x_dict[key % zl_basename] = x_dict_zl[key]

	for q in x_dict:
		if len(x_dict[q]) == 1:
			x_dict[q] += ['best']

	for quantity in quantity_list \
			 + (['run', 'lumi', 'event'] if data_quantities else ['npu']):
		# normal comparison
		d = {
			'x_expressions': [quantity],
			'cutlabel': True,
			'analysis_modules': ['Ratio'],
			'ratio_denominator_no_errors': False,
			'y_subplot_lims': [0.75, 1.25],
			'y_log': quantity in ['jet1pt', 'zpt']
		}
		if quantity in x_dict:
			d["x_bins"] = [x_dict[quantity][0]]
			d["legend"] = x_dict[quantity][1]

		if additional_dictionary:
			d.update(additional_dictionary)
		if quantity == 'alpha' and (additional_dictionary is None or 'zjetfolders' not in additional_dictionary):
			d['zjetfolders'] = ['noalphacuts']

		if quantity=='zphi':
			d['y_rel_lims']=[1,1.3]
		elif quantity== 'zpt':
			d['y_rel_lims']=[1,400]
		if not only_normalized:
			plots.append(d)

		# shape comparison
		d2 = copy.deepcopy(d)
		d2.update({
			'analysis_modules': ['NormalizeToFirstHisto', 'Ratio'],
			'filename': quantity+"_shapeComparison",
			'title': "Shape Comparison",
			'legend': 'upper right',
			'y_subplot_lims': [0.75, 1.25],
		})
		if channel in ("eemm", "mmee"):
			d2['y_label']= 'Electron Events'
		if additional_dictionary:
			d2.update(additional_dictionary)
		plots.append(d2)
	return [PlottingJob(plots=plots, args=args)]

def basic_profile_comparisons(args=None, additional_dictionary=None):
	""" Some basic profile plots. """
	plots = []
	for xquantity, yquantity in zip(['zpt'], ['zmass']):
		d = {
			'x_expressions': [xquantity],
			'y_expressions': [yquantity],
			'analysis_modules': ['Ratio'],
			'ratio_denominator_no_errors': False,
			'tree_draw_options': 'prof',
			'cutlabel': True,
			'y_subplot_lims': [0.99, 1.01],
			'x_log': True,
			'x_bins': "zpt",
			'markers': ['o', 'd'],
		}
		if yquantity == 'zmass':
			z_mass_pdg = 91.1876
			z_width_pdg = 2.4952
			z_peak = 0.01
			z_window = 5
			d['y_lims'] =  [z_mass_pdg - z_window, z_mass_pdg + z_window],
			d['plot_modules'] = ["PlotMplZJet", "PlotMplRectangle"]
			d["rectangle_y"] = [
				z_mass_pdg-z_width_pdg, z_mass_pdg+z_width_pdg,
				z_mass_pdg-z_peak, z_mass_pdg+z_peak,
			]
			d["rectangle_alpha"] = [0.2, 0.5]
			d["rectangle_color"] = ["blue", "green"]
		plots.append(d)
	for x_expression in ['npv', 'npumean']:
		for y_expression in ['rho', 'npv']:
			d = {
				'x_expressions': [x_expression],
				'y_expressions': [y_expression],
				#'y_lims':[0,30],
				'analysis_modules': ['Ratio'],
				'ratio_denominator_no_errors': False,
				'tree_draw_options': 'prof',
				'cutlabel': True,
				'markers': ['o', 'd'],
				'y_subplot_lims': [0.5, 1.5],
				'x_bins': "25,0.5,25.5",
				'legend': 'lower right',
			}
			if (x_expression=='npv' and y_expression=='rho'): d['y_lims']= [0,30]
			plots.append(d)
	if additional_dictionary != None:
		for plot in plots:
			plot.update(additional_dictionary)
	return [PlottingJob(plots=plots, args=args)]


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
			'ratio_denominator_no_errors': False,
		}
		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]


def pf_fractions(args=None, additional_dictionary=None, subtract_hf=True):
	"""PF fractions and contributions to leading jet vs. ZpT, NPV, jet |eta|"""
	plots = []

	# for 'incoming' labels, add them to the PFfraction-labels
	if additional_dictionary is not None:
		additional_dictionary = additional_dictionary.copy()
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
	pflabels = labels
	if labels != ['', '']:
		labels = ["({0})".format(l) for l in labels]

	for absolute_contribution in [False, True]:
		for x_quantity, x_binning in zip(['zpt', 'abs(jet1eta)', 'npv'],
			['zpt', 'abseta', 'npv'],
		):
			# put together the list for quantities, labels, nicks
			pftypes = ["CHad", r"$\\gamma$", "NHad", r"$e$", r"$\\mu$"]
			quantities = ["jet1chf", "jet1pf",
			              ("(jet1nhf-jet1hfhf)" if subtract_hf else "jet1nhf"),  # no subtraction for pre-73X samples
			              "jet1ef", "jet1mf"]
			if x_quantity == 'abs(jet1eta)':
				pftypes += ["HFhad", "HFem"]
				quantities += ["jet1hfhf", "jet1hfemf"]
			plotlabels = []
			nicks = []
			for pftype in pftypes:
				for label in labels:
					plotlabels += [pftype + " " + label]
					nicks +=  [pftype + label]
			d = {
				# input
				"nicks": nicks,
				"stacks": ["a", "b"]*len(pftypes),
				"tree_draw_options": ["prof"],
				"x_expressions": [x_quantity],
				"x_bins": [x_binning],
				"y_expressions": [i for i in quantities for _ in (0,1)],
				# analysis modules
				"analysis_modules": ["Ratio"],
				'ratio_denominator_no_errors': False,
				"ratio_numerator_nicks": nicks[::2],
				"ratio_denominator_nicks": nicks[1::2],
				# formatting
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
				"labels": plotlabels,
				"markers": ["o", "fill"]*len(pftypes) + ["o"]*len(pftypes),
				"y_label": "Leading Jet PF Energy Fraction",
				"y_lims": [0.0, 1.0],
				'y_subplot_lims' : [0, 2],
				'legend': "None",
				"legend_cols": 2,
				# output
				'filename': "PFfractions_{}".format(x_quantity),
			}
			if x_quantity == 'zpt':
				d["x_log"] = True
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			elif x_quantity == 'abs(jet1eta)':
				d["zjetfolders"] = ["noetacuts"]
				d["colors"] = d["colors"][:10]+['black', 'grey', 'red', '#D35658']+d["colors"][10:]+['grey', 'red']
				# legend table options
				d['plot_modules'] = ['PlotMplZJet', 'PlotMplLegendTable']
				d["legend_table_column_headers"] = pflabels
				d["legend_table_row_headers"] = pftypes
				d["legend_table_invert"] = True
				d["legend_table_filename"] = "PF_legend"
			if absolute_contribution:
				d["y_expressions"] = ["{0}*jet1pt".format(i) for i in d["y_expressions"]]
				d.pop("y_lims")
				d["filename"] = "PFcontributions_{}".format(x_quantity)
				d["y_label"] = r"Leading Jet PF Energy / GeV"

			if additional_dictionary != None:
				d.update(additional_dictionary)
			plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def jet_resolution(args=None, additional_dictionary=None):
	"""Plot the jet resolution vs pt, abs(eta) and npv."""
	plots = []

	methoddict = {
		'mpf': 'MPF',
		'ptbalance': r'$\\mathit{p}_T$ balance',
		'trueresponse': r'$p_T^\\mathrm{reco}$/$p_T^\\mathrm{ptcl}$',
	}
	for quantity in ['zpt', 'npv', 'jet1abseta']:
		for method in ['mpf', 'ptbalance', 'trueresponse']:
			d = {
				'cutlabel': True,
				'corrections': ['L1L2L3Res', 'L1L2L3'],
				'x_expressions': quantity,
				'x_bins': [quantity],
				'x_errors': [True],
				'x_log': (True if quantity == 'zpt' else False),
				'y_expressions': [method, method],
				'y_lims': [0.0, 0.5],
				'y_label': 'Jet resolution ({})'.format(methoddict[method]),
				'nicks': ['data', 'mc'],
				'markers': ['o', 'o'],
				'marker_fill_styles': ['full', 'none'],
				'x_errors': [True],
				'tree_draw_options': 'profs',
				'analysis_modules': ['ConvertToHistogram', 'StatisticalErrors',],
				'stat_error_nicks': ['data','mc'],
				'convert_nicks': ['data','mc'],
				'nicks': ['data','mc'],
				'labels': ['data','mc'],
				'filename': 'jet_resolution_{0}_vs_{1}'.format(method, quantity),
			}
			if method == 'trueresponse':
				d['weights'] = ['matchedgenjet1pt > 0']
			if quantity == 'zpt':
				d['x_lims'] = [30, 1000]
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			elif quantity == 'jet1abseta':
				d['zjetfolders'] = ['noetacuts']
				d['x_lims'] = [0, 5.2]
			elif quantity == 'npv':
				d['x_lims'] = [0, 40]

			if additional_dictionary != None:
				d.update(additional_dictionary)
			plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

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
			'markers': ['o', 'fill'],
			'filename': 'cutflow' + ('_relative' if rel else ''),
		}
		plots.append(d)
		if additional_dictionary != None:
			d.update(additional_dictionary)
	return [PlottingJob(plots=plots, args=args)]


def full_comparison(args=None, d=None, data_quantities=True, only_normalized=False,
	                channel="mm", inputtuple="datamc", subtract_hf=True):
	""" Do all comparison plots"""
	plotting_jobs = []
	plotting_jobs += basic_comparisons(args, d, data_quantities, only_normalized, channel)
	plotting_jobs += basic_profile_comparisons(args, d)
	plotting_jobs += pf_fractions(args, d, subtract_hf=subtract_hf)
	plotting_jobs += response_nevents(args, d, data_quantities)
	plotting_jobs += response_comparisons(args, d, data_quantities)
	plotting_jobs += response_extrapolation(args, d, inputtuple)
	plotting_jobs += jet_resolution(args, additional_dictionary=d)
	plotting_jobs += vertex_reco_efficiency(args, d)
	plotting_jobs += z_response(args, d)
	#plotting_jobs += z_pt_resolution(args, d)
	#plotting_jobs += response_rms(args, d)
	plotting_jobs += response_correlations(args, d)
	return plotting_jobs


def comparison_ee_mc(args=None):
	"""Run2: full comparisons for work/ee.root and work/ee_80.root"""
	plotting_jobs = []
	d = {
		'files': ['work/ee.root', 'work/ee_80.root'],
		'labels': ['MC CMSSW 7.6', 'MC CMSSW 8'],
		'corrections': ['L1L2L3', 'L1L2L3'],
		'algorithms': ['ak4PFJetsCHS'],
	}
	plotting_jobs += full_comparison(args, d, data_quantities=False, channel="ee", inputtuple='mcmc')
	d.update({'folders': ['finalcuts_ak4PFJetsCHSL1L2L3', 'finalcuts_ak4PFJetsCHSL1L2L3']})
	plotting_jobs += cutflow(args, d)
	return plotting_jobs

def comparison_mm_mc(args=None):
	"""Run2: full comparisons for work/mm.root and work/mm_80.root"""
	plotting_jobs = []
	d = {
		'files': ['work/mm.root', 'work/mm_80.root'],
		'labels': ['MC CMSSW 7.6', 'MC CMSSW 8'],
		'corrections': ['L1L2L3', 'L1L2L3'],
		'algorithms': ['ak4PFJetsCHS'],
	}
	plotting_jobs += full_comparison(args, d, data_quantities=False, channel="mm", inputtuple='mcmc')
	d.update({'folders': ['finalcuts_ak4PFJetsCHSL1L2L3', 'finalcuts_ak4PFJetsCHSL1L2L3']})
	plotting_jobs += cutflow(args, d)
	return plotting_jobs

def comparison_mmee_mc(args=None):
	"""Run2: full ee mm comparisons for work/mc15_25ns.root and work/mc15_25ns_ee.root"""
	plotting_jobs = []
	d = {
		'files': ['work/ee_80.root', 'mm_80.root'],
		'labels': ['MCe', 'MCmu'],
		'corrections': ['L1L2L3', 'L1L2L3'],
		'algorithms': ['ak4PFJetsCHS'],
	}
	plotting_jobs += full_comparison(args, d, data_quantities=False, channel="eemm", inputtuple='mcmc')
	d.update({'folders': ['finalcuts_ak4PFJetsCHSL1L2L3', 'finalcuts_ak4PFJetsCHSL1L2L3']})
	plotting_jobs += cutflow(args, d)
	return plotting_jobs
#####


if __name__ == '__main__':
	basic_comparisons()
