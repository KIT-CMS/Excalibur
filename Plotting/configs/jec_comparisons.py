#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, basiccutlabel, get_lumis, generate_dict, get_list_slice, get_special_parser

import time
import argparse
import copy
import jec_factors
import jec_files

def response_comparisons(args2=None, additional_dictionary=None, data_quantities=True):
	"""Comparison of Response vs. quantities as profile plot"""
	known_args, args = get_special_parser(args2)

	plots = []
	# TODO put these default binning values somewhere more globally
	for quantity, bins in zip(*get_list_slice([
		['zpt', 'abs(jet1eta)','jet1pt','npv','run'],# 'abs(jet2eta)']
		['zpt', 'abseta','jet1pt','npv','run']#,'abseta'] 
	], known_args.no_quantities)):
		for method in get_list_slice([['ptbalance', 'mpf'] + (['trueresponse'] if not data_quantities else [])], known_args.no_methods)[0]:
			d = {
				'y_expressions': [method],
				'x_expressions': [quantity],
				'x_bins': bins,
				'y_lims': [0.6, 1.2],
				'x_errors': [1],
				'tree_draw_options': 'prof',
				'markers': ['o', 's',' d'],
				'cutlabel': True,
				'lines': [1.0],
				'analysis_modules': ['Ratio'],
				'ratio_denominator_no_errors': False,
				'filename': method + "_" + quantity.replace("(", "").replace(")", ""),
				'y_subplot_lims': [0.9, 1.1],
				'legend': 'upper right',#'lower left',
			}
#########################################################
			if method == 'mpf':
				d['y_lims'] = [0.8,1.2]				
			if method == 'ptbalance':
				d['y_lims'] = [0.6,1.2]
#########################################################
			if quantity == 'abs(jet1eta)' or quantity == 'abs(jet2eta)':
				d['zjetfolders'] = ["noetacuts"]
				d['x_bins'] = ["0.001 0.261 0.522 0.783 1.044 1.305 1.479 1.653 1.930 2.172 2.322 2.500 2.650 2.853 2.964 3.139 3.489 3.839 5.191"]
			if quantity == 'zpt' or quantity == 'jet1pt':
				d['x_log'] = True
				d['x_bins'] = ["30 40 50 60 85 105 130 175 230 300 400 500 700 1000 1500 2000"]
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			if quantity == 'npv':
				d['x_bins']=["1 5 10 12 15 20 25 30 50"]
			if quantity == 'run':
				d['x_bins']=['40,297000,304000']
			if method == 'trueresponse':
				d['filename'] = "true_response__vs__" + quantity
				d['weights'] = "matchedgenjet1pt>0"
			if additional_dictionary != None:
				d.update(additional_dictionary)
			plots.append(d)
	return [PlottingJob(plots=plots, args=args)]


def basic_comparisons(args=None, additional_dictionary=None, data_quantities=True, only_normalized=False, channel="mm"):
	"""Comparison of distributions of quantities"""
	plots = []
	x_dict=generate_dict(args=args)
	x_dict_zl={
		'%s1phi': ['20,-3.1415,3.1415',],
		'%s1pt': ['20,0,150'],
		'%s2pt': ['20,0,150'],
		'%sminuspt': ['20,0,150'],
		'%spluspt': ['20,0,150'],
	}

	quantity_list= ['zpt','zmass','ptbalance','mpf','jet1pt', 'jet1eta', 'jet1phi','npv','npumean','met']#, 'zy',  'zphi', 'jet1area',
			 #, 'rho', 'metphi', 'rawmet', 'rawmetphi', 'njets',
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
			'y_subplot_lims': [0.6, 1.4],
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

