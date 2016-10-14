#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files

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

def response_extrapolation(args=None, additional_dictionary=None, inputtuple='datamc'):
	"""Do the extrapolation plot for balance and MPF, add Ratio, display fit parameters. Default is an input tuple of data, mc, also possible is datadata and mcmc."""
	additional_dictionary = additional_dictionary.copy() if additional_dictionary else {}
	input_files, other_args = get_input_files(args)
	if input_files: # CLI is expected to overwrite script, do it explicitly
		additional_dictionary['files'] = input_files
		args = other_args
	assert additional_dictionary['files'] >= 2, "extrapolation requires 2 files as input"
	# explicitly clone expansion parameters to position additional MC quantities
	for key, default in (('files', None), ('corrections', ['L1L2L3Res', 'L1L2L3', 'L1L2L3Res', 'L1L2L3', 'L1L2L3'])):#, ('algorithms', ['AK5PFJetsCHS'])):
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
		'zjetfolders': ['noalphacuts'], #for the case, that alpha values beyond the alpha cut should be included into the extrapolation
		'lines': [1.0],
		'legend': 'lower left',
		'x_expressions': 'alpha',
		'x_bins': '6,0,0.3',
		'x_lims': [0,0.3],
		'y_expressions': yexpress,
		'y_label': 'Jet Response',
		#'y_lims': [0.88,1.03], #for Zmm
		'y_lims': [0.77,1.05], #for Zee
		'nicks': nicklist[inputtuple],
		'colors': colorlist[inputtuple],
		'markers': markerlist[inputtuple],
		'marker_fill_styles': filllist[inputtuple],
		'line_styles': linelist[inputtuple],
		'line_widths': ['1'],
		'tree_draw_options': 'prof',
		'analysis_modules': ['Ratio', 'FunctionPlot'],
		'plot_modules': ['PlotMplZJet', 'PlotExtrapolationText'],
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
		'ratio_denominator_no_errors': False,
		#'y_subplot_lims': [0.966, 1.034], #for Zmm
		'y_subplot_lims': [0.93, 1.1], #for Zee
		'extrapolation_text_position': [0.18, 1.025],
		'y_subplot_label': '{} / {}'.format(labels[0], labels[1]).replace('(','').replace(')',''),
		'subplot_fraction': 40,
		'subplot_legend': 'upper left',
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
				'y_lims': [0.6, 1.2],
				'x_errors': [1],
				'tree_draw_options': 'prof',
				'markers': ['o', 's'],
				'cutlabel': True,
				'lines': [1.0],
				'analysis_modules': ['Ratio'],
				#'analysis_modules': ['Divide'],
				'ratio_denominator_no_errors': False,
				'filename': method + "_" + quantity.replace("(", "").replace(")", ""),
				'y_subplot_lims': [0.8, 1.2],
				'legend': 'lower left',
			}
#########################################################
			if method == 'mpf':
				d['y_lims'] = [0.9,1.05]
			if method == 'ptbalance':
				if quantity == 'abs(jet1eta)':
					d['y_lims'] = [0.72,0.93]
				else:
					d['y_lims'] = [0.82,0.96]
#					d['legend'] = ['lower right']
#########################################################
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




def full_comparison(args=None, d=None, data_quantities=True, only_normalized=True,
	                channel="mm", inputtuple="datamc", subtract_hf=True):
	""" Do all comparison plots"""
	plotting_jobs = []
#	plotting_jobs += basic_comparisons(args, d, data_quantities, only_normalized, channel)
#	plotting_jobs += basic_profile_comparisons(args, d)
#	plotting_jobs += pf_fractions(args, d, subtract_hf=subtract_hf)
#	plotting_jobs += response_nevents(args, d, data_quantities)
	plotting_jobs += response_comparisons(args, d, data_quantities)
	plotting_jobs += response_extrapolation(args, d, inputtuple)
#	plotting_jobs += jet_resolution(args, additional_dictionary=d)
	return plotting_jobs


