#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, lims_from_binning
import Excalibur.Plotting.utility.binningsZJet as binningsZJet

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


def fit_function(dictionary):
	"""fits a distribution to the plot"""
	dictionary.update({"function_fit": ["nick0", "nick1"],
		"function_nicknames": ["nick0_fit", "nick1_fit"],
#
		#Gaussian function:
		#"functions": ["[2]*exp(-0.5*((x-[0])/[1])**2)"],
		#"function_parameters": ["91,5,200"],
		#"function_display_result": 'true',
		#"function_fit_parameter_names": ['mu', 'sigma', 'A'],
#
		#Cauchy/BreitWigner function:
		#"functions": ['[2]*[1]/((x-[0])**2+[1]**2/4)'],
		#"function_parameters": ["91,1,1000"],
		#"function_display_result": 'true',
		#"function-fit-parameter-names": ['mu', 'lambda', 'A'],
#
		#Voigt function:
		#"functions": "([3]*TMath::Voigt(x-[0],[2],[1]))",
		#"fit_text_npar": 3,
		#"fit_text_parameter_names": ['zmass', 'sigma', 'width', 'A'],
		#"functions": "([4]*TMath::Voigt(x-[0],2.4952,[1])+[2]*exp(-[3]*x))",		#fix width-parameter by value of PDG added drell yan exponential function
		#"fit_text_npar": 4,
		#"fit_text_parameter_names": ['zmass', 'sigma', 'k','A_exp','A_voigt'],
		"functions": "([2]*TMath::Voigt(x-[0],2.4952,[1]))",		#fix width-parameter by value of PDG
		"fit_text_npar": 2,
		"fit_text_parameter_names": ['zmass', 'sigma', 'A_voigt'],
		"function_parameters": "90,2.3,3100",
#
		"alphas": '0.5',
		"colors":['darkred','darkblue','black','darkred','darkblue'],
		'legend_cols': 1,
		"plot_modules": ["PlotMplZJet", 'PlotFitText'],#,'PlotMplMean'],
		"fit_text_nicks": ['nick0_fit', 'nick1_fit'],
		"fit_text_colors": ['darkred', 'darkblue'],
		"fit_text_position": [10, 10],
		"fit_text_size":'12',
		'legend':'center left',
		'y_subplot_lims': [0.0, 2.0],
		#"subplot_fraction": 40, 
	})

def fit_function_gen(dictionary):
	"""fits a distribution to the plot"""
	dictionary.update({"function_fit": ["nick0"],
		"function_nicknames": ["nick0_fit"],
#
		#Gaussian function:
		#"functions": ["[2]*exp(-0.5*((x-[0])/[1])**2)"],
		#"function_parameters": ["91,5,200"],
		#"function_display_result": 'true',
		#"function_fit_parameter_names": ['mu', 'sigma', 'A'],
#
		#Cauchy/BreitWigner function:
		#"functions": ['[2]*[1]/((x-[0])**2+[1]**2/4)'],
		#"function_parameters": ["91,1,1000"],
		#"function_display_result": 'true',
		#"function-fit-parameter-names": ['mu', 'lambda', 'A'],
#
		#Lorentz function:
		"functions": "[2]*(1/pi)*([1]/2)/((x-[0])*(x-[0]) + [1]*[1]/4)",
		"function_parameters": "91,2.2,1500",
		"fit_text_npar": 2,
		"fit_text_parameter_names": ['zmass', 'width', 'A'],
#
		"alphas": '0.5',
		"colors":['darkblue', 'darkblue'],
		'legend_cols': 1,
		"plot_modules": ["PlotMplZJet", 'PlotFitText'],#,'PlotMplMean'],
		"fit_text_nicks": ['nick0_fit'],
		"fit_text_colors": ['darkblue'],
		"fit_text_position": [10, 10],
		"fit_text_size":'12',
		'legend':'center left',
		'y_subplot_lims': [0.0, 2.0],
		#"subplot_fraction": 40,
	})

