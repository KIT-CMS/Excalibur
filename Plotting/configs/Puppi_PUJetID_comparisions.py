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
	ad = copy.deepcopy(additional_dictionary) if additional_dictionary else {}
	for quantity in ["files", "corrections", "algorithms", "zjetfolders"]:
		ad[quantity].append(ad[quantity][1])
		ad[quantity].extend(ad[quantity])
	ad["labels"].append("CHS with PUJetID")
	
	try:
		labels = ["({0})".format(name) for name in ad.pop('labels')]
	except KeyError:
		try:
			labels = ["({0})".format(name) for name in ad.pop('nicks')]
		except KeyError:
			labels = ['Data', 'MC']
	labellist = [
			r"$\\mathit{p}_T$ balance" + " {0}".format(labels[0]),
			r"$\\mathit{p}_T$ balance" + " {0}".format(labels[1]),
			r"$\\mathit{p}_T$ balance" + " {0}".format(labels[2]),
			'MPF {0}'.format(labels[0]),
			'MPF {0}'.format(labels[1]),
			'MPF {0}'.format(labels[2])]
	labellist.extend(['', '', '', '', '', ''])
	yexpress=['ptbalance', 'ptbalance', 'ptbalance', 'mpf', 'mpf', 'mpf']
	nicklist= {
		'datamc':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc','reco_gen_jet'],
		'mcmc':['ptbalance_puppi', 'ptbalance_chs', 'ptbalance_chs_pujetid','mpf_puppi', 'mpf_chs', 'mpf_chs_pujetid'],
		'datadata':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc'],
	}
	markerlist= {
		'datamc':['s', 'o', 's', 'o', '*', 'o', 'o'],
		'mcmc':['s', 'o',  '^', 's', 'o', '^'],
		'datadata':['s', 'o', 's', 'o', 'o', 'o'],
	}
	fitlist= {
		'datamc':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc','reco_gen_jet','ptbalance_ratio', 'mpf_ratio'],
		'mcmc':['ptbalance_puppi', 'ptbalance_chs', 'ptbalance_chs_pujetid','mpf_puppi', 'mpf_chs', 'mpf_chs_pujetid'],
		'datadata':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc', 'ptbalance_ratio', 'mpf_ratio'],
	}
	fitnicklist= {
		'datamc':['ptbalance_data_fit', 'ptbalance_mc_fit', 'mpf_data_fit', 'mpf_mc_fit', 'reco_gen_jet_fit', 'ptbalance_ratio_fit', 'mpf_ratio_fit'],
		'mcmc':['ptbalance_puppi_fit', 'ptbalance_chs_fit', 'ptbalance_chs_pujetid_fit','mpf_puppi_fit', 'mpf_chs_fit', 'mpf_chs_pujetid_fit'],
		'datadata':['ptbalance_data_fit', 'ptbalance_mc_fit', 'mpf_data_fit', 'mpf_mc_fit', 'ptbalance_ratio_fit', 'mpf_ratio_fit'],
	}
	colorlist= {
		'datamc':['orange', 'darkred', 'royalblue', 'darkblue', 'darkgreen', 'darkred', 'darkblue'],
		'mcmc':['orange', 'darkred', 'red', 'royalblue', 'darkblue', 'lightblue'],
		'datadata':['orange', 'darkred', 'royalblue', 'darkblue', 'darkred', 'darkblue'],
	}
	filllist= {
		'datamc':['none', 'none', 'full', 'full', 'full', 'none', 'full'],
		'mcmc':['none', 'none', 'none', 'full', 'full', 'full'],
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
		'alphas': [0.25],
		'lines': [1.0],
		'legend': 'lower left',
		'x_expressions': 'alpha',
		'x_bins': '6,0,0.3',
		'x_lims': [0,0.3],
		'y_expressions': yexpress,
		'y_label': 'Jet Response',
		'y_lims': [0.8,1.05],
		'weights' : ['1','1','jet1puidtight==1&jet2puidtight==1','1','1','jet1puidtight==1&jet2puidtight==1'],
		'nicks': nicklist[inputtuple],
		'colors': colorlist[inputtuple],
		'markers': markerlist[inputtuple],
		'marker_fill_styles': filllist[inputtuple],
		'line_styles': linelist[inputtuple],
		'line_widths': ['1'],
		'tree_draw_options': 'prof',
		'analysis_modules': ['FunctionPlot'],
		#'ratio_denominator_no_errors': False,
		'plot_modules': ['PlotMplZJet'],
		#'extrapolation_text_nicks': ['ptbalance_ratio_fit', 'mpf_ratio_fit'],
		#'extrapolation_text_colors': ['darkred', 'darkblue'],
		'functions': ['[0]+[1]*x'],
		'function_fit': fitlist[inputtuple],
		'function_parameters': ['1,1'],
		'function_ranges': ['0,0.3'],
		'function_nicknames': fitnicklist[inputtuple],
		#'ratio_numerator_nicks': ['ptbalance_data', 'mpf_data'],
		#'ratio_denominator_nicks': ['ptbalance_mc', 'mpf_mc'],
		#'ratio_result_nicks': ['ptbalance_ratio', 'mpf_ratio'],
		#'y_subplot_lims': [0.966, 1.034],
		#'extrapolation_text_position': [0.18, 1.025],
		#'y_subplot_label': '{} / {}'.format(labels[0], labels[1]).replace('(','').replace(')',''),
		#'subplot_fraction': 40,
		#'subplot_legend': 'lower left',
	}
	if ad != None:
		d.update(ad)
	if d['zjetfolders'][0] == 'finalcuts':
		d['zjetfolders'] = ['noalphacuts'],
	return [PlottingJob(plots=[d], args=args)]

