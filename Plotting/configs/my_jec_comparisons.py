#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files

import time
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
		#'zjetfolders': ['noalphacuts'], #for the case, that alpha values beyond the alpha cut should be included into the extrapolation
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
		'plot_modules': ['PlotExtrapolationValues','ExportRoot'],#'PlotExtrapolationText', 'PlotMplZJet',
		'extrapolation_text_nicks': ['ptbalance_ratio_fit', 'mpf_ratio_fit'],
		'extrapolation_text_colors': ['darkred', 'darkblue'],
		'extrapolation_values_nicks': ['ptbalance_data_fit'],#'ptbalance_mc_fit'],#fitnicklist[inputtuple],#
		'functions': ['[0]+[1]*x'],#+[2]*x**2'],
		'function_fit': ['ptbalance_data'],#fitlist[inputtuple],
		'function_parameters': ['1,1'],#1'],
		'function_ranges': ['0,0.3'],
		'function_nicknames': ['ptbalance_data_fit'],#fitnicklist[inputtuple],
		'ratio_numerator_nicks': ['ptbalance_data', 'mpf_data'],
		'ratio_denominator_nicks': ['ptbalance_mc', 'mpf_mc'],
		'ratio_result_nicks': ['ptbalance_ratio', 'mpf_ratio'],
		'ratio_denominator_no_errors': False,
		'y_subplot_lims': [0.966, 1.034], #for Zmm
		#'y_subplot_lims': [0.95, 1.05], #for Zee
		'extrapolation_text_position': [0.18, 1.025],
		'y_subplot_label': '{} / {}'.format(labels[0], labels[1]).replace('(','').replace(')',''),
		'subplot_fraction': 40,
		'subplot_legend': 'upper left',
	}
	if additional_dictionary != None:
		d.update(additional_dictionary)
	return [PlottingJob(plots=[d], args=args)]