def generate_dict(args=None, additional_dictionary=None, channel="m"):
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
		'genzmass': ['40,71,111'],
	}
	x_dict_ee={
		'e1phi': ['20,-3.1415,3.1415',],
		'e1pt': ['20,0,150'],
		'e2pt': ['20,0,150'],
		'eminuspt': ['20,0,150'],
		'epluspt': ['20,0,150'],
	}
	x_dict_mm={
		'mu1phi': ['20,-3.1415,3.1415',],
		'mu1pt': ['20,0,150'],
		'mu2pt': ['20,0,150'],
		'muminuspt': ['20,0,150'],
		'mupluspt': ['20,0,150'],
	}
	if channel=="m": x_dict.update(x_dict_mm)
	elif channel=="e": x_dict.update(x_dict_ee)

	for q in x_dict:
		if len(x_dict[q]) == 1:
			x_dict[q] += ['best']
	return x_dict

def genzmass_fit(args=None, additional_dictionary=None, data_quantities=True, only_normalized=False, channel="m", inputtuple="datamc", subtract_hf=True):
	"""Comparison of: zmass, both absolute and normalized"""
	plots = []
	x_dict=generate_dict()
	quantity='genzmass'
	d = {
		'x_expressions': [quantity],
		'cutlabel': True,
		'y_subplot_lims': [0.75, 1.25],
		'analysis_modules': ['FunctionPlot'],
		'filename': quantity+'_fit',
		'title': r'$\\mathrm{M_{Z,gen}}$',
		'legend': 'upper right',
		'y_subplot_lims': [0.75, 1.25],
		"markers": ["fill"],
	}
	if quantity in x_dict:
		d["x_bins"] = [x_dict[quantity][0]]
		d["legend"] = x_dict[quantity][1]
	if quantity in binningsZJet.BinningsDictZJet().binnings_dict:
		x_bins=binningsZJet.BinningsDictZJet().binnings_dict[quantity]
		x_lims=lims_from_binning(x_bins)
		d["x_bins"] = [x_bins]
		d["x_lims"] = x_lims
	elif quantity in x_dict:
		d["x_bins"] = [x_dict[quantity][0]]
		d["x_lims"] = lims_from_binning(x_dict[quantity][0])
	if additional_dictionary:
		d.update(additional_dictionary)
	fit_function_gen(d)
	if channel=="m":
		d.update({ "labels": [r"$\\mu_\\mathrm{MC}$", ""], #default format of labels ["MC", "MC_fit"]
			"texts": [r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{\\mu \\mu}$"],
		})
	elif channel=="e":
		d.update({ "labels": [r"$e_\\mathrm{MC}$", ""], #default format of labels ["MC", "MC_fit"]
			"texts": [r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{e e}$"],
		})
 	d.update({"texts_x": [0.03],
		"texts_y": [0.90],
		#"texts_size": [10],
		})
#	d.update({"texts": [d.get('texts'),r"$\\mathrm{\\Gamma_{Z,PDG} = 2.4952 \\pm 0.0023}$"],
#		"texts_x": [d.get('texts_x'),0.55],
#		"texts_y": [d.get('texts_y'),0.80],
#	})
	plots.append(d)
	d2={}
	weight_name='error'
	for det_part in ['Barrel','EndCap+','EndCap-']:
		d2["{0}".format(det_part)] = copy.deepcopy(d)
		if channel=="m": 
			cut='1.3'
			minus_quantity='muminuseta'
			plus_quantity='mupluseta'
		elif channel=="e":
			cut='1.479'
			minus_quantity='eminuseta'
			plus_quantity='epluseta'
		if det_part=="EndCap+": 
			weight_name=minus_quantity+'>'+cut+'&&'+plus_quantity+'>'+cut
			if channel == "m":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.2,1500",
				})
			if channel == "e":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.2,1500",
				})
		elif det_part=="EndCap-":
			weight_name=minus_quantity+'<-'+cut+'&&'+plus_quantity+'<-'+cut
			if channel == "m":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.2,1500",
				})
			if channel == "e":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.2,1500",
				})
		elif det_part=="Barrel":
			weight_name='abs('+minus_quantity+')<'+cut+'&&abs('+plus_quantity+')<'+cut
			if channel == "m":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.2,1500",
				})
			if channel == "e":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.2,1500",
				})
		d2["{0}".format(det_part)].update({
			'filename': quantity+'_'+det_part+'_fit',
			'title':  r'$M\\mathrm{_{Z}}'+'('+det_part+')$',
			'weights': weight_name,
			})
		plots.append(d2["{0}".format(det_part)])
	return [PlottingJob(plots=plots, args=args)]