def fake_events(args=None, additional_dictionary=None):
	plots = []
	ad = copy.deepcopy(additional_dictionary) if additional_dictionary else {}
	for quantity in ["files", "corrections", "algorithms", "zjetfolders"]:
		ad[quantity].append(ad[quantity][1])
		ad[quantity].extend(ad[quantity])
	ad["labels"] = ['Reco', 'Reco','Reco', 'Matched', 'Matched', 'Matched']

	d = {
		'cutlabel': True,
		'filename': 'fakes',
		'x_bins': ['0.5 1.5 2.5 3.5'],
		'x_lims': [0,4],
		'weights':['1','1','jet1puidtight==1&jet2puidtight==1','matchedgenjet2pt>0','matchedgenjet2pt>0','matchedgenjet2pt>0&jet1puidtight==1&jet2puidtight==1'],	
		'analysis_modules': ['Ratio'],
		
		'markers' : ['bar','bar','bar','bar','bar','bar','o','o','o'],
		'colors': ['red', 'red', 'red', 'green', 'green', 'green', 'black','black','black'],
		'nicks' : ['puppi', 'chs', 'chspuid','puppimatched', 'chsmatched', 'chspuidmatched'],
		'ratio_numerator_nicks' : ['puppimatched', 'chsmatched', 'chspuidmatched'],
		'ratio_denominator_nicks': ['puppi', 'chs', 'chspuid'],
		'ratio_result_nicks': ['puppi_ratio', 'chs_ratio', 'chspuid_ratio'],
		'y_subplot_lims' : [0.5,0.7],
		'x_expressions': ['1*(jet2pt<200)','2*(jet2pt<200)','3*(jet2pt<200)','1*(jet2pt<200)','2*(jet2pt<200)','3*(jet2pt<200)'],
		'x_label': 'Jet 2 matching',
		'x_ticks': [1,2,3],
		'x_tick_labels': ['Puppi', 'CHS', 'CHS with PUJetID'],
		'y_lims': [0,2.7e8],
		'y_label': 'Arbitrary Units',
		
	}

	if ad != None:
		d.update(ad)
	#d['texts'].append(r"$\\mathit{p}_\\mathrm{T}^\\mathrm{Jet2}<50 \\ GeV$")
	#d['texts_x'].append(0.03)
	#d['texts_y'].append(0.8)
	#d['texts_size'].append('large')
	plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
			