def response_comparisons(args2=None, additional_dictionary=None, data_quantities=True):
	"""Response (MPF/pTbal) vs zpt npv abs(jet1eta), with ratio"""
	known_args, args = get_special_parser(args2)

	plots = []
	# TODO put these default binning values somewhere more globally
	for quantity, bins in zip(*get_list_slice([
		['zpt', 'npv', 'abs(jet1eta)'],# 'abs(jet2eta)'],
		['zpt', 'npv','abseta']#,'abseta']
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
				'ratio_denominator_no_errors': False,
				'filename': method + "_" + quantity.replace("(", "").replace(")", ""),
				'y_subplot_lims': [0.97, 1.03],
				'legend': 'upper right',#'lower left',
			}
#########################################################
			if method == 'mpf':
				d['y_label'] = '$MPF$ response'
				d['y_lims'] = [0.95,1.05]				
			if method == 'ptbalance':
				d['y_label'] = '$p_T-balance$ response'
				if quantity == 'zpt':
					d['y_lims'] = [0.8,1.04]
				else:
					d['y_lims'] = [0.73,0.99]
#########################################################
			if quantity == 'abs(jet1eta)' or 'abs(jet2eta)':
				d['zjetfolders'] = ["noetacuts"]
				d['x_bins'] = ["0.001 0.261 0.522 0.783 1.044 1.305 1.479 1.653 1.930 2.172 2.322 2.500 2.650 2.853 2.964 3.139 3.489 3.839 5.191"]
			if quantity == 'zpt':
				d['x_log'] = True
				d['x_bins'] = ["30 40 50 60 85 105 130 175 230 300 400 500 700 1000 1500 2000"]
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			if quantity == 'npv':
				d['y_lims'] = [0.95,1.05]
				d['x_bins']=["0 5 10 12 15 20 25 30 50"]
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
		'alpha': ['80,0,1'],
		'jet1area': ['80,0.3,0.9'],
		'jet1eta': ['60,-5,5'],
		'jet1phi': ['40,-3.1415,3.1415',],
		'jet1pt': ['160,0,800'],
		'jet2eta': ['40,-5,5'],
		'jet2phi': ['40,-3.1415,3.1415',],
		'jet2pt': ['60,0,75'],
		'met': ['80,0,100'],
		'metphi': ['40,-3.1415,3.1415',],
		'mpf': ['80,0,2'],
		'npu': ['31,-0.5,60.5'],
		'npumean': ['100,0,50'],
		'npv': ['51,-0.5,50.5'],
		'ptbalance': ['80,0,2'],
		'rawmet': ['80,0,100'],
		'zmass': ['160,71,111'],
		'zphi': ['40,-3.1415,3.1415',],
		'zpt': ['80,0,400'],
		'zy': ['50,-2.5,2.5'],
		'genHT': ['3000,10.5,3000.5'],
		'jetHT': ['3000,10.5,3000.5']
	}
	x_dict_zl={
		'%s1phi': ['20,-3.1415,3.1415',],
		'%s1pt': ['20,0,150'],
		'%s2pt': ['20,0,150'],
		'%sminuspt': ['20,0,150'],
		'%spluspt': ['20,0,150'],
	}

	quantity_list= ['zpt']#, 'zy', 'zmass', 'zphi', 'jet1pt', 'jet1eta', 'jet1phi', 'jet1area',
			 #'npv', 'npumean', 'rho', 'met', 'metphi', 'rawmet', 'rawmetphi', 'njets',
			 #'ptbalance', 'mpf', 'jet2pt', 'jet2eta', 'jet2phi', 'alpha', 'genHT', 'jetHT']
	quantity_list_zl=[]#'%s1pt', '%s1eta', '%s1phi', '%s2pt', '%s2eta', '%s2phi','%sminusphi', '%sminuseta', '%sminuspt', '%splusphi', '%spluseta', '%spluspt']
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

	for quantity in quantity_list: #\
		#	 + (['run', 'lumi', 'event'] if data_quantities else ['npu']):
		# normal comparison
		d = {
			'x_expressions': [quantity],
			'cutlabel': True,
			#'analysis_modules': ['Ratio'],
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
		if quantity == 'genHT' or quantity == 'jetHT':
			#d['zjetfolders'] = ['nocuts']
			d['x_log'] = True,
			d['y_log'] = True,
			#d['x_bins'] = ["5 20 30 50 70 80 90 100 120 150 200 250 300 400 450 500 600 650 700 800 900 1000 1200 1400 2000 2500 3000 4000 5000"]
			d['x_ticks'] = [30, 70, 200, 400, 1200, 2500]
		if quantity == 'jet1eta' or quantity == 'jet2eta':
			d['zjetfolders'] = ['nocuts']	
		if quantity == 'genHT':
			d['x_label'] = '${H}_T^{Gen}/GeV$'
		if quantity == 'jetHT':
			d['x_label'] = '${H}_T^{Reco}/GeV$'
		
		if quantity=='zphi':
			d['y_rel_lims']=[1,1.3]
		elif quantity== 'zpt':
			d['y_rel_lims']=[1,400]
		if not only_normalized:
			plots.append(d)

		# shape comparison
		d2 = copy.deepcopy(d)
		d2.update({
			'analysis_modules': ['NormalizeToFirstHisto','Ratio'],#
			'filename': quantity+"_shapeComparison",
			'title': "Shape Comparison",
			'legend': 'upper right',
			'y_subplot_lims': [0.9, 1.1],
		})
		if channel in ("eemm", "mmee"):
			d2['y_label']= 'Electron Events'
		if additional_dictionary:
			d2.update(additional_dictionary)
		plots.append(d2)
	return [PlottingJob(plots=plots, args=args)]

def full_comparison(args=None, d=None, data_quantities=True, only_normalized=True,
	                channel="mm", inputtuple="datamc", subtract_hf=True):
	""" Do all comparison plots"""
	plotting_jobs = []
	plotting_jobs += basic_comparisons(args, d, data_quantities, only_normalized, channel)
	#plotting_jobs += response_comparisons(args, d, data_quantities)
	plotting_jobs += response_extrapolation(args, d, inputtuple)
	return plotting_jobs

def my_comparison_datamc_Zll(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	Res=0 # disable/enable residual corrrections
	Cut=1 # disable/enable cuts
	if Res==True:
		RES='Res'
	else:
		RES=''
	if Cut==True:
		CUT='finalcuts'
	else:
		CUT='noalphacuts'
	PU='CHS'#'PUPPI'
	RUN='BCDEFGH'
	CH='mm'
	MC='amc'#'amc'#
	RECO='remini'
	NICK =['Data','MC']
	
	plotting_jobs = []
	d = {
		'files': [	'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_'+RUN+'_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/mc16_'+RUN+'_'+CH+'_'+MC+'.root'],
		'corrections': ['L1L2L3'+RES, 'L1L2L3'],
		'zjetfolders': CUT,
#		'output_dir': '/ekpwww/web/tberger/public_html/plots_archive/'+time.strftime("%Y_%m_%d", time.localtime())+'/comparison_Z'+CH+'_'+RUN+'_'+RECO+'_'+PU+'_'+MC+'_'+CUT+RES,
		'www_title': 'Comparison of Datasets for Zll, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		'www': 'comparison_Z'+CH+'_'+RUN+'_'+RECO+'_'+PU+'_'+MC+'_'+CUT+RES,
		'labels': NICK,
		'y_subplot_label' : "Data/MC",
		#'y_subplot_lims' : [0.9,1.1],
		'texts_x': [0.34,0.69] if Res == True else [0.34,0.78],
		'texts_y': [0.95,0.09],
		'texts_size': [20,25],
#		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{work\\hspace{0.2}in\\hspace{0.2}progress \\hspace{3.2}}$"
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
		'plot_modules': ['ExportRoot'],
#		'formats': ['svg'],
	}
	if RUN=='BCD':
		d.update({'lumis': [12.61]})#'weights'	: [	'1','(run>=272007&&run<=276811)'],#					'lumis'		: [12.93]	})					 # ICHEP Dataset
	elif RUN=='EF':
		d.update({'lumis': [6.71]})#'weights'	: [	'1','(run>=276831&&run<=278801)'],#					'lumis'		: [6.89]	})
	elif RUN=='G':
		d.update({'lumis': [7.94]})#'weights'	: [	'1','(run>=278802&&run<=280385)'],#					'lumis'		: [8.13]	})
	elif RUN=='H':
		d.update({'lumis': [8.61]})#'weights'	: [	'1','(run>=280385)']#					'lumis'		: [8.86]	})
	elif RUN=='BCDEFGH':
		d.update({'lumis': [35.87]})#'weights'	: [	'1','(run>=280385)'],
	if CH=='ee':
		d.update({'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3Res}$"] if Res else [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3}$"]})
	elif CH=='mm':
		d.update({'texts': [r"$\\mathrm{\\bf{Z \\rightarrow}\\mu\\mu}$",r"$\\bf{L1L2L3Res}$"] if Res else [r"$\\mathrm{\\bf{Z \\rightarrow}\\mu\\mu}$",r"$\\bf{L1L2L3}$"]})
	
	plotting_jobs += full_comparison(args, d, channel=CH, inputtuple='datadata')  # usually datamc
	return plotting_jobs
	
def my_comparison_dataallmc_Zll(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	Res=1 # disable/enable residual corrrections
	Cut=1 # disable/enable cuts
	if Res==True:
		RES='Res'
	else:
		RES=''
	if Cut==True:
		CUT='finalcuts'
	else:
		CUT='noetacuts'
	PU='CHS'#'PUPPI'
	RUN='BCD'
	CH='mm'
	MC='amc'
	RECO='remini'
	NICK =['DataBCD','DataEF','DataG','DataH',MC]
	plotting_jobs = []
	d = {
		'files': [	'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_BCD_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_EF_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_G_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_H_'+CH+'_'+RECO+'.root',					
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/mc16_'+RUN+'_'+CH+'_'+MC+'.root'],
		'corrections': ['L1L2L3'+RES, 'L1L2L3'+RES, 'L1L2L3'+RES, 'L1L2L3'+RES, 'L1L2L3'],# 'L1L2L3'+RES],['',''],#
		'zjetfolders': CUT,
#		'output_dir': '/ekpwww/web/tberger/public_html/plots_archive/'+time.strftime("%Y_%m_%d", time.localtime())+'/comparison_Z'+CH+'_'+RUN+'_'+RECO+'_'+PU+'_'+MC+'_'+CUT+RES,
		'colors' : ['red','blue','green','orange','black','darkred','darkblue','darkgreen','darkorange'],
		'www_title': 'Comparison of Datasets for Zll, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		'www': 'comparison_Z'+CH+'_all_'+RECO+'_'+PU+'_'+MC+'_'+CUT+RES,
		'labels': ['DataBCD('+RECO+')','DataEF('+RECO+')','DataG('+RECO+')','DataH('+RECO+')','MC('+MC+')'],
		'nicks': NICK,				
		'markers': ['o', 's'],
		'y_subplot_label' : "Data/MC",
		#'y_subplot_lims' : [0.9,1.1],
		'ratio_numerator_nicks': [NICK[0:-1]],
		'ratio_denominator_nicks': [NICK[-1]],
		'texts_x': [0.34,0.69] if Res == True else [0.34,0.78],
		'texts_y': [0.95,0.09],
		'texts_size': [20,25],
#		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{work\\hspace{0.2}in\\hspace{0.2}progress \\hspace{3.2}}$"
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
	}
	if CH=='ee':
		d.update({'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3Res}$"] if Res else [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3}$"]})
	elif CH=='mm':
		d.update({'texts': [r"$\\mathrm{\\bf{Z \\rightarrow}\\mu\\mu}$",r"$\\bf{L1L2L3Res}$"] if Res else [r"$\\mathrm{\\bf{Z \\rightarrow}\\mu\\mu}$",r"$\\bf{L1L2L3}$"]})
	
	plotting_jobs += response_comparisons(args, d)# data_quantities)
	return plotting_jobs

def my_comparison_dataallmcalphaetabins_Zll(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	Res=0 # disable/enable residual corrrections
	Cut=0 # disable/enable cuts
	if Res==True:
		RES='Res'
	else:
		RES=''
	if Cut==True:
		CUT='finalcuts'
	else:
		CUT='noalphanoetacuts'
	PU='CHS'#'PUPPI'
	RUN='BCDEFGH'
	CH='mm'
	MC='madgraph_NJ'
	RECO='remini'
	NICK= ['DataBCD','DataEF','DataG','DataH',MC]
	#ETA= [0,0.8,1.3,1.9,2.5,3.0,5.2]#,2.4,5.191]#,2.4,10]#[0, 0.783, 1.305, 1.93, 2.5, 2.964, 3.139, 5.191]
	ETA= [0,1.3,]
	ALPHA= 0.3
	plotting_jobs = []
	d = {
		'files': [	'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_BCD_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_EF_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_G_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_H_'+CH+'_'+RECO+'.root',					
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V1/mc16_JECv1_'+PU+'_'+RUN+'_'+CH+'_'+MC+'.root'],
		'corrections': ['L1L2L3'+RES, 'L1L2L3'+RES, 'L1L2L3'+RES, 'L1L2L3'+RES, 'L1L2L3'],# 'L1L2L3'+RES],['',''],#
		'zjetfolders': CUT,
		'weights': ['abs(jet1eta)>%s'%ETA[0]+'&&abs(jet1eta)<%s'%ETA[1]+'&&alpha<%s'%ALPHA],
#		'output_dir': '/ekpwww/web/tberger/public_html/plots_archive/'+time.strftime("%Y_%m_%d", time.localtime())+'/comparison_Z'+CH+'_'+RUN+'_'+RECO+'_'+PU+'_'+MC+'_'+CUT+RES,
		'colors' : ['red','blue','green','orange','black','darkred','darkblue','darkgreen','darkorange'],
		'www_title': 'Comparison of Datasets for Zll, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		'www': 'comparison_Z'+CH+'_all_'+RECO+'_'+PU+'_'+MC+'eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+'_a_%s'%int(ALPHA*100)+RES,
		'labels': ['DataBCD('+RECO+')','DataEF('+RECO+')','DataG('+RECO+')','DataH('+RECO+')','MC('+MC+')'],
		'nicks': NICK,				
		'markers': ['o', 's'],
		'y_subplot_label' : "Data/MC",
		#'y_subplot_lims' : [0.9,1.1],
		'ratio_numerator_nicks': [NICK[0:-1]],
		'ratio_denominator_nicks': [NICK[-1]],
		'texts_x': [0.34,0.69,0.03,0.03] if Res == True else [0.34,0.78,0.05,0.05],
		'texts_y': [0.95,0.09,0.9,0.83],
		'texts_size': [20,25,15,15],		
#		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{work\\hspace{0.2}in\\hspace{0.2}progress \\hspace{3.2}}$"
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
	}
	if CH=='ee':
		if Res==True:
			d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3Res}$",r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha<%s$"%ALPHA]})
		else:
			d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3}$",r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha<%s$"%ALPHA]})
	elif CH=='mm':
		if Res==True:
			d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",r"$\\bf{L1L2L3Res}$",r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha<%s$"%ALPHA]})
		else:
			d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",r"$\\bf{L1L2L3}$",r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha<%s$"%ALPHA]})
	plotting_jobs += response_comparisons(args, d)# data_quantities)
	return plotting_jobs
	
