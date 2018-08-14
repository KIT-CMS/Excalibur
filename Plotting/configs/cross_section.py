# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
import Excalibur.Plotting.utility.binningsZJet as binningsZJet
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, get_lumis, cutlabel

import argparse
import copy
import math
import os
import ROOT
from array import array
import numpy as np

ticks = ({
    'zpt': [40, 60, 100, 200, 400, 1000],
    'phistareta': [1, 2, 4, 10, 25, 100],
    })

basiccutstring = ({
    '_mupt25':                               '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)',
    '_mupt25_zmass20':                       '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)',
    '_mupt25_zmass20_zpt30':                 '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)*(zpt>30)',
    '_mupt25_zmass20_jetpt30':               '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)*(jet1pt>30)',
    '_mupt25_zmass20_phistareta08':          '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)*(phistareta>0.8)',
    '_mupt25_zmass20_zpt30_jet24':           '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)*(zpt>30)*(abs(jet1y)<2.4)',
    '_mupt25_zmass20_zpt30_jetpt15_jet24':   '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)*(zpt>30)*(abs(jet1y)<2.4)*(jet1pt>15)',
    '_mupt25_zmass20_jetpt30_jet24':         '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)*(jet1pt>30)*(abs(jet1y)<2.4)',
    '_mupt25_zmass20_phistareta08_jet24':    '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)*(phistareta>0.8)*(abs(jet1y)<2.4)',
    'gen_mupt25':                            '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)',
    'gen_mupt25_zmass20':                    '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)',
    'gen_mupt25_zmass20_zpt30':              '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)*(genzpt>30)',
    'gen_mupt25_zmass20_jetpt30':            '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)*(genjet1pt>30)',
    'gen_mupt25_zmass20_phistareta08':       '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)*(genphistareta>0.8)',
    'gen_mupt25_zmass20_zpt30_jet24':        '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)*(genzpt>30)*(abs(genjet1y)<2.4)',
    'gen_mupt25_zmass20_zpt30_jetpt15_jet24':'(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)*(genzpt>30)*(abs(genjet1y)<2.4)*(genjet1pt>15)',
    'gen_mupt25_zmass20_jetpt30_jet24':      '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)*(genjet1pt>30)*(abs(genjet1y)<2.4)',
    'gen_mupt25_zmass20_phistareta08_jet24': '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)*(genphistareta>0.8)*(abs(genjet1y)<2.4)',
    })

datasets = ({
    'BCDEFGH' : '/storage/c/tberger/excalibur_results_xsec/2018-07-30/data16_mm_BCDEFGH_SiMu07Aug17.root',
    'amc' :     '/storage/c/tberger/excalibur_results_xsec/2018-07-30/mc16_mm_BCDEFGH_DYtoLLamcatnlo.root',
    #'amc' :     '/storage/c/tberger/excalibur_results_xsec/2018-07-30/mc16_mm_BCDEFGH_DYtoLLamcatnlo_noPUjetID.root',
    #'hpp' :     
    'TTJets' :  '/storage/c/tberger/excalibur_results_xsec/2018-07-30/mc16_mm_BCDEFGH_TTJetsmadgraph.root',
    'ZZ' :      '/storage/c/tberger/excalibur_results_xsec/2018-07-30/mc16_mm_BCDEFGH_ZZpythia8.root',
    'WZ' :      '/storage/c/tberger/excalibur_results_xsec/2018-07-30/mc16_mm_BCDEFGH_WZpythia8.root',
    'WW' :      '/storage/c/tberger/excalibur_results_xsec/2018-07-30/mc16_mm_BCDEFGH_WWpythia8.root',
    'WJets' :   '/storage/c/tberger/excalibur_results_xsec/2018-07-30/mc16_mm_BCDEFGH_WJetsToLNumadgraph.root',
    'ST':       '/storage/c/tberger/excalibur_results_xsec/2018-07-30/mc16_mm_BCDEFGH_ST.root',
    })

