# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files

import argparse
import copy
import math
import os

bins = ({
    #'zpt': ['3,1,401'],#['20 25 30 37 45 55 65 77 90 105 120 137 155 175 195 217 240 265 290 317 345 375 405 435 470'],
    #'zpt': ['0 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100 110 120 130 140 150 160 170 180 190 200 225 250 275 300 350 400'],
    #'zpt': ['0 10 20 30 40 50 60 70 80 90 100 120 140 160 180 200 400'],
    'zpt': ['35 40 45 50 55 60 65 70 75 80 85 90 95 100 110 120 130 140 150 160 170 180 190 200 225 250 275 300 350 400 1000'], #
    'zy': ['80,-3,3'],
    'zmass': ['45,70,115'],
    'mu1pt':['120,10,600'],
    'mu1eta': ['60,-3,3'],
    'mu2pt':['60,10,300'],
    'mu2eta': ['60,-3,3'],
    'phistareta': ['0.1 0.115 0.130 0.145 0.165 0.190 0.220 0.260 0.310 0.35 0.4 0.45 0.50 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 1.0 1.25 1.5 2 3 4 6 12 25 50 100'],
    #'phistareta': ['0.1 0.130 0.165 0.220 0.310 0.4 0.50 0.6 0.7 0.8 0.9 1.0 1.5 2 4 10 25 100'],
    'met':['70,0,350'],
    'ystar':['40,0,5'],
    'yboost':['40,0,5'],
    'jet1pt':['120,0,600'],
    'jet1eta':['60,-3,3'],
    'jet1y':['60,-3,3'],
    'leptonSFWeight':['400,1,1.4'],
    'leptonTriggerSFWeight':['200,1,1.1'],
    'npv':['80,0,80'],
    'npumean':['80,0,80'],
    #'genzpt': ['80,0,400'],#['20 25 30 37 45 55 65 77 90 105 120 137 155 175 195 217 240 265 290 317 345 375 405 435 470'],
    #'genzy': ['80,-3,3'],
    'genzmass': ['45,70,115'],
    #'genmu1pt':['120,0,600'],
    #'genmu1eta': ['80,-3,3'],
    #'genmu2pt':['60,0,300'],
    #'genmu2eta': ['80,-3,3'],
    #'genphistareta': ['50,0,50'],#['0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.115 0.130 0.145 0.165 0.190 0.220 0.26 0.310 0.35 0.4 0.45 0.50 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 1.0 1.25 1.5 2 3 4 6 12 25 50']
    })
ticks = ({
    'zpt': [40, 60, 100, 200, 400, 1000],
    'phistareta': [0.1, 1, 2, 4, 10, 25, 100],
    })
lumi = ({
    'BCD' : [12.6],#13.1?
    'BCDEF' : [19.7],
    'BCDEFG' : [27.2],
    'BCDEFGH': [35.8],
    'EF': [6.7],#7.1?
    'GH':  [16.5],#17.2?
    })

