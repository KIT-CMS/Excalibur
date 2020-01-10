# -*- coding: utf-8 -*-
'''
This script produces the plots used for my thesis: IEKP-KA/2019-16

The Skimming outputs can be found at srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming_94X/
The Excalibur outputs can be found at srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/ZJtriple_Excalibur/
The Histogram outputs can be found at srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/ZJtriple_Histograms/
The Theory calculations can be found at srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/ZJtriple_Theory/

This script is only meant to produce plots out of the histograms. For functions to produce the histograms see: qcd_cross_section_3Dhist.py
Use 'merlin.py --py plot_all' to create all plots defined here!
'''

import os
import ROOT
from copy import deepcopy
from Excalibur.Plotting.utility.toolsZJet import PlottingJob
from Excalibur.Plotting.utility.toolsQCD import invert_3Dhists, closure_chi2
from Excalibur.Plotting.utility.binningsZJet import rebinning

# The local adress of the Histogram output folder: (check if still valid!)
PLOTSFOLDER = '/storage/gridka-nrg/tberger/ZJtriple_Histograms'

# A local buffering folder is required and will be created in your Excalibur setup:
BUFFERFOLDER = os.environ['EXCALIBURPATH']+'/ZJtriple'
if not os.path.exists(BUFFERFOLDER):
    os.makedirs(BUFFERFOLDER)
    print 'The directory',BUFFERFOLDER,'has been created'

# Set CMS label to True if necessary:
CMSLABEL = False

# The unfolding closure tests need a list of MC samples to be compared to:
MCLIST      = ['amc','hpp','mad']

# Each MC simulation and calculation order has a specific marker and colour:
LABELDICT   = ({'amc':"P8+aMC",'hpp':"HW+MG",'mad':"P8+MG",
                'LO': "LO", 'NLO': "NLO", 'NNLO': "NNLO"})
MARKERDICT  = ({'amc':'s','hpp':'D','mad':'o',
                'LO':'^','NLO':'s','NNLO':'o'})
COLORDICT   = ({'amc':'red','hpp':'blue','mad':'green',
                'LO':'green','NLO':'blue','NNLO':'red'})

'''
               'toy':"Toy     ",
               'toy0':"P8+MG",'toy1':"P8+aMC",'toy2':"HW+MG",
               'LO': 'LO', 'NLO': 'NLO', 'NNLO': 'NNLO',
                })
MARKERDICT = ({'amc':'s','hpp':'D','mad':'o','toy':'d','toy0':'^','toy1':'<','toy2':'>','toy3':'v','LO':'^','NLO':'s','NNLO':'o'})
COLORDICT = ({'amc':'red','hpp':'blue','mad':'green','toy':'grey', 'toy0':'seagreen', 'toy1':'salmon', 'toy2': 'orchid','toy3':'gray','LO':'green','NLO':'blue','NNLO':'red'})
'''

##########################################################################################################################################################################

