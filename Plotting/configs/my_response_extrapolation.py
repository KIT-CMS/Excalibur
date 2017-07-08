#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files

import time
import argparse
import copy
import jec_factors
import jec_files

def response_extrapolation(args=None, additional_dictionary=None):
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
  labellist.extend([r'$\\mathit{p}_T$ balance',
      'MPF',
      '', '', '', '', '', '', '', '', ''])
  yexpress=['ptbalance', 'ptbalance', 'mpf', 'mpf']
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
    'nicks': ['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc'],
    'colors': ['orange', 'darkred', 'royalblue', 'darkblue', 'darkred', 'darkblue'],
    'markers': ['s', 'o', 's', 'o', 'o', 'o'],
    'marker_fill_styles': ['none', 'none', 'full', 'full', 'none', 'full'],
    'line_styles': [None, None, None, None, None, None, '--', '--', '--', '--', '--', '--', '--'],
    'line_widths': ['1'],
    'tree_draw_options': 'prof',
    'analysis_modules': ['Ratio', 'FunctionPlot'],
    'plot_modules': ['PlotMplZJet', 'PlotExtrapolationText'],
    'extrapolation_text_nicks': ['ptbalance_ratio_fit', 'mpf_ratio_fit'],
    'extrapolation_text_colors': ['darkred', 'darkblue'],
    'functions': ['[0]+[1]*x'],
    'function_fit': ['ptbalance_data', 'ptbalance_mc', 'mpf_data', 'mpf_mc', 'ptbalance_ratio', 'mpf_ratio'],
    'function_parameters': ['1,1'],
    'function_ranges': ['0,0.3'],
    'function_nicknames': ['ptbalance_data_fit', 'ptbalance_mc_fit', 'mpf_data_fit', 'mpf_mc_fit', 'ptbalance_ratio_fit', 'mpf_ratio_fit'],
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