######################################################################################################################################################
# delivers dictionary and sets basic options which are similar to all plots, i.e. a basic dictionary and strings that define the cutflow and weights
def basic_xsec(args=None, obs='zpt', cut='_mupt25_zmass20_zpt30_jet24', data='BCDEFGH', mc='amc', yboostbin=None,ystarbin=None):
    if yboostbin and ystarbin:
        cutstring = basiccutstring[cut]+'*(abs(jet1y+zy)/2>{})*(abs(jet1y+zy)/2<{})*(abs(jet1y-zy)/2>{})*(abs(jet1y-zy)/2<{})'.format(yboostbin[0],yboostbin[1],ystarbin[0],ystarbin[1])
        gencutstring = basiccutstring['gen'+cut]+'*(abs(genjet1y+genzy)/2>{})*(abs(genjet1y+genzy)/2<{})*(abs(genjet1y-genzy)/2>{})*(abs(genjet1y-genzy)/2<{})'.format(yboostbin[0],yboostbin[1],ystarbin[0],ystarbin[1])
        namestring = ('_yboost{}-{}_ystar{}-{}'.format(yboostbin[0],yboostbin[1],ystarbin[0],ystarbin[1])).replace('.','')
    else:
        cutstring = basiccutstring[cut]
        gencutstring = basiccutstring['gen'+cut]
        namestring = ''
    weightstring = '(leptonIDSFWeight)*(leptonIsoSFWeight)*(leptonTrackingSFWeight)*(leptonTriggerSFWeight)'
    d = ({  'corrections': [''],
            'zjetfolders': 'leptoncuts',
            'weights' : [cutstring+'*'+weightstring],
            'x_expressions': obs,
            'x_bins': obs,
            'x_log': obs in ['zpt','phistareta'],
            'x_label': obs,
            'x_errors': [1],
            'y_log': obs not in ['npv','npumean','rho','run','jet1puidraw'],
            'y_label': "Events per binsize",
            'title': namestring,
            'cutlabel': False,
            'filename' : obs,
            'texts_x': [0.03],
            'texts_size': [15],
            'ratio_denominator_no_errors' : False,
            'subplot_fraction': 40,
    })
    #if not data in ['amc','hpp']:
    get_lumis(args, d, data, 2016)
    cutlabel(args,d,cut)
    binningsZJet.rebinning(args,d,obs,yboostbin,ystarbin)
    return [d, cutstring, gencutstring, weightstring, namestring]

def genrecocomparisons(args=None, obs='zpt', cut='_mupt25_zmass20_zpt30_jet24', data='amc', mc='amc', yboostbin=None, ystarbin=None):
    # delivers dictionary to plot distributions in gen level compared to reco level
    # (including a comparison between applied and non-applied efficiency corrections, inofficially called Scale Factors (SF))
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    d.update({
        'files': [  datasets[mc],],
        'zjetfolders': ['leptoncuts_L1L2L3','leptoncuts_L1L2L3','genleptoncuts'],
        'nicks': ['nosf','reco','gen'],
        'x_expressions': [obs,obs,'gen'+obs],
        'y_lims': [1e0,1e5],
        'weights' : [cutstring,cutstring+'*'+weightstring,gencutstring],
        'www': 'comparison_Gen-Reco'+cut+namestring,
        'analysis_modules': ['NormalizeByBinWidth','Ratio'],
        #########################################################################################################
        #'nicks': ['nosfplus','recoplus','genplus','nosfminus','recominus','genminus'],
        #'x_expressions': ['muplus'+obs,'muplus'+obs,'genmuplus'+obs,'muminus'+obs,'muminus'+obs,'genmuminus'+obs],
        #'x_label': 'mu'+obs,
        #'analysis_modules': ['NormalizeByBinWidth','SumOfHistograms','Ratio'],
        #'sum_nicks' : ['nosfplus nosfminus','recoplus recominus','genplus genminus'],
        #'sum_result_nicks' : ['nosf','reco','gen'],
        #'nicks_blacklist': ['plus','minus'],
        #'filename' : 'mu'+obs,
        ##########################################################################################################
        'ratio_numerator_nicks': ['nosf','reco'],
        'ratio_denominator_nicks': ['gen'],
        'subplot_legend': 'upper left',
        'y_subplot_label': 'Ratio',
        'y_subplot_lims': [0.75,1.25],
        'labels': ['Reco(uncorrected)','Reco(corrected)','Gen','Reco(uncorrected)/Gen','Reco(corrected)/Gen'],
        'markers': ['.'],
        'colors': ['purple','red','blue','purple','red'],
    })
    return d