def plot_datamc(args=None, obs='zpt', data='17Jul2018', mc='mad'):
    plots=[]
    data_source = obs+'_'+data+'.root'
    mc_source   = obs+'_'+mc+'.root'
    bkg_list = ['TT','WZ','ZZ','TW','WW']
    bkg_source  =[obs+'_'+bkg+'.root' for bkg in bkg_list]
    filelist = [data_source,mc_source]+bkg_source
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x,PLOTSFOLDER,BUFFERFOLDER)
        filelist_binned.append(BUFFERFOLDER+'/'+x.replace('.root','_binned.root'))
    d0 = ({
        'files': filelist_binned,
        'folders': [''],
        'nicks': ['Data','DY']+bkg_list,
        'sum_nicks' : ['DY '+' '.join(bkg_list)],
        'analysis_modules': ['SumOfHistograms','NormalizeByBinWidth','Ratio'],
        'sum_result_nicks' : ['sim'],
        'ratio_numerator_nicks': ['Data'],
        'ratio_denominator_nicks': ['sim'],
        'ratio_result_nicks':['ratio'],
        'ratio_denominator_no_errors': False,
        'stacks':['data','mc']+len(bkg_list)*['mc']+['ratio'],
        'filename': obs,
        'x_errors': [1],
        'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
        'x_log': True,
        'x_label': obs,
        'y_log': True,
        'y_lims': [1e-2,1e5] if obs =='zpt' else [1e0,1e7],
        'y_label': 'Events per binsize',
        'nicks_blacklist': ['sim'],
        'y_subplot_label': 'Data/Sim',
        'y_subplot_lims': [0.75,1.25],
        'texts_size': [20],
        'texts_y': [1.07,0.97],
        'labelsize': 25,
        'lumis': [35.9],
        'energies': [13],
    })
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = deepcopy(d0)
            d.update({
                'x_expressions': [obs+namestring],
                'www': 'datamc_'+data+'_vs_'+mc+'/datamc'+namestring,
                'texts': [  r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$" if CMSLABEL else "",
                            r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
            })
            if ysmin>1.0:
                d['y_subplot_lims'] = [0.9,2.3]
            elif ysmin>0.5:
                d['y_subplot_lims'] = [0.8,1.8]
            elif ybmin>1.0:
                d['y_subplot_lims'] = [0.5,1.5]
            plots.append(d)
    return plots

def plot_resolution(args=None, obs='zpt', mc='mad', trunc = '_985'):
    plots = []
    folder = PLOTSFOLDER+'/resolution'+trunc+'/'
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'www': 'resolutions_'+mc+'/resolution'+trunc+namestring,
                'folders': [''],
                'x_log': True,
                'x_errors': [1],
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'texts': [  r"$\\bf{CMS} \\hspace{0.5} \\it{Simulation} \\hspace{0.2} \\it{Preliminary}$" if CMSLABEL else "",
                            r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'texts_size': [20],
                'analysis_modules': ['FunctionPlot'],
                'function_parameters': ['1,0.01,1,0'],
                'function_fit_parameter_names': ['p_0','p_1','p_2','p_3'],
                'function_fit_scale_errors_by_chi2': True,
                'alphas': [0.707],
                'nicks_whitelist': ['fit',''],
                #'function_display_result': True,
                'labelsize': 25,
            })
            d0 = deepcopy(d)
            rebinning(args,d0,obs,(ybmin,ybmin+0.5),(ysmin,ysmin+0.5))
            l_bins = [float(x) for x in d0['x_bins'][0].split(' ')][:2]
            d0.pop('x_bins')
            d0.pop('x_ticks')
            d0.pop('y_bins')
            d0.update({
                'x_log': False,
                'nicks': ['hist'],
                'analysis_modules': ['FunctionPlot'],
                'functions': ['[0]*ROOT::Math::crystalball_function(-abs(x), [1], [3], [2], 0)','[0]*exp(-x**2/[1]**2/2)'],
                'function_fit': ['hist'],
                'function_parameters': ['43.539223,1.3674205,0.013207260,4.9681730','38.866539,0.015700151'],
                'function_nicknames': ['CrystalBall','Gaussian'],
                'colors': ['black','darkviolet','darkorange'],
                'y_label': 'Arb. units',
                'y_ticks': [0],
                'texts_x': [0.03,0.03,0.03,0.05,0.05],
                'texts_y': [0.90,1.05,0.97,0.6,0.75],
                'legend': None,
                'function_display_result': True,
                'function_fit_scale_errors_by_chi2': False,
            })
            d0['texts'] = ['']+d0['texts']
            d1 = deepcopy(d)
            d1.update({
                'files': [  folder+obs+'_'+mc+namestring+'.root',
                            folder+'matchedjet1y_'+mc+namestring+'_bins_of_'+obs+'.root',
                            folder+'zy_'+mc+namestring+'_bins_of_'+obs+'.root'],
                'filename': obs+'_resolution',
                'x_expressions': ['rms'],
                'x_label': 'gen'+obs,
                'nicks': [obs,'jety','zy'],
                'labels': [(r'$p_T^Z$' if obs=='zpt' else r'$\\phi*_ \\eta$'),r'$y^{jet1}$',r'$y^Z$'],
                'markers': ['.'],
                'colors': ['green','orange','violet','darkgreen','darkorange','darkviolet'],
                'functions': ['[0]+[1]*sqrt(x)+[2]/sqrt(x)','[0]+[1]/sqrt(x)','[0]'] if obs == 'zpt' else ['[0]+[1]*x+[2]/x','[0]+[1]/x','[0]+[1]*log(x)'],
                'function_fit': [obs,'jety','zy'],
                'function_nicknames': ['fit_'+obs,'fit_jet1y','fit_zy'],
                'y_lims': [0,0.06],
                'y_label': 'Resolution',
                'texts_x': [0.05,0.05,0.05,0.03,0.03],#0.05,0.4,0.7],
                'texts_y': [0.90,0.82,0.74,1.05,0.97],#1.08,1.08,1.08],
            })
            d1['texts'] = ([r'$f_{p_T^Z}(x)=p_0+p_1\\sqrt{x}+p_2\\frac{1}{\\sqrt{x}}$',
                            r'$f_{y^{jet1}}(x)=p_0+p_1\\frac{1}{\\sqrt{x}}$',
                            r'$f_{y^Z}(x)=const$'] if obs=='zpt' else
                           [r'$f_{\\phi^*_\\eta}(x)=p_0+p_1x+p_2\\frac{1}{x}$',
                            r'$f_{y^{jet}}(x)=p_0+p_1\\frac{1}{x}$',
                            r'$f_{y^Z}(x)=p_0+p_1\\log(x)$'
                            ])+d1['texts']
            if ysmin==2.0 and obs=='zpt':
                d1['y_lims'] = [0,0.12]
            elif ybmin==2.0 and obs=='zpt':
                d1['y_lims'] = [0,0.16]
            elif ysmin+ybmin>1.0 and obs=='zpt':
                d1['y_lims'] = [0,0.15]
            d2 = deepcopy(d)
            d2.update({
                'files': [folder+obs+'_'+mc+namestring+'.root'],
                'filename': obs+'_rates',
                'x_expressions': ['losses','fakes'],
                'x_label': obs,
                'nicks': ['losses','fakes'],
                'labels': ['Acceptance','1-Fakerate'],
                'markers': ['.'],
                'colors': ['coral','slategray','lightcoral','lightslategray'],
                'functions': ['[0]/2*(2-erfc([1]*(x-[2])))+[3]',('[0]-[1]/x**3' if obs == 'zpt' else '[0]-[1]/x**4')],
                'function_fit': ['losses','fakes'],
                'function_nicknames': ['fit_acc','fit_fake'],
                'y_lims': [0.5,1.2],
                'y_label': 'Fraction',
                'texts_x': [0.05,0.05,0.03,0.03],#0.05,0.4,0.7],
                'texts_y': [0.88,0.81,1.05,0.97],#1.08,1.08,1.08],
                'lines': [1],
            })
            d2['texts'] = [r'$f_{Acceptance}(x)=\\frac{1}{2}p_0(1+erf(p_1(x-p_2)))+p_3$',r'$f_{1-Fakerate}(x)=p_0+p_1\\frac{1}{x'+('^3' if obs=='zpt' else '^4')+'}$']+d2['texts']
            d3 = deepcopy(d)
            d3.update({
                'files': [folder+obs+'_'+mc+namestring+'.root'],
                'filename': obs+'_fractions',
                'x_expressions': ['PU','matched','switched'],
                'x_label': obs,
                'nicks': ['PU','matched','switched'],
                'labels': ['pileup','matched','switched'],
                'markers': ['fill'],
                'colors': ['grey','steelblue','orange','brown'],
                'functions': ['[0]*exp(-[1]*x)'] if obs == 'zpt' else ['[0]+[1]/x'],
                'function_fit': ['switched'],
                'function_nicknames': ['fit_switched'],
                'y_lims': [0,1.25],
                'y_label': 'Fraction',
                'texts_x': [0.05,0.03,0.03],#0.05,0.4,0.7],
                'texts_y': [0.89,1.05,0.97],#1.08,1.08,1.08],
                'stacks': 3*['fraction']+['fit'],
                'lines': [1],
                'alphas': [1],
                'nicks_whitelist': [''],
            })
            # turn logscale on
            d3.update({
                'filename': obs+'_fractions_log',
                'y_lims': [0.01,3],
                'y_log': True,
                'y_ticks': [0.01,0.1,1],
            })
            d3['texts'] = ([r"$f_{switched}(x)=p_0exp(-p_1 x)$"] if obs =='zpt' else [r"$f_{switched}(x)=p_0+p_1\\frac{1}{x}$"]) + d3['texts']
            d4 = deepcopy(d)
            d4.update({
                'files': [folder+obs+'_'+mc+namestring+'.root'],
                'filename': obs+'_subprocesses',
                'x_expressions': ['qaq','aqg','qg','gg','qq','aqaq'],
                'x_label': obs,
                'nicks': ['qaq','gaq','qg','gg','qq','aqaq'],
                'labels': ['quark-antiquark','gluon-antiquark','quark-gluon','gluon-gluon','quark-quark','antiquark-antiquark'],
                'alphas': 1,
                'markers': ['fill'],
                'colors': ['turquoise','gold','coral','springgreen','mediumvioletred','cornflowerblue'],
                'y_lims': [0,1.5],
                'y_label': 'Subprocess fraction',
                'texts_x': [0.03,0.03],#0.05,0.4,0.7],
                'texts_y': [1.05,0.97],#1.08,1.08,1.08],
                'stacks': ['fraction'],
                'lines': [1],
                #'alphas': [1],
                #'nicks_whitelist': [''],
            })
            d4.pop('analysis_modules')
            #plots.append(d0)
            plots.append(d1)
            plots.append(d2)
            plots.append(d3)
            #plots.append(d4)
    return plots

