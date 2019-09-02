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
#PLOTSFOLDER = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple'
MCLIST = ['amc','hpp','mad']#'pow',
#LABELDICT = ({'pow':"Powheg",'amc':"aMC@NLO",'hpp':"Herwig++",'mad':"Madgraph",'toy':"Toy MC"})
LABELDICT = ({'pow':'"Powheg"','amc':'"P8+aMC"','hpp':'"HW+MG"','mad':'"P8+MG"','toy':'Toy'})
MARKERDICT = ({'pow':'p','amc':'s','hpp':'D','mad':'o','toy':'d'})
COLORDICT = ({'pow':'orange','amc':'red','hpp':'blue','mad':'green','toy':'grey'})

def plot_mc_comparison_inclusive(args=None, cut='_jet1pt20', data='17Jul2018', mc='mad', postfix=''):
#def plot_mc_comparison_inclusive(args=None, cut='_jet1pt20', data='17Jul2018', mc='mad', postfix='_noPURW'):
    plots=[]
    #cutstring = '1'
    cutstring = generate_basiccutstring(args,cut)
    #weightstring = '1'
    weightstring = '(leptonIDSFWeight)*(leptonIsoSFWeight)*(leptonTriggerSFWeight)'#/6225.42*4963.0'
    samples = [data,'mad','amc','hpp']
    #backgrounds = ['TTJets','WZ','ZZ','WW','TW']
    backgrounds = ['TTJets','WZ','ZZ','TW','WW']
    #for obs in ['zpt','phistareta']:
    for obs in ['zl1pt','zl2pt','zl1eta','zl2eta','npumean','npv','rho','zpt','phistareta','zy','zmass','mupluspt','muminuspt','muminuseta','mupluseta','jet1pt','jet1y','yboost','ystar']:
      d = ({
        'corrections': [''],
        'x_expressions': [obs],
        'x_bins': obs,
        'x_log': obs in ['zpt','phistareta'],
        'x_errors': [1],
        'x_label': obs, 
        'y_log': True,
        'y_label': 'Events per binwidth',
        #'analysis_modules': ['SumOfHistograms','NormalizeByBinWidth','Ratio'],
        'analysis_modules': ['SumOfHistograms','NormalizeByBinWidth','NormalizeHistogram','Ratio'],
        'normalization_base_histo': obs+'signal',
        'histograms_to_normalize': obs+'hpp',
        'ratio_denominator_no_errors': False,
        'filename': obs,
        'lumis': [35.9],
        #'no_energy_label': True,
        #'figsize': [12,8],
        #'legend_cols': 8,
        #'y_lims': [1e5,1e10],
        'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary} \\hspace{6.5}.$",
        'www': 'datamc_comparison_'+data+cut+postfix,
      })
      d1 = deepcopy(d)
      d1.update({
        'files': [DATASETS[x] for x in samples+backgrounds],
        'nicks': [obs+x for x in samples+backgrounds],
        'weights': [cutstring+'*'+weightstring]+[cutstring+'*6225.42/4963.0']+(len(samples+backgrounds)-2)*[cutstring],
        'zjetfolders': ['zjetcuts_L1L2L3Res']+(len(samples+backgrounds)-1)*['zjetcuts_L1L2L3'],
        'sum_result_nicks': [obs+'signal'],
        'sum_nicks': [obs+data+' '+obs+(' '+obs).join(backgrounds)],
        'sum_scale_factors': ['1'+' -1'*len(backgrounds)],
        'ratio_numerator_nicks': [obs+'signal'],
        'ratio_denominator_nicks': [obs+x for x in samples[1:]],
        'ratio_result_nicks': ['ratio'+x for x in samples[1:]],
        'colors': ['black']+[(COLORDICT[x],COLORDICT[x]) for x in samples[1:]],
        'markers': ['.']+[(MARKERDICT[x],MARKERDICT[x]) for x in samples[1:]],
        'step': True,
        'line_styles': ['']+(len(samples)-1)*['-',''],
        'y_subplot_label': '(Data$-$Bkg)/MC',
        'y_subplot_lims': [0.75,1.25],
        'labels': ['Data $-$ Bkg']+[(LABELDICT[x],LABELDICT[x]) for x in samples[1:]],
        'nicks_whitelist': ['signal']+samples[1:],
      })
      d1['www']+='_all_bkgsubtracted'
      d2 = deepcopy(d)
      d2.update({
        'files': [DATASETS[x] for x in [data,mc]+backgrounds],
        'nicks': [obs+x for x in [data,mc]+backgrounds],
        'weights': [cutstring+'*'+weightstring]+[cutstring+'*6225.42/4963.0']+len(backgrounds)*[cutstring],
        'zjetfolders': ['zjetcuts_L1L2L3Res']+(len(backgrounds)+1)*['zjetcuts_L1L2L3'],
        'sum_result_nicks': [obs+'sim'],
        'sum_nicks': [obs+mc+' '+obs+(' '+obs).join(backgrounds)],
        'stacks': ['data']+(len(backgrounds)+1)*['MC']+['ratio'],
        'ratio_numerator_nicks': [obs+data],
        'ratio_denominator_nicks': [obs+'sim'],
        'ratio_result_nicks': ['ratio'],
        'y_subplot_label': 'Data/Sim',
        'y_subplot_lims': [0.75,1.25],
        'labels': ['Data','DY ('+LABELDICT[mc]+')']+backgrounds+[''],
        'nicks_blacklist': ['sim'],
        'labelsize': 25,
        'legend': None,
        #'title': 'Before PU reweighting',
      })
      if postfix == '_noPURW':
          d2['weights'] = [cutstring+'*'+weightstring]+[cutstring+'*6225.42/4963.0/puWeight']+len(backgrounds)*[cutstring+'/puWeight'],
      d2['www'] += '_'+mc+'_bkgadded'
      plots.append(d1)
      #plots.append(d2)
      
    return [PlottingJob(plots=plots, args=args)]


