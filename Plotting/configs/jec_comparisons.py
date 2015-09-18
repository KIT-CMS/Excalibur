#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob

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
	"""Do the extrapolation plot for balance and MPF, add Ratio, display fit parameters."""
	if additional_dictionary is not None:
		additional_dictionary = additional_dictionary.copy()
		if 'files' in additional_dictionary and len(additional_dictionary['files']) == 2:
			files = [
				additional_dictionary['files'][0],
				additional_dictionary['files'][1],
				additional_dictionary['files'][0],
				additional_dictionary['files'][1],
				additional_dictionary['files'][1],
			]
			additional_dictionary.pop('files')
		else:
			files = None
		if 'corrections' in additional_dictionary and len(additional_dictionary['corrections']) == 2:
			corrections = [
				additional_dictionary['corrections'][0],
				additional_dictionary['corrections'][1],
				additional_dictionary['corrections'][0],
				additional_dictionary['corrections'][1],
				additional_dictionary['corrections'][1],
			]
			additional_dictionary.pop('corrections')
		else:
			corrections = ['L1L2L3Res', 'L1L2L3', 'L1L2L3Res', 'L1L2L3', 'L1L2L3']
		if 'algorithms' in additional_dictionary and len(additional_dictionary['algorithms']) == 2:
			algorithms = [
				additional_dictionary['algorithms'][0],
				additional_dictionary['algorithms'][1],
				additional_dictionary['algorithms'][0],
				additional_dictionary['algorithms'][1],
				additional_dictionary['algorithms'][1],
			]
			additional_dictionary.pop('algorithms')
		else:
			algorithms = ['AK5PFJetsCHS']
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

	d = {
		'filename': 'extrapolation',
		'labels': [
			r"$\\mathit{p}_{T}$ balance" + " {0}".format(labels[0]),
			r"$\\mathit{p}_{T}$ balance" + " {0}".format(labels[1]),
			'MPF {0}'.format(labels[0]),
			'MPF {0}'.format(labels[1]),
			r'$p_T^\\mathrm{reco}$/$p_T^\\mathrm{ptcl}$',
			r'$\\mathit{p}_{T}$ balance',
			'MPF',
			'', '', '', '', '', '', '', '', ''],
		'algorithms': algorithms,
		'corrections': corrections,
		'zjetfolders': ['noalphacuts'],
		'lines': [1.0],
		'legend': 'lower left',
		'x_expressions': 'alpha',
		'x_bins': '6,0,0.3',
		'x_lims': [0,0.3],
		'y_expressions': ['ptbalance', 'ptbalance', 'mpf', 'mpf', "jet1pt/matchedgenjet1pt"],
		'y_label': 'Jet Response',
		'y_lims': [0.88,1.03],
		'nicks': ['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc', 'reco_gen_jet'],
		'colors': ['orange', 'darkred', 'royalblue', 'darkblue', 'darkgreen', 'darkred', 'darkblue'],
		'markers': ['s', 'o', 's', 'o', '*', 'o', 'o'],
		'marker_fill_styles': ['none', 'none', 'full', 'full', 'full', 'none', 'full'],
		'line_styles': [None, None, None, None, None, None, None, '--', '--', '--', '--', '--', '--', '--'],
		'line_widths': ['1'],
		'tree_draw_options': 'prof',
		'analysis_modules': ['Ratio', 'FunctionPlot'],
		'plot_modules': ['PlotMplZJet', 'PlotExtrapolationText'],
		'extrapolation_text_nicks': ['ptbalance_ratio_fit', 'mpf_ratio_fit'],
		'extrapolation_text_colors': ['darkred', 'darkblue'],
		'functions': ['[0]+[1]*x'],
		'function_fit': ['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc', 'reco_gen_jet', 'ptbalance_ratio', 'mpf_ratio'],
		'function_parameters': ['1,1'],
		'function_ranges': ['0,0.3'],
		'function_nicknames': ['ptbalance_data_fit', 'ptbalance_mc_fit', 'mpf_data_fit', 'mpf_mc_fit', 'reco_gen_jet_fit', 'ptbalance_ratio_fit', 'mpf_ratio_fit'],
		'ratio_numerator_nicks': ['ptbalance_data', 'mpf_data'],
		'ratio_denominator_nicks': ['ptbalance_mc', 'mpf_mc'],
		'ratio_result_nicks': ['ptbalance_ratio', 'mpf_ratio'],
		'y_subplot_lims': [0.966, 1.015],
		'y_subplot_label': 'Data / MC',
		'subplot_fraction': 40,
		'subplot_legend': 'lower left',
	}

	if files is not None:
		d['files'] = files

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
			#'npv',
			#'abs(jet1eta)'
		],
		[
			r"$\\mathit{p}_{T}^{Z}$",
			#'$\\mathit{n}_{PV}$',
			#'|$\\mathit{\eta}_{Leading \ Jet}$|'
		],
		[
			"30 40 50 60 75 95 125 180 300 1000",
			#"-0.5 4.5 8.5 15.5 21.5 45.5",
			#"0 0.783 1.305 1.93 2.5 2.964 3.139 5.191"
		]
	):
		for method in ['ptbalance']:
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
			if method == 'trueresponse':
				d['filename'] = "true_response__vs__" + quantity
				d['weights'] = "matchedgenjet1pt>0"
			if additional_dictionary != None:
				d.update(additional_dictionary)
			plots.append(d)
	return [PlottingJob(plots=plots, args=args)]