def datamccomparisons(args=None, obs='zpt', cut='_mupt25_zmass20_zpt30_jet24', data='BCDEFGH', mc='amc', yboostbin=None, ystarbin=None):
    # delivers dictionary to plot reco distributions in simulation (signal+background) compared to data
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    d.update({
        'files': [  datasets[data],
                    datasets[mc],
                    datasets['TTJets'],
                    datasets['ZZ'],
                    datasets['WZ'],
                    datasets['WW'],
                    datasets['ST'],
                    datasets['WJets'],
                    ],
        'zjetfolders': ['leptoncuts_L1L2L3Res']+7*['leptoncuts_L1L2L3'],
        'nicks': ['data','DY','TTJets','ZZ','WZ','WW','ST','WJets'],
        'www': 'comparison_Data-MC'+cut+namestring,
        'weights' : [cutstring+'*'+weightstring],
        'analysis_modules': ['SumOfHistograms','NormalizeByBinWidth','Ratio'],
        'sum_nicks' : ['DY TTJets ZZ WZ WW ST WJets'],#
        'sum_result_nicks' : ['sim'],
        'stacks': ['data','MC','MC','MC','MC','MC','MC','MC','ratio'],#
        #'sum_scale_factors' : ["1 0"],
        'ratio_numerator_nicks' : ['sim'],
        'ratio_denominator_nicks' : ['data'],
        'ratio_result_nicks': ['ratio'],
        'nicks_blacklist': ['sim'],
        'y_subplot_lims': [0.5,1.5],
        'y_subplot_label': 'Sim/Data',
        'y_lims': [1e1,1e8],
        'subplot_fraction': 30,
    })
    return d

def responsematrix(args=None, obs='zpt', cut='_mupt25_zmass20_zpt30_jet24', data='amc', mc='amc', yboostbin=None, ystarbin=None):
    # delivers dictionary to write the response matrix as well gen level and reco level distributions (SF applied!) to root file
    # root file can be used as unfolding and plot_matrix input
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    d.update({
        'files': [datasets[mc],],
        'folders': ['allleptoncuts_L1L2L3/ntuple','leptoncuts_L1L2L3/ntuple','genleptoncuts/ntuple'],
        'nicks': ['response','reco'+obs,'gen'+obs],
        'weights' : [cutstring+'*'+gencutstring+'*'+weightstring,cutstring+'*'+weightstring,gencutstring],
        'x_expressions': [obs,obs,'gen'+obs],
        'x_label': 'reco'+obs,
        'y_expressions': ['gen'+obs,None,None],
        'y_bins': obs,
        'y_label': 'gen'+obs,
        'title': 'x',
        'y_log': obs in ['zpt','phistareta'],
        'y_ticks': ticks[obs] if obs in ['zpt','phistareta'] else None,
        'z_lims': [1e0,1e4],
        'z_log': True,
        'filename' : obs+namestring,
        #'nicks_whitelist': ['response'],
        #'www': 'response'+cut,
        'output_dir' : '/storage/c/tberger/plots/responsematrix_'+mc+cut,
        'file_mode': ('RECREATE'),
        'plot_modules': ['ExportRoot'],
    })
    return d

def plot_matrix(args=None, obs='zpt', cut='_mupt25_zmass20_zpt30_jet24', data='amc', mc='amc', yboostbin=None, ystarbin=None):
    # delivers dictionary to plot matrices from root files created either from MC files, toy MC files or unfolding covariance files
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    # specify source file and matrix (TH2D hist) name manually
    matrix_source = '/storage/c/tberger/plots/responsematrix_'+mc+cut+'/'+obs+namestring+'.root'
    matrix_name = 'response'
    d.update({
        'files': [matrix_source],
        'folders': [''],
        'nicks': ['response'],
        'x_expressions': [matrix_name],
        'x_label': 'reco'+obs,
        'y_label': 'gen'+obs,
        'y_log': obs in ['zpt','phistareta'],
        'z_log': True,
        #'z_lims':[-1,1],
        'z_lims':[1e-1,1e5],
        'www': matrix_name+cut+namestring,
        'filename': obs,
        'colormap': 'jet',#'hsv',#'seismic',#'bwr',#
    })
    return d