def zmass_comparison(args=None, additional_dictionary=None, data_quantities=True, only_normalized=False, channel="m", inputtuple="datamc", subtract_hf=True):
	"""Comparison of: zmass, both absolute and normalized"""
	plots = []
	x_dict=generate_dict()
	quantity='zmass'
	d = {
		'x_expressions': [quantity],
		'cutlabel': True,
		'analysis_modules': ['Ratio'],
		'y_subplot_lims': [0.75, 1.25],
		'analysis_modules': ['NormalizeToFirstHisto', 'Ratio', 'FunctionPlot'],
		'filename': quantity+'_fit',
		'title': r'$\\mathrm{M_{Z}}$',
		'legend': 'upper right',
		'y_subplot_lims': [0.75, 1.25],
	}
	if quantity in x_dict:
		d["x_bins"] = [x_dict[quantity][0]]
		d["legend"] = x_dict[quantity][1]
	if quantity in binningsZJet.BinningsDictZJet().binnings_dict:
		x_bins=binningsZJet.BinningsDictZJet().binnings_dict[quantity]
		x_lims=lims_from_binning(x_bins)
		d["x_bins"] = [x_bins]
		d["x_lims"] = x_lims
	elif quantity in x_dict:
		d["x_bins"] = [x_dict[quantity][0]]
		d["x_lims"] = lims_from_binning(x_dict[quantity][0])
	if additional_dictionary:
		d.update(additional_dictionary)
	fit_function(d)
	if channel=="m":
		d.update({ "labels": [r"$\\mu_\\mathrm{Data}$", r"$\\mu_\\mathrm{MC}$", "", "", ""], #default format of labels ["DATA", "MC", "Ratio", "DATA_fit", "MC_fit"]
			"texts": [r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{\\mu \\mu}$"],
		})
	elif channel=="e":
		d.update({ "labels": ["DATAe", "MCe", "", "", ""], #default format of labels ["DATA", "MC", "Ratio", "DATA_fit", "MC_fit"]
			"texts": [r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{e e}$"],
		})
	d.update({"texts_x": [0.03],
		"texts_y": [0.90],
		"texts_size": [10],
	})
	plots.append(d)
	d2={}
	weight_name='error'
	for det_part in ['Barrel','EndCap+','EndCap-']:
		d2["{0}".format(det_part)] = copy.deepcopy(d)
		if channel=="m": 
			cut='1.3'
			minus_quantity='muminuseta'
			plus_quantity='mupluseta'
		elif channel=="e":
			cut='1.479'
			minus_quantity='eminuseta'
			plus_quantity='epluseta'
		if det_part=="EndCap+": 
			weight_name=minus_quantity+'>'+cut+'&&'+plus_quantity+'>'+cut
			if channel == "m":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.3,3100",
				})
			if channel == "e":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.3,3100",
				})
		elif det_part=="EndCap-":
			weight_name=minus_quantity+'<-'+cut+'&&'+plus_quantity+'<-'+cut
			if channel == "m":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.3,3100",
				})
			if channel == "e":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.3,3100",
				})
		elif det_part=="Barrel":
			weight_name='abs('+minus_quantity+')<'+cut+'&&abs('+plus_quantity+')<'+cut
			if channel == "m":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.3,1000",
				})
			if channel == "e":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.3,1000",
				})
		d2["{0}".format(det_part)].update({
			'filename': quantity+'_'+det_part+'_fit',
			'title':  r'$M\\mathrm{_{Z}}'+'('+det_part+')$',
			'weights': weight_name,
			})
		plots.append(d2["{0}".format(det_part)])
	return [PlottingJob(plots=plots, args=args)]

