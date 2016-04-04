#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, lims_from_binning
import Excalibur.Plotting.utility.binningsZJet as binningsZJet

import argparse
import copy
import jec_factors
import jec_files

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
		'generatorWeight': ['100,-2,2'],
		'puWeight': ['100,0,10'],
		'hlt': ['100,-0.5,1.5'],
		'weight': ['100,-1,1'],
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


def fit_function_gen(dictionary):
	"""fits a distribution to the plot"""
	dictionary.update({"function_fit": ["nick0"],
		"function_nicknames": ["nick0_fit"],
#
		#Lorentz function:
		"functions": "[2]*(1/pi)*([1]/2)/((x-[0])*(x-[0])+[1]*[1]/4)",
		"function_parameters": "91,2.3,3500",
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

def genzmass_fit(args=None, additional_dictionary=None, only_normalized=False, channel="m"):
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
		'title': 'Work in Progress',#r'$\\mathrm{M_{Z,gen}}$',
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
			"function_parameters": "91,2.4,2500",
		})
	elif channel=="e":
		d.update({ "labels": [r"$e_\\mathrm{MC}$", ""], #default format of labels ["MC", "MC_fit"]
			"function_parameters": "91,2.3,5000",
		})
#	d.update({"texts": [d.get('texts'),r"$\\mathrm{\\Gamma_{Z,PDG} = 2.4952 \\pm 0.0023}$"],
#		"texts_x": [d.get('texts_x'),0.55],
#		"texts_y": [d.get('texts_y'),0.80],
#		})
	plots.append(d)
	d2={}
	weight_name='error'
	for det_part in ['Barrel','EndCap+','EndCap-']:#,'Barrel&EndCap+','Barrel&EndCap-','EndCap+&EndCap-']:
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
				"function_parameters": "91,2.2,2500",
				})
			if channel == "e":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.2,2500",
				})
		elif det_part=="EndCap-":
			weight_name=minus_quantity+'<-'+cut+'&&'+plus_quantity+'<-'+cut
			if channel == "m":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.2,2500",
				})
			if channel == "e":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.2,2500",
				})
		elif det_part=="Barrel":
			weight_name='abs('+minus_quantity+')<'+cut+'&&abs('+plus_quantity+')<'+cut
			if channel == "m":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.2,3500",
				})
			if channel == "e":
				d2["{0}".format(det_part)].update({
				"function_parameters": "91,2.3,4500",
				})

#		elif det_part=="Barrel&EndCap+":
#			weight_name='abs('+minus_quantity+')<'+cut+'&&'+plus_quantity+'>'+cut+'||abs('+plus_quantity+')<'+cut+'&&'+minus_quantity+'>'+cut
#			if channel == "m":
#				d2["{0}".format(det_part)].update({
#				"function_parameters": "91,2.2,3500",
#				})
#			if channel == "e":
#				d2["{0}".format(det_part)].update({
#				"function_parameters": "91,2.3,4500",
#				})
#
#		elif det_part=="Barrel&EndCap-":
#			weight_name='abs('+minus_quantity+')<'+cut+'&&'+plus_quantity+'>-'+cut+'||abs('+plus_quantity+')<'+cut+'&&'+minus_quantity+'>-'+cut
#			if channel == "m":
#				d2["{0}".format(det_part)].update({
#				"function_parameters": "91,2.2,3500",
#				})
#			if channel == "e":
#				d2["{0}".format(det_part)].update({
#				"function_parameters": "91,2.3,4500",
#				})
#
#		elif det_part=="EndCap+&EndCap-":
#			weight_name=minus_quantity+'>'+cut+'&&'+plus_quantity+'>-'+cut+'||'+plus_quantity+'>'+cut+'&&'+minus_quantity+'>-'+cut
#			if channel == "m":
#				d2["{0}".format(det_part)].update({
#				"function_parameters": "91,2.2,3500",
#				})
#			if channel == "e":
#				d2["{0}".format(det_part)].update({
#				"function_parameters": "91,2.3,4500",
#				})
		d2["{0}".format(det_part)].update({
			'filename': quantity+'_'+det_part+'_fit',
			'title':  'Work in Progress',#r'$M\\mathrm{_{Z}}'+'('+det_part+')$',
			'weights': weight_name,
			})
		plots.append(d2["{0}".format(det_part)])
	return [PlottingJob(plots=plots, args=args)]