######################################################################################################################################################
# delivers dictionary to plot unfolding results using response matrix specified by source file
# together with the corresponding reco distribution (and the gen distribution incl. ratio to unfolding if data input is MC)
def unfolding(args=None, obs='zpt', cut='_mupt25_zmass20_zpt30_jet24', data='BCDEFGH', mc='amc', yboostbin=None, ystarbin=None, method='tunfold'):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    # specify source file
    response_source = '/storage/c/tberger/plots/responsematrix_'+mc+cut+'/'+obs+namestring+'.root'
    output_path = '/storage/c/tberger/plots/covariance_'+data+'_by_'+mc+cut
    d.update({
        'files': [  response_source,
                    datasets[data],
                    datasets['TTJets'],
                    datasets['ST'],
                    datasets['ZZ'],
                    datasets['WZ'],
                    datasets['WW'],
                    datasets['WJets'],
                    response_source,
                    response_source,
                    ],
        'folders': ['']+7*['leptoncuts_L1L2L3Res/ntuple']+2*[''],
        'nicks': ['responsematrix','data','TTJets','ST','ZZ','WZ','WW','WJets','reco','gen'],
        'weights' :(['1']
                    +7*[cutstring+'*'+weightstring]
                    +2*['1']
                    ),
        'www': 'comparison_Unfold_'+data+'_by_'+mc+cut+namestring,
        'x_expressions': ['response']+7*[obs]+['reco'+obs]+['gen'+obs],
        'analysis_modules': ['SumOfHistograms','Unfolding','Ratio'],#,'NormalizeByBinWidth'],
        'sum_nicks' : ['data TTJets ST ZZ WZ WW WJets'],
        'sum_scale_factors' : ['1'+6*' -1'],
        'sum_result_nicks' : ['signal'],
        'unfolding': 'signal',
        'unfolding_mc_reco': 'reco',
        'unfolding_mc_gen': 'gen',
        'unfolding_new_nicks': 'unfolded',
        'unfolding_method' : method,
        'unfolding_responsematrix': 'responsematrix',
        'unfolding_regularization': 1e-10,
        'libRooUnfold': os.environ['EXCALIBURPATH']+'/RooUnfold/libRooUnfold.so',
        'ratio_numerator_nicks': ['unfolded'],
        'ratio_denominator_nicks': ['signal'],
        'ratio_result_nicks' : ['ratiotosig'],
        'subplot_legend': 'upper left',
        'subplot_nicks':  ['ratiotosig'],
        'nicks_whitelist': ['unfolded','signal','ratiotosig'],
        'labels': ['Unfolded','Measured','Unfolded/Signal'],
        'y_subplot_label': 'Ratio',
        'y_subplot_lims': [0.7,1.3],
        'y_lims': [1e1,1e8],
        'markers': ['.'],
        'colors': ['black','red','red'],
        'filename' : 'unfolded'+obs,
        'unfold_file' : [output_path+'/covmat_'+obs+namestring+'.root'],
        'write_matrix' : True,
    })
    # need to check if unfold_file directory exists and create it if necessary
    print 'response matrix has been taken from',response_source
    if (d['write_matrix']):
        print 'output will be written to',output_path+'/covmat_'+obs+namestring+'.root'
        if not os.path.exists(output_path):
            os.mkdir('/storage/c/tberger/plots/covariance_'+data+'_by_'+mc+cut)
    if data in ['amc','hpp']:
        d['files']+=[datasets[data]]
        d['nicks']+=['gen'+obs+'true']
        d['weights']+=[gencutstring]
        d['x_expressions']+=['gen'+obs]
        d['ratio_denominator_nicks']+=['gen'+obs+'true']
        d['ratio_result_nicks']+=['ratiototrue']
        d['labels']+=['Gen (->Measured)','Unfolded/Gen']
        d['nicks_whitelist']+=['gen'+obs+'true','ratiototrue']
        d['subplot_nicks']+=['ratiototrue'],
        d['folders'] = ['']+7*['leptoncuts_L1L2L3/ntuple']+2*['']+['genleptoncuts/ntuple']
        d['colors'] = ['black','red','red','blue','blue']
        d['sum_scale_factors'] = ['1'+6*' 0']
    return d

######################################################################################################################################################
# uses previously created dictionaries to plot in a loop
def plotloop(args=None):
    plots = []
    ybins = [0.0,2.5]#0.5,1.0,1.5,2.0,2.5]
    for obs in ['zpt']:#,'zy','jet1pt','jet1y','yboost','ystar']:
     for cut in ['_mupt25_zmass20_zpt30_jet24','_mupt25_zmass20_zpt30_jetpt15_jet24']:
      for yboostbin in zip(ybins[:-1],ybins[1:]):
       for ystarbin in zip(ybins[:-1],ybins[1:]):
        if not yboostbin[0]+ystarbin[0]>2:
            plots.append(genrecocomparisons(args, obs, cut, yboostbin=yboostbin, ystarbin=ystarbin))
            plots.append(datamccomparisons(args, obs, cut, yboostbin=yboostbin, ystarbin=ystarbin))
            plots.append(responsematrix(args, obs, cut, yboostbin=yboostbin, ystarbin=ystarbin))
            plots.append(plot_matrix(args, obs, cut, yboostbin=yboostbin, ystarbin=ystarbin))
            plots.append(unfolding(args, obs, cut, data='amc', yboostbin=yboostbin, ystarbin=ystarbin))
    if plots==[]:
        return
    else:
        return [PlottingJob(plots=plots, args=args)]