def plot_chi2(args=None, obs='zpt', mc='hpp'):
    plots = []
    d = ({
        'www': 'chi2_MC_by_'+mc,
        'files': [PLOTSFOLDER+'/chi2/'+obs+'_'+x+'_by_'+mc+'.root' for x in MCLIST],
        'folders': [''],
        'x_expressions': ["chi2_"+x+"_by_"+mc for x in MCLIST],
        'labels': [LABELDICT[x] for x in MCLIST],
        'markers': [MARKERDICT[x] for x in MCLIST],
        'colors': [COLORDICT[x] for x in MCLIST],
        'y_lims': [0,4],
        'lines': [1],
        'filename': obs,
        'x_errors': True,
        'x_ticks': range(1,16),
        'y_errors': False,
        'y_label': r'$\\mathit{\\chi}^2$/$\\mathit{n.d.f.}$',
        #'x_label': (r'$\\mathit{p}_T^Z$' if obs =='zpt' else r'$\\mathit{\\phi}^{*}_{\\eta}$')+' Bin',
        'x_label': 'Rapidity bin index',
        'x_lims': [0.5,15.5],
        'texts': [  r"$\\bf{CMS} \\hspace{0.5} \\it{Simulation} \\hspace{0.2} \\it{Preliminary}$" if CMSLABEL else "",
                    'unfolding in ',(r'($p_T^Z$,$y_b$,$y*$)' if obs=='zpt' else r'($\\phi*_\\eta$,$y_b$,$y*$)'),
                    'using',LABELDICT[mc],('Toy ' if 'toy' in mc else '')+'response'],
        'texts_size': 20,
        'texts_x': [0.05],
        'texts_y': [1.07,0.76,(0.71 if obs=='zpt' else 0.70),0.64,0.58,0.52],
        'labelsize': 25,
        'legend': 'upper left',
        'vertical_lines': [x+0.5 for x in [5,9,12,14]],
        'vertical_lines_styles': ['--'],
        #'vertical_lines_styles': 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--'],
    })
    plots.append(d)
    return plots