def basic_comparisons(args=None, additional_dictionary=None, data_quantities=True, only_normalized=False):
	"""Comparison of: zpt zy zmass zphi jet1pt jet1eta jet1phi npv, both absolute and normalized"""
	plots = []
	# TODO move this to more general location
	x_dict = {
		'npv': ["31,-0.5,30.5"],
		'npu': ["31,-0.5,30.5"],
		'npumean': ["40,0,40"],
		'mu1pt': ["20,0,150"],
		'mu2pt': ["20,0,150"],
		'mupluspt': ["20,0,150"],
		'muminuspt': ["20,0,150"],
		'met': ["20,0,100"],
		'rawmet': ["20,0,100"],
		'ptbalance': ["20,0,2"],
		'mpf': ["20,0,2"],
		'jet2pt': ["15,0,75"],
		'mu1phi': ["20,-3.1415,3.1415", "lower center"],
		'jet2phi': ["20,-3.1415,3.1415", "lower center"],
		'jet1phi': ["20,-3.1415,3.1415", "lower center"],
		'metphi': ["20,-3.1415,3.1415", "lower center"],
		'zphi': ["20,-3.1415,3.1415", "lower center"],
		'jet2eta': ["20,-5,5"],
		'jet1pt': ["20,0,400"],
		'jet1area': ["20,0.7,0.9"],
		'zpt': ["20,0,400"],
		'zy': ["25,-2.5,2.5"],
		'alpha': ["20,0,1"],
	}
	for q in x_dict:
		if len(x_dict[q]) == 1:
			x_dict[q] += ['best']

	for quantity in ['zpt', 'zy', 'zmass', 'zphi', 'jet1pt', 'jet1eta', 'jet1phi', 'jet1area',
			 'npv', 'npumean', 'rho', 'met', 'metphi', 'rawmet', 'rawmetphi', 'njets',
			 'mu1pt', 'mu1eta', 'mu1phi', 'mu2pt', 'mu2eta', 'mu2phi',
			 'ptbalance', 'mpf', 'jet2pt', 'jet2eta', 'jet2phi', 'alpha',
			 'muminusphi', 'muminuseta', 'muminuspt', 'muplusphi', 'mupluseta', 'mupluspt'] \
			 + (['run', 'lumi', 'event'] if data_quantities else ['npu']):
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
		if quantity == 'alpha' and (additional_dictionary is None or 'zjetfolders' not in additional_dictionary):
			d['zjetfolders'] = ['noalphacuts']

		if not only_normalized:
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
	return [PlottingJob(plots=plots, args=args)]

