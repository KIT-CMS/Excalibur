# -*- coding: utf-8 -*-

from Excalibur.Plotting.utility.toolsZJet import PlottingJob
from Excalibur.Plotting.utility.binningsZJet import rebinning
from Excalibur.Plotting.utility.toolsQCD import error, basic_xsec, generate_datasets, generate_ylims, generate_variationstring,generate_basiccutstring
import Excalibur.Plotting.utility.colors as colors

from copy import deepcopy
import ROOT
import numpy as np
import os
from array import array

DATASETS = generate_datasets(args=None)
#YLIMS = generate_ylims(args=None)
VARIATIONSTRING = generate_variationstring(args=None)
#PLOTSFOLDER = '/ceph/tberger/ZJtriple_2018/ZJtriple'
#PLOTSFOLDER = '/ceph/tberger/ZJtriple/ZJtriple'
PLOTSFOLDER = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple'
MCLIST = ['amc','hpp','mad']#'pow',
LABELDICT = ({'pow':"Powheg",'amc':"aMC@NLO",'hpp':"Herwig++",'mad':"Madgraph",'toy':"Toy MC"})
MARKERDICT = ({'pow':'p','amc':'s','hpp':'D','mad':'o','toy':'d'})
COLORDICT = ({'pow':'orange','amc':'red','hpp':'blue','mad':'green','toy':'grey'})

def plot_mc_comparison_inclusive(args=None, cut='_jet1pt20', data='BCDEFGH', mc='amc', postfix=''):
#def plot_mc_comparison_inclusive(args=None, cut='_jet1pt20', data='BCDEFGH', mc='amc', postfix='_oldSF'):
#def plot_mc_comparison_inclusive(args=None, cut='_jet1pt20', data='BCDEFGH', mc='amc', postfix='_nocuts'):
#def plot_mc_comparison_inclusive(args=None, cut='_jet1pt20', data='BCDEFGH', mc='amc', postfix='_noPUweight'):
    plots=[]
    #cutstring = '1'
    cutstring = generate_basiccutstring(args,cut)
    #weightstring = '1'
    weightstring = '(leptonIDSFWeight)*(leptonIsoSFWeight)*(leptonTriggerSFWeight)'
    samples = [data,'amc','hpp','mad']
    #backgrounds = ['TTJets','WZ','ZZ','WW','TW']
    backgrounds = ['TTJets','WZ','ZZ','TW','WW']
    #for obs in ['zpt','phistareta']:
    #for obs in ['npumean','npv','rho','zpt','zy','phistareta','zmass','mupluspt','muminuspt','muminuseta','mupluseta','jet1pt','jet1y','yboost','ystar']:
    for obs in ['zmass']:
      d = ({
        'corrections': [''],
        'x_expressions': [obs],
        'x_bins': obs,
        'x_log': obs in ['zpt','phistareta'],
        'x_errors': [1],
        'x_label': obs, 
        'y_log': True,
        'y_label': 'Events per binsize',
        'analysis_modules': ['SumOfHistograms','NormalizeByBinWidth','Ratio'],
        'ratio_denominator_no_errors': False,
        'filename': obs,
        'lumis': [35.9],
        'www': 'datamc_comparison_'+data+cut+postfix,
      })
      d1 = deepcopy(d)
      d1.update({
        'files': [DATASETS[x] for x in samples+backgrounds],
        'nicks': [obs+x for x in samples+backgrounds],
        'weights': [cutstring+'*'+weightstring]+(len(samples+backgrounds)-1)*[cutstring],#+'/puWeight'],
        'zjetfolders': ['zjetcuts_L1L2L3Res']+(len(samples+backgrounds)-1)*['zjetcuts_L1L2L3'],
        #'zjetfolders': ['nocuts_L1L2L3Res']+(len(samples+backgrounds)-1)*['nocuts_L1L2L3'],
        'sum_result_nicks': [obs+'signal'],
        'sum_nicks': [obs+'BCDEFGH '+obs+(' '+obs).join(backgrounds)],
        'sum_scale_factors': ['1'+' -1'*len(backgrounds)],
        'ratio_numerator_nicks': [obs+'signal'],
        'ratio_denominator_nicks': [obs+x for x in samples[1:]],
        'ratio_result_nicks': ['ratio'+x for x in samples[1:]],
        'colors': ['black']+[(COLORDICT[x],COLORDICT[x]) for x in samples[1:]],
        'markers': ['.']+[(MARKERDICT[x],MARKERDICT[x]) for x in samples[1:]],
        'step': True,
        'line_styles': ['']+(len(samples)-1)*['-',''],
        'y_subplot_label': '(Data$-$Bkg)/MC',
        'y_subplot_lims': [0.5,3.0],
        'labels': ['Data $-$ Bkg']+[(LABELDICT[x],LABELDICT[x]) for x in samples[1:]],
        'nicks_whitelist': ['signal']+samples[1:],
      })
      d1['www']+='_all_bkgsubtracted'
      d2 = deepcopy(d)
      d2.update({
        'files': [DATASETS[x] for x in [data,mc]+backgrounds],
        'nicks': [obs+x for x in [data,mc]+backgrounds],
        'weights': [cutstring+'*'+weightstring]+(len(backgrounds)+1)*[cutstring],#+'/puWeight'],
        'zjetfolders': ['zjetcuts_L1L2L3Res']+(len(backgrounds)+1)*['zjetcuts_L1L2L3'],
        #'zjetfolders': ['nocuts_L1L2L3Res']+(len(backgrounds)+1)*['nocuts_L1L2L3'],
        'sum_result_nicks': [obs+'sim'],
        'sum_nicks': [obs+mc+' '+obs+(' '+obs).join(backgrounds)],
        #'sum_scale_factors': ['1'+' 0'*len(backgrounds)],
        'stacks': ['data']+(len(backgrounds)+1)*['MC']+['ratio'],
        'ratio_numerator_nicks': [obs+data],
        'ratio_denominator_nicks': [obs+'sim'],
        'ratio_result_nicks': ['ratio'],
        'y_subplot_label': 'Data/Sim',
        'y_subplot_lims': [0.75,1.25],
        'labels': ['Data','DY ('+LABELDICT[mc]+')']+backgrounds+[''],
        'nicks_blacklist': ['sim'],
      })
      d2['www'] += '_'+mc+'_bkgadded'
      plots.append(d1)
      plots.append(d2)
      
    return [PlottingJob(plots=plots, args=args)]


