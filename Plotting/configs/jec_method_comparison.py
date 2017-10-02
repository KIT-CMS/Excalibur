#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, basiccutlabel, get_lumis

import time
import argparse
import copy
import jec_factors
import jec_files

def response_method_extrapolation_Zll(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	### Choose the channel ('ee' or 'mm'):	
	CH='ee'
	### Choose MC sample:
	MC='madgraph_NJ'
	### Choose data sample:
	RECO='remini'
	RUN= 'H'
	NICK= ['Data'+RUN,MC]
	### Choose JEC version:
	FOLDER='V7'
	### apply additional (extra) weights:
	EXW='1'
	### Cut quantities:
	ZPT= [30]
	ALPHA= [0.0]
	#ETA=[0.0,1.3]
	### Add comments to the output folder:
	COM=''
	plots = []
	RES= 'L1L2L3'
	for ETA in [[0.0,1.3],[2.5,3.5],[3.5,5.2]]:#[[2.5,3.0],[3.0,3.5]]:
	  SDW= 'abs(jet1eta)>%s'%ETA[0]+'&&abs(jet1eta)<%s'%ETA[1]+('&&zpt>%s'%ZPT[0]+'&&zpt<%s'%ZPT[1] if len(ZPT)==2 else '&&zpt>%s'%ZPT[0])
	  cut_quantities=['zpt','abs(jet1eta)','jet1pt'] #x_quantity on the plot
	  cut_binnings=[	'30 40 50 60 85 105 130 175 230 300 400 500 700 1000 1500', #zpt
						'0.001 0.261 0.522 0.783 1.044 1.305 1.479 1.653 1.930 2.172 2.322 2.500 2.650 2.853 2.964 3.139 3.489 3.839 5.191', #jet1eta
						'20 30 40 50 60 85 105 130 175 230 300 400 500 700 1000 1500 2000'] #jet1pt
	  for cut_index,cut_quantity in enumerate(cut_quantities):
		cut_binning=cut_binnings[cut_index].split()
		d =	{
				'files': [	'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_'+FOLDER+'/data16_'+RUN+'_'+CH+'_'+RECO+'.root',
							'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_'+FOLDER+'/mc16_BCDEFGH_'+CH+'_'+MC+'.root',
							'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_'+FOLDER+'/data16_'+RUN+'_'+CH+'_'+RECO+'.root',
							'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_'+FOLDER+'/mc16_BCDEFGH_'+CH+'_'+MC+'.root'],
				'nicks': ['ptdata','ptmc','mpfdata','mpfmc'],
				'corrections': [RES, 'L1L2L3', RES, 'L1L2L3'],
				'zjetfolders': 'basiccuts',
				'weights': [exw+'&&'+SDW for exw in EXW],
				'x_expressions': 'alpha',
				'x_bins': '6,0,0.3',
				'y_expressions': [],
				'y_lims': [0.6,1.3],
				'y_label': "Response",
				#'filename': 'response_'+quantity,
				#'output_dir': 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/comparison_Z'+CH+COM+'_all_'+RECO+'_'+MC+'_eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+('zpt_%s'%int(ZPT[0])+'-%s'%int(ZPT[1]) if len(ZPT)==2 else 'zpt_%s'%int(ZPT[0])+'-Inf')+'_alpha_%s'%int(ALPHA[0]*100)+'_'+RES,
				'www': 'response_comparison_Z'+CH+COM+'_'+RECO+'_'+MC+'_Jec'+FOLDER+'_eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+('zpt_%s'%int(ZPT[0])+'-%s'%int(ZPT[1]) if len(ZPT)==2 else 'zpt_%s'%int(ZPT[0])+'-Inf')+'_alpha_%s'%int(ALPHA[0]*100)+'_'+RES,	
				#'labels': ['ptbal_'+nick for nick in NICK]+['mpf_'+nick for nick in NICK],#['DataBCD('+RECO+')','DataEF('+RECO+')','DataG('+RECO+')','DataH('+RECO+')','MC('+MC+')'],
				'markers': ['d','.','o'],
				'tree_draw_options': 'prof',
				'y_subplot_label' : "Data/MC",
				'y_subplot_lims' : [0.8,1.2] ,#if (RES=='L1L2L3Res' or ETA==[0.0,1.3]) else [0.9,1.0],
				'subplot_fraction': 30,
				'analysis_modules': ['FunctionPlot', 'HistogramFromFitValues','Ratio'],#
				'filename': 'response_vs_'+cut_quantity.replace("(", "").replace(")", "")+'_extrapolated',
				}
		copyfiles=d['files']
		copynicks=d['nicks']
		copycorrections=d['corrections']
		copyweights=d['weights']
		files=[]
		nicks=[]
		corrections=[]
		weights=[]
		#labels=[]
		fit_hist_nicks=[]
		fit_function_nicks=[]
		x_bins=[]
		if cut_quantity == 'zpt':
			d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
		if cut_quantity == 'jet1pt':
			d['x_ticks'] = [20, 30, 50, 70, 100, 200, 400, 1000]
		for dataindex,dataset in enumerate(copynicks):
			fit_nicks=[]
			x_values=[]
			for index in range(len(cut_binning)-1):
				weights+=['('+weight+')&&'+str(cut_binning[index])+'<'+cut_quantity+'&&'+cut_quantity+'<'+str(cut_binning[index+1]) for weight in copyweights] # cut out one bin in each loop
				nicks+=['nick_'+cut_quantity+'_'+str(cut_binning[index])+'_'+str(cut_binning[index+1])+'_'+str(dataset)] #Get nicks for each bin and each file
				fit_nicks+=['nick_'+cut_quantity+'_'+str(cut_binning[index])+'_'+str(cut_binning[index+1])+'_'+str(dataset)+'_fit']			
				files+=[copyfiles[dataindex]]
				corrections+=[copycorrections[dataindex]]
				#labels+=[dataset]
				if dataset in ['ptdata','ptmc']:
					d['y_expressions']+=['ptbalance']
				elif dataset in ['mpfdata','mpfmc']:
					d['y_expressions']+=['mpf']
			fit_function_nicks+=fit_nicks
			fit_hist_nicks+=[" ".join(fit_nicks)]
			x_bins+=[" ".join(map(str,cut_binning))]
			#Now fit the entrys of each bin and each file seperately
			newnicks=['fit_'+dataset+'_values' for dataset in copynicks]
			d.update({
				'files': files,
				'nicks': nicks,
				'corrections': corrections,
				'weights': weights,
				"function_fit": nicks,
				"function_nicknames": fit_function_nicks,
				"functions": ['[0]+[1]*x'],
				"function_parameters": ["1.,1."],
				'nicks_whitelist': newnicks,
				'histogram_from_fit_nicks': fit_hist_nicks,
				'histogram_from_fit_newnick': newnicks,
				'histogram_from_fit_x_values': x_bins,
				'x_log':  cut_quantity in ['jet1pt', 'zpt'],
				'x_label': cut_quantity,
				'x_errors': [1],
				'colors' : ['red','red','darkred','blue','blue','darkblue'],
				'labels': ['ptbal_Data','ptbal_Ratio','ptbal_MC','mpf_Data','mpf_Ratio','mpf_MC'],
				'lines': [1.000],
				'ratio_numerator_nicks': [newnicks[0],newnicks[2]],#:len(newnicks)*1/4]+newnicks[len(newnicks)*2/4:len(newnicks)*3/4],
				'ratio_denominator_nicks': [newnicks[1],newnicks[3]],#:len(newnicks)*2/4]+newnicks[len(newnicks)*3/4:len(newnicks)*4/4],
				})
		print d['y_expressions']
		print d['ratio_numerator_nicks']
		print d['ratio_denominator_nicks']
		basiccutlabel(args,d,CH,ZPT,ALPHA,ETA,RES)
		lumilabel(args,d,RUN,16)
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def response_method_comparison_Zll(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	### Choose the channel ('ee' or 'mm'):	
	CH='mm'
	### Choose MC sample:
	MC='madgraph_NJ'
	### Choose data sample:
	RECO='prompt'#'remini'#
	RUN= 'BCD'
	NICK= ['Data'+RUN,MC]
	### Choose JEC version:
	FOLDER='2017_test'#'Summer16_03Feb2017_V7'#
	JEC= 'V7'
	### apply additional (extra) weights:
	EXW='1'
	### Cut quantities:
	ZPT= [30]
	ALPHA= [0.3]
	#ETA=[0.0,1.3]
	### Add comments to the output folder:
	COM=''
	plots = []
	RES= 'L1L2L3'
	for ETA in [[0.0,1.3],[2.5,3.5],[3.5,5.2],[0.0,5.2]]:
	  for quantity in ['zpt','jet1pt','jet1eta']:
		SDW= 'abs(jet1eta)>%s'%ETA[0]+'&&abs(jet1eta)<%s'%ETA[1]+('&&zpt>%s'%ZPT[0]+'&&zpt<%s'%ZPT[1] if len(ZPT)==2 else '&&zpt>%s'%ZPT[0])+'&&alpha<%s'%ALPHA[0]
		d =	{
			'files': [	'/storage/jbod/tberger/zjets/excalibur_results_datamc_'+FOLDER+'/data17_'+RUN+'_'+CH+'_'+RECO+'.root',
						'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V7/mc16_BCDEFGH_'+CH+'_'+MC+'.root',
						'/storage/jbod/tberger/zjets/excalibur_results_datamc_'+FOLDER+'/data17_'+RUN+'_'+CH+'_'+RECO+'.root',
						'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V7/mc16_BCDEFGH_'+CH+'_'+MC+'.root'],
			'nicks': ['ptdata','ptmc','mpfdata','mpfmc'],
			'corrections': [RES, 'L1L2L3', RES, 'L1L2L3'],
			'zjetfolders': 'basiccuts',
			'weights': [exw+'&&'+SDW for exw in EXW],
			'x_expressions': quantity,
			'x_bins': quantity,
			'y_expressions': ['ptbalance','ptbalance','mpf','mpf'],
			'y_lims': [0.6,1.3],
			'y_label': "Response",
			'filename': 'response_'+quantity,
			#'output_dir': 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/comparison_Z'+CH+COM+'_all_'+RECO+'_'+MC+'_eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+('zpt_%s'%int(ZPT[0])+'-%s'%int(ZPT[1]) if len(ZPT)==2 else 'zpt_%s'%int(ZPT[0])+'-Inf')+'_alpha_%s'%int(ALPHA[0]*100)+'_'+RES,
			'www': 'response_comparison_Z'+CH+COM+'_'+RECO+'_'+MC+'_Jec'+JEC+'_eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+('zpt_%s'%int(ZPT[0])+'-%s'%int(ZPT[1]) if len(ZPT)==2 else 'zpt_%s'%int(ZPT[0])+'-Inf')+'_alpha_%s'%int(ALPHA[0]*100)+'_'+RES,	
			'markers': ['d','o','d','o','.','.'],
			'tree_draw_options': 'prof',
			'y_subplot_label' : "Data/MC",
			'y_subplot_lims' : [0.9,1.1] ,#if (RES=='L1L2L3Res' or ETA==[0.0,1.3]) else [0.9,1.0],
			'subplot_fraction': 30,
			'analysis_modules': ['Ratio'],#
			'x_log':  quantity in ['jet1pt', 'zpt'],
			'x_errors': [1],
			'colors' : ['red','darkred','blue','darkblue','red','blue'],
			'labels': ['pT-Balance Data','pT-Balance MC','MPF Data','MPF MC'],
			'lines': [1.000],
			'ratio_numerator_nicks': ['ptdata','mpfdata'],
			'ratio_denominator_nicks': ['ptmc','mpfmc'],
			'lumis': [17.8],
			}
		if quantity == 'zpt':
			d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			d['x_bins'] = ['30 40 50 60 85 105 130 175 230 300 400 500 700 1000 1500']
		if quantity == 'jet1pt':
			d['x_ticks'] = [20, 30, 50, 70, 100, 200, 400, 1000]
			d['x_bins'] = ['20 30 40 50 60 85 105 130 175 230 300 400 500 700 1000 1500 2000']
		if quantity == 'jet1eta':
			d['x_bins'] = ["0.001 0.261 0.522 0.783 1.044 1.305 1.479 1.653 1.930 2.172 2.322 2.500 2.650 2.853 2.964 3.139 3.489 3.839 5.191"]
		basiccutlabel(args,d,CH,ZPT,ALPHA,ETA,RES)
		lumilabel(args,d,RUN,17)
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

if __name__ == '__main__':
	basic_comparisons()