def observables_distributions(args=None):
    plots = []
    for MC in ['amcatnlo','madgraph']:
     for BINSTAR in [[0.0,2.5]]:#[[0.0,0.5],[0.5,1.0],[1.0,1.5],[1.5,2.0],[2.0,2.5]]:#
      for BINBOOST in [[0.0,2.5]]:#[[0.0,0.5],[0.5,1.0],[1.0,1.5],[1.5,2.0],[2.0,2.5]]:#
       for DATA in ['BCDEFGH']:#['BCD','EF','GH']:
        for obs in ['zpt','zmass','phistareta','zy','mu1pt','mu1eta','mu2pt','mu2eta','met','ystar','yboost','jet1pt','jet1eta','jet1y']:
         #for obs in ['npv','npumean']:
         d = ({ 'corrections': '',
                'zjetfolders': 'zcuts',#'leptoncuts',#
                'weights' : ['(leptonSFWeight)*(leptonTriggerSFWeight)*(ystar>%s'%BINSTAR[0]+')*(ystar<%s'%BINSTAR[1]+')*(yboost>%s'%BINBOOST[0]+')*(yboost<%s'%BINBOOST[1]+')'],
                'x_expressions': obs,
                'x_bins': bins[obs],
                'x_log': obs in ['zpt','phistareta'],
                'x_errors': [1],
                'x_ticks': ticks[obs] if obs in ['zpt','phistareta'] else None,
                'y_log': obs not in ['npv','npumean'],
                'y_lims': [1e0,1e8],
                'cutlabel': False,
                'lumis': lumi[DATA],
         })
         d.update({  'files': [ '/storage/c/tberger/excalibur_results_xsec/2018-01-17/data16_mm_'+DATA+'_SiMuLegacy.root',
                                '/storage/c/tberger/excalibur_results_xsec/2018-01-17/mc16_mm_BCDEFGH_DYtoLL'+MC+'.root',
                                '/storage/c/tberger/excalibur_results_xsec/2018-01-17/mc16_bkg.root',
                                ],
                    'nicks': ['data','DY','bkg'],
                    'www': 'observables_distributions_'+DATA+'_background_zpt30_inclSF'+'_ystar%s'%int(BINSTAR[0]*10)+'-%s'%int(BINSTAR[1]*10)+'_yboost%s'%int(BINBOOST[0]*10)+'-%s'%int(BINBOOST[1]*10)+'_'+MC,
                    'analysis_modules': ['SumOfHistograms','NormalizeByBinWidth','Ratio'],#
                    'sum_nicks' : ['DY bkg'],
                    'sum_result_nicks' : ['sim'],
                    'ratio_denominator_nicks' : ['sim'],
                    'ratio_numerator_nicks' : ['data'],
                    'ratio_result_nicks': ['ratio'],
                    'ratio_denominator_no_errors' : False,
                    'nicks_whitelist': ['data','sim','bkg','ratio'],
                    'y_subplot_lims': [0.4,1.6],
                    'y_subplot_label': 'Data/Sim',
                    'texts_x': [0.03,0.03],
                    'texts_y': [0.96,0.90],
                    'texts': [r'$%s$'%BINSTAR[0]+r'$<\\mathrm{y^*}<%s$'%BINSTAR[1], r'$%s$'%BINBOOST[0]+r'$<\\mathrm{y_b}<%s$'%BINBOOST[1]],
                    'texts_size': [15,15],
                    'labels': ['data','DY','bkg'],
                    'subplot_fraction': 30,
                    'colors': ['black','steelblue','orange','black'],
         })
         if obs=='zpt' and ((BINSTAR==[0.0,0.5] and BINBOOST==[2.0,2.5])
                        or (BINSTAR==[0.5,1.0] and BINBOOST==[1.5,2.0]) 
                        or (BINSTAR==[1.5,2.0] and BINBOOST==[0.0,0.5])):
            d.update({'x_bins': ['35 40 45 50 55 60 65 70 75 80 85 90 95 100 110 120 130 140 150 160 170 180 190 200 225 250 275 300 350'],})
         elif obs=='zpt' and BINSTAR==[1.5,2.0] and BINBOOST==[0.5,1.0]:
            d.update({'x_bins': ['35 40 45 50 55 60 65 70 75 80 85 90 95 100 110 120 130 140 150 160 170 180 200 250 350'],})
         elif obs=='zpt' and BINSTAR==[1.0,1.5] and BINBOOST==[1.0,1.5]:
            d.update({'x_bins': ['35 40 45 50 55 60 65 70 75 80 85 90 95 100 110 120 130 140 150 160 170 180 190 200 225 250 300 400'],})
         elif obs=='zpt' and BINSTAR==[2.0,2.5] and BINBOOST==[0.0,0.5]:
            d.update({'x_bins': ['30 40 50 60 70 80 90 100 125 150 200'],})
         if not BINSTAR[0]+BINBOOST[0]>2:
            plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def background_subtraction(args=None):
    plots = []
    for DATA in ['BCDEFGH']:#'amcatnlo','madgraph']:#
        for obs in ['zpt','zmass','phistareta']:#,'zy','mu1pt','mu1eta','mu2pt','mu2eta',]:
            d = ({  
                'files': [  '/storage/c/tberger/excalibur_results_xsec/2018-01-17/data16_mm_'+DATA+'_SiMuLegacy.root',
                            #'/storage/c/tberger/excalibur_results_xsec/2018-01-17/mc16_mm_BCDEFGH_DYtoLL'+DATA+'.root',
                            '/storage/c/tberger/excalibur_results_xsec/2018-01-17/mc16_bkg.root'],
                'nicks': ['data','bkg'],
                'sum_nicks' : ['data bkg'],
                'sum_scale_factors' : ["1 -1"],
                'sum_result_nicks' : [obs],
                'corrections': '',
                'zjetfolders': 'zcuts',#'leptoncuts',#
                'weights' : ['(leptonSFWeight)*(leptonTriggerSFWeight)'],
                'analysis_modules': ['SumOfHistograms'],
                'nicks_whitelist': [obs],
                'x_expressions': obs,
                'x_bins': bins[obs],
                'output_dir': '/storage/c/tberger/excalibur_results_xsec/2018-01-17/',
                'filename': 'signal_'+DATA,
                'lumis': lumi[DATA],
                'y_log': True,
                'y_lims': [1,1e8],
                'plot_modules': ['ExportRoot'],
                'file_mode': 'UPDATE',#'RECREATE',#
            })
            plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def unfold_signal(args=None):
    plots = []
    for ALGO in ['dagostini']:#'inversion','tunfold','binbybin','svd']:#
     for DATA in ['BCDEFGH']:
      for MC in ['madgraph','amcatnlo']:
       for obs in ['zpt']:#,'zmass','phistareta']:#'zy','mu1pt','mu1eta','mu2pt','mu2eta',
        d = ({
            'files' : [ '/storage/c/tberger/excalibur_results_xsec/2018-01-17/mc16_mm_BCDEFGH_DYtoLL'+MC+'.root',
                        '/storage/c/tberger/excalibur_results_xsec/2018-01-17/signal_'+DATA+'.root',
                        '/storage/c/tberger/excalibur_results_xsec/2018-01-17/mc16_mm_BCDEFGH_DYtoLL'+MC+'.root',
                        '/storage/c/tberger/excalibur_results_xsec/2018-01-17/mc16_mm_BCDEFGH_DYtoLL'+MC+'.root'],
            'nicks': ['responsematrix', 'data', 'mc_reco', 'mc_gen'],#
            'folders' : ['allzcuts/ntuple','' ,'zcuts/ntuple','genzcuts/ntuple'],
            'x_expressions': [obs,obs,obs,'gen'+obs],
            'weights' : ['1','1','(leptonSFWeight)*(leptonTriggerSFWeight)','1'],
            'x_bins': bins[obs],
            'y_expressions': ['gen'+obs, None, None, None],# 
            'y_bins': bins[obs],
            'analysis_modules': ['Unfolding'],#,'NormalizeByBinWidth','PrintBinContent'],
            'unfolding': 'data',
            'unfolding_mc_gen': 'mc_gen',
            'unfolding_mc_reco': 'mc_reco',
            'unfolding_new_nicks': obs,
            #'unfold_file' : ['/storage/c/tberger/excalibur_results_xsec/2017-12-11/plots/unfold_file'+DATA+'.root'],
            'unfolding_method' : ALGO,
            'unfolding_iterations' : 4,
            'unfolding_regularization': 0.0001,
            'unfolding_responsematrix': 'responsematrix',
            'libRooUnfold': os.environ['EXCALIBURPATH']+'/../RooUnfold/libRooUnfold.so',
            #'write_matrix' : True,
            'output_dir' : '/storage/c/tberger/excalibur_results_xsec/2018-01-17/',
            'nicks_whitelist': [obs],
            'plot_modules' : ['ExportRoot'],
            'file_mode': 'UPDATE',#'RECREATE',#
            'lumis': lumi[DATA],
            'filename' : 'unfolded_'+DATA+'_by_'+MC+'_'+ALGO,
        })
        plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def unfold_comparison(args=None):
    plots = []
    for ALGO in ['dagostini']:#,'inversion','tunfold','svd','binbybin'
     for DATA in ['BCDEFGH']:
      for MC in ['amcatnlo','madgraph']:
       for obs in ['zpt']:#,'zmass','phistareta']:#,'zy','mu1pt','mu1eta','mu2pt','mu2eta']:
        d = ({
            'files': [  #'/storage/c/tberger/excalibur_results_xsec/2018-01-10/data16_mm_BCDEFGH_SiMuLegacy.root',
                        '/storage/c/tberger/excalibur_results_xsec/2018-01-17/unfolded_'+DATA+'_by_'+MC+'_'+ALGO+'.root',
                        '/storage/c/tberger/excalibur_results_xsec/2018-01-17/signal_'+DATA+'.root',
                        '/storage/c/tberger/excalibur_results_xsec/2018-01-17/mc16_mm_BCDEFGH_DYtoLLmadgraph.root',
                        '/storage/c/tberger/excalibur_results_xsec/2018-01-17/mc16_mm_BCDEFGH_DYtoLLmadgraph.root',
                        '/storage/c/tberger/excalibur_results_xsec/2018-01-17/mc16_mm_BCDEFGH_DYtoLLamcatnlo.root',
                        '/storage/c/tberger/excalibur_results_xsec/2018-01-17/mc16_mm_BCDEFGH_DYtoLLamcatnlo.root',
                        ],
            'folders' : ['','','genzcuts/ntuple','zcuts/ntuple','genzcuts/ntuple','zcuts/ntuple'],
            'nicks': ['unfolded','signal','madgen','madreco','amcgen','amcreco'],
            'labels':['Data (unfolded)','Data (signal)','Madgraph (gen)','Madgraph (reco)','Amc@NLO (gen)','Amc@NLO (reco)'],
            'weights':['1','1','1','(leptonSFWeight)*(leptonTriggerSFWeight)','1','(leptonSFWeight)*(leptonTriggerSFWeight)'],
            'x_expressions': [obs,obs,'gen'+obs,obs,'gen'+obs,obs],
            'x_bins': bins[obs],
            'x_label': obs,
            'x_errors': [1],
            'x_log': obs in ['zpt','phistareta'],
            'x_ticks': ticks[obs] if obs in ['zpt','phistareta'] else None,
            'y_log': True,
            'y_lims': [1e0,1e8],#[0.7,1.7],#
            'analysis_modules': ['NormalizeByBinWidth','Ratio'],
            'ratio_numerator_nicks': ['signal','madgen','madreco','amcgen','amcreco'],#['unfolded','amcgen', 'madgen'],
            'ratio_denominator_nicks': ['unfolded'],#['signal','amcreco','madreco'],
            'ratio_denominator_no_errors' : False,
            'subplot_fraction': 40,
            'y_subplot_label': 'Input/Unf.',
            'y_subplot_lims': [0.6,1.4],
            'filename' : obs+'_comp_signal_'+DATA+'_unfolded_by_'+MC+'_'+ALGO,
            'www': 'comparisons_'+DATA+'_unfolded_by_'+MC,#'frame',#+DATA+'',
            'markers': ['.','.','','','','','.','','','',''],
            'lumis': lumi[DATA],
            'colors': ['black','red','blue','green','orange','purple','red','blue','green','orange','purple'],#'yellow','turquoise','brown'
            'texts_x': [0.03,0.03],
            'texts_y': [0.96,0.90],
            'texts': [DATA+' unfolded by '+MC, ALGO+' algorithm'],
            'texts_size': [10,10],
        })
        if obs == 'zpt':
            d.update({'y_lims': [1e0,1e6],})
        elif obs == 'zmass':
            d.update({'y_lims': [1e3,1e7],})
        plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def ymaps(args=None):
    plots = []
    for DATA in ['BCDEFGH']:
      for obs in [['yboost','ystar'],['jet1y','zy']]:#['abs(yboost)','abs(ystar)'],['abs(zy)','abs(jet1y)']]:#
        d = ({
            'files': ['/storage/c/tberger/excalibur_results_xsec/2017-12-11/data16_mm_'+DATA+'_SiMuLegacy.root'],
            'x_expressions': [obs[0]],
            #'x_bins': ['0 0.5 1.0 1.5 2.0 2.5 3.0'],
            'x_bins': ['12,-3.0,3.0'],
            'y_expressions': [obs[1]],
            #'y_bins': ['0 0.5 1.0 1.5 2.0 2.5 3.0'],
            'y_bins': ['12,-3.0,3.0'],
            'z_log': True,
            'z_lims': [1e3,1e6],
            'folders' : ['leptoncuts/ntuple'],
            'weights' : ['(zpt>40)*(abs(jet1eta)<2.5)*(leptonSFWeight)*(leptonTriggerSFWeight)'],
            'www': 'ymaps_'+DATA,
            'lumis': lumi[DATA],
        })
        plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def unfold_response(args=None):
	plots = []
	for DATA in ['BCDEFGH']:
	 for obs in ['zmass']:#,'zpt','phistareta','zy','mu1pt','mu1eta','mu2pt','mu2eta','phistareta']:
		d = ({	
			'files' : [	'/storage/c/tberger/excalibur_results_xsec/2017-12-11/mc16_mm_'+DATA+'_DYtoLLamcatnlo_1filemissing.root'],
			'nicks': ['responsematrix'],#
			'folders' : ['allleptoncuts/ntuple'],#
			'x_expressions': [obs],#
			'x_bins': bins[obs],
			'x_log': obs in ['zpt','phistareta'],
			'x_ticks': ticks[obs],
			'y_expressions': ['gen'+obs],# 
			'y_bins': bins[obs],
			'y_log': obs in ['zpt','phistareta'],
			'y_ticks': ticks[obs],
			'z_lims': [1,1e7],
			'z_log': True,
			'www': 'unfold_response_'+DATA,
			#'output_dir' : '/storage/jbod/tberger/zjets/excalibur_results_datamc_xsec/plots/',	
			'lumis': lumi[DATA],
			'filename' : obs+'_responsematrix_'+DATA,
		})
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]