def plot_responses_inclusive(args=None, cut='_jet1pt20', mc='mad', postfix=''):
    plots=[]
    cutstring    = generate_basiccutstring(args,cut)
    gencutstring = generate_basiccutstring(args,'gen'+cut)
    for obs in ['zpt','phistareta','zy','jet1y','yboost','ystar']:
      d = ({
        'corrections': [''],
        'files': [DATASETS[mc]],
        'x_expressions': ['gen'+obs],
        'x_bins': obs,
        'x_log': obs in ['zpt','phistareta'],
        'x_label': 'gen'+obs,
        'y_expressions': [obs],
        'y_bins': obs,
        'y_log': obs in ['zpt','phistareta'],
        'y_label': obs,
        'z_log': True,
        'z_lims': [1e-4,1],
        'analysis_modules': ['NormalizeRowsToUnity'],
        'filename': obs,
        'www': 'responses_'+mc+cut+postfix,
        'nicks': [obs],
        'weights': [cutstring+'*'+gencutstring],
        'zjetfolders': ['zjetcuts_L1L2L3'],
        'colormap': 'summer_r',
        'figsize': [8,6.5],
      })
      if obs == 'zpt':
        d['x_ticks'] = [30,60,100,200,400,1000]
        d['y_ticks'] = [30,60,100,200,400,1000]
      elif obs == 'phistareta':
        d['x_ticks'] = [0.5,1.0,2.0,4.0,10,30]
        d['y_ticks'] = [0.5,1.0,2.0,4.0,10,30]
        d['y_lims']  = [0.4,50]
      plots.append(d)
    return [PlottingJob(plots=plots, args=args)]


def georg_correction(args=None):
    plots=[]
    for (obsx,obsy) in [('(matchedgenjet1y-genzy)/2','(matchedgenjet1y+genzy)/2')]:#,('matchedgenjet1y','genzy'),('genjet1y','genzy')]:
      d = ({
        'files': [DATASETS['mad']],
        'folders': ['genzjetcuts_L1L2L3/ntuple'],
        'x_expressions': [obsx],
        'y_expressions': [obsy],
        #'nicks': [obsx],
        'weights': ['(abs(genmupluseta)<2.4)&&(abs(genmuminuseta)<2.4)&&(genmupluspt>25)&&(genmuminuspt>25)&&(abs(genzmass-91.1876)<20)&&(genjet1pt>20)&&(matchedgenjet1pt<genjet1pt)'],
        'x_bins': ['48,-2.4,2.4'],
        'y_bins': ['48,-2.4,2.4'],
        #'z_log': True,
        #'plot_modules': ['ExportRoot'],
        'www': 'tests',
        'colormap': 'jet',
      })
      plots.append(d)
    return [PlottingJob(plots=plots, args=args)]
    
def plot_something_here(args=None,cut='_jet1pt10'):
    cutstring = generate_basiccutstring(args,cut)
    weightstring = '(leptonIDSFWeight)*(leptonIsoSFWeight)*(leptonTriggerSFWeight)'
    plots = []
    d = ({
        'files': [  #'/storage/8/tberger/excalibur_results/2019-06-17/data16_mm_BCDEFGH_SiMu17Jul2018.root',
                    '/storage/8/tberger/excalibur_results/2019-06-17/data16_mm_BCDEFGH_SiMu07Aug17.root',
                    '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_DYtoLLamcatnlo.root',
                ],
        'folders': ['nocuts_L1L2L3Res/ntuple','nocuts_L1L2L3/ntuple'],
        #'folders': ['zjetcuts_L1L2L3Res/ntuple','zjetcuts_L1L2L3/ntuple'],
        #'weights': ['(abs(zmass-91.1876)<20)'],#,'(abs(zmass-91.1876)<20)/puWeight'],
        'weights': [weightstring,'1'],#+'/puWeight'],
        'x_expressions': ['npumean'],
        'x_bins': 'npumean',
        #'www': 'test_noPU',
        'www': 'test_inclPU',
        'analysis_modules': ['Ratio'],
        'y_log': True,
        'y_subplot_lims': [0.5,1.5],
        'lumis': [35.9],
    })
    plots.append(d)
    return [PlottingJob(plots=plots, args=args)]




