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

def response_comparisons(args2=None, additional_dictionary=None, data_quantities=True):
	"""Response (MPF/pTbal) vs zpt npv abs(jet1eta), with ratio"""
	known_args, args = get_special_parser(args2)

	plots = []
	# TODO put these default binning values somewhere more globally
	for quantity, bins in zip(*get_list_slice([
		['zpt', 'abs(jet1eta)'],# 'abs(jet2eta)'], 'npv',
		['zpt', 'abseta']#,'abseta'] 'npv',
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
				d['y_lims'] = [0.95,1.05]				
			if method == 'ptbalance':
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

	quantity_list= ['zpt','ptbalance','mpf','jet1pt', 'jet1eta', 'jet1phi']#, 'zy', 'zmass', 'zphi', 'jet1area',
			 #'npv', 'npumean', 'rho', 'met', 'metphi', 'rawmet', 'rawmetphi', 'njets',
			 #'jet2pt', 'jet2eta', 'jet2phi', 'alpha', 'genHT', 'jetHT']
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
			'line_styles': ['-'],
			'markers': ['_'],
			'step': True,
		})
		if channel in ("eemm", "mmee"):
			d2['y_label']= 'Electron Events'
		if additional_dictionary:
			d2.update(additional_dictionary)
		plots.append(d2)
	return [PlottingJob(plots=plots, args=args)]

def my_comparison_datamc_Zll(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	Res=0 # disable/enable residual corrrections
	if Res==True:
		RES='Res'
	else:
		RES=''
	PU='CHS'#'PUPPI'
	RUN='BCD'
	CH='mm'
	MC='amc'#'amc'#
	RECO='remini'
	NICK =['Data','MC']
	ID= '_07-07-2017'
	
	plotting_jobs = []
	d = {
		'files': [	'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/data16_'+RUN+'_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/mc16_'+CH+'_'+MC+'.root'],
		'corrections': ['L1L2L3'+RES, 'L1L2L3'],
		'zjetfolders': 'finalcuts',
		'output_dir': 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/comparison_Z'+CH+'_'+RUN+'_'+RECO+'_'+PU+'_'+MC+RES,
		'www_title': 'Comparison of Datasets for Zll, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		'colors': ['red','black'],
#		'www': 'comparison_Z'+CH+'_'+RUN+'_'+RECO+'_'+PU+'_'+MC+RES,
		'labels': NICK,
		'y_subplot_label' : "Data/MC",
		#'y_subplot_lims' : [0.9,1.1],
		'texts_x': [0.34,0.69] if Res == True else [0.34,0.78],
		'texts_y': [0.95,0.09],
		'texts_size': [20,25],
#		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{work\\hspace{0.2}in\\hspace{0.2}progress \\hspace{3.2}}$"
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'plot_modules': ['ExportRoot'],
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
	
	plotting_jobs += basic_comparisons(args, d, data_quantities=True, only_normalized=True, channel=CH)
	plotting_jobs += response_comparisons(args, d, data_quantities=True)
	return plotting_jobs

def my_comparison_dataallmcbins_Zll(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	Res=1 # disable/enable residual corrrections
	if Res==True:
		RES='Res'
	else:
		RES=''
	COM=''#
	CH='mm'
	MC='madgraph_NJ'
	RECO='remini'
	NICK= ['DataBCD','DataEF','DataG','DataH',MC]
	### Choose the ID methods used by the analysis:
	ID='_07-07-2017'#'_validjetIDnone_validelectronIDtight+invalidjets'##'_validjetIDnone_validelectronIDnone'#'_validjetIDloose_validelectronIDtight'
	### apply additional (extra) weights:
	EXW=''#(''+#('(1*('+
		#'(jet1eta>-2.650&&jet1eta<-2.500&&jet1phi>-1.35&&jet1phi<-1.05)||'+
		#'(jet1eta>-2.964&&jet1eta<-2.650&&jet1phi>-1.10&&jet1phi<-0.80)||'+
		#'(jet1eta>-2.964&&jet1eta<-2.650&&jet1phi>-0.25&&jet1phi<0.1)||'+
		#'(jet1eta>-2.964&&jet1eta<-2.650&&jet1phi>-3.14159&&jet1phi<-2.8)||'+
		#'(jet1eta>-2.964&&jet1eta<-2.650&&jet1phi>2.9&&jet1phi<3.14159)||'+
		#'(jet1eta>2.650&&jet1eta<2.964&&jet1phi>-2.0&&jet1phi<-1.6)||'+
		#'(jet1eta>2.650&&jet1eta<3.139&&jet1phi>0&&jet1phi<0.25)))&&')
	ZPT= [20]
	ETA= [0.0,1.3]#[3.2,5.2]#[3.2,5.2]#[2.5,5.2]#[4.2,5.2]#
	ALPHA= [0.3]
	plotting_jobs = []
	d = {
		'files': [	'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/data16_BCD_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/data16_EF_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/data16_G_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/data16_H_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/mc16_'+CH+'_'+MC+'.root'],
		'corrections': ['L1L2L3'+RES, 'L1L2L3'+RES, 'L1L2L3'+RES, 'L1L2L3'+RES, 'L1L2L3'],
		'zjetfolders': 'basiccuts',
		'weights': [EXW+'abs(jet1eta)>%s'%ETA[0]+'&&abs(jet1eta)<%s'%ETA[1]+('&&zpt>%s'%ZPT[0]+'&&zpt<%s'%ZPT[1] if len(ZPT)==2 else '&&zpt>%s'%ZPT[0])+'&&alpha<%s'%ALPHA[0]],
		'colors' : ['red','blue','green','orange','black','darkred','darkblue','darkgreen','darkorange'],
		'www_title': 'Comparison of Datasets for Zll, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		'output_dir': 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/comparison_Z'+CH+COM+'_all_'+RECO+'_'+MC+'_eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+('zpt_%s'%int(ZPT[0])+'-%s'%int(ZPT[1]) if len(ZPT)==2 else 'zpt_%s'%int(ZPT[0])+'-Inf')+'_alpha_%s'%int(ALPHA[0]*100)+RES,
#		'www': 'comparison_Z'+CH+COM+'_all_'+RECO+'_'+MC+'_eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+('zpt_%s'%int(ZPT[0])+'-%s'%int(ZPT[1]) if len(ZPT)==2 else 'zpt_%s'%int(ZPT[0])+'-Inf')+'_alpha_%s'%int(ALPHA[0]*100)+RES,	
		'labels': NICK,#['DataBCD('+RECO+')','DataEF('+RECO+')','DataG('+RECO+')','DataH('+RECO+')','MC('+MC+')'],
		'nicks': NICK,
		#'analysis_modules': None,
		#'marker_fill_styles': [''],
		'y_subplot_label' : "Data/MC",
		'y_subplot_lims' : [0.95,1.05],
		'ratio_numerator_nicks': [NICK[0:-1]],
		'ratio_denominator_nicks': [NICK[-1]],
		'texts_x': [0.34,0.69,0.03,0.03,0.03] if Res == True else [0.34,0.78,0.05,0.05,0.05],
		'texts_y': [0.95,0.09,0.83,0.90,0.97],
		'texts_size': [20,25,15,15,15],		
#		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{work\\hspace{0.2}in\\hspace{0.2}progress \\hspace{3.2}}$"
		'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
#		'formats': ['pdf'],
	}
	if len(ZPT)==2:
		if CH=='ee':
			if Res==True:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3Res}$",r"$%s<"%ZPT[0]+r"\\mathrm{p}^Z_T/GeV<%s$"%ZPT[1],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha<%s$"%ALPHA[0]]})
			else:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3}$",r"$%s<"%ZPT[0]+r"\\mathrm{p}^Z_T/GeV<%s$"%ZPT[1],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha<%s$"%ALPHA[0]]})
		elif CH=='mm':
			if Res==True:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",r"$\\bf{L1L2L3Res}$",r"$%s<"%ZPT[0]+r"\\mathrm{p}^Z_T/GeV<%s$"%ZPT[1],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha<%s$"%ALPHA[0]]})
			else:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",r"$\\bf{L1L2L3}$",r"$%s<"%ZPT[0]+r"\\mathrm{p}^Z_T/GeV<%s$"%ZPT[1],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha<%s$"%ALPHA[0]]})
	else:
		if CH=='ee':
			if Res==True:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3Res}$",r"$\\mathrm{p}^Z_T/GeV>%s$"%ZPT[0],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha<%s$"%ALPHA[0]]})
			else:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3}$",r"$\\mathrm{p}^Z_T/GeV>%s$"%ZPT[0],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha<%s$"%ALPHA[0]]})
		elif CH=='mm':
			if Res==True:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",r"$\\bf{L1L2L3Res}$",r"$\\mathrm{p}^Z_T/GeV>%s$"%ZPT[0],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha<%s$"%ALPHA[0]]})
			else:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",r"$\\bf{L1L2L3}$",r"$\\mathrm{p}^Z_T/GeV>%s$"%ZPT[0],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha<%s$"%ALPHA[0]]})
	plotting_jobs += response_comparisons(args, d)# data_quantities)
	plotting_jobs += basic_comparisons(args, d, only_normalized=True, channel=CH)
	#plotting_jobs += cutflow(args, d)
	return plotting_jobs

if __name__ == '__main__':
	basic_comparisons()