def plot_unfolding_closure(args=None, obs='zpt', mc='mad'):
    varlist = 2*['stats_'+mc]
    plots=[]
    px,py = ROOT.Double(0),ROOT.Double(0)
    ybinedges = [0,5,9,12,14,0]
    if 'toy' in mc:
        varlist = ['stats_toy','model_toy','Robs','Ryj','Ryz','switch','F','A']
    filelist_binned = []
    filelist_chi2 = []
    for sample in MCLIST:
        f = ROOT.TFile(PLOTSFOLDER+'/chi2/'+obs+'_'+sample+'_by_'+mc+'.root','READ')
        h = f.Get('chi2_'+sample+'_by_'+mc)
        filelist_chi2.append(deepcopy(h))
        f.Close()
        invert_3Dhists(args,obs+'_'+sample+'.root',PLOTSFOLDER,BUFFERFOLDER)
        filelist_binned.append(BUFFERFOLDER+'/'+obs+'_'+sample+'_binned.root')
        invert_3Dhists(args,obs+'_'+sample+'_by_'+mc+'.root',PLOTSFOLDER+'/unfolded',BUFFERFOLDER+'/unfolded')
        filelist_binned.append(BUFFERFOLDER+'/unfolded/'+obs+'_'+sample+'_by_'+mc+'_binned.root')
    for var in varlist:
        invert_3Dhists(args,obs+'_17Jul2018_'+var+'.root',PLOTSFOLDER+'/uncertainty',BUFFERFOLDER+'/uncertainty')
        filelist_binned.append(BUFFERFOLDER+'/uncertainty/'+obs+'_17Jul2018_'+var+'_binned.root')
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            chi2 = []
            for i in xrange(len(MCLIST)):
                filelist_chi2[i].GetPoint(ybinedges[int(2*ysmin)]+int(2*ybmin),px,py)
                chi2.append(1.0*py)
                #calculate_closure_chi2(args,obs,cut,x,mc,match,postfix,int(2*ybmin),int(2*ysmin)))
            d = ({
                'www': 'unfolding_MC_by_'+mc+'/unfolded'+namestring,
                'files': filelist_binned,
                'x_expressions': len(MCLIST)*['gen'+obs+namestring,'unfolded'+obs+namestring]+['uncertainty_'+x+namestring for x in varlist],
                'folders': [''],
                'nicks': [(x+'gen',x+'unf') for x in MCLIST]+['unc_'+x for x in varlist],
                'analysis_modules': ['QuadraticSumOfHistograms','Ratio','SumOfHistograms'],
                'quad_sum_nicks': ['unc_'+' unc_'.join(varlist[1:])],
                'quad_sum_result_nicks': ['unc_model'],
                'ratio_numerator_nicks': ['unc_model']+[x+'unf' for x in MCLIST],
                'ratio_denominator_nicks': ['unc_model']+[x+'gen' for x in MCLIST],
                'ratio_result_nicks': ['unity']+[x+'ratio' for x in MCLIST],
                'sum_nicks' : ['unity unc_'+varlist[0],'unity unc_'+varlist[0],'unity unc_model','unity unc_model'],
                'sum_scale_factors' : ['1 1', '1 -1','1 1', '1 -1'],
                'sum_result_nicks': ['stats_up','stats_down','model_up','model_down'],
                'labels': ["Toy Stat. Unc.","","Toy Syst. Unc.",""
                                    ]+[(LABELDICT[x]+' (chi2/ndf={:.3f})').format(chi2[i]) for (i,x) in list(enumerate(MCLIST))],
                'subplot_legend': 'upper left',
                'subplot_fraction': 45,
                'subplot_nicks': ['up','down','ratio'],
                'y_subplot_label': 'Unfolded/Gen',
                'filename': obs,
                'x_label': obs,
                'x_errors': 4*[0]+len(MCLIST)*[1],
                'x_log': True,
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'y_label': 'Unfolded/Gen',
                'y_lims': [0.9,1.1],
                'y_errors': 4*[False]+len(MCLIST)*[True],
                'y_log': False,
                'step': 2*[True]+2*[True]+len(MCLIST)*[False],
                'line_styles': len(MCLIST)*3*['']+2*['-']+2*['-'],
                'markers': 2*['fill']+2*['']+[MARKERDICT[x] for x in MCLIST],
                'colors': ['yellow','white','black','black']+[COLORDICT[x] for x in MCLIST],
                'nicks_whitelist': ['stats','model','ratio'],
                'nicks_blacklist': ['unity','unc'],
                'y_subplot_lims': [0.9,1.1],
                'texts': [  r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$" if CMSLABEL else "",
                            r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'texts_x': [0.03], 
                'texts_y': [1.07,0.97],
                'texts_size': [20],
                'labelsize': 25,
                'line_styles': 2*['']+2*['-']+len(MCLIST)*[''],
                'subplot_nicks': ['dummy'],
                'legend': 'lower left',
            })
            if not 'toy' in mc:
                d['labels'][len(MCLIST)]   = LABELDICT[mc]+" Stat. Unc."
                #d0['labels'][len(MCLIST)+2] = LABELDICT[mc]+" Syst. Unc."
                d['labels'][len(MCLIST)+1] = " "
                d['nicks_blacklist']+=['model']
                d.update({
                    'nicks_whitelist': ['stats','ratio'],
                    'x_errors': 2*[0]+len(MCLIST)*[1],
                    'labels': [LABELDICT[x]+" Stat. Unc.",""
                                ]+[(LABELDICT[x]+' (chi2/ndf={:.3f})').format(chi2[i]) for (i,x) in list(enumerate(MCLIST))],
                    'y_errors': 2*[False]+len(MCLIST)*[True],
                    'step': 2*[True]+len(MCLIST)*[False],
                    'line_styles': 2*['']+len(MCLIST)*[''],
                    'markers': 2*['fill']+[MARKERDICT[x] for x in MCLIST],
                    'colors': ['yellow','white']+[COLORDICT[x] for x in MCLIST],
                })
            if ysmin==2.0:
                d['y_lims'] = [0.5,1.5]
            elif ybmin==2.0:
                d['y_lims'] = [0.75,1.25]
            elif ysmin+ybmin>1.0:
                d['y_lims'] = [0.65,1.35]
            plots.append(d)
    return plots

def plot_uncertainties(args=None, obs='zpt'):
    plots = []
    l_var = ['stat','systematic','lumi','bkg','eff','unf','jec','jer']
    varlist = l_var
    invert_3Dhists(args,obs+'_17Jul2018_systematic.root',PLOTSFOLDER+'/uncertainty',BUFFERFOLDER+'/uncertainty')
    filelist_binned =[BUFFERFOLDER+'/uncertainty/'+obs+'_17Jul2018_systematic_binned.root']
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'files': filelist_binned,
                'folders': [''],
                'nicks': varlist,
                'x_expressions': ['uncertainty_'+var+namestring for var in varlist],
                'filename': obs,
                'labels': ['Statistical','Total systematic','Luminosity','Background','Efficiency','Unfolding','JEC','JER'],
                'alphas': [0.5],
                'x_log': True,
                'x_label': obs,
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'x_lims': [25,1000] if obs =='zpt' else [0.4,50],
                'y_errors': False,
                'y_lims': [0.0,0.1],
                'y_label': "Relative Uncertainty",
                'www': 'uncertainties/uncertainties'+namestring,
                'step': [True],
                'legend': None,
                'line_styles': ['-'],
                'markers': ['fill','o','v','^','>','<','s','D'],
                'colors': ['grey','black','red','blue','green','purple','orange','turquoise'],
                'texts': [  r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$" if CMSLABEL else "",
                                    r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'texts_size': [20],
                'texts_y': [1.05,0.97],
                'labelsize': 25,
            })
            if ysmin>1.5:
                d['y_lims'] = [0,0.29]
                d['vertical_lines'] = [250 if obs =='zpt' else 5]
            elif ysmin>1.0:
                d['y_lims'] = [0,0.2]
            elif ysmin>0.5:
                d['y_lims'] = [0,0.15]
            elif ybmin+ysmin>1:
                d['y_lims'] = [0,0.17]
            plots.append(d)
    return plots