def general_comparison(args=None, additional_dictionary=None, data_quantities=True, only_normalized=False, channel="m", inputtuple="datamc", subtract_hf=True):
	"""Comparison of: zmass, both absolute and normalized"""
	plots = []
	x_dict=generate_dict()
	print x_dict
	quantity_list= ['zmass','zpt','zeta']
	quantity_list_ee=[]
	quantity_list_mm=[]
	if channel=="m": quantity_list.extend(quantity_list_mm)
	elif channel=="e": quantity_list.extend(quantity_list_ee)
	for quantity in quantity_list:
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

		if quantity in binningsZJet.BinningsDictZJet().binnings_dict:
			x_bins=binningsZJet.BinningsDictZJet().binnings_dict[quantity]
			x_lims=lims_from_binning(x_bins)
			d["x_bins"] = [x_bins]
			d["x_lims"] = x_lims
		elif quantity in x_dict:
			d["x_bins"] = [x_dict[quantity][0]]
			d["x_lims"] = lims_from_binning(x_dict[quantity][0])

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
		if channel=='em':
			d2['y_label']= 'Electron Events'
		if additional_dictionary:
			d2.update(additional_dictionary)
		plots.append(d2)
	
#	#2D-Plotting generated to reconstructed quantities:
#	quantity_gen_reco_list= ['zmass','zpt']
#	for quantity in quantity_gen_reco_list:
#		genquantity='gen'+quantity
#		d3 = copy.deepcopy(d)
#		d3.update({'files':'work/mc15_25ns.root',
#			'corrections':['L1L2L3','L1L2L3'],
#			'y_expressions':genquantity,
#			'x_expressions':quantity,
#			'tree_draw_options': '',
#			'cutlabel': True,
#			'analysis_modules': ['NormalizeToFirstHisto'],
#			'y_log': quantity in [''],
#			'x_log': quantity in [''],
#			#'y_log': quantity in ['jet1pt', 'zpt'],
#			#'x_log': quantity in ['jet1pt', 'zpt'],
#		})
#		lims_list=lims_from_binning(x_dict[quantity][0])
#		d3["x_bins"] = [x_dict[quantity][0]]
#		d3["x_lims"] = [lims_list]
#		d3["y_bins"] = [x_dict[quantity][0]]
#		d3["y_lims"] = [lims_list]
#		plots.append(d3)

	#Plotting profile plots of various quantities:
	quantity_2d_list= [['zeta','zmass'],['zpt','zmass'],]
	if channel == 'm':
		quantity_2d_list.extend([['muminuseta','zmass'],['mupluseta','zmass'],])
	elif channel == 'e':
		quantity_2d_list.extend([['eminuseta','zmass'],['epluseta','zmass'],])
	x_dict.update({'zmass': ['40,86,96'],})

	for quantity_pair in quantity_2d_list:
		d4 = copy.deepcopy(d)
		d4.update({'y_expressions':[quantity_pair[1]],
			'x_expressions':[quantity_pair[0]],
			'tree_draw_options': 'prof',
			'cutlabel': True,
			#'analysis_modules': ['FunctionPlot'],
			"plot_modules": ["PlotMplZJet"],
			"title": quantity_pair[0]+' vs. '+quantity_pair[1],
			'y_log': quantity_pair[1] in ['jet1pt', 'zpt'],
			'x_log': quantity_pair[0] in ['jet1pt', 'zpt'],
		})
		if quantity_pair[1]=="zmass":
			d4['lines'] = ['91.1876']
		if quantity_pair[0] in ['zeta','mupluseta','muminuseta','epluseta','eminuseta']:
			d4["plot_modules"] = ["PlotMplZJet","PlotMplRectangle"]
			if channel == 'm':
				d4["rectangle_x"] = [-6,-1.3,1.3,6]
			elif channel == 'e':
				d4["rectangle_x"] = [-6,-1.479,1.479,6]
			d4["rectangle_alpha"] = [0.2]
			d4["rectangle_color"] = ["red"]
		if quantity_pair[0] in binningsZJet.BinningsDictZJet().binnings_dict:
			x_bins=binningsZJet.BinningsDictZJet().binnings_dict[quantity_pair[0]]
			x_lims=lims_from_binning(x_bins)
			d4["x_bins"] = [x_bins]
			d4["x_lims"] = x_lims
		elif quantity_pair[0] in x_dict:
			d4["x_bins"] = [x_dict[quantity_pair[0]][0]]
			d4["x_lims"] = lims_from_binning(x_dict[quantity_pair[0]][0])
		if quantity_pair[1] in binningsZJet.BinningsDictZJet().binnings_dict:
			y_bins=binningsZJet.BinningsDictZJet().binnings_dict[quantity_pair[1]]
			y_lims=lims_from_binning(x_bins)
		#	d4["y_bins"] = [y_bins]
			d4["y_lims"] = y_lims
		elif quantity_pair[1] in x_dict:
		#	d4["y_bins"] = [x_dict[quantity_pair[1]][0]]
			d4["y_lims"] = lims_from_binning(x_dict[quantity_pair[1]][0])
		plots.append(d4)


	return [PlottingJob(plots=plots, args=args)]