def basic_comparisons(args=None, additional_dictionary=None, data_quantities=True, only_normalized=False, channel="mm"):
	"""Comparison of: zpt zy zmass zphi jet1pt jet1eta jet1phi npv, both absolute and normalized"""
	plots = []
	ad = copy.deepcopy(additional_dictionary) if additional_dictionary else {}
	for quantity in ["files", "corrections", "algorithms", "zjetfolders"]:
		ad[quantity].append(ad[quantity][1])
	ad["labels"].append("CHS with PUJetID")
	# TODO move this to more general location
	x_dict = {
		'alpha': ['20,0,0.3'],
		'jet1area': ['40,0.3,0.9'],
		'jet1eta': ['30,-1.5,1.5'],
		'jet1phi': ['20,-3.1415,3.1415',],
		'jet1pt': ['0 10 20 30 40 50 70 90 120 150 200 250 300 350'],
		'jet2eta': ['20,-5,5'],
		'jet2phi': ['20,-3.1415,3.1415',],
		'jet2pt': ['14,0,70'],
		'met': ['40,0,80'],
		'metphi': ['20,-3.1415,3.1415',],
		'mpf': ['40,0,2'],
		'npu': ['31,-0.5,30.5'],
		'npumean': ['40,0,40'],
		'npv': ['31,-0.5,30.5'],
		'ptbalance': ['40,0,2'],
		'rawmet': ['40,0,100'],
		'zmass': ['100,71,111'],
		'zphi': ['20,-3.1415,3.1415',],
		'zpt': ['40,0,400'],
		'zy': ['25,-2.5,2.5'],
		'njets20': ['0.5 1.5 2.5 3.5 4.5 5.5 6.5'],
	}
	x_dict_zl={
		'%s1phi': ['20,-3.1415,3.1415',],
		'%s1pt': ['20,0,150'],
		'%s2pt': ['20,0,150'],
		'%sminuspt': ['20,0,150'],
		'%spluspt': ['20,0,150'],
	}

	quantity_list= ['zpt', 'zy', 'zmass', 'zphi', 'jet1pt', 'jet1eta', 'jet1phi', 'jet1area',
			 'npv', 'npumean', 'rho', 'met', 'metphi', 'rawmet', 'rawmetphi',
			 'ptbalance', 'mpf', 'jet2pt', 'jet2eta', 'jet2phi', 'alpha', 'njets20']
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
			'cutlabel': True,
			'x_expressions': [quantity],
			'analysis_modules': ['NormalizeByBinWidth', 'ConvertToTGraphErrors'],
			'nicks' : ['puppi', 'chs', 'chspuid'],
			'weights' : ['1', '1','jet1puidtight==1&jet2puidtight==1'],
			'colors' : ['black','red','blue'],
			'y_label' : 'Arbitrary Units',
			'y_log': quantity in ['jet1pt', 'zpt']
		}
		if quantity in x_dict:
			d["x_bins"] = [x_dict[quantity][0]]
			d["legend"] = x_dict[quantity][1]

		if ad:
			d.update(ad)
		if quantity == 'alpha' and (additional_dictionary is None or 'zjetfolders' not in additional_dictionary):
			d['zjetfolders'] = ['noalphacuts']

		if quantity=='zphi':
			d['y_rel_lims']=[1,1.3]
		elif quantity == 'jet1pt':
			d['y_lims']=[10e3,1.4e7]
			d['x_lims']=[0,300]
		elif quantity== 'zpt':
			d['y_lims']=[10e2,3.5e7]
		elif quantity == 'jet2eta':
			d['y_lims']=[0,4.8e7]
		elif quantity == 'alpha':
			d['y_lims']=[0,1.45e9]
			d['x_lims']=[0,0.31]
		elif quantity == 'njets20':
			d['y_lims']=[0,2.3e8]
			d['x_lims']=[0,6]
			d['x_label']="Number of Jets with "+r"$\\mathit{p}_\\mathrm{T}$ > 20 GeV"
		elif quantity == 'jet2pt':
			d['y_lims']=[0,1.6e7]
			d['x_ticks']=[0,10,20,30,40,50,60,70]
		if not only_normalized:
			plots.append(d)
		

		# shape comparison
		d2 = copy.deepcopy(d)
		d2.update({
			'analysis_modules': ['NormalizeToFirstHisto', 'ConvertToTGraphErrors'],
			'filename': quantity+"_shapeComparison",
			'title': "Shape Comparison",
			'legend': 'upper right',
		})
		if channel in ("eemm", "mmee"):
			d2['y_label']= 'Electron Events'
		if ad != None:
			d.update(ad)
		plots.append(d2)
	return [PlottingJob(plots=plots, args=args)]