def plot_crosssections(args=None,obs='zpt',pdf='',mclist=['mad','amc']):
    plots=[]
    invert_3Dhists(args,obs+'_17Jul2018_total.root',PLOTSFOLDER+'/uncertainty',BUFFERFOLDER+'/uncertainty')
    data_source  = [BUFFERFOLDER+'/uncertainty/'+obs+'_17Jul2018_total_binned.root']
    mc_source =[]
    for mc in mclist:
      if 'LO' in mc:
        invert_3Dhists(args,obs+'_'+mc+'_'+pdf+'.root',PLOTSFOLDER+'/theory',BUFFERFOLDER+'/theory')
        mc_source.append(BUFFERFOLDER+'/theory/'+obs+'_'+mc+'_'+pdf+'_binned.root')
      else:
        invert_3Dhists(args,obs+'_'+mc+'.root',PLOTSFOLDER,BUFFERFOLDER)
        mc_source.append(BUFFERFOLDER+'/'+obs+'_'+mc+'_binned.root')
    invert_3Dhists(args,obs+'_17Jul2018_systematic.root',PLOTSFOLDER+'/uncertainty',BUFFERFOLDER+'/uncertainty')
    unc_source  = [BUFFERFOLDER+'/uncertainty/'+obs+'_17Jul2018_systematic_binned.root']
    filelist_binned =  data_source+mc_source+unc_source
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'www': 'crosssections_'+'_'.join(mclist)+('_'+pdf if not pdf=='' else pdf)+'/xsec'+namestring,
                'files': filelist_binned,
                'folders': [''],
                'x_expressions': [obs+'_total'+namestring]+len(mclist)*['gen'+obs+'_asym'+namestring]+[obs+'_systematic'+namestring],
                'x_label': obs,
                'x_log': True,
                'x_ticks': [30,60,100,200,400,1000] if obs=='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'x_lims': [25,1000] if obs=='zpt' else [0.4,50],
                'x_errors': [1],
                'lumis': [35.9],
                'energies':[13],
                'nicks': ['data']+mclist+['uncertainty'],
                'analysis_modules': ['ScaleHistograms','NormalizeByBinWidth','Ratio'],
                'scale_nicks':  ['data','uncertainty']+mclist,
                'scales': [1e0/35.9/1000*(5941.0/6225.42 if x=='amc' else 1) for x in ['data','uncertainty']+mclist],
                'ratio_numerator_nicks':   ['uncertainty','data']+2*mclist,
                'ratio_denominator_nicks': (2+2*len(mclist))*['data'],
                'ratio_result_nicks': ['ratio'+x for x in ['syst','total']+mclist]+['unc'+x for x in mclist],
                'nicks_blacklist': ['uncertainty'],
                'filename': obs,
                'markers': ['.']+[MARKERDICT[x] for x in mclist]+['fill','errorband']+[MARKERDICT[x] for x in mclist]+len(mclist)*['errorband'],
                'colors': ['black']+[COLORDICT[x] for x in mclist]+['gray','grey']+2*[COLORDICT[x] for x in mclist],
                'hatch': (1+len(mclist))*[None]+['//',None]+2*len(mclist)*[None],
                'alphas': (1+len(mclist))*[1]+[1,0.707]+2*len(mclist)*[0.3],
                'zorder': [5]+len(mclist)*[1]+[3,2]+2*len(mclist)*[4],
                'step': [True],
                'line_styles': [''],
                'y_log': True,
                'y_lims': [1e-6,1e1] if obs =='zpt' else [1e-5,1e3],
                'y_errors': False,
                'y_subplot_lims': [0.75,1.25],
                'y_label': 'Events per binwidth',
                'y_subplot_label': 'Ratio to Data',#'Sim/Data' if 'amc' in mclist else 'Theory/Data',
                'subplot_legend': 'lower left',
                'subplot_nicks': ['ratio','unc'],
                'subplot_fraction': 50,
                'labels': ['Data']+[LABELDICT[x] for x in mclist]+['Syst. Unc','Syst.+Stat. Unc']+2*len(mclist)*[''],
                'labelsize': 25,
                'texts_size': [20],
                'texts_x': [0.02],
                'texts': [r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$" if CMSLABEL else "",
                          r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'texts_y': [1.10,0.97],
            })
            if obs == 'zpt':
                d['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\mathit{p}_T^Z dy_b dy^*}/(\\frac{pb}{GeV})$'
            elif obs == 'phistareta':
                d['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\phi^{*}_{\\eta} dy_b dy^*}/pb$'
    
            if ysmin>1.5: 
                d['y_subplot_lims'] = [0.0,1.5]
                d['vertical_lines'] = [250 if obs =='zpt' else 5]
            elif ysmin+ybmin>1.0:
                d['y_subplot_lims'] = [0.5,1.5]
            plots.append(d)
    return plots

def plot_crosssection_overview(args=None,obs='zpt',pdf='NNPDF31_nnlo_as_0118',mc='NNLO'):
    plots=[]
    invert_3Dhists(args,obs+'_17Jul2018_by_toy0.root',PLOTSFOLDER+'/unfolded',BUFFERFOLDER+'/unfolded')
    data_source  = [BUFFERFOLDER+'/unfolded/'+obs+'_17Jul2018_by_toy0_binned.root']
    if 'LO' in mc:
        invert_3Dhists(args,obs+'_'+mc+'_'+pdf+'.root',PLOTSFOLDER+'/theory',BUFFERFOLDER+'/theory')
        mc_source = [BUFFERFOLDER+'/theory/'+obs+'_'+mc+'_'+pdf+'_binned.root']
    else:
        invert_3Dhists(args,obs+'_'+mc+'.root',PLOTSFOLDER,BUFFERFOLDER)
        mc_source = [BUFFERFOLDER+'/'+obs+'_'+mc+'_binned.root']
    filelist_binned =  data_source+mc_source
    ybins = [0.0,0.5,1.0,1.5,2.0,2.5]
    ylist = [((xb,yb),(xs,ys))  for (xs,ys) in zip(ybins[:-1],ybins[1:]) for (xb,yb) in zip(ybins[:-1],ybins[1:]) if xb+xs<2.5]
    markerlist = ['^','1','d','+','*','<','2','o','x','>','3','s','v','4','p']
    colorlist = ['red','salmon','crimson','violet','brown','blue','cyan','royalblue','teal','orange','gold','yellow','green','lime','purple']
    scalelist = [1e20,1e19,1e18,1e17,1e16,1e13,1e12,1e11,1e10,1e7,1e6,1e5,1e2,1e1,1e0]
    namelist = ['_yb{}_ys{}'.format(int(2*yboost[0]),int(2*ystar[0])) for (yboost,ystar) in ylist]
    d = ({
        'www': 'crosssections_vs_'+mc,
        'files': [filelist_binned],
        'folders': [''],
        'x_expressions': [('unfolded'+obs+name,'gen'+obs+name) for name in namelist],
        'nicks':       [('unf'+name,'gen'+name) for name in namelist],
        'analysis_modules': ['ScaleHistograms','NormalizeByBinWidth'],
        'scale_nicks':  [('unf'+name,'gen'+name) for name in namelist],
        'scales': [(1e0/35.9/1000*x,1e0/35.9/1000*x) for x in scalelist],
        'x_errors': [0],
        'x_log': True,
        'y_log': True,
        'title': LABELDICT[mc] if mc in ['amc','hpp','mad'] else mc,
        'y_errors': [0],
        'step': [0,1],
        'line_styles': ['','-'],
        'line_widths': [3],
        'zorder': ['unf','gen'],
        'y_lims': [1e-5,1e20] if obs == 'zpt' else [1e-4,1e22],
        'marker_fill_styles': ['none'],
        'markeredgewidth': 2.5,
        'markersize': 12,
        'labelsize': 40,
        'markers': [(x,'') for x in markerlist],
        'colors': [('black',x) for x in colorlist],
        'labels': [('bin'+x,'bin'+x) for x in namelist],
        'filename': obs,
        'x_label': obs,
        'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
        'legend': None,
        'figsize': [10,16],
        'lumis': [35.9],
        'texts': [  r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$" if CMSLABEL else "",
                    r"$35.9\\mathrm{\\,fb}^{-1} \\hspace{0.2}$(13TeV)"],
        'texts_size': [30,25],
        'texts_x':[0.03,(0.64 if obs =='zpt' else 0.65)],
        'texts_y':[1.03,1.035],
    })
    if obs == 'zpt':
        d['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\mathit{p}_T^Z dy_b dy^*}/(\\frac{pb}{GeV})$'
    elif obs == 'phistareta':
        d['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\phi^{*}_{\\eta} dy_b dy^*}/pb$'
    plots.append(d)
    return plots

def plot_crosssection_ratio(args=None,obs='zpt',pdf='NNPDF31_nnlo_as_0118',mc='NNLO'):
    plots=[]
    invert_3Dhists(args,obs+'_17Jul2018_total.root',PLOTSFOLDER+'/uncertainty',BUFFERFOLDER+'/uncertainty')
    data_source  = [BUFFERFOLDER+'/uncertainty/'+obs+'_17Jul2018_total_binned.root']
    if 'LO' in mc:
        invert_3Dhists(args,obs+'_'+mc+'_'+pdf+'.root',PLOTSFOLDER+'/theory',BUFFERFOLDER+'/theory')
        mc_source = [BUFFERFOLDER+'/theory/'+obs+'_'+mc+'_'+pdf+'_binned.root']
    else:
        invert_3Dhists(args,obs+'_'+mc+'.root',PLOTSFOLDER,BUFFERFOLDER)
        mc_source = [BUFFERFOLDER+'/'+obs+'_'+mc+'_binned.root']
    invert_3Dhists(args,obs+'_17Jul2018_systematic.root',PLOTSFOLDER+'/uncertainty',BUFFERFOLDER+'/uncertainty')
    unc_source  = [BUFFERFOLDER+'/uncertainty/'+obs+'_17Jul2018_systematic_binned.root']
    filelist_binned =  data_source+mc_source+unc_source
    ybins = [0.0,0.5,1.0,1.5,2.0,2.5]
    ylist = [((xb,yb),(xs,ys))  for (xs,ys) in zip(ybins[:-1],ybins[1:]) for (xb,yb) in zip(ybins[:-1],ybins[1:]) if xb+xs<2.5]
    markerlist = ['^','1','d','+','*','<','2','o','x','>','3','s','v','4','p']
    colorlist = ['red','salmon','crimson','violet','brown','blue','cyan','royalblue','teal','orange','gold','yellow','green','lime','purple']
    namelist = ['_yb{}_ys{}'.format(int(2*yboost[0]),int(2*ystar[0])) for (yboost,ystar) in ylist]
    d = ({
        'www': 'crosssections_vs_'+mc,
        'files': [filelist_binned],
        'folders': [''],
        'x_expressions': [(obs+'_total'+name,'gen'+obs+'_asym'+name,obs+'_systematic'+name) for name in namelist],
        'nicks':       [('unf'+name,'gen'+name,'unc'+name) for name in namelist],
        'x_errors': [0],
        'y_errors': [0],
        'x_log': True,
        'title': LABELDICT[mc] if mc in ['amc','hpp','mad'] else mc,
        'marker_fill_styles': ['none'],
        'markeredgewidth': 2.5,
        'markersize': 12,
        'labelsize': 40,
        'labels': [('bin'+x,'bin'+x) for x in namelist],
        'filename': obs,
        'x_label': obs,
        'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
        'x_lims': [25,1000] if obs =='zpt' else [0.4,50],
        'legend': None,
        'figsize': [10,16],
        'lumis': [35.9],
        'texts': [  r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$" if CMSLABEL else "",
                    r"$35.9\\mathrm{\\,fb}^{-1} \\hspace{0.2}$(13TeV)"],
        'texts_size': [30,25],
        'texts_y':[1.03,1.035],
        'filename': obs+'_ratio',
        'analysis_modules': ['Ratio','AddHistograms'],
        'ratio_numerator_nicks':   [('unf'+name,  'gen'+name,  'unf'+name, 'unc'+name) for name in namelist],
        'ratio_denominator_nicks': [('unf'+name,  'gen'+name,  'gen'+name, 'gen'+name) for name in namelist],
        'ratio_result_nicks':    [('unity'+name,'scale'+name,'ratio'+name,'syst'+name) for name in namelist],
        'add_nicks':             [('unity'+name+' ratio'+name,'unity'+name+' scale'+name,'unity'+name+' ratio'+name,'unity'+name+' syst'+name) for name in namelist],
        'add_result_nicks':      [('stacked1'+name,           'stacked2'+name,           'stacked3'+name,           'stacked4'+name) for name in namelist],
        'add_no_error_scale': [True],
        'zorder': len(namelist)*[2]+len(namelist)*[1]+len(namelist)*[3]+len(namelist)*[4],
        'step':   3*len(namelist)*[1]+len(namelist)*[0],
        'line_styles':  [''],
        'line_widths': [1.5],
        'labels': ['bin'+x for x in namelist],
        'markers': len(namelist)*['fill']+2*len(namelist)*['errorband']+markerlist[:len(namelist)],
        'hatch':   len(namelist)*['//']+len(namelist)*['']+len(namelist)*['']+len(namelist)*[''],
        'colors':  len(namelist)*['gray']+len(namelist)*['grey']+colorlist[:len(namelist)]+len(namelist)*['black'],
        'nicks_whitelist': ['stacked4','stacked3','stacked2','stacked1'],
        'alphas': len(namelist)*[1]+3*len(namelist)*[0.707],
        'subplot_nicks': ['dummy'],
        'lines_styles': ['-',':',':'],
        'y_label': 'Ratio to theory',
        'y_lims': [0.5,15.5],
        'add_scale_factors': [(str(len(ylist)-x-1)+' 1',str(len(ylist)-x-1)+' 1',str(len(ylist)-x-1)+' 1',str(len(ylist)-x-1)+' 1') for x in xrange(len(ylist))],
        'lines': [(0.5+x,0.75+x,1.25+x) for x in xrange(len(namelist))],
        'y_ticks': [(0.75+x,1.0+x,1.25+x) for x in xrange(len(namelist))],
        'texts_x':[0.03,(0.65 if obs =='zpt' else 0.66)],
    })
    plots.append(d)
    return plots

##########################################################################################################################################################
# To create all possible plots
def plot_all(args=None):
    plots=[]
    for obs in ['zpt','phistareta']:
      for mc in ['mad','amc']:
        for data in ['17Jul2018']:
            plots+=plot_datamc(obs=obs, data=data, mc=mc)
      plots+=plot_uncertainties(obs=obs)
      plots+=plot_crosssections(obs=obs,mclist=['mad','amc'])
      plots+=plot_crosssections(obs=obs,pdf='NNPDF31_nnlo_as_0118',mclist=['NLO','NNLO'])
      plots+=plot_crosssection_overview(obs=obs,pdf='NNPDF31_nnlo_as_0118',mc='NNLO')
      plots+=plot_crosssection_ratio(obs=obs,pdf='NNPDF31_nnlo_as_0118',mc='NNLO')
      for mc in ['mad','hpp']:
        plots+=plot_resolution(obs=obs, mc=mc)
        plots+=plot_chi2(obs=obs, mc=mc)
        plots+=plot_unfolding_closure(obs=obs, mc=mc)
      plots+=plot_unfolding_closure(obs=obs, mc='toy0')
      plots+=plot_unfolding_closure(obs=obs, mc='toy2')
    return [PlottingJob(plots=plots,args=args)]