def plot_responses_inclusive(args=None, cut='_jet1pt20', mc='mad', postfix='_cuts'):
    plots=[]
    cutstring    = generate_basiccutstring(args,cut)
    gencutstring = generate_basiccutstring(args,'gen'+cut)
    print DATASETS[mc]
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
        'y_label': 'reco'+obs,
        'z_log': True,
        'z_lims': [1e-3,1e0],
        'analysis_modules': ['NormalizeRowsToUnity'],
        'filename': obs,
        'www': 'responses_'+mc+cut+postfix,
        'nicks': [obs],
        'weights': [cutstring+'*'+gencutstring+'*(jet2pt/jet1pt<0.5)'],
        'zjetfolders': ['zjetcuts_L1L2L3'],
        'colormap': 'summer_r',
        'no_energy_label': True,
        'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Simulation} \\hspace{0.2} \\it{Preliminary} \\hspace{9.2} .$",
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

def plot_zpt_phistareta_correlation(args=None, cut='_jet1pt20', mc='mad', postfix=''):
    plots=[]
    gen = 'gen'
    cutstring    = generate_basiccutstring(args,gen+cut)
    d = ({
        'corrections': [''],
        'files': [DATASETS[mc]],
        'y_expressions': [gen+'zpt'],
        'y_bins': 'zpt',
        'y_log': True,
        'y_label': gen+'zpt',
        'y_ticks': [30,60,100,200,400,1000],
        'y_lims': [25,1000],
        'x_expressions': [gen+'phistareta'],
        'x_bins': 'phistareta',
        'x_log': True,
        'x_label': gen+'phistareta',
        'x_ticks': [0.5,1.0,2.0,4.0,10,30],
        'x_lims': [0.4,50],
        'z_log': True,
        'z_lims': [1e0,1e4],
        'analysis_modules': ['GetCorrelationFactor'],
        #'analysis_modules': ['NormalizeRowsToUnity'],
        #'analysis_modules': ['NormalizeToUnity'],
        'filename': gen+'phistareta_'+gen+'zpt',
        'www': 'responses_'+mc+cut+postfix,
        'nicks': ['correlation'],
        'weights': [cutstring],
        'zjetfolders': [gen+'zjetcuts_L1L2L3'],
        'figsize': [8,6.5],
        'no_energy_label': True,
        'texts': [r"$\\bf{CMS} \\hspace{0.5} \\it{Simulation} \\hspace{0.2} \\it{Preliminary}$"],
        #'plot_modules': ['ExportRoot'],
        'texts_size': [20],
        'texts_y': [1.06,0.1],
        'texts_x': [0.03,0.15],
    })
    plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def plot_yb_ystar_correlation(args=None, cut='_jet1pt20', mc='mad', postfix=''):
    plots=[]
    gen = 'gen'
    cutstring    = generate_basiccutstring(args,gen+cut)
    d = ({
        'corrections': [''],
        'files': [DATASETS[mc]],
        'y_expressions': [gen+'ystar'],
        'y_bins': 'ystar',
        'y_label': gen+'ystar',
        #'y_ticks': [30,60,100,200,400,1000],
        #'y_lims': [25,1000],
        'x_expressions': [gen+'yboost'],
        'x_bins': 'yboost',
        'x_label': gen+'yboost',
        #'x_ticks': [0.5,1.0,2.0,4.0,10,30],
        #'x_lims': [0.4,50],
        'z_log': True,
        'z_lims': [1e2,4e4],
        #'analysis_modules': ['GetCorrelationFactor'],
        'filename': gen+'yboost_'+gen+'ystar',
        'www': 'responses_'+mc+cut+postfix,
        'nicks': ['correlation'],
        'weights': [cutstring+'&&('+gen+'yboost+'+gen+'ystar<2.5)'],
        'zjetfolders': [gen+'zjetcuts_L1L2L3'],
        'figsize': [8,6.5],
        'no_energy_label': True,
        'texts': [r"$\\bf{CMS} \\hspace{0.5} \\it{Simulation} \\hspace{0.2} \\it{Preliminary}$"],
        #'plot_modules': ['ExportRoot'],
        'texts_size': [20],
        'texts_y': [1.06],
        'texts_x': [0.03],
    })
    plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def plot_calibration_quantities(args=None,cuts='finalcuts',jec='L1L2L3Res'):
    plots=[]
    #datalist = ['BCDEFGH']
    datalist = ['BCD','EF','GH']
    d = ({
        'files': ['/ceph/tberger/excalibur_results/2019-07-25/mc16_mm_BCDEFGH_DYNJtoLLmadgraph.root']
                 #['/portal/ekpbms3/home/tfesenbecker/excalibur_work/merged/mc16_mm_BCDEFGH_DYJets_Madgraph.root']
                +['/ceph/tberger/excalibur_results/2019-07-25/data16_mm_'+x+'_DoMu17Jul2018.root' for x in datalist],
                #+['/ceph/tberger/excalibur_results/2019-07-25/data16_mm_'+x+'_SiMu17Jul2018.root' for x in datalist],
                #+['/portal/ekpbms3/home/tfesenbecker/excalibur_work/merged/data16_mm_BCDEFGH_07Aug2017.root'],
        'www': 'calibration_DoMu_distribution'+('_' if len(datalist)==1 else 's_')+cuts+'_'+jec,
        #'www': 'calibration_SiMu_distribution'+('_' if len(datalist)==1 else 's_')+cuts+'_'+jec,
        'corrections': [jec] if not 'Res' in jec else ['L1L2L3']+len(datalist)*[jec],
        'zjetfolders': [cuts],
        'lumis': [35.9],
        'texts': [r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$",('' if jec=='L1L2L3' else 'incl. residual corrections')],
        #'texts': [r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$",r"$\\bf{"+jec+"}$",cuts],
        'texts_size': [20],
        'texts_y': [1.07,0.95],#,0.95,0.85],
        #'texts_y': [1.07,0.1,0.2],#,0.95,0.85],
        'labelsize': 25,
        #'no_energy_label': True,
        #'output_dir': 'calibration_distributions_'+cuts+'_'+jec,
        'nicks': ['MC']+datalist,
        'ratio_numerator_nicks': datalist,
        'ratio_denominator_nicks': ['MC'],
        'ratio_denominator_no_errors': False,
        'x_errors': True,
        'y_subplot_label': 'Data/Sim',
    })
    if len(datalist)==1:
        d['labels'] = ['Simulation','Data']
        d['markers'] = ['fill','o','.']
        d['colors']  = ['steelblue','black','black']
    if len(datalist)==3:
       d['markers'] = ['.']+2*['D','s','o'],
       d['colors']  = ['black']+2*['red','blue','green'],
    for obs in ['mupluspt','muminuspt','mupluseta','muminuseta','zpt','zy','zmass','jet1pt','jet1eta','jet2pt','alpha','ptbalance','mpf']:#
    #for obs in ['alpha']:
      d1 = deepcopy(d)
      d1.update({
        'analysis_modules': ['NormalizeToFirstHisto','NormalizeByBinWidth','Ratio'],
        'filename': obs,
        'x_expressions': [obs],
        'x_log': obs in ['zpt'],
        'step': len(datalist)!=1,
        'line_styles': ['-'] if not len(datalist)==1 else [''],
        'x_bins': obs,
        'y_log': obs not in ['mupluseta','muminuseta','ptbalance','mpf','zmass'],
        'y_label': 'Events per binsize',
        'y_subplot_lims': [0.75,1.25],
      })
      if not d1['y_log']:
          d1.update({'texts_x': [0.1,0.03]})
      #if obs=='zpt':
      #    d1.update({'x_lims': [30,1000]})
      if obs in ['alpha','jet2pt']:
        d1.update({ 'zjetfolders': ['basiccuts'],'weights': ['(zpt>30)&&(abs(jet1eta)<1.3)']})
      if obs=='jet1eta':
        d1.update({ 'zjetfolders': ['basiccuts'],'weights': ['(zpt>30)&&(alpha<0.3)']})
      plots.append(d1)
    for obs in [['zpt','mpf'],['zpt','ptbalance'],['jet1eta','mpf'],['jet1eta','ptbalance'],['absjet1eta','mpf'],['absjet1eta','ptbalance']]:
      d2 = deepcopy(d)
      d2.update({
        'filename': obs[0]+'_vs_'+obs[1],
        'x_expressions': [obs[0]],
        'y_expressions': [obs[1]],
        'x_log': obs[0] in ['zpt'],
        'x_bins': obs[0],
        #'y_bins': obs[1],
        'analysis_modules': ['Ratio'],
        'tree_draw_options': 'prof',
        'y_lims': [0.9,1.05] if obs[1]=='mpf' else [0.7,1.05],
        'y_subplot_lims': [0.94,1.04],
      })
      if len(datalist)==1:
        d2['markers'] = ['.','o','.']
        d2['colors']  = ['black','purple','black']
      if obs[0] in ['jet1eta','absjet1eta']:
        d2.update({ 'zjetfolders': ['basiccuts'],'weights': ['(zpt>30)&&(alpha<0.3)']})
      plots.append(d2)
    return [PlottingJob(plots=plots, args=args)]

def plot_calibration_extrapolation(args=None,cuts='finalcuts',jec='L1L2L3'):
    plots = []
    obs = 'alpha'
    d = ({
        'files': (['/ceph/tberger/excalibur_results/2019-07-25/mc16_mm_BCDEFGH_DYNJtoLLmadgraph.root']
                 #['/portal/ekpbms3/home/tfesenbecker/excalibur_work/merged/mc16_mm_BCDEFGH_DYJets_Madgraph.root']
                +['/ceph/tberger/excalibur_results/2019-07-25/data16_mm_BCDEFGH_DoMu17Jul2018.root'])*2,
                #+['/ceph/tberger/excalibur_results/2019-07-25/data16_mm_BCDEFGH_SiMu17Jul2018.root'])*2,
                #+['/portal/ekpbms3/home/tfesenbecker/excalibur_work/merged/data16_mm_BCDEFGH_07Aug2017.root'],
        'www': 'calibration_DoMu_extrapolation_'+cuts+'_'+jec,
        #'www': 'calibration_SiMu_extrapolation_'+cuts+'_'+jec,
        'nicks': ['mpfMC','mpfData','ptbMC','ptbData'],
        'corrections': [jec] if not 'Res' in jec else ['L1L2L3',jec],
        #'weights': ['alpha>0.05'],
        'zjetfolders': [cuts],
        'lumis': [35.9],
        'texts': [r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$",('' if jec=='L1L2L3' else 'incl. residual corrections')],
        #'texts': [r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$",r"$\\bf{"+jec+"}$",cuts],
        'texts_size': [20],
        'texts_y': [1.09,0.95],#,0.95,0.85],
        'texts_x': [0.03],
        #'texts_y': [1.07,0.1,0.2],#,0.95,0.85],
        'labelsize': 25,
        'lines': [1],
        'filename': obs,
        'x_expressions': 4*['alpha'],
        'y_expressions': 2*['mpf']+2*['ptbalance'],
        'x_label': r'$\\alpha$',
        #'x_bins': '10,0,0.5',
        'x_bins': '6,0,0.3',
        'analysis_modules': ['Ratio','FunctionPlot'],
        'markers': ['o','d','s','p','o','s'],
        'colors': ['royalblue','navy','coral','orangered','navy','orangered'],
        'alphas': [0.5],
        'function_fit': ['mpfMC','mpfData','ptbMC','ptbData','mpfRatio','ptbRatio'],
        'function_nicknames': ['fit_mpfMC','fit_mpfData','fit_ptbMC','fit_ptbData','fit_mpfRatio','fit_ptbRatio'],
        'functions': '[0]-[1]*x+[2]*x**2',
        'function_parameters': ['1,0.3,0.1'],
        'tree_draw_options': 'prof',
        'y_lims': [0.8,1.05],
        'y_subplot_lims': [0.96,1.06],
        'legend': 'lower left',
        'labels': ['MPF (Simulation)','MPF (Data)',r'$p_T$ balance (Simulation)',r'$p_T$ balance (Data)','MPF',r'$p_T$ balance'],
        #'nicks_whitelist': ['mpfData','mpfMC','mpfRatio','ptbData','ptbMC','ptbRatio'],
        'plot_modules': ['PlotMplZJet','PlotExtrapolationText'],
        'extrapolation_text_nicks': ['fit_mpfRatio','fit_ptbRatio'],
        'extrapolation_text_colors': ['royalblue', 'coral'],
        #'extrapolation_text_position': [0.1,0.5],
        #'extrapolation_text_size': 20,
        #'extrapolation_text_label': "$\mathit{R}_0$",
        'ratio_numerator_nicks': ['mpfData','ptbData'],
        'ratio_denominator_nicks': ['mpfMC','ptbMC'],
        'ratio_result_nicks': ['mpfRatio','ptbRatio'],
        'ratio_denominator_no_errors': False,
        #'x_errors': True,
        'subplot_nicks': ['Ratio'],
        'subplot_fraction': 40,
        'subplot_legend': 'upper left',
        'y_subplot_label': 'Data/Sim',
    })
    plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def plot_calibration_zmass(args=None,cuts='finalcuts',jec='L1L2L3'):
    plots=[]
    obs = 'zmass'
    d = ({
        'files': #(['/ceph/tberger/excalibur_results/2019-07-25/mc16_mm_BCDEFGH_DYNJtoLLmadgraph.root']
                 (['/portal/ekpbms3/home/tfesenbecker/excalibur_work/merged/mc16_mm_BCDEFGH_DYJets_Madgraph.root']
                #+['/ceph/tberger/excalibur_results/2019-07-25/data16_mm_'+x+'_DoMu17Jul2018.root' for x in datalist],
                #+['/ceph/tberger/excalibur_results/2019-07-25/data16_mm_BCDEFGH_SiMu17Jul2018.root'])*2,
                +['/portal/ekpbms3/home/tfesenbecker/excalibur_work/merged/data16_mm_BCDEFGH_07Aug2017.root'])*2,
        #'www': 'calibration_DoMu_zmassfit_'+cuts+'_'+jec,
        'www': 'calibration_SiMu_zmassfit_'+cuts+'_'+jec,
        'nicks': ['MC','Data'],
        'corrections': [jec] if not 'Res' in jec else ['L1L2L3',jec],
        #'weights': ['alpha>0.05'],
        'zjetfolders': [cuts],
        'lumis': [35.9],
        'texts': [r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$"],
        #'texts': [r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$",r"$\\bf{"+jec+"}$",cuts],
        'texts_size': [20],
        'texts_y': [1.09],#,0.95,0.85],
        'texts_x': [0.1],
        #'texts_y': [1.07,0.1,0.2],#,0.95,0.85],
        'labelsize': 25,
        'filename': obs,
        'x_expressions': [obs],
        'x_label': obs,
        'x_bins': obs,
        'analysis_modules': ['NormalizeToFirstHisto','Ratio','FunctionPlot'],
        'labels': ['Simulation','Data'],
        'markers': ['fill','o','.'],
        'colors': ['steelblue','black','black','royalblue','dimgray'],
        'alphas': [0.7],
        'function_fit': ['MC','Data'],
        'function_nicknames': ['fit_MC','fit_Data'],
        'functions': '([4]*TMath::Voigt(x-[0],[1],2.4952)+[2]*x+[3])',
        #'functions': '[3]*TMath::Voigt(x-[0],[1],[2])',
        #'functions': '[2]/((x-[0])**2+[1]**2)',
        #'functions': '[2]*exp((x-[0])**2/[1]**2/2)',
        'function_parameters': '90,2.3,0.,0.,100000',
        'y_subplot_lims': [0.75,1.25],
        'labels': ['Simulation','Data'],
        'plot_modules': ['PlotMplZJet','PlotExtrapolationText'],
        'extrapolation_text_nicks': ['fit_MC','fit_Data'],
        'extrapolation_text_colors': ['royalblue','dimgray'],
        'extrapolation_text_size': 15,
        'ratio_numerator_nicks': ['Data'],
        'ratio_denominator_nicks': ['MC'],
        'ratio_result_nicks': ['Ratio'],
        'ratio_denominator_no_errors': False,
        'x_errors': True,
        'subplot_nicks': ['Ratio'],
        'subplot_fraction': 40,
        #'subplot_legend': 'upper left',
        'y_subplot_label': 'Data/Sim',
    })
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

def plot_npcorrections(args=None,cut='_jet1pt10'):
    cutstring = generate_basiccutstring(args,cut)
    plots = []
    d = ({
        'files': [  '/ceph/tberger/excalibur_work/excalibur/mc16_mm_BCDEFGH_DYtoLLcreated_nonNP_2019-08-19_15-15/out.root',
                    '/ceph/tberger/excalibur_work/excalibur/mc16_mm_BCDEFGH_DYtoLLcreated_2019-08-19_14-29/out.root',
                ],
        'folders': ['genzjetcuts_L1L2L3/ntuple'],
        'nicks': ['nonNP','official'],
        'weights': ['304191/608366','1'],
        'x_expressions': ['genzpt'],
        'x_bins': 'zpt',
        'x_log': True,
        'www': 'NPC',
        'analysis_modules': ['Ratio'],
        'y_log': True,
        'y_subplot_lims': [0.9,1.1],
        'lumis': [35.9],
    })
    plots.append(d)
    return [PlottingJob(plots=plots, args=args)]