def basic_profile_comparisons(args=None, additional_dictionary=None):
	""" Some basic profile plots. """
	plots = []
	ad = copy.deepcopy(additional_dictionary) if additional_dictionary else {}
	for quantity in ["files", "corrections", "algorithms", "zjetfolders"]:
		ad[quantity].append(ad[quantity][1])
	ad["labels"].append("CHS with PUJetID")
	for yquantity in ('zmass','jet1pt','mpf','ptbalance'):
		d = {
			'x_expressions': ['zpt'],
			'y_expressions': [yquantity],
			'cutlabel': True,
			'analysis_modules': ['ConvertToTGraphErrors', "Ratio"],
			'weights' : ['1', '1','jet1puidtight==1&jet2puidtight==1'],
			'tree_draw_options': 'prof',

			'colors' : ['black','red','blue'],
			'x_bins': '10,0,200',
			'markers': ['o', 'd', '^'],
			'nicks' : ['puppi', 'chs', 'chspuid'],
			'ratio_numerator_nicks' : ['chspuid', 'puppi'],
			'ratio_denominator_nicks': ['chs', 'chs'],
			'ratio_result_nicks': ['puid_ratio', 'puppi_ratio'],
			'y_subplot_lims': [0.966, 1.034],
		}
		if yquantity == 'zmass':
			z_mass_pdg = 91.1876
			z_width_pdg = 2.4952
			z_peak = 0.01
			z_window = 5
			d['y_lims'] =  [z_mass_pdg - z_window, z_mass_pdg + z_window],


		plots.append(d)
	for x_expression in ['npv', 'npumean']:
		for y_expression in ['rho', 'npv']:
			d = {
				'x_expressions': [x_expression],
				'y_expressions': [y_expression],
				'y_lims':[0,30],
				'tree_draw_options': 'prof',
				'cutlabel': True,
				'markers': ['o', 'd', '^'],
				'x_bins': "25,0.5,25.5",
				'legend': 'lower right',
			}
			if (x_expression=='npv' and y_expression=='rho'): d['y_lims']= [0,30]
			plots.append(d)
	if ad != None:
		for plot in plots:
			plot.update(ad)
	return [PlottingJob(plots=plots, args=args)]