def my_comparison_dataalphabins_Zll(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	Res=1 # disable/enable residual corrrections
	Cut=0 # disable/enable cuts
	if Res==True:
		RES='Res'
	else:
		RES=''
	if Cut==True:
		CUT='finalcuts'
	else:
		CUT='noalphacuts'
	PU='CHS'#'PUPPI'
	RUN='BCDEFGH'
	CH='mm'
	MC='madgraph_NJ'#'amc'#
	RECO='remini'
	NICK =['Data'+RUN+'a<05','Data'+RUN+'a<10','Data'+RUN+'a<15','Data'+RUN+'a<20','Data'+RUN+'a<30'],
	
	plotting_jobs = []
	d = {
		'files': [	#'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V1/mc16_JECv1_'+PU+'_'+RUN+'_'+CH+'_'+MC+'.root',
					#'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V1/mc16_JECv1_'+PU+'_'+RUN+'_'+CH+'_'+MC+'.root',
					#'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V1/mc16_JECv1_'+PU+'_'+RUN+'_'+CH+'_'+MC+'.root',
					#'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V1/mc16_JECv1_'+PU+'_'+RUN+'_'+CH+'_'+MC+'.root',
					#'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V1/mc16_JECv1_'+PU+'_'+RUN+'_'+CH+'_'+MC+'.root'],
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_'+RUN+'_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_'+RUN+'_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_'+RUN+'_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_'+RUN+'_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_'+RUN+'_'+CH+'_'+RECO+'.root'],
		'corrections': ['L1L2L3'+RES,'L1L2L3'+RES,'L1L2L3'+RES,'L1L2L3'+RES, 'L1L2L3'+RES],
		'weights':['alpha<0.05','alpha<0.1','alpha<0.15','alpha<0.2','alpha<0.3'],
		'zjetfolders': CUT,
#		'output_dir': '/ekpwww/web/tberger/public_html/plots_archive/'+time.strftime("%Y_%m_%d", time.localtime())+'/comparison_Z'+CH+'_'+RUN+'_'+RECO+'_'+PU+'_'+MC+'_'+CUT+RES,
		'colors': ['teal','violet','yellow','salmon','purple'],#'black','yellow','brown','violet','purple'],
		'www_title': 'Comparison of Datasets for Zll, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		#'www': 'comparison_Z'+CH+'_'+RUN+'_'+RECO+'_'+PU+'_'+MC+'_'+CUT+RES,
		#'labels': ['Data'+RUN+'('+RECO+')','MC('+MC+')'],
		'labels': NICK,
		'y_lims':[0.84,1.1],
		'www': 'comparison_Z'+CH+'_'+RUN+'_'+RECO+'_'+PU+'_alpha'+RES,
		'analysis_modules': None, #['StatisticalErrors'],
		#'ratio_numerator_nicks': [NICK[0:-1]],
		#'ratio_denominator_nicks': [NICK[-1]],
		#'y_subplot_label' : "Data/MC",
		#'y_subplot_lims' : [0.9,1.1],		
		'texts_x': [0.34,0.69] if Res == True else [0.34,0.78],
		'texts_y': [0.95,0.09],
		'texts_size': [20,25],
#		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{work\\hspace{0.2}in\\hspace{0.2}progress \\hspace{3.2}}$"
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
	}
	if RUN=='BCD':
		d.update({'lumis': [12.61]})#'weights'	: [	'1','(run>=272007&&run<=276811)'],#					'lumis'		: [12.93]	})					 # ICHEP Dataset
	elif RUN=='EF':
		d.update({'lumis': [6.71]})#'weights'	: [	'1','(run>=276831&&run<=278801)'],#					'lumis'		: [6.89]	})
	elif RUN=='G':
		d.update({'lumis': [7.94]})#'weights'	: [	'1','(run>=278802&&run<=280385)'],#					'lumis'		: [8.13]	})
	elif RUN=='H':
		d.update({'lumis': [8.61]})#'weights'	: [	'1','(run>=280385)']#					'lumis'		: [8.86]	})
	elif RUN=='BCDEFGH':
		d.update({'lumis': [35.87]})#'weights'	: [	'1','(run>=280385)'],
	if CH=='ee':
		d.update({'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3Res}$"] if Res else [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3}$"]})
	elif CH=='mm':
		d.update({'texts': [r"$\\mathrm{\\bf{Z \\rightarrow}\\mu\\mu}$",r"$\\bf{L1L2L3Res}$"] if Res else [r"$\\mathrm{\\bf{Z \\rightarrow}\\mu\\mu}$",r"$\\bf{L1L2L3}$"]})
	
	plotting_jobs += response_comparisons(args, d)
	return plotting_jobs
	
def my_extrapolation_datamczptetabins_Zll(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	Res=1 # disable/enable residual corrrections
	if Res==True:
		RES='Res'
	else:
		RES=''
	PU='CHS'#'PUPPI'
	RUN='BCDEFGH'
	CH='mm'
	RECO='remini'
	MC='madgraph_NJ'
	NICK =[MC,'Data'+RUN]
	ETA = [0,0.8,1.3,1.9,2.5,3.0,5.2]
	#ETA = [0,0.8,1.3]
	ZPT = [30,50]
	
	plotting_jobs = []
	d = {
		'files': [	'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/data16_'+RUN+'_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3/mc16_'+RUN+'_'+CH+'_'+MC+'.root'],
		'corrections': ['L1L2L3'+RES, 'L1L2L3'],
		'zjetfolders': 'nocuts',
		'histogram_from_fit_eta_values': ETA,#[etastring],
		'histogram_from_fit_zpt_values': ZPT,#[zptstring],
		#'algorithms': ['ak4PFJetsPUPPI'],
		'www_title': 'Comparison of Datasets for Zll, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		'www': 'extrapolation_Z'+CH+'_'+RUN+RECO+'_'+PU+'_miniAOD_'+MC+'_'+RES,
		'labels': NICK,
		#'nicks': NICK,
		'y_lims': [0.5,1.2],
		'y_subplot_label' : "MC/Data",
		'y_subplot_lims' : [0.95,1.05],
		#'ratio_numerator_nicks': [NICK[0]],
		#'ratio_denominator_nicks': [NICK[1]],
		'texts_x': [0.84,0.78,0.05,0.05] if not Res else [0.84,0.69,0.05,0.05],
		'texts_y': [0.93,0.09,0.89,0.97],
		'texts_size': [20,25,15,15],
#		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{work\\hspace{0.2}in\\hspace{0.2}progress \\hspace{3.2}}$"
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
	}
	if RUN=='BCD':
		d.update({	#'weights'	: [	'1','(run>=272007&&run<=276811)'],
					'lumis'		: [12.93]	})					 # ICHEP Dataset
	elif RUN=='EF':
		d.update({	#'weights'	: [	'1','(run>=276831&&run<=278801)'],
					'lumis'		: [6.89]	})
	elif RUN=='G':
		d.update({	#'weights'	: [	'1','(run>=278802&&run<=280385)'],
					'lumis'		: [8.13]	}) # special break in RunF
	elif RUN=='H':
		d.update({	#'weights'	: [	'1','(run>=280385)'],
					'lumis'		: [8.86]	})	
		
	for eta1,eta2 in zip(ETA[:-1],ETA[1:]):
		for zpt1,zpt2 in zip(ZPT[:-1],ZPT[1:]):
			d.update({	'filename': 'extrapolation_eta%s'%eta1+'-eta%s'%eta2+'_zpt%s'%zpt1+'-zpt%s'%zpt2,
						'weights': ['abs(jet1eta)>%s'%eta1+'&&abs(jet1eta)<%s'%eta2+'&&zpt>%s'%zpt1+'&&zpt<%s'%zpt2],
						'etavalues': [eta1, eta2],
						'zptvalues': [zpt1, zpt2]})
			if CH=='ee':
				if Res==True:
					d.update({'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3Res}$",r"$%s<"%eta1+r"|\\eta^\\mathrm{Jet1}|<%s$"%eta2,r"$%s"%zpt1+r"<\\mathit{p}^\\mathrm{Z}_\\mathrm{T}/GeV<%s$"%zpt2]}) 
				else:
					d.update({'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3}$",r"$%s<"%eta1+r"|\\eta^\\mathrm{Jet1}|<%s$"%eta2,r"$%s"%zpt1+r"<\\mathit{p}^\\mathrm{Z}_\\mathrm{T}/GeV<%s$"%zpt2]}) 
			elif CH=='mm':
				if Res==True:
					d.update({'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",r"$\\bf{L1L2L3Res}$",r"$%s<"%eta1+r"|\\eta^\\mathrm{Jet1}|<%s$"%eta2,r"$%s"%zpt1+r"<\\mathit{p}^\\mathrm{Z}_\\mathrm{T}/GeV<%s$"%zpt2]})
				else:
					d.update({'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",r"$\\bf{L1L2L3}$",r"$%s<"%eta1+r"|\\eta^\\mathrm{Jet1}|<%s$"%eta2,r"$%s"%zpt1+r"<\\mathit{p}^\\mathrm{Z}_\\mathrm{T}/GeV<%s$"%zpt2]})
			plotting_jobs += response_extrapolation(args, d, inputtuple='datadata')
	#d.update({'folders': ['nocuts_L1L2L3', 'nocuts_L1L2L3'+RES]})
	return plotting_jobs
	
if __name__ == '__main__':
	basic_comparisons()