def fit_function(dictionary):
	"""fits a distribution to the plot"""
	dictionary.update({"function_fit": ["nick0", "nick1"],
		"function_nicknames": ["nick0_fit", "nick1_fit"],
#
		#Voigt function:
		#"functions": "([3]*TMath::Voigt(x-[0],[2],[1]))",
		#"fit_text_npar": 3,
		#"fit_text_parameter_names": ['zmass', 'sigma', 'width', 'A'],
		"functions": "([4]*TMath::Voigt(x-[0],[1],2.4952)+[2]*x+[3])",	#fix width-parameter by value of PDG added background linear function
		"fit_text_npar": 2,
		"fit_text_parameter_names": ['zmass', 'sigma', 'm', 'c', 'A_voigt'],
		"function_parameters": "90,2.3,0.,0.,3100",
		#"functions": "([4]*TMath::Voigt(x-[0],[1],2.4952)+[2]*exp(-[3]*x))",	#fix width-parameter by value of PDG added drell yan exponential function
		#"fit_text_npar": 4,
		#"fit_text_parameter_names": ['zmass', 'sigma', 'k','A_exp','A_voigt'],
		#"functions": "([2]*TMath::Voigt(x-[0],2.4952,[1]))",	#fix width-parameter by value of PDG
		#"fit_text_npar": 2,
		#"fit_text_parameter_names": ['zmass', 'sigma', 'A_voigt'],
		#"function_parameters": "90,2.3,2500",
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


def zmass_comparison(args=None, additional_dictionary=None, only_normalized=False, channel="m"):
	"""Comparison of: zmass, both absolute and normalized"""
	plots = []
	x_dict=generate_dict()
	quantity='zmass'
	d = {
		'x_expressions': [quantity],
		'cutlabel': True,
		'y_subplot_lims': [0.75, 1.25],
		#'analysis_modules': ['NormalizeToFirstHisto','Ratio', 'FunctionPlot'],
		'analysis_modules': ['Ratio', 'FunctionPlot'],
		'filename': quantity+'_fit',
		'title': 'Work in Progress',#r'$\\mathrm{M_{Z}}$',
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
	if channel == "m":
		d.update({
		#"function_parameters": "91,2.3,3100",
		"function_parameters": "91,2.2,0.,0.,3500",
		})
	if channel == "e":
		d.update({
		#"function_parameters": "91,2.3,3100",
		"function_parameters": "91,2.2,0.,0.,3100",
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
				#"function_parameters": "91,2.3,3100",
				"function_parameters": "91,2.2,0.,0.,3000",
				})
			if channel == "e":
				d2["{0}".format(det_part)].update({
				#"function_parameters": "91,2.3,3100",
				"function_parameters": "91,2.2,0.,0.,3100",
				})
		elif det_part=="EndCap-":
			weight_name=minus_quantity+'<-'+cut+'&&'+plus_quantity+'<-'+cut
			if channel == "m":
				d2["{0}".format(det_part)].update({
				#"function_parameters": "91,2.3,3100",
				"function_parameters": "91,2.2,0.,0.,3100",
				})
			if channel == "e":
				d2["{0}".format(det_part)].update({
				#"function_parameters": "91,2.3,3100",
				"function_parameters": "91,2.2,0.,0.,3100",
				})
		elif det_part=="Barrel":
			weight_name='abs('+minus_quantity+')<'+cut+'&&abs('+plus_quantity+')<'+cut
			if channel == "m":
				d2["{0}".format(det_part)].update({
				#"function_parameters": "91,2.3,1000",
				"function_parameters": "91,2.2,0.,0.,1200",
				})
			if channel == "e":
				d2["{0}".format(det_part)].update({
				#"function_parameters": "91,2.3,1000",
				"function_parameters": "91,2.2,0.,0.,1000",
				})
		d2["{0}".format(det_part)].update({
			'filename': quantity+'_'+det_part+'_fit',
			'title':  'Work in Progress',#r'$M\\mathrm{_{Z}}'+'('+det_part+')$',
			'weights': weight_name,
			})
		plots.append(d2["{0}".format(det_part)])
	return [PlottingJob(plots=plots, args=args)]

def general_mc_comparison(args=None, additional_dictionary=None, channel="m"):
	"""Comparison of: various quantities, both absolute and normalized"""
	plots = []
	x_dict=generate_dict()
	quantity_list= ['puWeight','generatorWeight','weight','hlt']#
	quantity_list_ee=[]
	quantity_list_mm=[]
	if channel=="m": quantity_list.extend(quantity_list_mm)
	elif channel=="e": quantity_list.extend(quantity_list_ee)
	for quantity in quantity_list:
		# normal comparison
		d = {
			'x_expressions': [quantity],
			'cutlabel': True,
			'no_weight': quantity in ['generatorWeight', 'weight', 'puWeight', 'hlt'],
			'y_log': quantity in ['jet1pt', 'zpt'],
			'x_log': quantity in ['jet1pt', 'zpt'],
			"plot_modules": ["PlotMplZJet"],
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
		elif quantity in ['generatorWeight', 'weight', 'puWeight', 'hlt']:
			d['plot_modules'] = ['PlotMplZJet','PlotMplMean']

		if quantity in binningsZJet.BinningsDictZJet().binnings_dict:
			x_bins=binningsZJet.BinningsDictZJet().binnings_dict[quantity]
			x_lims=lims_from_binning(x_bins)
			d["x_bins"] = [x_bins]
			d["x_lims"] = x_lims
		elif quantity in x_dict:
			d["x_bins"] = [x_dict[quantity][0]]
			d["x_lims"] = lims_from_binning(x_dict[quantity][0])

		if quantity in ['zeta','mupluseta','muminuseta','epluseta','eminuseta']:
			d["plot_modules"] = ["PlotMplZJet","PlotMplRectangle"]
			if channel == 'm':
				d["rectangle_x"] = [-6,-1.3,1.3,6]
			elif channel == 'e':
				d["rectangle_x"] = [-6,-1.479,1.479,6]
			d["rectangle_alpha"] = [0.2]
			d["rectangle_color"] = ["red"]

		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def general_comparison(args=None, additional_dictionary=None, only_normalized=False, channel="m"):
	"""Comparison of: various quantities, both absolute and normalized"""
	plots = []
	x_dict=generate_dict()
	quantity_list= ['zpt','zeta','zphi','zy','metphi','met']
	quantity_list_ee=['epluseta','eminuseta','eminuspt','epluspt','eminusphi','eplusphi']
	quantity_list_mm=['mupluseta','muminuseta','muminuspt','mupluspt','muminusphi','muplusphi']
	if channel=="m": quantity_list.extend(quantity_list_mm)
	elif channel=="e": quantity_list.extend(quantity_list_ee)
	for quantity in quantity_list:
		# normal comparison
		d = {
			'x_expressions': [quantity],
			'cutlabel': True,
			'analysis_modules': ['Ratio'],
			'y_subplot_lims': [0.75, 1.25],
			'y_log': quantity in ['jet1pt', 'zpt'],
			'x_log': quantity in ['jet1pt', 'zpt'],
			"plot_modules": ["PlotMplZJet"],
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

		if quantity in ['zeta','mupluseta','muminuseta','epluseta','eminuseta']:
			d["plot_modules"] = ["PlotMplZJet","PlotMplRectangle"]
			if channel == 'm':
				d["rectangle_x"] = [-6,-1.3,1.3,6]
			elif channel == 'e':
				d["rectangle_x"] = [-6,-1.479,1.479,6]
			d["rectangle_alpha"] = [0.2]
			d["rectangle_color"] = ["red"]


		if not only_normalized:
			plots.append(d)

		# shape comparison
		d2 = copy.deepcopy(d)
		d2.update({
			'analysis_modules': ['NormalizeToFirstHisto', 'Ratio'],
			'filename': quantity+"_shapeComparison",
			'title': 'Work in Progress',#"Shape Comparison",
			'legend': 'upper right',
			'y_subplot_lims': [0.75, 1.25],
		})
		if channel=='em':
			d2['y_label']= 'Electron Events'
		if additional_dictionary:
			d2.update(additional_dictionary)
		plots.append(d2)

	return [PlottingJob(plots=plots, args=args)]

def profplot_datamc_comparison(args=None, additional_dictionary=None, only_normalized=False, channel="m"):
	"""Comparison in 2D Plots"""
	plots = []
	x_dict=generate_dict()

	#Plotting profile plots of various quantities:
	quantity_2d_list= [['zeta','zmass'],['zpt','zmass'],]
	if channel == 'm':
		quantity_2d_list.extend([['muminuseta','zmass'],['mupluseta','zmass'],])
	elif channel == 'e':
		quantity_2d_list.extend([['eminuseta','zmass'],['epluseta','zmass'],])
#	x_dict.update({'zmass': ['40,90,92'],})
	x_dict.update({'zmass': ['40,86.1876,96.1876'],})
	for quantity_pair in quantity_2d_list:
		d = {	'cutlabel': True,
			'analysis_modules': ['Ratio'],
			'tree_draw_options': 'prof',
			"plot_modules": ["PlotMplZJet"],
			'y_subplot_lims': [0.99, 1.01],
		}
		if additional_dictionary:
			d.update(additional_dictionary)
		d.update({'y_expressions':[quantity_pair[1]],
			'x_expressions':[quantity_pair[0]],
			"title": 'Work in Progress',#quantity_pair[0]+' vs. '+quantity_pair[1],
			'filename':quantity_pair[0]+'_vs_'+quantity_pair[1],
			'y_log': quantity_pair[1] in ['jet1pt', 'zpt'],
			'x_log': quantity_pair[0] in ['jet1pt', 'zpt'],
		})
		if quantity_pair[1]=="zmass":
			d['lines'] = ['91.1876']
		if quantity_pair[0] in ['zeta','mupluseta','muminuseta','epluseta','eminuseta']:
			d["plot_modules"] = ["PlotMplZJet","PlotMplRectangle"]
			if channel == 'm':
				d["rectangle_x"] = [-6,-1.3,1.3,6]
			elif channel == 'e':
				d["rectangle_x"] = [-6,-1.479,1.479,6]
			d["rectangle_alpha"] = [0.2]
			d["rectangle_color"] = ["red"]
		if quantity_pair[0] in binningsZJet.BinningsDictZJet().binnings_dict:
			x_bins=binningsZJet.BinningsDictZJet().binnings_dict[quantity_pair[0]]
			x_lims=lims_from_binning(x_bins)
			d["x_bins"] = [x_bins]
			d["x_lims"] = x_lims
		elif quantity_pair[0] in x_dict:
			d["x_bins"] = [x_dict[quantity_pair[0]][0]]
			d["x_lims"] = lims_from_binning(x_dict[quantity_pair[0]][0])
		if quantity_pair[1] in binningsZJet.BinningsDictZJet().binnings_dict:
			y_bins=binningsZJet.BinningsDictZJet().binnings_dict[quantity_pair[1]]
			y_lims=lims_from_binning(x_bins)
		#	d["y_bins"] = [y_bins]
			d["y_lims"] = y_lims
		elif quantity_pair[1] in x_dict:
		#	d["y_bins"] = [x_dict[quantity_pair[1]][0]]
			d["y_lims"] = lims_from_binning(x_dict[quantity_pair[1]][0])
		plots.append(d)

	return [PlottingJob(plots=plots, args=args)]


def twodimplot_datamc_comparison(args=None, additional_dictionary=None, only_normalized=False, channel="m"):
	"""Comparison in 2D Plots"""
	plots = []
	x_dict=generate_dict()

	#Plotting profile plots of various quantities:
	quantity_2d_list= []
	if channel == 'm':
		quantity_2d_list.extend([['muminuseta','mupluseta'],])
	elif channel == 'e':
		quantity_2d_list.extend([['eminuseta','epluseta'],])
	
	for quantity_pair in quantity_2d_list:
		nick_list=['nick0','nick1','nick_div']
		for nick,label in [[nick_list[0],'DATA'],[nick_list[1],'MC'],[nick_list[2],'DATA/MC']]:
			print nick
			d = {	'cutlabel': True,
				#'analysis_modules': ['NormalizeToFirstHisto'],
				#"plot_modules": ["PlotMplZJet"],
				#'y_subplot_lims': [0.99, 1.01],
				'colormap': 'Blues',
			}
			if additional_dictionary:
				d.update(additional_dictionary)
			d.update({'y_expressions':[quantity_pair[1]],
				'x_expressions':[quantity_pair[0]],
				'labels': label,
				"title": 'Work in Progress',#quantity_pair[0]+' vs. '+quantity_pair[1],
				'filename':quantity_pair[0]+'_vs_'+quantity_pair[1]+'_'+nick,
				#'y_log': quantity_pair[1] in ['jet1pt', 'zpt'],
				#'x_log': quantity_pair[0] in ['jet1pt', 'zpt'],
				})
			if nick=='nick_div':
				d.update({
					'analysis_modules': ['Divide'],
					'divide_numerator_nicks': 'nick1',
					'divide_denominator_nicks': 'nick0',
					'divide_result_nicks': nick,
					'event_number_label': False,
				})
			d.update({
				'nicks_blacklist': list(filter(lambda x: x!= nick, nick_list)),
				'nicks_whitelist': nick,
				})

			if quantity_pair[0] in binningsZJet.BinningsDictZJet().binnings_dict:
				x_bins=binningsZJet.BinningsDictZJet().binnings_dict[quantity_pair[0]]
				x_lims=lims_from_binning(x_bins)
				d["x_bins"] = [x_bins]
				d["x_lims"] = x_lims
			elif quantity_pair[0] in x_dict:
				d["x_bins"] = [x_dict[quantity_pair[0]][0]]
				d["x_lims"] = lims_from_binning(x_dict[quantity_pair[0]][0])
			if quantity_pair[1] in binningsZJet.BinningsDictZJet().binnings_dict:
				y_bins=binningsZJet.BinningsDictZJet().binnings_dict[quantity_pair[1]]
				y_lims=lims_from_binning(x_bins)
				d["y_bins"] = [y_bins]
				d["y_lims"] = y_lims
			elif quantity_pair[1] in x_dict:
				d["y_bins"] = [x_dict[quantity_pair[1]][0]]
				d["y_lims"] = lims_from_binning(x_dict[quantity_pair[1]][0])
			print d
			plots.append(d)

	return [PlottingJob(plots=plots, args=args)]



#def profplot_genreco_comparison(args=None, additional_dictionary=None, only_normalized=False, channel="m"):
#	"""Comparison generated level to reconstructed level in 2D Plots"""
#	plots = []
#	x_dict=generate_dict()
#
#	#Plotting profile plots of various quantities:
#	quantity_2d_list= ['zpt','zeta',]
#	if channel == 'm':
#		quantity_2d_list.extend(['muminuseta','mupluseta',])
#	elif channel == 'e':
#		quantity_2d_list.extend(['eminuseta','epluseta',])
#	x_dict.update({'zmass': ['40,90,92'],})
#	
#	for quantity in quantity_2d_list:
#		genrecoquantity=quantity+'/gen'+quantity
#		d = {	'cutlabel': True,
#			#'analysis_modules': ['Ratio'],
#			'tree_draw_options': 'prof',
#			"plot_modules": ["PlotMplZJet"],
#			'y_subplot_lims': [0.99, 1.01],
#		}
#		if additional_dictionary:
#			d.update(additional_dictionary)
#		d.update({'y_expressions':genrecoquantity,
#			'x_expressions':quantity,
#			'weights':quantity,
#			"title":quantity+' gen/reco comparison',
#			'filename':quantity+'_gen_reco_comparison',
#			#'y_log': quantity in ['jet1pt', 'zpt'],
#			'x_log': quantity in ['jet1pt', 'zpt'],
#		})
#		if quantity in ['zeta','mupluseta','muminuseta','epluseta','eminuseta']:
#			d["plot_modules"] = ["PlotMplZJet","PlotMplRectangle"]
#			if channel == 'm':
#				d["rectangle_x"] = [-6,-1.3,1.3,6]
#			elif channel == 'e':
#				d["rectangle_x"] = [-6,-1.479,1.479,6]
#			d["rectangle_alpha"] = [0.2]
#			d["rectangle_color"] = ["red"]
#		if quantity in binningsZJet.BinningsDictZJet().binnings_dict:
#			x_bins=binningsZJet.BinningsDictZJet().binnings_dict[quantity]
#			x_lims=lims_from_binning(x_bins)
#			d["x_bins"] = [x_bins]
#			d["x_lims"] = x_lims
#		elif quantity in x_dict:
#			d["x_bins"] = [x_dict[quantity][0]]
#			d["x_lims"] = lims_from_binning(x_dict[quantity][0])
#		plots.append(d)
#
#	return [PlottingJob(plots=plots, args=args)]

def fit_zmass_profplot_datamc(args=None, additional_dictionary=None, only_normalized=False, channel="m"):
	"""Profile Plot of fitted Zmasses in bins of any quantity"""
	plots = []
	bins=[]
	x_dict=generate_dict()
	cut_quantities=['zpt','zeta']
	cut_binnings=['30 40 50 60 85 105 130 175 275 500','-5.191 -2.964 -2.5 -1.93 -1.305 -0.783 0 0.783 1.305 1.93 2.5 2.964 5.191']
	for cut_index,cut_quantity in enumerate(cut_quantities):
		cut_binning=cut_binnings[cut_index].split()
		fit_quantity='zmass'
		d = {
			'x_expressions': fit_quantity,
			'cutlabel': True,
			'analysis_modules': ['FunctionPlot', 'HistogramFromFitValues','Ratio'],
			'filename': fit_quantity+'_vs_'+cut_quantity+'_fit_profplot',
			'title': 'Work in Progress',#r'$\\mathrm{M_{Z}}$',
			'legend': 'upper right',
		}
		if additional_dictionary:
			d.update(additional_dictionary)
		copyfiles=d['files']
		weights=[]
		nicks=[]
		files=[]
		labels=[]
		corrections=[]
		fit_hist_nicks=[]
		fit_function_nicks=[]
		x_bins=[]

		for dataset in ['Data','MC']:
			fit_nicks=[]
			x_values=[]
			for index in range(len(cut_binning)-1):
				weights+=[str(cut_binning[index])+'<'+cut_quantity+'&&'+cut_quantity+'<'+str(cut_binning[index+1])]
				nicks+=['nick_'+str(cut_quantity)+'_'+str(dataset)+'_'+str(index)]
				fit_nicks+=['nick_'+str(cut_quantity)+'_'+str(dataset)+'_'+str(index)+'_fit']
				if dataset=='Data':
					files+=[copyfiles[0]]
					labels+=['DATA']
				elif dataset=='MC':
					files+=[copyfiles[1]]
					labels+=['MC']
				corrections+=['L1L2L3']
			fit_function_nicks+=fit_nicks
			fit_hist_nicks+=[" ".join(fit_nicks)]
			x_bins+=[" ".join(map(str,cut_binning))]

		d.update({
			'nicks':nicks,
			'files': files,
			'corrections': corrections,
			"function_fit": nicks,
			"function_nicknames": fit_function_nicks,
			#Voigt function:
			"functions": ['([4]*TMath::Voigt(x-[0],[1],2.4952)+[2]*x+[3])'],	#fix width-parameter by value of PDG added background linear function
			"function_parameters": ["91,2.3,0.,0.,2500"],
			'weights': weights,
			'nicks_whitelist': ['fit_data_values','fit_mc_values'],
			'histogram_from_fit_nicks': fit_hist_nicks,
			'histogram_from_fit_newnick': ['fit_data_values','fit_mc_values'],
			'histogram_from_fit_x_values': x_bins,
			'y_lims': [86,96],
			'y_label': 'zmass',
			#'x_lims': [min(cut_binning),max(cut_binning)],
			'x_log':  cut_quantity in ['jet1pt', 'zpt'],
			'x_label': cut_quantity,
			'markers': ['d','o', 'd'],
			"colors":['black', 'black', 'blue'],
			'labels':['Data','Ratio','MC'],
			'lines': [91.1876],
			'ratio_numerator_nicks': 'fit_data_values',
			'ratio_denominator_nicks': 'fit_mc_values',
			'y_subplot_lims': [0.99, 1.01],
			})

		plots.append(d)
	
	return [PlottingJob(plots=plots, args=args)]

#######################################################################################################################################################################

def zmass_comparison_datamc_Zmm_run2(args=None):
	"""Run2: full data mc comparisons for work/data15_25ns.root and work/mc15_25ns.root for Zmm"""
	zjetfolder='finalcuts'
	plotting_jobs = []
	d = {
		'files': ['work/data15_25ns.root', 'work/mc15_25ns.root'],
		'labels': ['DATAmu', 'MCmu'],
		'corrections': ['L1L2L3Res', 'L1L2L3'],
		'algorithms': ['ak4PFJetsCHS'],
		'www': zjetfolder+'_zmass_comparison_datamc_Zmm_run2',
		'www_title': 'Comparison Data MC for Zmm, run2, '+zjetfolder,
		'www_text':'Run2: Zmass data mc comparisons for work/data15_25ns.root and work/mc15_25ns.root for Zmm',
		'zjetfolders': [zjetfolder],
		}
	d.update({ "labels": [r"$\\mu_\\mathrm{Data}$", r"$\\mu_\\mathrm{MC}$", "", "", ""], #default format of labels ["DATA", "MC", "Ratio", "DATA_fit", "MC_fit"]
		"texts": [r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{\\mu \\mu}$"],
	})
	d.update({"texts_x": [0.03],
		"texts_y": [0.70],
		"texts_size": [10],
	})
	plotting_jobs += fit_zmass_profplot_datamc(args, d, channel="m")
	plotting_jobs += zmass_comparison(args, d, channel="m")#usually datamc
	plotting_jobs += general_comparison(args, d, channel="m", only_normalized=False)
	plotting_jobs += profplot_datamc_comparison(args, d, channel="m")
	#plotting_jobs += twodimplot_datamc_comparison(args, d, channel="m")
	d.update({'files': ['work/mc15_25ns.root'],
		'labels': ['MCmu'],
		'corrections': ['L1L2L3'],})
	#plotting_jobs += general_mc_comparison(args, d, channel="m")
	plotting_jobs += genzmass_fit(args, d, channel="m")
#	plotting_jobs += profplot_genreco_comparison(args, d, channel="m")
#	plotting_jobs += cutflow(args, d)
	return plotting_jobs

def zmass_comparison_datamc_Zee_run2(args=None):
	"""Run2: full data mc comparisons for work/data15_25ns_ee.root and work/mc15_25ns_ee.root"""
	zjetfolder='finalcuts'
	plotting_jobs = []
	d = {
		'files': ['work/data15_25ns_ee.root', 'work/mc15_25ns_ee.root'],
		'labels': ['DATAe', 'MCe'],
		'corrections': ['L1L2L3Res', 'L1L2L3'],
		'algorithms': ['ak4PFJetsCHS'],
		'www': zjetfolder+'_zmass_comparison_datamc_Zee_run2',
		'www_title': 'Comparison Data MC for Zee, run2, '+zjetfolder,
		'www_text':'Run2: Zmass data mc comparisons for work/data15_25ns_ee.root and work/mc15_25ns_ee.root',
		'zjetfolders': [zjetfolder],
		}

	d.update({ "labels": ["DATAe", "MCe", "", "", ""], #default format of labels ["DATA", "MC", "Ratio", "DATA_fit", "MC_fit"]
		"texts": [r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{e e}$"],
	})
	d.update({"texts_x": [0.03],
		"texts_y": [0.70],
		"texts_size": [10],
	})
	plotting_jobs += fit_zmass_profplot_datamc(args, d, channel="e")
	plotting_jobs += zmass_comparison(args, d, channel="e")#usually datamc
	plotting_jobs += general_comparison(args, d, channel="e", only_normalized=False)
	plotting_jobs += profplot_datamc_comparison(args, d, channel="e")
	#plotting_jobs += twodimplot_datamc_comparison(args, d, channel="e")
	d.update({'files': ['work/mc15_25ns_ee.root'],
		'labels': ['MCe'],
		'corrections': ['L1L2L3'],})
	#plotting_jobs += general_mc_comparison(args, d, channel="e")
	plotting_jobs += genzmass_fit(args, d, channel="e")
#	plotting_jobs += profplot_genreco_comparison(args, d, channel="e")
#	plotting_jobs += cutflow(args, d)
	return plotting_jobs

if __name__ == '__main__':
	zmass_comparison_datamc_Zee_run2()
	zmass_comparison_datamc_Zmm_run2()