def fit_extrapolation_profplot_datamc(args=None, additional_dictionary=None, only_normalized=False, channel='m'):
	"""Profile Plot of fitted Zmasses in bins of any quantity"""
	plots = []
	bins=[]
	cut_quantities=['zpt','abs(jet1eta)'] #x_quantity on the plot
	fit_quantities=['ptbalance','mpf']
	#cut_binnings=['50 100 200','0 5.191'] # x_bins in plot
	cut_binnings=[	'20 30 40 50 60 85 105 130 175 230 300 400 500 700 1000 1500 2000', 
					'0.001 0.261 0.522 0.783 1.044 1.305 1.479 1.653 1.930 2.172 2.322 2.500 2.650 2.853 2.964 3.139 3.489 3.839 5.191']
					#'0.001 0.087 0.174 0.261 0.348 0.435 0.522 0.609 0.696 0.783 0.879 0.957 1.044 1.131 1.218 1.305 1.392 1.479 1.566 1.653 1.830 1.930 2.043 2.172 2.322 2.500 2.853 2.964 3.139 5.232']
	#cut_binnings=['30 40 50 60 85 105 130 175 275 500','0 0.783 1.305 1.93 2.5 2.964 5.191'] # x_bins in plot  
	for fit_quantity in fit_quantities:
		for cut_index,cut_quantity in enumerate(cut_quantities):
			#cut_quantity=cut_quantities[cut_index]
			cut_binning=cut_binnings[cut_index].split()
			#fit_quantity=fit_quantities[cut_index]
			d = {
				'y_expressions': fit_quantity, #y_expression in the plot
				'x_expressions': 'alpha',
				'x_bins': '6,0,0.3',
				'tree_draw_options': 'prof',
				'cutlabel': True,
				'analysis_modules': ['FunctionPlot', 'HistogramFromFitValues','Ratio'],
				'filename': fit_quantity+'_vs_'+cut_quantity.replace("(", "").replace(")", "")+'_fit_profplot',
				'title': 'Work in Progress',#r'$\\mathrm{M_{Z}}$',
				'legend': 'upper right',
				}
			if additional_dictionary:
				d.update(additional_dictionary)
			if cut_quantity == 'zpt':
				#d.update({'x_ticks' : [30, 50, 70, 100, 200, 400, 1000]})
				d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
			
			copynicks=d['nicks']
			copyfiles=d['files']
			copycorrections=d['corrections']
			copyweights=d['weights']
			weights=[]
			nicks=[]
			files=[]
			labels=[]
			corrections=[]
			fit_hist_nicks=[]
			fit_function_nicks=[]
			x_bins=[]
		
			for dataindex,dataset in enumerate(copynicks):#['Data','MC']:
			#dataset='Data'
				fit_nicks=[]
				x_values=[]
				for index in range(len(cut_binning)-1):
					weights+=['('+copyweights+')&&'+str(cut_binning[index])+'<'+cut_quantity+'&&'+cut_quantity+'<'+str(cut_binning[index+1])] # cut out one bin in each loop
					nicks+=['nick_'+cut_quantity+'_'+str(cut_binning[index])+'_'+str(cut_binning[index+1])+'_'+str(dataset)] #Get nicks for each bin and each file
					fit_nicks+=['nick_'+cut_quantity+'_'+str(cut_binning[index])+'_'+str(cut_binning[index+1])+'_'+str(dataset)+'_fit']
					
					files+=[copyfiles[dataindex]]
					corrections+=[copycorrections[dataindex]]
					labels+=[dataset]
					
					#if dataset=='Data':
					#	files+=[copyfiles[0]] 
					#	labels+=['DATA']
					#elif dataset=='MC':
					#	files+=[copyfiles[1]]
					#	labels+=['MC']
					#corrections+=['L1L2L3']
				fit_function_nicks+=fit_nicks
				fit_hist_nicks+=[" ".join(fit_nicks)]
				x_bins+=[" ".join(map(str,cut_binning))]
			#Now fit the entrys of each bin and each file seperately
			newnicks=['fit_'+dataset+'_values' for dataset in copynicks]
			labels=[]
			for dataset in copynicks[0:-1]:
				labels+=[dataset, dataset+'_ratio']
			labels+=[copynicks[-1]]
			d.update({
				'nicks':nicks,
				'files': files,
				'corrections': corrections,
				"function_fit": nicks,
				"function_nicknames": fit_function_nicks,
				"functions": ['[0]+[1]*x'],
				"function_parameters": ["1.,1."],
				'weights': weights,
				'nicks_whitelist': newnicks,
				'histogram_from_fit_nicks': fit_hist_nicks,
				'histogram_from_fit_newnick': newnicks,
				'histogram_from_fit_x_values': x_bins,
				'y_label': fit_quantity,
				#'x_lims': [min(cut_binning),max(cut_binning)],
				'x_log':  cut_quantity in ['jet1pt', 'zpt'],
				'x_label': cut_quantity,
				'markers': 'd',
				"colors":['red', 'darkred','blue','darkblue','green','darkgreen','orange','darkorange','black'],
				'labels': labels,#copynicks,#['Data','Ratio','MC'],
				'lines': [1.3,1.000],
				'ratio_numerator_nicks': newnicks[0:-1],
				'ratio_denominator_nicks': newnicks[-1],
				})
			plots.append(d)
	return [PlottingJob(plots=plots, args=args)]