def zmass_comparison_run2(args=None):
	"""Comparison for run2 samples."""
	plotting_jobs = []
	d = {
		'labels': ['Data L1L2L3Res','MC L1L2L3'],
		'y_subplot_label' : "Data/MC",
		'algorithms': ['ak4PFJetsCHS'],
		'corrections': ['L1L2L3Res', 'L1L2L3'],
	}
	plotting_jobs += zmass_comparison(args, d, only_normalized=True)

	d.update({'folders': ['finalcuts_ak4PFJetsCHSL1L2L3Res', 'finalcuts_ak4PFJetsCHSL1L2L3']})
	#plotting_jobs += cutflow(args, d)
	jec_factors.jec_factors(args, {
		'files': ['work/mc15.root'],
		'algorithms': ['ak4PFJetsCHS'],
		'corrections': ['L1L2L3'],
	}, rc=False, res=False)
	return plotting_jobs

def zmass_comparison_datamc_Zmm_run2(args=None):
	"""Run2: full data mc comparisons for work/data15_25ns.root and work/mc15_25ns.root for Zmm"""
	zjetfolder='zcuts'
	plotting_jobs = []
	d = {
		'files': ['work/data15_25ns.root', 'work/mc15_25ns.root'],
		'labels': ['DATAmu', 'MCmu'],
		'corrections': ['L1L2L3Res', 'L1L2L3'],
		'algorithms': ['ak4PFJetsCHS'],
		'www': zjetfolder+'_zmass_comparison_datamc_Zmm_run2',
		'www_title': 'Comparison Data MC for Zmm, run2, '+zjetfolder,
		'www_text':'Run2: Zmass data mc comparisons for work/data15_25ns.root and work/mc15_25ns.root for Zmm',
	}
	d.update({'zjetfolders': [zjetfolder]})
	plotting_jobs += zmass_comparison(args, d, channel="m", inputtuple='datadata')#usually datamc
	d.update({'files': ['work/mc15_25ns.root'],
		'labels': ['MCmu'],
		'corrections': ['L1L2L3'],})
	plotting_jobs += genzmass_fit(args, d, channel="m", inputtuple='datadata')
	#plotting_jobs += cutflow(args, d)
	return plotting_jobs

def zmass_comparison_datamc_Zee_run2(args=None):
	"""Run2: full data mc comparisons for work/data15_25ns_ee.root and work/mc15_25ns_ee.root"""
	zjetfolder='zcuts'
	plotting_jobs = []
	d = {
		'files': ['work/data15_25ns_ee.root', 'work/mc15_25ns_ee.root'],
		'labels': ['DATAe', 'MCe'],
		'corrections': ['L1L2L3Res', 'L1L2L3'],
		'algorithms': ['ak4PFJetsCHS'],
		'www': zjetfolder+'_zmass_comparison_datamc_Zee_run2',
		'www_title': 'Comparison Data MC for Zee, run2, '+zjetfolder,
		'www_text':'Run2: Zmass data mc comparisons for work/data15_25ns_ee.root and work/mc15_25ns_ee.root',
	}
	d.update({'zjetfolders': [zjetfolder]})
	plotting_jobs += zmass_comparison(args, d, channel="e", inputtuple='datadata')#usually datamc
	d.update({'files': ['work/mc15_25ns_ee.root'],
		'labels': ['MCe'],
		'corrections': ['L1L2L3'],})
	plotting_jobs += genzmass_fit(args, d, channel="e", inputtuple='datadata')
	#plotting_jobs += cutflow(args, d)
	return plotting_jobs

if __name__ == '__main__':
	zmass_comparisons()