def jet_resolution(args=None, additional_dictionary=None):
	ad = copy.deepcopy(additional_dictionary) if additional_dictionary else {}
	for quantity in ["files", "corrections", "algorithms", "zjetfolders"]:
		ad[quantity].append(ad[quantity][1])
	ad["labels"].append("CHS with PUJetID")
	"""Plot the jet resolution vs pt, abs(eta) and npv."""
	plots = []

	methoddict = {
		'mpf': 'MPF',
		'ptbalance': r'$\\mathit{p}_T$ balance',
		'trueresponse': r'$p_T^\\mathrm{reco}$/$p_T^\\mathrm{ptcl}$',
	}
	for quantity in ['zpt', 'npv', 'jet1abseta']:
		for method in ['mpf', 'ptbalance']:
			d = {
				'cutlabel': True,
				'corrections': ['L1L2L3Res', 'L1L2L3'],
				'x_expressions': quantity,
				'x_bins': [quantity],
				'x_errors': [True],
				'x_log': (True if quantity == 'zpt' else False),
				'y_expressions': [method, method, method],
				#'y_lims': [0.0, 0.5],
				'y_label': 'Jet resolution ({})'.format(methoddict[method]),
				'weights' : ['1', '1','jet1puidtight==1&jet2puidtight==1'],
				'colors' : ['black','red','blue'],
				'markers': ['o', 'd', '^'],
				'x_errors': [True],
				'tree_draw_options': 'profs',
				'analysis_modules': ['ConvertToHistogram', 'StatisticalErrors',],
				'stat_error_nicks': ['puppi', 'chs', 'chspuid'],
				'convert_nicks': ['puppi', 'chs', 'chspuid'],
				'nicks': ['puppi', 'chs', 'chspuid'],
				'filename': 'jet_resolution_{0}_vs_{1}'.format(method, quantity),
			}
			if ad != None:
				d.update(ad)
			if method == 'trueresponse':
				d['weights'] = ['matchedgenjet1pt > 0']
			if quantity == 'zpt':
				d['x_lims'] = [30, 1000]
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			elif quantity == 'jet1abseta':
				if d['zjetfolders'][0] == 'finalcuts':
					d['zjetfolders'] = ['noetacuts']
				elif d['zjetfolders'][0] == 'noalphacuts':
					d['zjetfolders'] = ['noalphanoetacuts']
				d['x_lims'] = [0, 5.2]
			elif quantity == 'npv':
				d['x_lims'] = [0, 40]


			plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def full_comparison(args=None, d=None, data_quantities=True, only_normalized=False,
	                channel="mm", inputtuple="datamc", subtract_hf=True):
	""" Do all comparison plots"""
	plotting_jobs = []
	plotting_jobs += response_extrapolation(args, d, inputtuple)
	plotting_jobs += basic_comparisons(args, d, data_quantities, only_normalized, channel)
	plotting_jobs += basic_profile_comparisons(args, d)
	plotting_jobs += fake_events(args,d)
	plotting_jobs += jet_resolution(args, additional_dictionary=d)
	return plotting_jobs

def comparison_CHS_Puppi_mm(args=None):
	plotting_jobs = []
	cuts = 'finalcuts'
	d = {
		'files': ['work/mmPuppi_PUJetID_njets20.root', 'work/mm_PUJetID_njets20.root'],
		'labels': ['Puppi', 'CHS'],
		'algorithms': ['ak4PFJetsPuppi', 'ak4PFJetsCHS'],
		'corrections': ['L1L2L3', 'L1L2L3'],
		'zjetfolders': [cuts,cuts],
		'texts': [r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{\\mu \\mu}$"],
		'texts_x': [0.648],
		'texts_y': [1.07],
		'texts_size': [16],
		'www': 'Comparison_CMS_vs._Puppi_PUJetID_njets20_'+cuts,
	}
	plotting_jobs += full_comparison(args, d, channel="mm", inputtuple='mcmc')
	return plotting_jobs

def comparison_CHS_Puppi_ee(args=None):
	plotting_jobs = []
	d = {
		'files': ['work/eePuppi_80.root', 'work/ee_80.root'],
		'labels': ['Puppi', 'CHS'],
		'algorithms': ['ak4PFJetsPuppi', 'ak4PFJetsCHS'],
		'zjetfolders': ['finalcuts','finalcuts'],
		'corrections': ['L1L2L3', 'L1L2L3'],
		'www': 'Comparison_CMS_vs._Puppi_PUJetID_ee',
	}
	plotting_jobs += full_comparison(args, d, channel="ee", inputtuple='mcmc')
	d.update({'folders': ['nocuts_ak4PFJetsCHSL1L2L3', 'nocuts_ak4PFJetsCHSL1L2L3']})
	return plotting_jobs
