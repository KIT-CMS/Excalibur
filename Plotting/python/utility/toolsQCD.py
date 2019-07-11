# -*- coding: utf-8 -*-

import logging
from collections import namedtuple
import Artus.Utility.logger as logger

log = logging.getLogger(__name__)

import os
import sys
import inspect
import argparse
import pkgutil
import math
import numpy as np
import ROOT
import copy

import Artus.Utility.jsonTools as jsonTools
import Artus.HarryPlotter.utility.roottools as roottools
import Artus.Utility.tools as tools

import Excalibur.Plotting.utility.colors as colors
import Excalibur.Plotting.utility.binningsZJet as binningsZJet
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, get_lumis, cutlabel
from Excalibur.Plotting.utility.binningsZJet import rebinning
from array import array

def error(a,b,c):
    # gives the root of the squared sum of a,b,c
    return np.sqrt(a**2+b**2+c**2)

def generate_variationstring(args=None):
    variationstring=({1:'Up',0: '',-1:'Down'})
    return variationstring

def generate_ylims(args=None):
    ylims = ({
        'phistareta':[1e1 ,1e11],
        'zpt'       :[1e-2,1e8 ],
        'zmass'     :[1e4 ,1e7 ],
        'zy'        :[1e3 ,1e8 ],
        'mupluspt'  :[1e-2,1e7 ],
        'muminuspt' :[1e-2,1e7 ],
        'zl1pt'     :[1e-2,1e7 ],
        'zl2pt'     :[1e-2,1e7 ],
        'mupluseta' :[1e3 ,1e8 ],
        'muminuseta':[1e3 ,1e8 ],
        'zl1eta'    :[1e3 ,1e8 ],
        'zl2eta'    :[1e3 ,1e8 ],
        'muplusphi' :[1e3 ,1e8 ],
        'muminusphi':[1e3 ,1e8 ],
        'jet1pt'    :[1e0 ,1e8 ],
        'jet1y'     :[1e3 ,1e8 ],
        'yboost'    :[1e2 ,1e9 ],
        'ystar'     :[1e2 ,1e9 ],
        'npv'       :[0   ,8e5 ],
        'rho'       :[0   ,8e5 ],
        'npumean'   :[0   ,8e5 ],
        'deltaphizjet1': [1e2,1e7],
    })
    return ylims

def generate_basiccutstring(args=None, cut='_jet1pt20'):
    basicrecocutstring='(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)'
    basicgencutstring='(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)'
    cut=cut.split('_')
    if 'gen' in cut:
        basiccutstring = basicgencutstring
    else:
        basiccutstring = basicrecocutstring
    if 'jet1pt10' in cut:
        basiccutstring+='*('+cut[0]+'jet1pt>10)'
    if 'jet1pt15' in cut:
        basiccutstring+='*('+cut[0]+'jet1pt>15)'
    if 'jet1pt20' in cut:
        basiccutstring+='*('+cut[0]+'jet1pt>20)'
    if 'jet1pt30' in cut:
        basiccutstring+='*('+cut[0]+'jet1pt>30)'
    if 'zpt30' in cut:
        basiccutstring+='*('+cut[0]+'zpt>30)'
    if 'phistareta04' in cut:
        basiccutstring+='*('+cut[0]+'phistareta>0.4)'
    if 'backtoback' in cut:
        basiccutstring+='*(abs(abs('+cut[0]+'zphi-'+cut[0]+'jet1phi)-3.14159)<1.57)'
    if 'alpha05' in cut:
        basiccutstring+='*('+cut[0]+'jet2pt/'+cut[0]+'zpt<0.5)'
    return basiccutstring

def generate_cutlabel(args=None, cut='_jet1pt20'):
    cutlabel=[]
    cut=cut.split('_')
    if 'jet1pt10' in cut:
        cutlabel.append(r'$\\mathrm{p^{jet1}_T}>10\\mathrm{GeV}$')
    if 'jet1pt15' in cut:
        cutlabel.append(r'$\\mathrm{p^{jet1}_T}>15\\mathrm{GeV}$')
    if 'jet1pt20' in cut:
        cutlabel.append(r'$\\mathrm{p^{jet1}_T}>20\\mathrm{GeV}$')
    if 'jet1pt30' in cut:
        cutlabel.append(r'$\\mathrm{p^{jet1}_T}>30\\mathrm{GeV}$')
    if 'zpt30' in cut:
        cutlabel.append(r'$\\mathrm{p^{Z}_T}>30\\mathrm{GeV}$')
    if 'phistareta04' in cut:
        cutlabel.append(r'$\\mathrm{\\Phi^*_\\eta}>0.4$')
    if 'backtoback' in cut:
        cutlabel.append(r'$\\mathrm{\\Delta\\Phi(Z,jet1)}>\\pi$')
    if 'alpha05' in cut:
        cutlabel.append(r"$\\alpha<0.5$")
    return cutlabel
   
    

