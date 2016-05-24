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
	for quantity in ["files", "corrections", "algorithms", "zjetfolders"]: #Copy everything to print pt_balance and mpf in same plot
		ad[quantity].extend(ad[quantity]) 
	
	try:
		labels = ["({0})".format(name) for name in ad.pop('labels')]
	except KeyError:
		try:
			labels = ["({0})".format(name) for name in ad.pop('nicks')]
		except KeyError:
			labels = ['Data', 'MC']
	labellist = [ #Print response method in front of normal labels
			r"$\\mathit{p}_T$ balance" + " {0}".format(labels[0]),
			r"$\\mathit{p}_T$ balance" + " {0}".format(labels[1]),
			r"$\\mathit{p}_T$ balance" + " {0}".format(labels[2]),
			r"$\\mathit{p}_T$ balance" + " {0}".format(labels[3]),
			'MPF {0}'.format(labels[0]),
			'MPF {0}'.format(labels[1]),
			'MPF {0}'.format(labels[2]),
			'MPF {0}'.format(labels[3])]
	labellist.extend(['', '', '', '', '', ''])
	yexpress=['ptbalance', 'ptbalance', 'ptbalance', 'ptbalance', 'mpf', 'mpf', 'mpf', 'mpf']
	nicklist= {
		'datamc':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc','reco_gen_jet'],
		'mcmc':['ptbalance_puppi', 'ptbalance_chs', 'ptbalance_chs_pujetidtight','ptbalance_chs_pujetidmedium','mpf_puppi', 'mpf_chs', 'mpf_chs_pujetidtight', 'mpf_chs_pujetidmedium'],
		'datadata':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc'],
	}
	markerlist= {
		'datamc':['s', 'o', 's', 'o', '*', 'o', 'o'],
		'mcmc':['s', 'o',  '^','d', 's', 'o', '^','d'],
		'datadata':['s', 'o', 's', 'o', 'o', 'o'],
	}
	fitlist= {
		'datamc':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc','reco_gen_jet','ptbalance_ratio', 'mpf_ratio'],
		'mcmc':['ptbalance_puppi', 'ptbalance_chs', 'ptbalance_chs_pujetidtight','ptbalance_chs_pujetidmedium','mpf_puppi', 'mpf_chs', 'mpf_chs_pujetidtight', 'mpf_chs_pujetidmedium'],
		'datadata':['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc', 'ptbalance_ratio', 'mpf_ratio'],
	}
	fitnicklist= {
		'datamc':['ptbalance_data_fit', 'ptbalance_mc_fit', 'mpf_data_fit', 'mpf_mc_fit', 'reco_gen_jet_fit', 'ptbalance_ratio_fit', 'mpf_ratio_fit'],
		'mcmc':['ptbalance_puppi_fit', 'ptbalance_chs_fit', 'ptbalance_chs_pujetidtight_fit', 'ptbalance_chs_pujetidmedium_fit','mpf_puppi_fit', 'mpf_chs_fit', 'mpf_chs_pujetidtight_fit','mpf_chs_pujetidmedium_fit'],
		'datadata':['ptbalance_data_fit', 'ptbalance_mc_fit', 'mpf_data_fit', 'mpf_mc_fit', 'ptbalance_ratio_fit', 'mpf_ratio_fit'],
	}
	colorlist= {
		'datamc':['orange', 'darkred', 'royalblue', 'darkblue', 'darkgreen', 'darkred', 'darkblue'],
		'mcmc':['orange', 'darkred', 'red', 'violet','royalblue', 'darkblue', 'cyan', 'lightblue'],
		'datadata':['orange', 'darkred', 'royalblue', 'darkblue', 'darkred', 'darkblue'],
	}
	filllist= {
		'datamc':['none', 'none', 'full', 'full', 'full', 'none', 'full'],
		'mcmc':['none', 'none', 'none','none', 'full', 'full', 'full', 'full'],
		'datadata':['none', 'none', 'full', 'full', 'none', 'full'],
	}
	linelist= {
		'datamc':[None, None, None, None, None, None, None, '--', '--', '--', '--', '--', '--', '--'],
		'mcmc':[None, None, None, None, None, None, None, None, None, None, '--', '--', '--', '--', '--', '--', '--', '--', '--'],
		'datadata':[None, None, None, None, None, None, '--', '--', '--', '--', '--', '--', '--'],
	}
	d = {
		'filename': 'extrapolation',
		'labels': labellist,
		'alphas': [0.3],
		'lines': [1.0],
		'legend': 'lower left',
		'x_expressions': 'alpha',
		'x_bins': '6,0,0.2',
		'x_lims': [0,0.2],
		'y_expressions': yexpress,
		'y_label': 'Jet Response',
		'y_lims': [0.8,1.05],
		'nicks': nicklist[inputtuple],
		'colors': colorlist[inputtuple],
		'markers': markerlist[inputtuple],
		'marker_fill_styles': filllist[inputtuple],
		'line_styles': linelist[inputtuple],
		'line_widths': ['1'],
		'tree_draw_options': 'prof',
		'analysis_modules': ['FunctionPlot'], #Fit for extrapolation
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
def alpha_efficiency(args=None, additional_dictionary=None):
	'''Calculate the fraction of passed events and matched 2nd jets in dependance of the height of the alpha cut'''
	plots = []
	ad = {"files" : [], "corrections": [], "algorithms": [], 'labels': []}
	
	for quant in ['events', 'matched']: #2 plots: passed events, and matched 2nd jets
		d = {
			'cutlabel': True,
			'x_expressions': [],
			'weights' : [],
			'filename' : 'alpha_efficiency'+quant,
			'zjetfolders' : 'noalphacuts',
			'nicks' : ['puppi', 'chs', 'chspuidtight', 'chspuidmedium','puppia', 'chsa', 'chspuidtighta', 'chspuidmediuma'],
			'divide_denominator_nicks' : ['puppi', 'chs', 'chspuidtight', 'chspuidmedium'],
			"divide_numerator_nicks" : ['puppia', 'chsa', 'chspuidtighta', 'chspuidmediuma'],
			"divide_result_nicks" : ['puppi_eff', 'chs_eff', 'chspuidtight_eff', 'chspuidmedium_eff'],
			'nicks_whitelist': ['puppi_eff', 'chs_eff', 'chspuidtight_eff', 'chspuidmedium_eff'],
			'analysis_modules': ['Divide', 'ConvertToTGraphErrors'],
			'colors' : ['black','red','blue', 'green'],
			'x_bins' : ['0.025 0.075 0.125 0.175 0.225 0.275 0.325'],
			'x_label': r"$\\alpha_\\mathrm{max}$",
			'texts': [r"MC $\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{\\mu \\mu}$"],
			'texts_x': [0.4],
			'texts_y': [1.06],
			'texts_size': [16],
			'www' : additional_dictionary['www'],
			'zjetfolders' : 'noalphacuts',
			'x_lims' : [0.025,0.325],
			'y_lims' : [0,1],
			
		}
		d2 = copy.deepcopy(d)
		for amax in range(5, 35, 5): # Steps of alpha, where fractions are calculated 
			d['x_expressions'] += [(str(amax/100.))]*8
			d2['x_expressions'] += [(str(amax/100.))]*8
			for quantity in ["files", "corrections", "algorithms", "labels"]: #Copy everything for each step
				ad[quantity]+=(additional_dictionary[quantity])
			d.update(ad)
			d2.update(ad)
			if quant == 'events':
				d['weights'] += ['1']*4 #Denominator: All events
				d['weights'] += ['alpha<'+str(amax/100.)]*4 #Numerator: Events that pass
				d['y_label'] = 'Fraction of passed events'
			elif quant == 'matched':
				d2['weights'] += ['alpha<'+str(amax/100.)]*4 #Denominator: All events that pass				
				d2['weights'] += ['alpha<'+str(amax/100.)+'&matchedgenjet2pt>0']*4 #Numerator: Events that pass and have matched 2nd jet
				d2['y_label'] = 'Fraction of matched 2nd jets'
		if quant == 'events':
			plots.append(d)
		else:
			plots.append(d2)
	return [PlottingJob(plots=plots, args=args)]
def fake_events(args=None, additional_dictionary=None):
	plots = []
	ad = copy.deepcopy(additional_dictionary) if additional_dictionary else {}
	d = {
		'cutlabel': True,
		'filename': 'fakes',
		'x_bins': ['0.5 1.5 2.5 3.5 4.5'],
		'x_lims': [0,5],
		'weights':['jet2eta<2.5','jet2eta<2.5','jet2eta<2.5','jet2eta<2.5','jet2eta<2.5&matchedgenjet2pt>0','jet2eta<2.5&matchedgenjet2pt>0','jet2eta<2.5&matchedgenjet2pt>0','jet2eta<2.5&matchedgenjet2pt>0'], # Plot all files first with all events in central eta region, and another time only matched 2nd jet events	
		'analysis_modules': ['Ratio'],
		'markers' : ['bar','bar','bar','bar','bar','bar','bar', 'bar','o','o','o', 'o'],
		'colors': ['red', 'red', 'red', 'red','green', 'green', 'green','green', 'black','black','black', 'black'], #Red vor all events, green for matched, black for ratios
		'nicks' : ['puppi', 'chs', 'chspuidtight', 'chspuidmedium','puppimatched', 'chsmatched', 'chspuidtightmatched', 'chspuidmediummatched'],
		'ratio_numerator_nicks' : ['puppimatched', 'chsmatched', 'chspuidtightmatched', 'chspuidmediummatched'],
		'ratio_denominator_nicks': ['puppi', 'chs', 'chspuidtight', 'chspuidmedium'],
		'ratio_result_nicks': ['puppi_ratio', 'chs_ratio', 'chspuidtight_ratio', 'chspuidmedium_ratio'],
		'y_subplot_lims' : [0.5,0.75],
		'x_expressions': ['1','2','3','4','1','2','3','4'], #Get different bins for each file, same bin for all events and matched
		'x_label': 'Jet 2 matching',
		'x_ticks': [1,2,3,4],
		'x_tick_labels': ['Puppi', 'CHS', 'PuIDtight','PuIDmed'],
		'y_lims': [0,2.9e8],
		'y_label': 'Arbitrary Units',
		
	}
	
	if ad != None:
		d.update(ad)
	d['texts'] += [r"|$\\mathit{\\eta}^{\\mathrm{jet2}}$|$<2.5$"] #Additional label for the jet2eta cut taken because puppi takes it in general
	d['texts_x'] += [0.03]
	d['texts_y'] += [0.79]
	d['texts_size'] += ['large']
	d['labels'] = ['Fakes','Fakes','Fakes','Fakes','Matched','Matched','Matched','Matched']
	plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
			

def basic_comparisons(args=None, additional_dictionary=None, data_quantities=True, only_normalized=False, channel="mm"):
	"""Comparison of some quantities both absolute and normalized"""
	plots = []
	ad = copy.deepcopy(additional_dictionary) if additional_dictionary else {}
	for quantity in ["files", "corrections", "algorithms", "zjetfolders"]:
		ad[quantity].append(ad[quantity][1])
	ad["labels"].append("CHS with PUJetID")
	# TODO move this to more general location
	x_dict = { #x_bins, y_lims, ... of the quantity
		'alpha': ['20,0,0.3',[0,1.4e9]],
		'jet1area': ['40,0.3,0.9'],
		'jet1eta': ['30,-1.5,1.5'],
		'jet1phi': ['20,-3.1415,3.1415',],
		'jet1pt': ['0 10 20 30 40 50 70 90 120 150 200 250 300 350',[10e3,2e7]],
		'jet2eta': ['20,-5,5',[0,4.9e7]],
		'jet2phi': ['20,-3.1415,3.1415',],
		'jet2pt': ['14,0,70',[0,1.8e7]],
		'met': ['40,0,80'],
		'metphi': ['20,-3.1415,3.1415',],
		'mpf': ['40,0,2'],
		'npu': ['31,-0.5,30.5'],
		'npumean': ['40,0,40'],
		'npv': ['31,-0.5,30.5'],
		'ptbalance': ['40,0,2'],
		'rawmet': ['40,0,100'],
		'zmass': ['100,71,111',[0,5.3e7]],
		'zphi': ['20,-3.1415,3.1415',],
		'zpt': ['40,0,400',[10e2,3.5e7]],
		'zy': ['25,-2.5,2.5',[0,2.3e8]],
		'njets20': ['0.5 1.5 2.5 3.5 4.5 5.5 6.5',[0,2.5e8]],
		'jet1pt-matchedgenjet1pt' : ['20,-10,10',[0,2e7]],
		'jet2pt-matchedgenjet2pt' : ['20,-10,10'],
		'genjet2pt': ['14,0,70',[0,0.8e7]],
		'genjet2eta': ['20,-5,5'],
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
			 'ptbalance', 'mpf', 'jet2pt', 'jet2eta', 'jet2phi', 'alpha', 'njets20', 'jet1pt-matchedgenjet1pt', 'jet2pt-matchedgenjet2pt']
	quantity_list_zl=['%s1pt', '%s1eta', '%s1phi', '%s2pt', '%s2eta', '%s2phi','%sminusphi', '%sminuseta', '%sminuspt', '%splusphi', '%spluseta', '%spluspt']
	quantity_list_genjets= ['jet1pt-matchedgenjet1pt', 'jet2pt-matchedgenjet2pt']
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


	for quantity in quantity_list: #\
			 #+ (['run', 'lumi', 'event'] if data_quantities else ['npu']):
		# normal comparison
		d = {
			'cutlabel': True,
			'x_expressions': [quantity],
			'legend' : True,
			'analysis_modules': ['NormalizeByBinWidth', 'ConvertToTGraphErrors'],
			'nicks' : ['puppi', 'chs', 'chspuidtight', 'chspuidmedium'],
			'colors' : ['black','red','blue','green'],
			'y_label' : 'Arbitrary Units',
			'y_log': quantity in ['jet1pt', 'zpt']
		}
		if quantity in x_dict:
			d["x_bins"] = [x_dict[quantity][0]]
			if len(x_dict[quantity]) >1:
				d["y_lims"] = x_dict[quantity][1]

		if additional_dictionary:
			d.update(additional_dictionary)
		if quantity == 'alpha' and (additional_dictionary is None or 'zjetfolders' not in additional_dictionary):
			d['zjetfolders'] = ['noalphacuts']

		elif quantity == 'jet1pt':
			d['x_lims']=[0,300]
		elif quantity == 'jet1pt-matchedgenjet1pt':
			d['filename']='jet1reco'
			d['x_label']= r"$\\mathit{p}_\\mathrm{T}^\\mathrm{jet1}$-$\\mathit{p}_\\mathrm{T}^\\mathrm{genjet1}$"
		elif quantity == 'jet2pt-matchedgenjet2pt':
			d['filename']='jet2reco'
			d['x_label']= r"$\\mathit{p}_\\mathrm{T}^\\mathrm{jet2}$-$\\mathit{p}_\\mathrm{T}^\\mathrm{genjet2}$"
			d['y_log'] = True
			d['legend'] = 'lower right'
		elif quantity == 'alpha':
			d['x_lims']=[0,0.31]
		elif quantity == 'njets20':
			d['x_lims']=[0,6]
			d['x_label']="Number of Jets with "+r"$\\mathit{p}_\\mathrm{T}$ > 20 GeV"
		elif quantity == 'jet2pt':
			d['x_ticks']=[0,10,20,30,40,50,60,70]
		if not only_normalized:
			plots.append(d)
		

		# shape comparison
		#d2 = copy.deepcopy(d)
		#d2.update({
		#	'analysis_modules': ['NormalizeToFirstHisto', 'ConvertToTGraphErrors'],
		#	'filename': quantity+"_shapeComparison",
		#	'title': "Shape Comparison",
		#	'legend': 'upper right',
		#})
		#if channel in ("eemm", "mmee"):
		#	d2['y_label']= 'Electron Events'
		#if ad != None:
		#	d.update(ad)
		#plots.append(d2)
	return [PlottingJob(plots=plots, args=args)]

def basic_profile_comparisons(args=None, additional_dictionary=None):
	""" Some basic profile plots. """
	plots = []
	for yquantity in ('zmass','jet1pt','mpf','ptbalance'):
		d = {
			'x_expressions': ['zpt'],
			'y_expressions': [yquantity],
			'cutlabel': True,
			'analysis_modules': ['ConvertToTGraphErrors', "Ratio"],
			'tree_draw_options': 'prof',
			'x_bins': '10,0,200',
			'colors' : ['black','red','blue','green','green','blue','black'],
			'markers': ['o', 'd', '^','s','s','^', 'o'],
			'nicks' : ['puppi', 'chs', 'chspuidtight', 'chspuidmedium'],
			'ratio_numerator_nicks' : ['chspuidmedium','chspuidtight', 'puppi'],
			'ratio_denominator_nicks': ['chs', 'chs', 'chs'],
			'ratio_result_nicks': ['puidtight_ratio', 'puidmedium_ratio','puppi_ratio'],
			'y_subplot_lims': [0.966, 1.034],
			'y_subplot_label': 'Ratio to CHS',
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
				'markers': ['o', 'd', '^', 's'],
				'x_bins': "25,0.5,25.5",
				'legend': 'lower right',
			}
			if (x_expression=='npv' and y_expression=='rho'): d['y_lims']= [0,30]
			plots.append(d)
	if additional_dictionary != None:
		for plot in plots:
			plot.update(additional_dictionary)
	return [PlottingJob(plots=plots, args=args)]

def genjet_profile_comparisons(args=None, additional_dictionary=None):
	""" Some profile plots showing differences of matched genjets and recojets. """
	plots = []
	jet1_quantities = ['jet1pt-matchedgenjet1pt']#'abs(jet1eta-matchedgenjet1eta)', 'abs(jet1phi-matchedgenjet1phi)','sqrt((jet1eta-matchedgenjet1eta)^2+(jet1phi-matchedgenjet1phi)^2)']
	jet2_quantities = ['jet2pt-matchedgenjet2pt']#,'abs(jet2eta-matchedgenjet2eta)', 'abs(jet2phi-matchedgenjet2phi)','sqrt((jet2eta-matchedgenjet2eta)^2+(jet2phi-matchedgenjet2phi)^2)']
	
	y_dict = { #filename, label, y_lims of the quantity
		'jet1pt-matchedgenjet1pt': ['jet1delta_pt', r"$\\mathit{p}_\\mathrm{T}^\\mathrm{jet1}$-$\\mathit{p}_\\mathrm{T}^\\mathrm{genjet1}$",[-10,15]],
		'abs(jet1eta-matchedgenjet1eta)':['jet1delta_eta', r"|$\\mathit{\\eta}^{\\mathrm{jet1}}-\\mathit{\\eta}^\\mathrm{genjet1}$|",[0,1.5]], 
		'abs(jet1phi-matchedgenjet1phi)':['jet1delta_phi',r"|$\\mathit{\\phi}^{\\mathrm{jet1}}-\\mathit{\\phi}^\\mathrm{genjet1}$|",[0,3.6]],
		'sqrt((jet1eta-matchedgenjet1eta)^2+(jet1phi-matchedgenjet1phi)^2)': ['jet1delta_R',r"$\\Delta R(jet1,genjet1)$",[0,3.9]],
		'jet2pt-matchedgenjet2pt': ['jet2delta_pt',r"$\\mathit{p}_\\mathrm{T}^\\mathrm{jet2}-\\mathit{p}_\\mathrm{T}^\\mathrm{genjet2}$",[-10,10]],
		'abs(jet2eta-matchedgenjet2eta)': ['jet2delta_eta',r"|$\\mathit{\\eta}^{\\mathrm{jet2}}-\\mathit{\\eta}^\\mathrm{genjet2}$|",[0,4]], 
		'abs(jet2phi-matchedgenjet2phi)': ['jet2delta_phi',r"|$\\mathit{\\phi}^{\\mathrm{jet2}}-\\mathit{\\phi}^\\mathrm{genjet2}$|",[0,4]],
		'sqrt((jet2eta-matchedgenjet2eta)^2+(jet2phi-matchedgenjet2phi)^2)': ['jet2delta_R',r"$\\Delta R(jet2,genjet2)$",[0,5]],
	}
		
	for xquantity in ('matchedgenjet1pt','matchedgenjet2pt'): #Plot jet1 y-properties over jet1pt, same for jet2
		d = {
			'x_expressions': [xquantity],
			'cutlabel': True,
			'analysis_modules': ['ConvertToTGraphErrors'],
			'weights' : 'jet1pt>0&jet2pt>0&matchedgenjet1pt>0&matchedgenjet2pt>0', #Take only matched jets for this analysis
			'tree_draw_options': 'prof',
			'colors' : ['black','red','blue','green','green','blue','black'],
			'markers': ['o', 'd', '^','s','s','^', 'o'],
			'nicks' : ['puppi', 'chs', 'chspuidtight', 'chspuidmedium'],
			#'ratio_numerator_nicks' : ['chspuidmedium','chspuidtight', 'puppi'],
			#'ratio_denominator_nicks': ['chs', 'chs', 'chs'],
			#'ratio_result_nicks': ['puidtight_ratio', 'puidmedium_ratio','puppi_ratio'],
			#'y_subplot_lims': [0.5, 1.5],
			#'y_subplot_label': 'Ratio to CHS',
		}
		if xquantity == 'matchedgenjet1pt':

			for yquantity in jet1_quantities: #Jet1
				d1 = copy.deepcopy(d)
				d1["x_bins"] = ['12,30,150']
				d1['y_expressions'] = yquantity
				d1["filename"] = y_dict[yquantity][0]
				d1['y_label'] = y_dict[yquantity][1]
				d1['y_lims'] = y_dict[yquantity][2]
				plots.append(d1)
		elif xquantity == 'matchedgenjet2pt': #Jet2
			d["x_bins"] = ['14.0,70']
			for yquantity in jet2_quantities:
				d2 = copy.deepcopy(d)
				d2["x_bins"] = ['7,0,70']
				d2['x_lims'] = [0, 70]
				d2['y_expressions'] = yquantity
				d2["filename"] = y_dict[yquantity][0]
				d2['y_label'] = y_dict[yquantity][1]
				d2['y_lims'] = y_dict[yquantity][2]
				plots.append(d2)
	if additional_dictionary != None:
		for plot in plots:
			plot.update(additional_dictionary)
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
				'colors' : ['black','red','blue','green'],
				'markers': ['o', 'd', '^', 's'],
				'x_errors': [True],
				'tree_draw_options': 'profs',
				'analysis_modules': ['ConvertToHistogram', 'StatisticalErrors',],
				'stat_error_nicks': ['puppi', 'chs', 'chspuidtight','chspuidmedium' ],
				'convert_nicks': ['puppi', 'chs', 'chspuidtight', 'chspuidmedium'],
				'nicks': ['puppi', 'chs', 'chspuidtight', 'chspuidmedium'],
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
	if additional_dictionary != None:
		for plot in plots:
			plot.update(additional_dictionary)
	return [PlottingJob(plots=plots, args=args)]

def full_comparison(args=None, d=None, data_quantities=True, only_normalized=False,
	                channel="mm", inputtuple="datamc", subtract_hf=True):
	""" Do all comparison plots"""
	plotting_jobs = []
	#plotting_jobs += response_extrapolation(args, d, inputtuple)
	#plotting_jobs += basic_comparisons(args, d, data_quantities, only_normalized, channel)
	#plotting_jobs += basic_profile_comparisons(args, d)
	#plotting_jobs += genjet_profile_comparisons(args, d)
	plotting_jobs += fake_events(args,d)
	plotting_jobs += alpha_efficiency(args,d)
	#plotting_jobs += jet_resolution(args, additional_dictionary=d)
	return plotting_jobs

def comparison_CHS_Puppi_mm(args=None):
	plotting_jobs = []
	cuts = 'finalcuts'
	d = {
		'files': ['work/mm_Puppi.root', 'work/mm_CHS.root', 'work/mm_PUJetID_tight.root','work/mm_PUJetID_medium.root'],
		'labels': ['Puppi', 'CHS', 'CHS with tight PUJetID', "CHS with medium PUJetID"],
		'algorithms': ['ak4PFJetsPuppi', 'ak4PFJetsCHS', 'ak4PFJetsCHS', 'ak4PFJetsCHS'],
		'corrections': ['L1L2L3', 'L1L2L3','L1L2L3','L1L2L3'],
		'zjetfolders': [cuts,cuts, cuts, cuts],
		'texts': [r"MC $\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{\\mu \\mu}$"],
		'texts_x': [0.4],
		'texts_y': [1.06],
		'texts_size': [16],
		'www': 'Comparison_CMS_vs._Puppi_PUJetID_genjets_'+cuts,
	}
	plotting_jobs += full_comparison(args, d, channel="mm", inputtuple='mcmc')
	return plotting_jobs
def filter_comparisons(args=None):
	plotting_jobs = []
	cuts = 'finalcuts'
	d = {
		'files': ['work/mm_Puppi.root', 'work/mm_CHS.root','work/mm_Puppi.root', 'work/mm_CHS.root'],
		'labels': ['Puppi', 'CHS', 'Puppi w/o corrections', "CHS w/o corrections"],
		'algorithms': ['ak4PFJetsPuppi', 'ak4PFJetsCHS', 'ak4PFJetsPuppi', 'ak4PFJetsCHS'],
		'corrections': ['L1L2L3', 'L1L2L3','',''],
		'zjetfolders': [cuts,cuts, cuts, cuts],
		'texts': [r"MC $\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{\\mu \\mu}$"],
		'texts_x': [0.4],
		'texts_y': [1.07],
		'texts_size': [16],
		'www': 'Comparison_CMS_vs._Puppi_PUJetID_genjets_filter',
	}
	plotting_jobs += full_comparison(args, d, channel="mm", inputtuple='mcmc')
	return plotting_jobs
def ak8_comparisons(args=None):
	plotting_jobs = []
	cuts = 'finalcuts'
	d = {
		'files': ['work/mm_Puppi.root', 'work/mm_CHS.root','work/mm_Puppi_ak8.root', 'work/mm_CHS_ak8.root'],
		'labels': ['Puppi', 'CHS', 'Puppi ak8', "CHS ak8"],
		'algorithms': ['ak4PFJetsPuppi', 'ak4PFJetsCHS', 'ak8PFJetsPuppi', 'ak8PFJetsCHS'],
		'corrections': ['L1L2L3', 'L1L2L3','L1L2L3','L1L2L3'],
		'zjetfolders': [cuts,cuts, cuts, cuts],
		'texts': [r"MC $\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{\\mu \\mu}$"],
		'texts_x': [0.4],
		'texts_y': [1.07],
		'texts_size': [16],
		'www': 'Comparison_CMS_vs._Puppi_PUJetID_genjets_ak8',
	}
	plotting_jobs += full_comparison(args, d, channel="mm", inputtuple='mcmc')
	return plotting_jobs
def comparison_CHS_Puppi_ee(args=None):
	plotting_jobs = []
	cuts = 'finalcuts'
	d = {
		'files': ['work/eePuppi_PUJetID.root', 'work/ee_PUJetID.root'],
		'labels': ['Puppi', 'CHS'],
		'algorithms': ['ak4PFJetsPuppi', 'ak4PFJetsCHS'],
		'corrections': ['L1L2L3', 'L1L2L3'],
		'zjetfolders': [cuts,cuts],
		'texts': [r"MC $\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{ee}$"],
		'texts_x': [0.4],
		'texts_y': [1.06],
		'texts_size': [16],
		'www': 'Comparison_CMS_vs._Puppi_PUJetID_ee_'+cuts,
	}
	plotting_jobs += full_comparison(args, d, channel="ee", inputtuple='mcmc')
	return plotting_jobs