def muon_2d(args=None, additional_dictionary=None):
	"""2D plot of muon eta-phi-distribution. works for one file."""
	d = {
		# input
		'folders': ['nocuts_L1L2L3/muons'],
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

def my_comparison_datamc_Zee_CHS(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	Res=True # disable/enable residual corrrections
	plotting_jobs = []
	d = {
		'files': [	'/storage/a/cheidecker/zjets/excalibur/mc16_25ns_ee_2016-08-03_02-56/out.root',
					#'/storage/a/cheidecker/zjets/excalibur/data16_25ns_ee_2016-08-03_09-24/out.root'],
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_ee_all.root'],
#					'/storage/jbod/tberger/working/excalibur/data16G_25ns_ee_2016-09-06_12-32/out.root'],
		'corrections': ['L1L2L3', 'L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3'],
		#'algorithms': ['ak4PFJetsCHS'],
		#'weights'	: [	'1',#'(run>272007 && run<275376)','(run>275657 && run<276283)','(run>276315 && run<276811)'
		#				'(run>272007 && run<276811)'],
		#				'(run>276831 && run<278808)'],#'(run>276831 && run<277420)','(run>277772 && run<278808)'
		#				'(run>278820)'],
		'www_title': 'Comparison of Datasets for Zee, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		'www': 'comparison_datamc_Zee_CHS_miniAOD',
		#'y_lims' : [0.73, 1.05],
		'labels': ['MC','Data'],
		'y_subplot_label' : "Data/MC",
		'y_subplot_lims' : [0.97,1.07],
		'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"],
		'texts_x': [0.84],
		'texts_y': [0.93],
		'texts_size': [20],
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
#		'lumis': [20.88],
	}
	plotting_jobs += full_comparison(args, d, channel="ee", inputtuple='datadata')  # usually datamc
	d.update({'folders': ['finalcuts_L1L2L3Res', 'finalcuts_L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3']})
	return plotting_jobs

def my_comparison_datamc_Zmm_CHS(args=None):
	"""Run2: full data mc comparisons for work/data16BCD_25ns_mm.root and work/mc16_25ns_mm.root"""
	Res=True # disable/enable residual corrrections
	plotting_jobs = []
	d = {
		'files': [	'/storage/a/cheidecker/zjets/excalibur/mc16_25ns_2016-08-03_01-36/out.root',
					#'/storage/a/cheidecker/zjets/excalibur/data16_25ns_2016-08-02_16-49/out.root'],
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_mm_all.root'],
		'corrections': ['L1L2L3', 'L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3'],
		#'algorithms': ['ak4PFJetsCHS'],
		#'weights'	: [	'1',#'(run>272007 && run<275376)','(run>275657 && run<276283)','(run>276315 && run<276811)'
		#				'(run>272007 && run<276811)',
		#				'(run>276831 && run<278808)',#'(run>276831 && run<277420)','(run>277772 && run<278808)'
		#				'(run>278820)'],
		'www_title': 'Comparison of Datasets for Zmm, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		'www': 'comparison_datamc_Zmm_CHS_miniAOD',
#		'y_lims' : [0.73, 1.05],
		'labels': ['MC','Data'],
		'y_subplot_label' : "Data/MC",
		'y_subplot_lims' : [0.989,1.05],
		'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$"],
		'texts_x': [0.84],
		'texts_y': [0.93],
		'texts_size': [20],
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
#		'lumis': [20.88],
	}
	plotting_jobs += full_comparison(args, d, channel="mm", inputtuple='datadata')  # usually datamc
	d.update({'folders': ['finalcuts_L1L2L3Res', 'finalcuts_L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3']})
	return plotting_jobs
def my_comparison_datamc_Zee_PUPPI(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	Res=True # disable/enable residual corrrections
	plotting_jobs = []
	d = {
		'files': [	'/storage/a/cheidecker/zjets/excalibur/mc16_25ns_ee_2016-08-03_02-56/out.root',
					'/storage/jbod/tberger/zjets/excalibur_data16_25ns_ee.root',
					'/storage/jbod/tberger/zjets/excalibur_data16_25ns_puppi_ee.root'],
		'corrections': ['', '', ''] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3'],
		#'algorithms': ['ak4PFJetsCHS'],
		#'weights'	: [	'1',#'(run>272007 && run<275376)','(run>275657 && run<276283)','(run>276315 && run<276811)'
		#				'(run>272007 && run<276811)'],
		#				'(run>276831 && run<278808)'],#'(run>276831 && run<277420)','(run>277772 && run<278808)'
		#				'(run>278820)'],
		'www_title': 'Comparison of Datasets for Zee, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		'www': 'comparison_datamc_Zee_PUPPI',
		#'y_lims' : [0.73, 1.05],
		'labels': ['MC CHS','Data CHS','Data PUPPI'],
#		'y_subplot_label' : "Data/MC",
#		'y_subplot_lims' : [0.97,1.07],
		'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"],
		'texts_x': [0.84],
		'texts_y': [0.93],
		'texts_size': [20],
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
#		'lumis': [20.88],
	}
	plotting_jobs += full_comparison(args, d, channel="ee", inputtuple='datamc')  # usually datamc
	d.update({'folders': ['finalcuts_L1L2L3Res', 'finalcuts_L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3']})
	return plotting_jobs

def my_comparison_datamc_Zmm_PUPPI(args=None):
	"""Run2: full data mc comparisons for work/data16BCD_25ns_mm.root and work/mc16_25ns_mm.root"""
	Res=True # disable/enable residual corrrections
	plotting_jobs = []
	d = {
		'files': [	'/storage/a/cheidecker/zjets/excalibur/mc16_25ns_2016-08-03_01-36/out.root',
					'/storage/jbod/tberger/zjets/excalibur_data16_25ns_mm.root',
					'/storage/jbod/tberger/zjets/excalibur_data16_25ns_puppi_mm.root'],
		'corrections': ['', '', ''] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3'],
		#'algorithms': ['ak4PFJetsCHS'],
		#'weights'	: [	'1',#'(run>272007 && run<275376)','(run>275657 && run<276283)','(run>276315 && run<276811)'
		#				'(run>272007 && run<276811)',
		#				'(run>276831 && run<278808)',#'(run>276831 && run<277420)','(run>277772 && run<278808)'
		#				'(run>278820)'],
		'www_title': 'Comparison of Datasets for Zmm, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		'www': 'comparison_datamc_Zmm_PUPPI',
#		'y_lims' : [0.73, 1.05],
		'labels': ['MC CHS','Data CHS','Data PUPPI'],
#		'y_subplot_label' : "Data/MC",
#		'y_subplot_lims' : [0.989,1.05],
		'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$"],
		'texts_x': [0.84],
		'texts_y': [0.93],
		'texts_size': [20],
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
#		'lumis': [20.88],
	}
	plotting_jobs += full_comparison(args, d, channel="mm", inputtuple='datamc')  # usually datamc
	d.update({'folders': ['finalcuts_L1L2L3Res', 'finalcuts_L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3']})
	return plotting_jobs

def my_comparison_datamc_Zee_AOD(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	Res=True # disable/enable residual corrrections
	plotting_jobs = []
	d = {
		'files': [	'/storage/a/cheidecker/zjets/excalibur/mc16_25ns_ee_2016-08-03_02-56/out.root',
					'/storage/a/cheidecker/zjets/excalibur/data16_25ns_ee_2016-08-03_09-24/out.root',
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_ee_all.root'],
#					'/storage/jbod/tberger/working/excalibur/data16G_25ns_ee_2016-09-06_12-32/out.root'],
		'corrections': ['L1L2L3', 'L1L2L3', 'L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3'],
		#'algorithms': ['ak4PFJetsCHS'],
		'weights'	: [	'1',#'(run>272007 && run<275376)','(run>275657 && run<276283)','(run>276315 && run<276811)'
						'run<276811',
						'run<276811'],
		#				'(run>272007 && run<276811)'],
		#				'(run>276831 && run<278808)'],#'(run>276831 && run<277420)','(run>277772 && run<278808)'
		#				'(run>278820)'],
		'www_title': 'Comparison of Datasets for Zee, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		'www': 'comparison_datamc_Zee_AOD',
		#'y_lims' : [0.73, 1.05],
		'labels': ['MC','Data AOD','Data miniAOD'],
		'y_subplot_label' : "Data/MC",
		'y_subplot_lims' : [0.97,1.07],
		'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"],
		'texts_x': [0.84],
		'texts_y': [0.93],
		'texts_size': [20],
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
#		'lumis': [20.88],
	}
	plotting_jobs += full_comparison(args, d, channel="ee", inputtuple='datamc')  # usually datamc
	d.update({'folders': ['finalcuts_L1L2L3Res', 'finalcuts_L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3']})
	return plotting_jobs

def my_comparison_datamc_Zmm_AOD(args=None):
	"""Run2: full data mc comparisons for work/data16BCD_25ns_mm.root and work/mc16_25ns_mm.root"""
	Res=True # disable/enable residual corrrections
	plotting_jobs = []
	d = {
		'files': [	'/storage/a/cheidecker/zjets/excalibur/mc16_25ns_2016-08-03_01-36/out.root',
					'/storage/a/cheidecker/zjets/excalibur/data16_25ns_2016-08-02_16-49/out.root',
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_mm_all.root'],
		'corrections': ['L1L2L3', 'L1L2L3', 'L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3'],
		#'algorithms': ['ak4PFJetsCHS'],
		'weights'	: [	'1',#'(run>272007 && run<275376)','(run>275657 && run<276283)','(run>276315 && run<276811)'
						'run<276811',
						'run<276811'],
		#				'(run>272007 && run<276811)',
		#				'(run>276831 && run<278808)',#'(run>276831 && run<277420)','(run>277772 && run<278808)'
		#				'(run>278820)'],
		'www_title': 'Comparison of Datasets for Zmm, AOD and miniAOD to MC, run2',
		'www_text':'Run2: full dataAOD/dataminiAOD/MC comparisons for Run2',
		'www': 'comparison_datamc_Zmm_AOD',
#		'y_lims' : [0.73, 1.05],
		'labels': ['MC','Data AOD','Data miniAOD'],
#		'y_subplot_label' : "Data/MC",
#		'y_subplot_lims' : [0.989,1.05],
		'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$"],
		'texts_x': [0.84],
		'texts_y': [0.93],
		'texts_size': [20],
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
#		'lumis': [20.88],
	}
	plotting_jobs += full_comparison(args, d, channel="mm", inputtuple='datamc')  # usually datamc
	d.update({'folders': ['finalcuts_L1L2L3Res', 'finalcuts_L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3']})
	return plotting_jobs

def my_comparison_datamc_Zee_all(args=None):
	"""Run2: full data mc comparisons for work/data16BCD_25ns_mm.root and work/mc16_25ns_mm.root"""
	Res=True # disable/enable residual corrrections
	plotting_jobs = []
	d = {
		'files': [	'/storage/a/cheidecker/zjets/excalibur/mc16_25ns_ee_2016-08-03_02-56/out.root',
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_BCD_ee.root',
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_E_ee.root',
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_F_ee.root',
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_G_ee.root'],
		'corrections': ['L1L2L3', 'L1L2L3', 'L1L2L3', 'L1L2L3', 'L1L2L3'],# if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3'],
		#'algorithms': ['ak4PFJetsCHS'],
		'weights'	: [	'1',#'(run>272007 && run<275376)','(run>275657 && run<276283)','(run>276315 && run<276811)'
						'(run>272007 && run<276811)',
						'(run>276831 && run<277420)',
						'(run>277772 && run<278808)',#'(run>276831 && run<277420)','(run>277772 && run<278808)'
						'(run>278820)'],
		'colors' : ['black','red','blue','green','orange'],
		'www_title': 'Comparison of Datasets for Zee, AOD and miniAOD to MC, run2',
		'www_text':'Run2: full dataAOD/dataminiAOD/MC comparisons for Run2',
		'www': 'comparison_datamc_Zee_BCD-E-F-G',
#		'y_lims' : [0.73, 1.05],
		'labels': ['MC','Data BCD','Data E','Data F','Data G'],
#		'y_subplot_label' : "Data/MC",
#		'y_subplot_lims' : [0.989,1.05],
		'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"],
		'texts_x': [0.84],
		'texts_y': [0.93],
		'texts_size': [20],
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
#		'lumis': [20.88],
	}
	plotting_jobs += full_comparison(args, d, channel="mm", inputtuple='datamc')  # usually datamc
	d.update({'folders': ['finalcuts_L1L2L3Res', 'finalcuts_L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3']})
	return plotting_jobs

def my_comparison_datamc_Zmm_all(args=None):
	"""Run2: full data mc comparisons for work/data16BCD_25ns_mm.root and work/mc16_25ns_mm.root"""
	Res=True # disable/enable residual corrrections
	plotting_jobs = []
	d = {
		'files': [	'/storage/a/cheidecker/zjets/excalibur/mc16_25ns_2016-08-03_01-36/out.root',
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_BCD_mm.root',
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_E_mm.root',
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_F_mm.root',
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_G_mm.root'],
		'corrections': ['L1L2L3', 'L1L2L3', 'L1L2L3', 'L1L2L3', 'L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3'],
		#'algorithms': ['ak4PFJetsCHS'],
		'weights'	: [	'1',#'(run>272007 && run<275376)','(run>275657 && run<276283)','(run>276315 && run<276811)'
						'(run>272007 && run<276811)',
						'(run>276831 && run<277420)',
						'(run>277772 && run<278808)',#'(run>276831 && run<277420)','(run>277772 && run<278808)'
						'(run>278820)'],
		'www_title': 'Comparison of Datasets for Zmm, AOD and miniAOD to MC, run2',
		'www_text':'Run2: full dataAOD/dataminiAOD/MC comparisons for Run2',
		'www': 'comparison_datamc_Zmm_BCD-E-F-G',
#		'y_lims' : [0.73, 1.05],
		'labels': ['MC','Data BCD','Data E','Data F','Data G'],
#		'y_subplot_label' : "Data/MC",
#		'y_subplot_lims' : [0.989,1.05],
		'colors' : ['black','red','blue','green','orange'],
		'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$"],
		'texts_x': [0.84],
		'texts_y': [0.93],
		'texts_size': [20],
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
#		'lumis': [20.88],
	}
	plotting_jobs += full_comparison(args, d, channel="mm", inputtuple='datamc')  # usually datamc
	d.update({'folders': ['finalcuts_L1L2L3Res', 'finalcuts_L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3']})
	return plotting_jobs
	
def my_comparison_data_Zmmee(args=None):
	"""Run2: full data mc comparisons for work/data16BCD_25ns_mm.root and work/mc16_25ns_mm.root"""
	Res=True # disable/enable residual corrrections
	plotting_jobs = []
	d = {
		'files': [	'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_mm_all.root',
					'/storage/jbod/tberger/zjets/excalibur_results_2016-10-07/excalibur_data16_25ns_ee_all.root'],
		'corrections': ['L1L2L3', 'L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3'],
		#'algorithms': ['ak4PFJetsCHS'],
		'weights'	: [	#'(run>272007 && run<275376)','(run>275657 && run<276283)','(run>276315 && run<276811)'
						#'(run>272007 && run<276811)','(run>272007 && run<276811)'],
						#'(run>276831 && run<277420)','(run>276831 && run<277420)'],
						'(run>277772 && run<278808)','(run>277772 && run<278808)'],#'(run>276831 && run<277420)','(run>277772 && run<278808)'
		#				'(run>278820)','(run>278820)'],
		'colors' : ['blue','red'],
		'www_title': 'Comparison of Datasets for Zmm and Zee, run2',
		'www_text':'Run2: full data comparisons for Zee and Zmm, Run2',
		'www': 'comparison_data_Zmmee_F',
#		'y_lims' : [0.73, 1.05],
		'labels': [	#'DataBCD, 'r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$", 
					#'DataE, 'r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",
					'DataF, 'r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",
					#'Data, 'r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",
					#'DataBCD, 'r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"],
					#'DataE, 'r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"],
					'DataF, 'r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"],
					#'Data, 'r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"],
		'y_subplot_label' : "mm/ee",
		'y_subplot_lims' : [0.989,1.015],
#		'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$"],
		'texts_x': [0.84],
		'texts_y': [0.93],
		'texts_size': [20],
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
#		'lumis': [20.88],
	}
	plotting_jobs += full_comparison(args, d, channel="mm", inputtuple='datamc')  # usually datamc
	d.update({'folders': ['finalcuts_L1L2L3Res', 'finalcuts_L1L2L3'] if not Res == False else ['finalcuts_L1L2L3', 'finalcuts_L1L2L3']})
	return plotting_jobs

if __name__ == '__main__':
	basic_comparisons()