def generate_datasets(args=None):
    datasets = ({
        #'BCDEFGH' : '/storage/8/tberger/excalibur_results/2019-05-20/data16_mm_BCDEFGH_SiMu07Aug17_oldTriggerSF.root',
        'BCDEFGH'   : '/storage/8/tberger/excalibur_results/2019-06-17/data16_mm_BCDEFGH_SiMu07Aug17.root',
        '17Jul2018' : '/storage/8/tberger/excalibur_results/2019-06-17/data16_mm_BCDEFGH_SiMu17Jul2018.root',
        #'BCDEFGH' : '/storage/8/tberger/excalibur_results/2019-06-17/data16_mm_BCDEFGH_SiMu07Aug17_bare.root',
        #'BCDEFGH' : '/storage/8/tberger/excalibur_results/2019-06-17/data16_mm_BCDEFGH_SiMu07Aug17_oldSF.root',
        #'BCDEFGH' : '/storage/8/tberger/excalibur_results/2019-06-17/data16_mm_BCDEFGH_SiMu07Aug17_oldSFrelative.root',
        #'GH':       '/storage/8/tberger/excalibur_work/excalibur/data16_mm_GH_SiMu07Aug17_2019-05-31_10-49/out.root',
        'amc' :     '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_DYtoLLamcatnlo.root',
        'hpp' :     '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_DYtoLLherwigpp.root',
        'mad' :     '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_DYtoLLmadgraph.root',
        #'amc' :     '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_DYtoLLamcatnlo_bare.root',
        #'hpp' :     '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_DYtoLLherwigpp_bare.root',
        #'mad' :     '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_DYtoLLmadgraph_bare.root',
        #'pow' :     '/storage/8/tberger/excalibur_results/2019-06-13/mc16_mm_BCDEFGH_ZtoMMpowheg.root',
        #'ptz' :     '/storage/8/tberger/excalibur_results/2019-06-13/mc16_mm_BCDEFGH_DYtoLLamcatnlo_Pt0ToInf.root',
        'TTJets' :  '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_TTJetsmadgraph.root',
        'ZZ' :      '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_ZZpythia8.root',
        'WZ' :      '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_WZJToLLLNu.root',
        'WW' :      '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_WWTo2L2Nupowheg.root',
        'TW':       '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_TW.root',
    })
    return datasets

def basic_xsec(args=None, obs='zpt', cut='_jet1pt20', data='BCDEFGH', mc='amc', yboostbin=None,ystarbin=None, jet1match=False):
# delivers dictionary and sets basic options which are similar to all plots, i.e. a basic dictionary and strings that define the cutflow and weights
    ylims           = generate_ylims(args)
    match = '' if not jet1match else 'matched'
    if yboostbin and ystarbin:
        cutstring = generate_basiccutstring(args,cut)+'*(abs(jet1y+zy)/2>{})*(abs(jet1y+zy)/2<{})*(abs(jet1y-zy)/2>{})*(abs(jet1y-zy)/2<{})'.format(yboostbin[0],yboostbin[1],ystarbin[0],ystarbin[1])
        gencutstring = (generate_basiccutstring(args,'gen'+cut).replace('genjet',match+'genjet')
        #(basiccutstring['gen'+cut].replace('genjet',match+'genjet')
                        +('*(abs('+match+'genjet1y+genzy)/2>{})*(abs('
                                  +match+'genjet1y+genzy)/2<{})*(abs('
                                  +match+'genjet1y-genzy)/2>{})*(abs('
                                  +match+'genjet1y-genzy)/2<{})').format(yboostbin[0],yboostbin[1],ystarbin[0],ystarbin[1]))
        namestring = ((match+'_yboost_{}-{}'+match+'_ystar_{}-{}').format(yboostbin[0],yboostbin[1],ystarbin[0],ystarbin[1])).replace('.','')
    else:
        cutstring = generate_basiccutstring(args,cut)
        gencutstring = generate_basiccutstring(args,'gen'+cut).replace('genjet',match+'genjet')
        #basiccutstring['gen'+cut].replace('genjet',match+'genjet')
        namestring = ''
    weightstring = '(leptonIDSFWeight)*(leptonIsoSFWeight)*(leptonTriggerSFWeight)'#*(leptonTrackingSFWeight)'
    d = ({  'corrections': [''],
            'zjetfolders': 'leptoncuts',
            'weights' : [cutstring+'*'+weightstring],
            'x_expressions': obs,
            'x_bins': obs,
            'x_log': obs in ['zpt','phistareta'],
            'x_label': obs,
            'x_errors': [1],
            'y_log': obs not in ['npv','npu','npumean','rho','run','jet1puidraw'],
            'y_label': "Events per binsize",
            'y_lims': ylims[obs],
            'y_subplot_lims': [0.75,1.25],
            #'title': namestring,
            'cutlabel': False,
            'filename' : obs,
            'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{6.2}}$",
            'texts': [],
            'texts_x': [0.03],
            #'texts_y': [0.98,0.89,0.81],
            'texts_size': [15],
            'ratio_denominator_no_errors' : False,
            'subplot_fraction': 35,
            'lumis' : [35.9],
    })
    if not data in ['amc','hpp','mad','toy']:
        get_lumis(args, d, data, 2016)
        d['title'] = r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{4.2}}$ 35.9 fb$^{-1}$ (13 TeV)"
    cutlabel(args,d,cut)
    if yboostbin and ystarbin:
        d['texts']+=[r'${}<y_b<{}$, ${}<y^*<{}$'.format(yboostbin[0],yboostbin[1],ystarbin[0],ystarbin[1])]
    d['texts_y']=[0.98,0.89,0.81,0.71][0:len(d['texts'])]
    binningsZJet.rebinning(args,d,obs,yboostbin,ystarbin)
    return [d, cutstring, gencutstring, weightstring, namestring]

    
    
    
    
    