def comparison_data16allmcbins_Zll(args=None):
	RES=''
	COM=''#
	CH='mm'
	MC='madgraph_NJ'
	RECO='remini'
	NICK= ['DataBCD','DataEF','DataG','DataH','MC']	
	FOLDER='Summer16_03Feb2017_V7'#
	### apply additional (extra) weights:
	EXW=['1']
	ZPT= [30]
	ETA= [0.0,5.2]#[3.2,5.2]#[3.2,5.2]#[2.5,5.2]#[4.2,5.2]#
	ALPHA= [0.3]
	SDW='abs(jet1eta)>%s'%ETA[0]+'&&abs(jet1eta)<%s'%ETA[1]+('&&zpt>%s'%ZPT[0]+'&&zpt<%s'%ZPT[1] if len(ZPT)==2 else '&&zpt>%s'%ZPT[0])+'&&alpha<%s'%ALPHA[0]
	plotting_jobs = []
	d = {
		'files': [	'/storage/jbod/tberger/zjets/excalibur_results_datamc_'+FOLDER+'/data16_BCD_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_'+FOLDER+'/data16_EF_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_'+FOLDER+'/data16_G_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_'+FOLDER+'/data16_H_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_'+FOLDER+'/mc16_BCDEFGH_'+CH+'_'+MC+'.root'],
		'corrections': [RES, RES, RES, RES]+ [RES if not RES=='L1L2L3Res' else 'L1L2L3'],
		'zjetfolders': 'basiccuts',
		'weights': [exw+'&&'+SDW for exw in EXW],
		'colors' : ['red','blue','green','orange','black','darkred','darkblue','darkgreen','darkorange'],
		'www_title': 'Comparison of Datasets for Zll, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		#'output_dir': 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/comparison_Z'+CH+COM+'_all_'+RECO+'_'+MC+'_eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+('zpt_%s'%int(ZPT[0])+'-%s'%int(ZPT[1]) if len(ZPT)==2 else 'zpt_%s'%int(ZPT[0])+'-Inf')+'_alpha_%s'%int(ALPHA[0]*100)+RES,
		'www': 'comparison_Z'+CH+COM+'_all_'+RECO+'_'+MC+'_'+RES+'_eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+('zpt_%s'%int(ZPT[0])+'-%s'%int(ZPT[1]) if len(ZPT)==2 else 'zpt_%s'%int(ZPT[0])+'-Inf')+'_alpha_%s'%int(ALPHA[0]*100),	
		'labels': NICK,
		'nicks': NICK,
		#'analysis_modules': None,
		'y_subplot_label' : "Data/MC",
		#'y_subplot_lims' : [0.7,1.3],
		'ratio_numerator_nicks': [NICK[0:-1]],
		'ratio_denominator_nicks': [NICK[-1]],
#		'formats': ['pdf'],
	}
	basiccutlabel(args,d,CH,ZPT,ALPHA,ETA,RES)
	plotting_jobs += response_comparisons(args, d)
	plotting_jobs += basic_comparisons(args, d, only_normalized=True, channel=CH)
	return plotting_jobs

def comparison_data17allmcbins_Zll(args=None):
	RES=''
	COM=''#
	CH='mm'
	MC='madgraph_NJ'
	RECO='prompt'
	NICK= ['DataB','DataC','DataD','MC']	
	FOLDER='2017_test'#
	### apply additional (extra) weights:
	EXW=['run>=297020&&run<=299329','run>=299337&&run<=302029','run>=302030&&run<=303434','1']
	ZPT= [30]
	ETA= [0.0,5.2]#[3.2,5.2]#[3.2,5.2]#[2.5,5.2]#[4.2,5.2]#
	ALPHA= [0.3]
	SDW='abs(jet1eta)>%s'%ETA[0]+'&&abs(jet1eta)<%s'%ETA[1]+('&&zpt>%s'%ZPT[0]+'&&zpt<%s'%ZPT[1] if len(ZPT)==2 else '&&zpt>%s'%ZPT[0])+'&&alpha<%s'%ALPHA[0]
	plotting_jobs = []
	d = {
		'files': [	'/storage/jbod/tberger/zjets/excalibur_results_datamc_'+FOLDER+'/data17_BCD_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_'+FOLDER+'/data17_BCD_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_'+FOLDER+'/data17_BCD_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_'+FOLDER+'/mc16_BCDEFGH_'+CH+'_'+MC+'.root'],
		'corrections': [RES, RES, RES]+ [RES if not RES=='L1L2L3Res' else 'L1L2L3'],
		'zjetfolders': 'basiccuts',
		'weights': [exw+'&&'+SDW for exw in EXW],
		'colors' : ['red','blue','green','black','darkred','darkblue','darkgreen'],
		'www_title': 'Comparison of Datasets for Zll, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		#'output_dir': 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/comparison_Z'+CH+COM+'_all_'+RECO+'_'+MC+'_eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+('zpt_%s'%int(ZPT[0])+'-%s'%int(ZPT[1]) if len(ZPT)==2 else 'zpt_%s'%int(ZPT[0])+'-Inf')+'_alpha_%s'%int(ALPHA[0]*100)+RES,
		'www': 'comparison_Z'+CH+COM+'_all_'+RECO+'_'+MC+'_'+RES+'_eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+('zpt_%s'%int(ZPT[0])+'-%s'%int(ZPT[1]) if len(ZPT)==2 else 'zpt_%s'%int(ZPT[0])+'-Inf')+'_alpha_%s'%int(ALPHA[0]*100),	
		'labels': NICK,
		'nicks': NICK,
		#'analysis_modules': None,
		'y_subplot_label' : "Data/MC",
		#'y_subplot_lims' : [0.7,1.3],
		'ratio_numerator_nicks': [NICK[0:-1]],
		'ratio_denominator_nicks': [NICK[-1]],
#		'formats': ['pdf'],
	}
	basiccutlabel(args,d,CH,ZPT,ALPHA,ETA,RES)
	plotting_jobs += response_comparisons(args, d)
	plotting_jobs += basic_comparisons(args, d, only_normalized=True, channel=CH)
	return plotting_jobs

if __name__ == '__main__':
	basic_comparisons()