def my_extrapolation_datamczptetabins_Zll(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	Res=1 # disable/enable residual corrrections
	if Res==True:
		RES='Res'
	else:
		RES=''
	COM=''
	RUN='BCDEFGH'
	CH='mm'
	RECO='remini'
	MC='madgraph_NJ'
	NICK =['Data'+RUN,MC]
	ETA = [0,1.3,2.5,3.2,5.2]
	ZPT = [20,60]
	ID='_07-07-2017'
	plotting_jobs = []
	d = {
		'files': [	'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/data16_'+RUN+'_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/mc16_'+CH+'_'+MC+'.root'],
		'corrections': ['L1L2L3'+RES, 'L1L2L3'],
		'zjetfolders': 'basiccuts',
		#'algorithms': ['ak4PFJetsPUPPI'],
		'www_title': 'Comparison of Datasets for Zll, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		'output_dir': 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/extrapolation_Z'+CH+COM+'_'+RUN+RECO+'_'+MC+RES,
		#'www': 'extrapolation_Z'+CH+COM+'_'+RUN+RECO+'_'+MC+RES,
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
			d.update({	'filename': 'extrapolation_eta%s'%int(eta1*10)+'-eta%s'%int(eta2*10)+'_zpt%s'%zpt1+'-zpt%s'%zpt2,
						'weights': ['abs(jet1eta)>%s'%eta1+'&&abs(jet1eta)<%s'%eta2+'&&zpt>%s'%zpt1+'&&zpt<%s'%zpt2]})
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
			plotting_jobs += response_extrapolation(args, d)
	return plotting_jobs

def my_comparison_dataallmcalpha0_Zll(args=None):
	"""Run2: full data mc comparisons for data16_25ns_ee.root and work/mc16_25ns_ee.root"""
	Res=0 # disable/enable residual corrections
	if Res==True:
		RES='Res'
	else:
		RES=''
	COM=''
	CH='ee'
	RECO='remini'
	MC='madgraph_NJ'
	NICK =['DataBCD','DataEF','DataG','DataH',MC]
	ID='_07-07-2017'
	EXW=''#
	ZPT= [30]
	ETA= [0.0,1.3]#[3.2,5.2]#[3.2,5.2]#[2.5,5.2]#[4.2,5.2]#
	plotting_jobs = []
	d = {
		'files': [	'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/data16_BCD_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/data16_EF_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/data16_G_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/data16_H_'+CH+'_'+RECO+'.root',
					'/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V3'+ID+'/mc16_'+CH+'_'+MC+'.root'],
		'corrections': ['L1L2L3'+RES,'L1L2L3'+RES,'L1L2L3'+RES,'L1L2L3'+RES, 'L1L2L3'],
		'zjetfolders': 'basiccuts',
		'weights': EXW+'abs(jet1eta)>%s'%ETA[0]+'&&abs(jet1eta)<%s'%ETA[1]+('&&zpt>%s'%ZPT[0]+'&&zpt<%s'%ZPT[1] if len(ZPT)==2 else '&&zpt>%s'%ZPT[0]),
		#'algorithms': ['ak4PFJetsPUPPI'],
		'www_title': 'Comparison of Datasets for Zll, run2',
		'www_text':'Run2: full data/MC comparisons for Run2',
		#'www': 'comparison_Z'+CH+COM+'_all_'+RECO+'_'+MC+'_eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+('zpt_%s'%int(ZPT[0])+'-%s'%int(ZPT[1]) if len(ZPT)==2 else 'zpt_%s'%int(ZPT[0])+'-Inf')+'_alpha_0'+RES,
		'output_dir': 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/comparison_Z'+CH+COM+'_all_'+RECO+'_'+MC+'_eta_%s'%int(ETA[0]*10)+'-%s'%int(ETA[1]*10)+('zpt_%s'%int(ZPT[0])+'-%s'%int(ZPT[1]) if len(ZPT)==2 else 'zpt_%s'%int(ZPT[0])+'-Inf')+'_alpha_0'+RES,
		'labels': NICK,
		'nicks': NICK,
		'y_subplot_label' : "Data/MC",
		'y_subplot_lims' : [0.95,1.05],
		'y_lims': [0.7,1.3],
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
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3Res}$",r"$%s<"%ZPT[0]+r"\\mathrm{p}^Z_T/GeV<%s$"%ZPT[1],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha=0$"]})
			else:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3}$",r"$%s<"%ZPT[0]+r"\\mathrm{p}^Z_T/GeV<%s$"%ZPT[1],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha=0$"]})
		elif CH=='mm':
			if Res==True:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",r"$\\bf{L1L2L3Res}$",r"$%s<"%ZPT[0]+r"\\mathrm{p}^Z_T/GeV<%s$"%ZPT[1],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha=0$"]})
			else:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",r"$\\bf{L1L2L3}$",r"$%s<"%ZPT[0]+r"\\mathrm{p}^Z_T/GeV<%s$"%ZPT[1],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha=0$"]})
	else:
		if CH=='ee':
			if Res==True:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3Res}$",r"$\\mathrm{p}^Z_T/GeV>%s$"%ZPT[0],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha=0$"]})
			else:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} e e}$",r"$\\bf{L1L2L3}$",r"$\\mathrm{p}^Z_T/GeV>%s$"%ZPT[0],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha=0$"]})
		elif CH=='mm':
			if Res==True:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",r"$\\bf{L1L2L3Res}$",r"$\\mathrm{p}^Z_T/GeV>%s$"%ZPT[0],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha=0$"]})
			else:
				d.update({	'texts': [r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$",r"$\\bf{L1L2L3}$",r"$\\mathrm{p}^Z_T/GeV>%s$"%ZPT[0],r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1],r"$\\alpha=0$"]})
	plotting_jobs += fit_extrapolation_profplot_datamc(args, d)
	#d.update({'folders': ['nocuts_L1L2L3', 'nocuts_L1L2L3'+RES]})
	return plotting_jobs

if __name__ == '__main__':
	basic_comparisons()