def basic_profile_comparisons(args=None, additional_dictionary=None):
	""" Some basic profile plots. """
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
			'x_bins': "zpt",
			'markers': ['o', 'd'],
		}
		plots.append(d)

		for x_expression in ['npv', 'npumean']:
			for y_expression in ['rho', 'npv']:
				d = {
					'x_expressions': [x_expression],
					'y_expressions': [y_expression],
					'analysis_modules': ['Ratio'],
					'tree_draw_options': 'prof',
					'cutlabel': True,
					'markers': ['o', 'd'],
					'y_subplot_lims': [0.5, 1.5],
					'x_bins': "25,0.5,25.5",
					'legend': 'lower right',
				}
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
		}
		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]


def pf_fractions(args=None, additional_dictionary=None):
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
			quantities = ["jet1chf", "jet1pf", "jet1nhf", "jet1ef", "jet1mf"]
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
				'x_log': (True if quantity == 'zpt' else False),
				'y_expressions': method,
				'y_lims': [0.0, 0.5],
				'y_label': 'Jet resolution ({})'.format(methoddict[method]),
				'nicks': ['data', 'mc'],
				'markers': ['o', 'o'],
				'marker_fill_styles': ['full', 'none'],
				'x_errors': [True],
				'tree_draw_options': 'prof',
				'analysis_modules': ['JetResolution'],
				'response_nicks': ['data', 'mc'],
				'resolution_nicks': ['data_resolution', 'mc_resolution'],
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


def full_comparison(args=None, d=None, data_quantities=True, only_normalized=False):
	""" Do all comparison plots"""
	plotting_jobs = []
	plotting_jobs += basic_comparisons(args, d, data_quantities, only_normalized)
	plotting_jobs += basic_profile_comparisons(args, d)
	plotting_jobs += pf_fractions(args, d)
	plotting_jobs += response_comparisons(args, d, data_quantities)
	plotting_jobs += response_extrapolation(args, d)
	plotting_jobs += jet_resolution(args, additional_dictionary=d)
	return plotting_jobs


def muon_2d(args=None, additional_dictionary=None):
	"""2D plot of muon eta-phi-distribution. works for one file."""
	d = {
		# input
		'folders': ['nocuts_AK5PFJetsCHSL1L2L3/muons'],
		'y_expressions': ['object.p4.Phi()'],
		'x_expressions': ['object.p4.Eta()'],
		'no_weight': True,
		'x_bins': '200,-2.3,2.3',
		'y_bins': '200,-3.14159,3,14159',
		# formatting
		'y_lims': [-3.14159, 3,14159],
		'x_label': 'mueta',
		'y_label': 'muphi',
		# output
		'filename': 'muon_eta_phi',
	}
	if additional_dictionary != None:
		d.update(additional_dictionary)
	return [PlottingJob(plots=[d], args=args)]

def comparison_datamc(args=None):
	"""full data mc comparisons for work/data.root and work/mc.root"""
	plotting_jobs = []
	d = {
		'files': ['work/data.root', 'work/mc.root'],
		'labels': ['Data', 'MC'],
		'corrections': ['L1L2L3Res', 'L1L2L3'],
		'legend': None,
	}
	plotting_jobs += full_comparison(args, d)
	return plotting_jobs

def comparison_run2(args=None):
	"""Comparison for run2 samples."""
	plotting_jobs = []
	d = {
		'files': [
			'work/data15.root',
			'work/mc15.root',
		],
		'labels': ['Data L1L2L3Res','MC L1L2L3'],
		'y_subplot_label' : "Data/MC",
		'algorithms': ['ak4PFJetsCHS'],
		'corrections': ['L1L2L3Res', 'L1L2L3'],
	}
	plotting_jobs += full_comparison(args, d, only_normalized=True)

	d.update({'folders': ['finalcuts_ak4PFJetsCHSL1L2L3Res', 'finalcuts_ak4PFJetsCHSL1L2L3']})
	plotting_jobs += cutflow(args, d)

	jec_factors.jec_factors(args, {
		'files': ['work/mc15.root'],
		'algorithms': ['ak4PFJetsCHS'],
		'corrections': ['L1L2L3'],
	}, rc=False, res=False)

	return plotting_jobs

def comparison_run2_jec(args=None):
	""" evaluate the latest JEC files for RUn2"""
	jec_files.jec_files(args+[
		'--jec-dir','data/jec/PY8_RunIISpring15DR74_bx50',
		'--jec-algo', 'AK4PFchs',
	])


if __name__ == '__main__':
	basic_comparisons()
