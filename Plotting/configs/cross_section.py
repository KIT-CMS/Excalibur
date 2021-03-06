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

def error(a,b,c):
    # gives the root of the squared sum of a,b,c
    return np.sqrt(a**2+b**2+c**2)

ticks = ({
    'zpt': [40, 60, 100, 200, 400, 1000],
    'phistareta': [1, 2, 4, 10, 25, 100],
    })
variationstring=({1:'Up',0: '',-1:'Down'})

basiccutstring = ({
    '_zpt30':                       '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)*(zpt>30)',
    '_phistareta08':                '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)*(phistareta>0.8)',
    '_jet1pt30':                    '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)*(jet1pt>30)',
    '_phistareta08_jet1pt10':       '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)*(phistareta>0.8)*(jet1pt>10)',
    '_zpt30_jet1pt10':              '(abs(mupluseta)<2.4)*(abs(muminuseta)<2.4)*(mupluspt>25)*(muminuspt>25)*(abs(zmass-91.1876)<20)*(zpt>30)*(abs(jet1y)<2.4)*(jet1pt>10)',
    'gen_zpt30':                    '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)*(genzpt>30)',
    'gen_phistareta08':             '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)*(genphistareta>0.8)',
    'gen_jet1pt30':                 '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)*(genjet1pt>30)',
    'gen_phistareta08_jet1pt10':    '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)*(genphistareta>0.8)*(genjet1pt>10)',
    'gen_zpt30_jet1pt10':           '(abs(genmupluseta)<2.4)*(abs(genmuminuseta)<2.4)*(genmupluspt>25)*(genmuminuspt>25)*(abs(genzmass-91.1876)<20)*(genzpt>30)*(genjet1pt>10)',
    })

datasets = ({
    'BCDEFGH' : '/storage/c/tberger/excalibur_results_xsec/2018-09-11/data16_mm_BCDEFGH_SiMu07Aug17.root',
    'amc' :     '/storage/c/tberger/excalibur_results_xsec/2018-09-11/mc16_mm_BCDEFGH_DYtoLLamcatnlo.root',
    'hpp' :     '/storage/c/tberger/excalibur_results_xsec/2018-09-11/mc16_mm_BCDEFGH_DYtoLLherwigpp.root',
    'TTJets' :  '/storage/c/tberger/excalibur_results_xsec/2018-09-11/mc16_mm_BCDEFGH_TTJetsmadgraph.root',
    'ZZ' :      '/storage/c/tberger/excalibur_results_xsec/2018-09-11/mc16_mm_BCDEFGH_ZZpythia8.root',
    'WZ' :      '/storage/c/tberger/excalibur_results_xsec/2018-09-11/mc16_mm_BCDEFGH_WZpythia8.root',
    'WW' :      '/storage/c/tberger/excalibur_results_xsec/2018-09-11/mc16_mm_BCDEFGH_WWpythia8.root',
    'WJets' :   '/storage/c/tberger/excalibur_results_xsec/2018-09-11/mc16_mm_BCDEFGH_WJetsToLNumadgraph.root',
    'ST':       '/storage/c/tberger/excalibur_results_xsec/2018-09-11/mc16_mm_BCDEFGH_ST.root',
    })

######################################################################################################################################################
# delivers dictionary and sets basic options which are similar to all plots, i.e. a basic dictionary and strings that define the cutflow and weights
def basic_xsec(args=None, obs='zpt', cut='_zpt30_jet1pt10', data='BCDEFGH', mc='amc', yboostbin=None,ystarbin=None):
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
            #'title': namestring,
            'cutlabel': False,
            'filename' : obs,
            'texts_x': [0.03],
            'texts_y': [0.99,0.91,0.84],
            'texts_size': [15],
            'ratio_denominator_no_errors' : False,
            'subplot_fraction': 40,
            #'lumis' : [35.8],
    })
    if not data in ['amc','hpp']:
        get_lumis(args, d, data, 2016)
    cutlabel(args,d,cut)
    if yboostbin and ystarbin:
        d['texts']+=[r'${}<y_b<{}$, ${}<y^*<{}$'.format(yboostbin[0],yboostbin[1],ystarbin[0],ystarbin[1])]
        d['texts_y']+=[0.75]
    binningsZJet.rebinning(args,d,obs,yboostbin,ystarbin)
    return [d, cutstring, gencutstring, weightstring, namestring]

def genrecocomparisons(args=None, obs='zpt', cut='_zpt30_jet1pt10', data='amc', mc='amc', yboostbin=None, ystarbin=None):
    # delivers dictionary to plot distributions in gen level compared to reco level
    # (including a comparison between applied and non-applied efficiency corrections, inofficially called Scale Factors (SF))
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    d.update({
        'files': [  datasets[mc],],
        'zjetfolders': ['zjetcuts_L1L2L3','zjetcuts_L1L2L3','genzjetcuts_L1L2L3'],
        #'zjetfolders': ['leptoncuts','leptoncuts','genleptoncuts'],
        'nicks': ['nosf','reco','gen'],
        'x_expressions': [obs,obs,'gen'+obs],
        'y_lims': [1e-2,1e5],
        'weights' : [cutstring,cutstring+'*'+weightstring,gencutstring],
        'www': 'comparison_Gen-Reco_'+mc+cut+namestring,
        'analysis_modules': ['NormalizeByBinWidth','Ratio'],#
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
        'y_subplot_lims': [0.65,1.35],
        'labels': ['Reco(uncorrected)','Reco(corrected)','Gen','Reco(uncorrected)/Gen','Reco(corrected)/Gen'],
        'markers': ['.'],
        'colors': ['purple','red','blue','purple','red'],
    })
    return d

def datamccomparisons(args=None, obs='zpt', cut='_zpt30_jet1pt10', data='BCDEFGH', mc='amc', yboostbin=None, ystarbin=None):
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
        'zjetfolders': ['zjetcuts_L1L2L3Res']+7*['zjetcuts_L1L2L3'],
        'nicks': ['data','DY','TTJets','ZZ','WZ','WW','ST','WJets'],
        'www': 'comparison_Data-MC_'+mc+cut+namestring,
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
        'y_subplot_lims': [0.75,1.25],
        'y_subplot_label': 'Sim/Data',
        'y_lims': [1e-2,1e9],
    })
    return d

def responsematrix(args=None, obs='zpt', cut='_zpt30_jet1pt10', data='amc', mc='amc', yboostbin=None, ystarbin=None):
    # delivers dictionary to write the response matrix as well gen level and reco level distributions (SF applied!) to root file
    # root file can be used as unfolding and plot_matrix input
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    d.update({
        'files': [datasets[mc],],
        'folders': ['allzjetcuts_L1L2L3/ntuple','zjetcuts_L1L2L3/ntuple','genzjetcuts/ntuple'],
        'nicks': ['response','reco'+obs,'gen'+obs],
        'weights' : [cutstring+'*'+gencutstring+'*'+weightstring,cutstring+'*'+weightstring,gencutstring],
        #'no_weight': True,
        'x_expressions': [obs,obs,'gen'+obs],
        'x_label': 'reco'+obs,
        'y_expressions': ['gen'+obs,None,None],
        'y_bins': obs,
        'y_label': 'gen'+obs,
        'y_log': obs in ['zpt','phistareta'],
        'z_lims': [1e0,1e4],
        'z_log': True,
        'filename' : obs+namestring,
        #'nicks_whitelist': ['response'],
        #'www': 'response'+cut,
        'output_dir' : '/storage/c/tberger/plots/response/responsematrix_'+mc+cut,
        'file_mode': ('RECREATE'),
        'plot_modules': ['ExportRoot'],
    })
    return d

def plot_matrix(args=None, obs='zpt', cut='_zpt30_jet1pt10', data='amc', mc='amc', yboostbin=None, ystarbin=None, resolution='_rms', variation=0, varquantity='_resolution'):
    # delivers dictionary to plot matrices from root files created either from MC files, toy MC files or unfolding covariance files
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    # specify source file and matrix (TH2D hist) name manually
    if not mc=='toy':
        resolution, variation = '',0
    if variation==0:
        varquantity = ''
    matrix_source = '/storage/c/tberger/plots/response/responsematrix_'+mc+cut+'/'+obs+namestring+resolution+varquantity+variationstring[variation]+'.root'
    matrix_name = 'response'
    #matrix_source = '/storage/c/tberger/plots/unfolding/covariance_'+data+'_by_'+mc+cut+'/covmat_'+obs+namestring+resolution+'.root'
    #matrix_name = 'corr_matrix'
    d.update({
        'files': [matrix_source],
        'folders': [''],
        'nicks': ['response'],
        'x_expressions': [matrix_name],
        'x_label': 'reco'+obs,
        'y_label': 'gen'+obs,
        'y_log': obs in ['zpt','phistareta'],
        'y_ticks': ticks[obs] if obs in ['zpt','phistareta'] else None,
        'z_log': True,
        #'z_lims':[-1,1],
        'z_lims':[1e-1,1e5],
        'www': matrix_name+'_'+mc+cut+namestring+resolution+varquantity+variationstring[variation],
        'filename': obs,
        'colormap': 'jet',#'bwr',#'hsv',#'seismic',#
    })
    #d['y_ticks']=d['x_ticks']
    return d

######################################################################################################################################################
# writes a ROOT file that contains the distributions of the observable's resolution in each bin 
# and profile plots of the RMS/fakerate/purity/stability/acceptance over bins
def resolution(args=None, obs='zpt', cut='_zpt30_jet1pt10', data='amc', mc='amc', yboostbin=None, ystarbin=None):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    outpath = "/storage/c/tberger/plots/resolution/resolution_"+mc+cut+"/"+obs+namestring+".root"
    file_in = ROOT.TFile(datasets[mc],"READ")
    ntuple_gen, ntuple_reco = file_in.Get("genleptoncuts_L1L2L3/ntuple"), file_in.Get("leptoncuts_L1L2L3/ntuple")
    N_gen, N_reco = 1.0*ntuple_gen.GetEntries(gencutstring), 1.0*ntuple_reco.GetEntries(cutstring)
    if cut=='_zpt30_jet1pt10':
        ntuple_gen, ntuple_reco = file_in.Get("genzjetcuts_L1L2L3/ntuple"), file_in.Get("zjetcuts_L1L2L3/ntuple")
    if d['x_bins'] == obs:
        bins = binningsZJet.BinningsDictZJet.binnings_dict[obs]
    else:
        bins = [float(x) for x in d['x_bins'][0].split(' ')]
    N = 50
    hmin, hmax = -0.2,0.2
    if obs in ['jet1y','yboost','ystar']:
        hmin, hmax = -1.0, 1.0
    if obs in ['jet1pt']:
        hmin, hmax = -1.0, 2.0
    # safety step to avoid overwriting of existing files
    if os.path.exists(outpath):
        print "file "+outpath+" already exists. Check if it can be removed!"
        return
    file_out = ROOT.TFile(outpath,"RECREATE")
    histlist = ["rms","sigma","SF","fakerate","acceptance","stability","purity","PU","matched","switched"]#,"negEvents"
    h_weight = ROOT.TH1D("weight","", len(bins)-1, array('d',bins))
    [h_rms, h_sigma, h_SF, h_fake, h_acceptance, h_stability, h_purity, h_PU, h_match, h_switch] = [h_weight.Clone(name) for name in histlist]#, h_neg
    for j in xrange(len(bins)-1):
        genmin, genmax = 1.0*bins[j], 1.0*bins[j+1]
        print "resolution estimation in", genmin, "to", genmax
        binname = "_{}_{}".format(int(genmin),int(genmax))
        if obs in ['zy','jet1y','yboost','ystar']:
            binname = "_{}_{}".format(int(genmin*10),int(genmax*10))
        h_resolution = ROOT.TH1D("resolution"+binname,"",N,hmin,hmax)
        h_genweight, h_SFweight = ROOT.TH1D("genweight","",4,-2,2), ROOT.TH1D("SFweight","",4,0,2)
        print 'fill histograms'
        ntuple_gen.Draw("(("+obs+"/gen"+obs+")-1)>>resolution"+binname,(gencutstring+"*(gen"+obs+">{})*(gen"+obs+"<{})").format(genmin,genmax),"goff")
        ntuple_gen.Draw("weight>>genweight",(gencutstring+"*(gen"+obs+">{})*(gen"+obs+"<{})").format(genmin,genmax),"goff")
        ntuple_reco.Draw("("+weightstring+")>>SFweight",(cutstring+"*("+obs+">{})*("+obs+"<{})").format(genmin,genmax),"goff")
        h_resolution.Fit("gaus")
        genweight = h_genweight.GetMean()
        print 'count events'
        # events with negative weight in gen bin:
        #N_genbinneg  = 1.0*ntuple_gen.GetEntries((gencutstring+"*(weight<0)*(gen"+obs+">{})*(gen"+obs+"<{})").format(genmin,genmax))
        # events in gen bin:
        N_genbin  = 1.0*ntuple_gen.GetEntries((gencutstring+"*(gen"+obs+">{})*(gen"+obs+"<{})").format(genmin,genmax))
        # events in reco bin: h_SFbinweight.GetMean()*
        N_recobin = 1.0*ntuple_reco.GetEntries((cutstring+"*("+obs+">{})*("+obs+"<{})").format(genmin,genmax))
        # events in gen bin that pass global reco selection:
        N_reco_genbin  = 1.0*ntuple_gen.GetEntries((cutstring+"*"+gencutstring+"*(gen"+obs+">{})*(gen"+obs+"<{})").format(genmin,genmax))
        # events in reco bin that pass global gen selection: h_SFbinweightgen.GetMean()*
        N_gen_recobin  = 1.0*ntuple_reco.GetEntries((gencutstring+"*"+cutstring+"*("+obs+">{})*("+obs+"<{})").format(genmin,genmax))
        # events in gen AND reco bin:
        N_genbin_recobin = 1.0*ntuple_gen.GetEntries((cutstring+"*"+gencutstring+"*(gen"+obs+">{})*(gen"+obs+"<{})*("+obs+">{})*("+obs+"<{})").format(genmin,genmax,genmin,genmax))
        # events with PU leading jet in gen bin:
        N_PU  = 1.0*ntuple_reco.GetEntries(("(matchedgenjet1pt<0)*"+cutstring+"*("+obs+">{})*("+obs+"<{})").format(genmin,genmax))
        # events with correctly matched leading jet
        N_match  = 1.0*ntuple_reco.GetEntries(("(matchedgenjet1pt>0)*(matchedgenjet1pt==genjet1pt)*"+cutstring+"*("+obs+">{})*("+obs+"<{})").format(genmin,genmax))
        # events with incorrectly matched leading jet
        N_switch  = 1.0*ntuple_reco.GetEntries(("(matchedgenjet1pt>0)*(matchedgenjet1pt<genjet1pt)*"+cutstring+"*("+obs+">{})*("+obs+"<{})").format(genmin,genmax))
        
        h_rms.SetBinContent(j+1,h_resolution.GetRMS())
        h_sigma.SetBinContent(j+1,h_resolution.GetFunction("gaus").GetParameter(2))
        h_weight.SetBinContent(j+1,genweight*N_genbin/N_gen)
        h_SF.SetBinContent(j+1,h_SFweight.GetMean())
        #h_neg.SetBinContent(j+1,N_genbinneg/N_genbin)
        h_fake.SetBinContent(j+1,1-N_gen_recobin/N_recobin)
        h_acceptance.SetBinContent(j+1,N_reco_genbin/N_genbin)
        h_purity.SetBinContent(j+1,N_genbin_recobin/N_recobin)
        h_stability.SetBinContent(j+1,N_genbin_recobin/N_genbin)
        h_PU.SetBinContent(j+1,N_PU/N_recobin)
        h_match.SetBinContent(j+1,N_match/N_recobin)
        h_switch.SetBinContent(j+1,N_switch/N_recobin)
        
        h_rms.SetBinError(j+1,h_resolution.GetRMSError())
        h_sigma.SetBinError(j+1,h_resolution.GetFunction("gaus").GetParError(2))
        h_weight.SetBinError(j+1,error(h_genweight.GetMeanError()*N_genbin/N_gen,genweight*np.sqrt(N_genbin)/N_gen,genweight*N_genbin/N_gen**2*np.sqrt(N_gen)))
        h_SF.SetBinError(j+1,h_SFweight.GetMeanError())
        h_fake.SetBinError(j+1, error(  (N_recobin-N_gen_recobin)/N_recobin**2*np.sqrt(N_gen_recobin),
                                        (N_gen_recobin)/N_recobin**2*np.sqrt(N_recobin-N_gen_recobin),
                                        0))
        h_acceptance.SetBinError(j+1,error( (N_genbin-N_reco_genbin)/N_genbin**2*np.sqrt(N_reco_genbin),
                                            (N_reco_genbin)/N_genbin**2*np.sqrt(N_genbin-N_reco_genbin),
                                            0))
        h_purity.SetBinError(j+1,error( (N_genbin_recobin)/N_recobin**2*np.sqrt(N_recobin-N_genbin_recobin),
                                        (N_recobin-N_genbin_recobin)/N_recobin**2*np.sqrt(N_genbin_recobin),
                                        0))
        h_stability.SetBinError(j+1,error(  (N_genbin_recobin)/N_genbin**2*np.sqrt(N_genbin-N_genbin_recobin),
                                            (N_genbin-N_genbin_recobin)/N_genbin**2*np.sqrt(N_genbin_recobin),
                                            0))
        h_PU.SetBinError(j+1,np.sqrt(N_PU/N_recobin*(1-N_PU/N_recobin)/N_recobin))
        h_match.SetBinError(j+1,np.sqrt(N_match/N_recobin*(1-N_match/N_recobin)/N_recobin))
        h_switch.SetBinError(j+1,np.sqrt(N_switch/N_recobin*(1-N_switch/N_recobin)/N_recobin))
        h_genweight.Delete()
        h_SFweight.Delete()
        h_resolution.Write()
    h_resolution.Delete()
    file_out.Write()
    file_out.Close()
    print "resolution information written to "+outpath
    return

def plot_resolutionrootfiles(args=None, obs='zpt', cut='_zpt30_jet1pt10', data='amc', mc='amc', yboostbin=None, ystarbin=None, variation=0, resolution='_rms', varquantity='_resolution'):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    d.update({
        'files': [  "/storage/c/tberger/plots/resolution/resolution_"+mc+cut+"/"+obs+namestring+".root"],
        'folders': [''],
        'x_expressions': ['fakerate','acceptance','purity','stability','sigma','rms','PU','matched','switched'],
        'x_label': obs,
        'markers': ['.'],
        'nicks': ['F','A','P','S','SIG','RMS','PU','MA','SW'],
        'y_log':False,
        'y_lims': [0,1.25],
        'y_label': '',
        'www': 'resolution_'+mc+cut+namestring,
        'lines': [1],
        #'subplot_fraction': 50,
        #'subplot_legend': 'upper right',
        #'subplot_lines': [0,1],
        #'y_subplot_lims': [-0.05,1.05],
        #'y_subplot_label': 'Fakerate & Acceptance',
        #'output_dir': 'resolutionplots'+cut+namestring,
        
        #'nicks_whitelist':['SIG','RMS'],
        #'labels': ['Gaussian Width','RMS'],
        #'filename' : obs,
        #'colors': ['green','blue'],
        #'y_lims': [0.01,0.1],
        
        'nicks_whitelist':['PU','MA','SW'],
        'labels': ['PU','matched leading jet','switched leading jet'],
        'filename' : 'fraction_'+obs,
        'markers': ['fill'],
        'stacks': ['stack'],
        'colors': ['grey','steelblue','orange'],
        
        #'nicks_blacklist':['SIG','RMS','MA','SW','PU','P','S'],
        #'labels': ['Fakerate','Acceptance'],
        #'filename' : 'rates_'+obs,
    })
    return d
    
######################################################################################################################################################
# writes a ROOT file that contains a toy response matrix derived from the resolution information
def toymontecarlo(args=None, obs='zpt', cut='_zpt30_jet1pt10', data='amc', mc='amc', yboostbin=None, ystarbin=None, variation=0, resolution='_rms', varquantity='_resolution'):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    inpath = "/storage/c/tberger/plots/resolution/resolution_"+mc+cut+"/"+obs+namestring+".root"
    if not variation==0:
        outpath = "/storage/c/tberger/plots/response/responsematrix_toy"+cut+"/"+obs+namestring+resolution+varquantity+variationstring[variation]+".root"
    else:
        outpath = "/storage/c/tberger/plots/response/responsematrix_toy"+cut+"/"+obs+namestring+resolution+".root"
    print "resolution information taken from", inpath
    if d['x_bins'] == obs:
        bins = binningsZJet.BinningsDictZJet.binnings_dict[obs]
    else:
        bins = [float(x) for x in d['x_bins'][0].split(' ')]
    file_in = ROOT.TFile(inpath,"READ")
    h_sigma = file_in.Get(resolution.replace('_',''))
    h_weight = file_in.Get("weight")
    h_SF =file_in.Get("SF")
    h_fake =file_in.Get("fakerate")
    h_acceptance = file_in.Get("acceptance")
    h_stability = file_in.Get("stability")
    h_purity = file_in.Get("purity")
    # safety step to avoid overwriting of existing files
    if os.path.exists(outpath):
        print "file "+outpath+" already exists. Check if it can be removed!"
        return
    file_out = ROOT.TFile(outpath,"RECREATE")
    h_toygen = ROOT.TH1D("gen"+obs,"", len(bins)-1, array('d',bins))
    h_toyreco = ROOT.TH1D("reco"+obs,"",len(bins)-1, array('d',bins))
    h_toyresponse = ROOT.TH2D("response","", len(bins)-1, array('d',bins),len(bins)-1, array('d',bins))
    for j in xrange(len(bins)-1):
        N_toy = 1000000
        genmin = bins[j]
        genmax = bins[j+1]
        print "create toys in", genmin, "to", genmax
        sigma = h_sigma[j+1]
        if varquantity=='_resolution':
            sigma+=variation*h_sigma.GetBinError(j+1)
        weight = h_weight[j+1]
        if varquantity=='_weight':
            weight+=variation*h_weight.GetBinError(j+1)
        SF = h_SF[j+1]*h_acceptance[j+1]/(1-h_fake[j+1])
        if varquantity=='_SF':
            SF+=variation*error(h_SF.GetBinError(j+1)*h_acceptance[j+1]/(1-h_fake[j+1]),h_SF[j+1]*h_acceptance.GetBinError(j+1)/(1-h_fake[j+1]),-h_SF[j+1]*h_acceptance[j+1]/(1-h_fake[j+1])**2*h_fake.GetBinError(j+1))
        for i in xrange(N_toy):
            genrand = genmin+(genmax-genmin)*np.random.random()
            recorand = genrand*(1+sigma*np.random.randn())
            h_toygen.Fill(genrand,weight)
            h_toyreco.Fill(recorand,weight*SF)
            h_toyresponse.Fill(recorand,genrand,weight*SF)
    file_out.Write()
    file_out.Close()
    print "toyMC written to "+outpath
    return

######################################################################################################################################################
# delivers dictionary to plot unfolding results using response matrix specified by source file
# together with the corresponding reco distribution (and the gen distribution incl. ratio to unfolding if data input is MC)
def unfolding(args=None, obs='zpt', cut='_zpt30_jet1pt10', data='BCDEFGH', mc='amc', yboostbin=None, ystarbin=None, 
                method='tunfold', resolution='_rms', variation=0, varquantity='_statistics'):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    # specify source file
    response_source = '/storage/c/tberger/plots/response/responsematrix_'+mc+cut+'/'+obs+namestring+resolution+varquantity+variationstring[variation]+'.root'
    if not mc=='toy':
        resolution, varquantity= '','_statistics'
        response_source = '/storage/c/tberger/plots/response/responsematrix_'+mc+cut+'/'+obs+namestring+resolution+'.root'
    if variation==0:
        varquantity = ''
        response_source = '/storage/c/tberger/plots/response/responsematrix_'+mc+cut+'/'+obs+namestring+resolution+'.root'
    output_path = '/storage/c/tberger/plots/unfolding/covariance_'+data+'_by_'+mc+cut
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
        'folders': ['']+['leptoncuts_L1L2L3Res/ntuple']+6*['leptoncuts_L1L2L3/ntuple']+2*[''],
        'nicks': ['responsematrix','data','TTJets','ST','ZZ','WZ','WW','WJets','reco','gen'],
        'weights' :(['1']
                    +7*[cutstring+'*'+weightstring]
                    +2*['1']
                    ),
        'x_expressions': ['response']+7*[obs]+['reco'+obs]+['gen'+obs],
        'analysis_modules': ['SumOfHistograms','Unfolding','Ratio'],#,'NormalizeByBinWidth'],
        'sum_nicks' : ['data TTJets ST ZZ WZ WW WJets'],
        'sum_scale_factors' : ['1'+6*' -1'],
        'sum_result_nicks' : ['signal'],
        'unfolding_variation': variation if varquantity=='_statistics' else 0,
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
        'y_subplot_lims': [0.5,1.5],
        'y_lims': [1e1,1e8],
        'markers': ['.'],
        'colors': ['black','red','red'],
        'www': None,#'comparison_Unfold_'+data+'_by_'+mc+cut+namestring+resolution+varquantity+variationstring[variation],
        'filename' : 'unfolded'+obs,
        #'output_dir' : output_path,
        #'filename' : obs+namestring+resolution+varquantity+variationstring[variation],
        'unfold_file' : [output_path+'/covmat_'+obs+namestring+resolution+varquantity+variationstring[variation]+'.root'],
        'write_matrix' : True,
    })
    # need to check if unfold_file directory exists and create it if necessary
    print 'response matrix has been taken from',response_source
    if (d['write_matrix']):
        print 'output will be written to',d['unfold_file'][0]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
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

def plot_unfoldingrootfiles(args=None, obs='zpt', cut='_zpt30_jet1pt10', data='amc', mc='amc', yboostbin=None, ystarbin=None, resolution='_rms', varquantity='_statistics', variation=0):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    if (not mc=='toy'):
        print 'the only variation possible for this MC is statistical'
        resolution, varquantity = '','_statistics'
    d.update({
        'files': [  '/storage/c/tberger/plots/unfolding/covariance_'+data+'_by_'+mc+cut+'/covmat_'+obs+namestring+resolution+varquantity+variationstring[-1]+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_'+data+'_by_'+mc+cut+'/covmat_'+obs+namestring+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_'+data+'_by_'+mc+cut+'/covmat_'+obs+namestring+resolution+varquantity+variationstring[1]+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_'+data+'_by_'+mc+cut+'/covmat_'+obs+namestring+resolution+'.root',
                    '/storage/c/tberger/plots/response/responsematrix_'+data+cut+'/'+obs+namestring+'.root',
                    ],
        'folders': [''],
        'x_expressions': ['truth_hist','truth_hist','truth_hist','data_hist','gen'+obs],
        'nicks': ['unfolddown','unfolded','unfoldup','reco'+obs,'gen'+obs],
        'analysis_modules': ['NormalizeByBinWidth','Ratio','SumOfHistograms'],
        'ratio_denominator_nicks': ['unfolddown','unfolded','unfoldup','reco'+obs,'gen'+obs],
        'ratio_numerator_nicks': ['unfolded'],
        'ratio_result_nicks' : ['ratiodown','ratiounfold','ratioup','ratioreco','ratiogen'],
        'sum_nicks' : ['ratiounfold ratiounfold','ratiodown ratiounfold','ratioup ratiounfold','ratiounfold ratiodown','ratiounfold ratioup'],
        'sum_result_nicks' : ['sumunf','sumdown1','sumup1','sumdown2','sumup2'],
        'sum_scale_factors' : ['0.707 -0.707'],
        'title': varquantity.split('_')[1],
        #'subplot_nicks': ['sum'],
        'subplot_fraction': 40,
        'x_label': obs,
        'www': 'comparison_Unfold_'+data+'_by_'+mc+cut+namestring+resolution+varquantity+variationstring[variation],
        'subplot_legend': 'upper left',
        #'nicks_whitelist':['unfolddown','unfolded','unfoldup','reco'+obs,'gen'+obs,'sumunf','sumdown1','sumup1','sumdown2','sumup2'],
        'nicks_whitelist':['sumunf','sumdown1','sumup1','sumdown2','sumup2'],
        'filename' : obs+'_variation',#_highN',#+namestring+resolution+varquantity,
        'ratio_denominator_no_errors': True,
        'y_lims': [-0.07,0.07],
        'y_subplot_lims': [-0.5,0.5],
        'y_log': False,
        'y_label': 'Relative Uncertainties',
        'legend': 'lower right',
        #'labels': ['Unfolded(Down)','Unfolded','Unfolded(Up)','Measured','Gen (->Measured)','Relative Unfolding Uncertainties','Systematic Variation','','',''],
        'labels': ['Statistical Uncertainties','Systematic Variation','','',''],
        #'markers': ['.','.','.','.','.','.','fill','fill','fill','fill'],
        'markers': ['.','fill','fill','fill','fill'],
        #'colors': ['gray','black','darkgray','red','blue','black','yellow','yellow','yellow','yellow'],
        'colors': ['black','yellow','yellow','yellow','yellow'],
        #'y_errors': [False,True,False,True,True,True,False,False,False,False],
        'y_errors': [True,False,False,False,False],
        #'nicks_whitelist':['unfolded','reco','gen'],#'ratio'],
        #'filename' : obs,#_highN',#+namestring+resolution+varquantity,
        ##'ratio_denominator_no_errors': [True,True,True,False,False],
        #'y_lims': [1e-1,1e6],
        #'y_subplot_lims': [0.5,1.5],
        #'y_log': obs in ['zpt','phistareta'],
        #'subplot_legend': 'upper right',
        #'labels': ['Unfolded','Measured','Unfolded/Measured','Gen (->Measured)','Unfolded/Gen','','',''],
        #'markers': ['.']*5+['fill']*2+['.'],
        #'colors': ['black','red','red','blue','blue','yellow','white','black'],
        
    })
    if data=='BCDEFGH':
        d['files'].pop()
        d['x_expressions'].pop()
        d['ratio_denominator_nicks'].pop()
        d['ratio_result_nicks'].pop()
    return d
    
def print_unfoldingrootfiles(args=None, obs='zpt', cut='_zpt30_jet1pt10', data='amc', mc='amc', yboostbin=None, ystarbin=None, resolution='_rms', varquantity='_statistics', variation=0):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    if (not mc=='toy'):
        print 'the only variation possible for this MC is statistical'
        resolution, varquantity = '','_statistics'
    d.update({
        #'files': ['/storage/c/tberger/plots/unfolding/covariance_'+data+'_by_'+mc+cut+'/covmat_'+obs+namestring+resolution+varquantity+variationstring[0]+'.root'],
        'files': ['/storage/c/tberger/plots/unfolding/covariance_'+data+'_by_'+mc+cut+'/covmat_'+obs+namestring+resolution+variationstring[0]+'.root'],
        'folders' : [''],
        'analysis_modules': ['NormalizeByBinWidth','PrintResults'],
        'filename' : '/storage/c/tberger/plots/results/crosssections_'+data+'_by_'+mc+cut+'/'+obs+namestring,
        'nicks' : [obs],
        'x_expressions': ['truth_hist'],
        'plot_modules': ['ExportRoot'],
    })
    return d  

def plot_crosssection(args=None, obs='zpt', cut='_zpt30_jet1pt10', data='BCDEFGH', mc='amc', yboostbin=None, ystarbin=None, resolution='_rms'):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    d.update({
        'files': [  '/storage/c/tberger/plots/unfolding/covariance_'+data+'_by_toy'+cut+'/covmat_'+obs+namestring+resolution+'.root',
                    '/storage/c/tberger/plots/response/responsematrix_'+mc+cut+'/'+obs+namestring+'.root',
                    ],
        'folders' : [''],
        'x_expressions': ['data_hist','gen'+obs],
        'y_lims':[1e-6,1e2],
        'y_subplot_lims': [0.65,1.35],
        'y_subplot_label': 'Sim/Data',
        'y_label': r'$ \\frac{d^3\\mathit{\\sigma}}{d\\mathit{p}_T^Z d\\mathit{y_b} d\\mathit{y^*}}/(\\frac{p\\mathit{b}}{GeV})$',
        'nicks': ['data','sim'],
        'analysis_modules': ['NormalizeByBinWidth','ScaleHistograms','Ratio'],
        'ratio_numerator_nicks': ['sim'],
        'ratio_denominator_nicks': ['data'],
        'ratio_result_nicks' : ['ratio'],
        'scale_nicks': ['data','sim'],
        'scales':[1e0/35.8*4/1000,1e0/1.0*4/1000],
        'www': 'comparison_Results_'+data+'_'+mc+cut+namestring,
        'markers':['d','_'],
        'lumis' : [35.8],
        'labels': ['Data','Sim'],
    })
    return d
    
######################################################################################################################################################
# uses previously created dictionaries to plot in a loop
def plotloop(args=None):
    plots = []
    ybins = [0.0,0.5]#,1.0,1.5,2.0,2.5]
    for cut in ['_zpt30_jet1pt10']:#]:#'_mupt25_zmass20_zpt30','_mupt25_zmass20_zpt30_jet24',
     for obs in ['zpt']:#,'zy','zmass','jet1pt','jet1y','mupluspt','mupluseta','muminuspt','muminuseta']:#['yboost','ystar']:#,'jet2pt','jet2y']:
      for yboostbin in zip(ybins[:-1],ybins[1:]):#[(0.0,0.5)]: #
       for ystarbin in zip(ybins[:-1],ybins[1:]):#[(0.0,0.5),(2.0,2.5)]:#,(1.5,2.0),(2.0,2.5)]: #
        if not yboostbin[0]+ystarbin[0]>2:
         for mc in ['amc','hpp']:
            plots.append(genrecocomparisons(args, obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin))
            plots.append(datamccomparisons(args, obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin))
            plots.append(responsematrix(args, obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin))
            plots.append(plot_matrix(args, obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin))
            #plots.append(plot_resolutionrootfiles(args, obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin))
         for variation in [0,-1,1]:
          for varquantity in ['_statistics','_SF','_weight','_sigma']:
           for resolution in ['_rms']:#,'_sigma']:
            plots.append(plot_matrix(args, obs, cut, mc='toy', yboostbin=yboostbin, ystarbin=ystarbin, resolution=resolution, variation=variation, varquantity=varquantity))
      for mc in ['amc','hpp']:
        plots.append(genrecocomparisons(args, obs, cut, mc=mc))
        plots.append(datamccomparisons(args, obs, cut, mc=mc))
        plots.append(responsematrix(args, obs, cut, mc=mc))
        #plots.append(plot_matrix(args, obs, cut, mc=mc))
    if plots==[]:
        return
    else:
        return [PlottingJob(plots=plots, args=args)]

######################################################################################################################################################
# uses previously created dictionaries to calculate quantities

def resolutionloop(args=None):
    plots = []
    ybins = [0.0,0.5]#,1.0,1.5,2.0,2.5]
    for obs in ['zpt']:#,'mupluspt','muminuspt']:#,'jet1pt','jet1y','yboost','ystar']:#]:#
     for cut in ['_zpt30_jet1pt10']:
      for yboostbin in zip(ybins[:-1],ybins[1:]):
       for ystarbin in zip(ybins[:-1],ybins[1:]):
        if not yboostbin[0]+ystarbin[0]>2:
         for mc in ['amc','hpp']:
            resolution(args, obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin)
    return

def toyloop(args=None):
    plots = []
    ybins = [0.0,0.5]#,1.0,1.5,2.0,2.5]
    for obs in ['zpt']:
     for cut in ['_zpt30_jet1pt10']:
      for yboostbin in zip(ybins[:-1],ybins[1:]):
       for ystarbin in zip(ybins[:-1],ybins[1:]):
        if not yboostbin[0]+ystarbin[0]>2:
         for resolution in ['_rms']:#,'_sigma']:
          for variation in [0,-1,1]:
           for varquantity in ['_SF','_sigma','_weight','_statistics']:
            toymontecarlo(args, obs, cut, mc='amc', resolution=resolution, yboostbin=yboostbin, ystarbin=ystarbin, variation=variation, varquantity=varquantity)
    return
    
def unfoldingloop(args=None):
    plots = []
    ybins = [0.0,0.5]#,1.0,1.5,2.0,2.5]
    for obs in ['zpt']:
     for cut in ['_zpt30_jet1pt10']:
      for yboostbin in zip(ybins[:-1],ybins[1:]):
       for ystarbin in zip(ybins[:-1],ybins[1:]):
        if not yboostbin[0]+ystarbin[0]>2:
         for resolution in ['_rms']:#,'_sigma']:
          for variation in [0,-1,1]:
           for varquantity in ['_SF','_sigma','_weight','_statistics']:
            plots.append(unfolding(args, obs, cut, data='amc', mc='toy', yboostbin=yboostbin, ystarbin=ystarbin, resolution=resolution,variation=variation,varquantity=varquantity))
            plots.append(unfolding(args, obs, cut, data='BCDEFGH', mc='toy', yboostbin=yboostbin, ystarbin=ystarbin, resolution=resolution,variation=variation,varquantity=varquantity))
    return [PlottingJob(plots=plots, args=args)]

def unfoldingplotloop(args=None):
    plots = []
    ybins = [0.0,0.5]#,1.0,1.5,2.0,2.5]
    for obs in ['zpt']:
     for cut in ['_zpt30_jet1pt10']:
      for yboostbin in zip(ybins[:-1],ybins[1:]):
       for ystarbin in zip(ybins[:-1],ybins[1:]):
        if not yboostbin[0]+ystarbin[0]>2:
         for resolution in ['_rms']:#,'_sigma']:
          for variation in [0]:
           for varquantity in ['_sigma','_SF','_weight','_statistics']:
            plots.append(plot_unfoldingrootfiles(args, obs, cut, data='amc', mc='toy', yboostbin=yboostbin, ystarbin=ystarbin, resolution=resolution,variation=0,varquantity=varquantity))
            plots.append(plot_unfoldingrootfiles(args, obs, cut, data='BCDEFGH', mc='toy', yboostbin=yboostbin, ystarbin=ystarbin, resolution=resolution,variation=0,varquantity=varquantity))
    return [PlottingJob(plots=plots, args=args)]

# writes a ROOT file that contains a 2D map with the response matrices' condition numbers on the 3rd axis
def conditionnumber(args=None, obs='zpt', cut='_mupt25_zmass20_zpt30_jet24', data='amc', mc='amc', yboostbin=None, ystarbin=None):
    ybins = [0.0,0.5,1.0,1.5,2.0,2.5]
    jb,js = 0,0
    inpath = "/storage/c/tberger/plots/response/responsematrix_toy"+cut
    outpath = "/storage/c/tberger/plots/condition"+cut+".root"
    file_out = ROOT.TFile(outpath,"RECREATE")
    h_condition = ROOT.TH2D("condition","", len(ybins)-1, array('d',ybins), len(ybins)-1, array('d',ybins))
    for yboostbin in zip(ybins[:-1],ybins[1:]):#[(0.0,0.5)]:#
      jb+=1
      for ystarbin in zip(ybins[:-1],ybins[1:]):#[(2.0,2.5)]:#
       if not yboostbin[0]+ystarbin[0]>2:
        js+=1
        [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
        file_in = ROOT.TFile(inpath+"/"+obs+namestring+".root","READ")

        h = file_in.Get("response")
        #h.Scale(1.0/h.Integral())
        m = ROOT.TMatrixD(h.GetNbinsX(),h.GetNbinsY())
        a = ROOT.TArrayD(h.GetNbinsX()*h.GetNbinsY())
        for i in xrange(h.GetNbinsX()*h.GetNbinsY()):
            a[i]=h.GetBinContent(i/h.GetNbinsX()+1,i%h.GetNbinsY()+1)/h.Integral()
        m.SetMatrixArray(a.GetArray())
        svd = ROOT.TDecompSVD(m)
        print [x for x in svd.GetSig()]
        print sum([x for x in svd.GetSig()])
        print jb,js,svd.Condition(),yboostbin,ystarbin
        h_condition.SetBinContent(jb,js,svd.Condition())
        file_in.Close()
      js = 0
    file_out.Write()
    file_out.Close()
    print "condition hist written to "+outpath
    return
'''
def folding(args=None, obs='zpt', cut='_mupt25_zmass20_zpt30_jet24', data='amc', mc='amc', yboostbin=None, ystarbin=None, resolution='', variation=0):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
    inpath = '/storage/c/tberger/plots/unfolding/covariance_'+data+'_by_'+mc+cut+'/covmat_'+obs+namestring+resolution+variationstring[variation]+'.root'
    print inpath
    file_in = ROOT.TFile(inpath,"READ")
    h_gen = file_in.Get("gen_hist")
    h_reco = file_in.Get("reco_hist")
    h_truth = file_in.Get("truth_hist")
    h_meas = file_in.Get("meas_hist")
    h_resp = file_in.Get("resp_matrix")
    
    resp_list = [[h_resp.GetBinContent(i+1,j+1) for i in xrange(h_resp.GetNbinsX())] for j in xrange(h_resp.GetNbinsY())]
    gen_list = [h_gen.GetBinContent(i+1) for i in xrange(h_gen.GetNbinsX())]
    reco_list = [h_reco.GetBinContent(i+1) for i in xrange(h_reco.GetNbinsX())]
    truth_list = [h_truth.GetBinContent(i+1) for i in xrange(h_truth.GetNbinsX())]
    meas_list = [h_meas.GetBinContent(i+1) for i in xrange(h_meas.GetNbinsX())]
    
    response = np.matrix(resp_list)
    truth = np.matrix(truth_list)
    
    print response
    print response.truth
    return

def plot_correlations(args=None, obs=None, cut='_mupt25_zmass20_zpt30', data='amc', mc='amc', yboostbin=None, ystarbin=None, resolution='_rms', varquantity='_statistics', variation=0):
    plots=[]
    #cut = '_mupt25_zmass20_zpt30_jet24'
    #cut = '_mupt25_zmass20_zpt30_jetpt15_jet24'
    for [obsy, obsx] in [#['jet1y','genjet1y'],['jet1y','genjet2y'],['jet1y','genjet3y'],
                         #['jet2y','genjet1y'],['jet2y','genjet2y'],['jet2y','genjet3y'],
                         #['jet3y','genjet1y'],['jet3y','genjet2y'],['jet3y','genjet3y'],
                         #['alpha','jet1y'],['genalpha','genjet1y'],
                         #['deltaphizjet1','jet1y'],['gendeltaphizjet1','genjet1y'],
                         ['deltaphizjet1','jet1match'],['zphi','jet1phi'],['genzphi','genjet1phi'],['deltaphizjet1','gendeltaphizjet1'],['deltaphijet1jet2','gendeltaphijet1jet2'],
                        ]:
        [d1, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin, ystarbin)
        d1.update({
            'files': [datasets[mc]],
            'folders' : ['genleptoncuts_L1L2L3/ntuple'],
            'filename': obsy+'_'+obsx,
            'x_expressions': [obsx],
            'x_bins': obsx.split('gen')[1] if 'gen' in obsx else obsx,
            'x_label': obsx,
            'x_log': False,
            'y_expressions': [obsy],
            'y_bins': obsy.split('gen')[1] if 'gen' in obsy else obsy,
            'y_label': obsy,
            'y_log': False,
            'z_log': True,
            'z_lims': [1e1,1e4],
            #'no_weight': True,
            #'weights': ['(1-'+gencutstring+')'],#*(abs(jet1y)>2.4)
            #'www': 'y_correlations'+cut+'_inversegencuts',#_jet1ymin24_match',
            'weights': [gencutstring],#+'*(genzpt>60)'],#+'*(genjet1pt>30)'],#+'*(matchedgenjet1pt>0)'],#'*(abs(jet1y)>2.4)'
            'www': 'y_correlations'+cut+'_gencuts',#_highzpt',#_jet1ymin24',
        })
        #plots.append(d1)
        #d2 = copy.deepcopy(d1)
        #d2.update({ 'folders' : ['genleptoncuts_L1L2L3/ntuple'],
        #            #'weights': ['(1-'+cutstring+')'],#*(abs(genjet1y)>2.4)
        #            #'www': 'y_correlations'+cut+'_inverserecocuts',#_genjet1ymin24_match',
        #            'weights': [gencutstring+'*(genalpha<0.4)'],#+'*(zpt>60)'],#+'*(jet1pt>30)'],#(matchedgenjet1pt>0)'*(abs(genjet1y)>2.4)
        #            'www': 'y_correlations'+cut+'_gencuts_alpha',#_highzpt',#_genjet1ymin24',
        #})
        #plots.append(d2)
        #d3 = copy.deepcopy(d1)
        #d3.update({ 'folders' : ['genleptoncuts_L1L2L3/ntuple'],
        #            #'weights': ['(1-'+gencutstring+')'],#*(abs(jet1y)>2.4)
        #            #'www': 'y_correlations'+cut+'_inversegencuts',#_jet1ymin24_match',
        #            'weights': [gencutstring+'*(matchedgenjet1pt>0)'],#+'*'],#*(abs(jet1y)>2.4)'
        #            'www': 'y_correlations'+cut+'_match',#_jet1ymin24',
        #})
        #plots.append(d3)
        #d4 = copy.deepcopy(d1)
        #d4.update({ 'folders' : ['genleptoncuts_L1L2L3/ntuple'],
        #            #'weights': ['(1-'+cutstring+')'],#*(abs(genjet1y)>2.4)
        #            #'www': 'y_correlations'+cut+'_inverserecocuts',#_genjet1ymin24_match',
        #            'weights': [gencutstring+'*(genzpt<60)'],#+'*(matchedgenjet1pt>0)'],#'(jet1pt<30)*(abs(genjet1y)>2.4)
        #            'www': 'y_correlations'+cut+'_lowzpt',#_match',#_genjet1ymin24',
        #})
        #plots.append(d4)
        #d5 = copy.deepcopy(d1)
        #d5.update({ 'folders' : ['genleptoncuts_L1L2L3/ntuple'],
        #            #'weights': ['(1-'+cutstring+')'],#*(abs(genjet1y)>2.4)
        #            #'www': 'y_correlations'+cut+'_inverserecocuts',#_genjet1ymin24_match',
        #            'weights': [gencutstring+'*(genzpt>60)'],#+'*(matchedgenjet1pt>0)'],#'(jet1pt<30)*(abs(genjet1y)>2.4)
        #            'www': 'y_correlations'+cut+'_highzpt',#_match',#_genjet1ymin24',
        #})
        #plots.append(d5)
        #d6 = copy.deepcopy(d1)
        #d6.update({ 'folders' : ['genleptoncuts_L1L2L3/ntuple'],
        #            #'weights': ['(1-'+cutstring+')'],#*(abs(genjet1y)>2.4)
        #            #'www': 'y_correlations'+cut+'_inverserecocuts',#_genjet1ymin24_match',
        #            'weights': [gencutstring+'*(genjet1pt<30)'],#+'*(matchedgenjet1pt>0)'],#'(jet1pt<30)*(abs(genjet1y)>2.4)
        #            'www': 'y_correlations'+cut+'_lowjetpt',#_match',#_genjet1ymin24',
        #})
        #plots.append(d6)
        #d7 = copy.deepcopy(d1)
        #d7.update({ 'folders' : ['genleptoncuts_L1L2L3/ntuple'],
        #            #'weights': ['(1-'+cutstring+')'],#*(abs(genjet1y)>2.4)
        #            #'www': 'y_correlations'+cut+'_inverserecocuts',#_genjet1ymin24_match',
        #            'weights': [gencutstring+'*(genjet1pt>30)'],#+'*(matchedgenjet1pt>0)'],#'(jet1pt<30)*(abs(genjet1y)>2.4)
        #            'www': 'y_correlations'+cut+'_highjetpt',#_match',#_genjet1ymin24',
        #})
        #plots.append(d7)
        d8 = copy.deepcopy(d1)
        d8.update({ 'folders' : ['leptoncuts_L1L2L3/ntuple'],
                    #'weights': ['(1-'+cutstring+')'],#*(abs(genjet1y)>2.4)
                    #'www': 'y_correlations'+cut+'_inverserecocuts',#_genjet1ymin24_match',
                    'weights': [cutstring+'*(abs(jet1y)<2.4)'],#+'*(matchedgenjet1pt>0)'],#'(jet1pt<30)*(abs(genjet1y)>2.4)
                    'www': 'y_correlations'+cut+'_lowrecojety',#_match',#_genjet1ymin24',
        })
        plots.append(d8)
        d9 = copy.deepcopy(d1)
        d9.update({ 'folders' : ['leptoncuts_L1L2L3/ntuple'],
                    #'weights': ['(1-'+cutstring+')'],#*(abs(genjet1y)>2.4)
                    #'www': 'y_correlations'+cut+'_inverserecocuts',#_genjet1ymin24_match',
                    'weights': [cutstring+'*(abs(jet1y)>2.4)'],#+'*(matchedgenjet1pt>0)'],#'(jet1pt<30)*(abs(genjet1y)>2.4)
                    'www': 'y_correlations'+cut+'_highrecojety',#_match',#_genjet1ymin24',
        })
        plots.append(d9)
    return [PlottingJob(plots=plots, args=args)]
'''

def plot_crosssections_all(args=None, obs='zpt', cut='_mupt25_zmass20_zpt30_jetpt10_jet24', data='BCDEFGH', mc='toy', resolution='_rms'):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, mc, yboostbin=None, ystarbin=None)
    plots=[]
    d.update({
        'files': [  '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost00-05_ystar00-05'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost00-05_ystar05-10'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost00-05_ystar10-15'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost00-05_ystar15-20'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost00-05_ystar20-25'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost05-10_ystar00-05'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost05-10_ystar05-10'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost05-10_ystar10-15'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost05-10_ystar15-20'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost10-15_ystar00-05'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost10-15_ystar05-10'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost10-15_ystar10-15'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost15-20_ystar00-05'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost15-20_ystar05-10'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_BCDEFGH_by_'+mc+cut+'/covmat_'+obs+'_yboost20-25_ystar00-05'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost00-05_ystar00-05'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost00-05_ystar05-10'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost00-05_ystar10-15'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost00-05_ystar15-20'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost00-05_ystar20-25'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost05-10_ystar00-05'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost05-10_ystar05-10'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost05-10_ystar10-15'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost05-10_ystar15-20'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost10-15_ystar00-05'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost10-15_ystar05-10'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost10-15_ystar10-15'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost15-20_ystar00-05'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost15-20_ystar05-10'+resolution+'.root',
                    '/storage/c/tberger/plots/unfolding/covariance_amc_by_'+mc+cut+'/covmat_'+obs+'_yboost20-25_ystar00-05'+resolution+'.root',
                    ],
        'folders': [''],
        'x_expressions': ['data_hist'],
        'analysis_modules': ['NormalizeByBinWidth','ScaleHistograms'],#'Ratio'],
        'legend_cols': 2,
        'x_bins': None,
        'nicks': [  'datyb0ys0','datyb0ys1','datyb0ys2','datyb0ys3','datyb0ys4','datyb1ys0','datyb1ys1','datyb1ys2','datyb1ys3','datyb2ys0','datyb2ys1','datyb2ys2','datyb3ys0','datyb3ys1','datyb4ys0',
                    'amcyb0ys0','amcyb0ys1','amcyb0ys2','amcyb0ys3','amcyb0ys4','amcyb1ys0','amcyb1ys1','amcyb1ys2','amcyb1ys3','amcyb2ys0','amcyb2ys1','amcyb2ys2','amcyb3ys0','amcyb3ys1','amcyb4ys0'],
        'ratio_numerator_nicks':    ['datyb0ys0','datyb0ys1','datyb0ys2','datyb0ys3','datyb0ys4','datyb1ys0','datyb1ys1','datyb1ys2','datyb1ys3','datyb2ys0','datyb2ys1','datyb2ys2','datyb3ys0','datyb3ys1','datyb4ys0'],
        'ratio_denominator_nicks':  ['amcyb0ys0','amcyb0ys1','amcyb0ys2','amcyb0ys3','amcyb0ys4','amcyb1ys0','amcyb1ys1','amcyb1ys2','amcyb1ys3','amcyb2ys0','amcyb2ys1','amcyb2ys2','amcyb3ys0','amcyb3ys1','amcyb4ys0'],
        #'nicks_whitelist': ['yb0ys0','yb0ys4','yb4ys0'],
        'y_subplot_lims': [0.5,1.5],
        'y_subplot_label': 'Data/Sim',
        #'y_log': False,
        'subplot_fraction': 25,
        'labels': [ '($0.0<y_b<0.5$; $0.0<y^*<0.5$) x $10^9$',
                    '($0.0<y_b<0.5$; $0.5<y^*<1.0$) x $10^9$',
                    '($0.0<y_b<0.5$; $1.0<y^*<1.5$) x $10^9$',
                    '($0.0<y_b<0.5$; $1.5<y^*<2.0$) x $10^9$',
                    '($0.0<y_b<0.5$; $2.0<y^*<2.5$) x $10^9$',
                    '($0.5<y_b<1.0$; $0.0<y^*<0.5$) x $10^6$',
                    '($0.5<y_b<1.0$; $0.5<y^*<1.0$) x $10^6$',
                    '($0.5<y_b<1.0$; $1.0<y^*<1.5$) x $10^6$',
                    '($0.5<y_b<1.0$; $1.5<y^*<2.0$) x $10^6$',
                    '($1.0<y_b<1.5$; $0.0<y^*<0.5$) x $10^3$',
                    '($1.0<y_b<1.5$; $0.5<y^*<1.0$) x $10^3$',
                    '($1.0<y_b<1.5$; $1.0<y^*<1.5$) x $10^3$',
                    '($1.5<y_b<2.0$; $0.0<y^*<0.5$) x $10^1$',
                    '($1.5<y_b<2.0$; $0.5<y^*<1.0$) x $10^1$',
                    '($2.0<y_b<2.5$; $0.0<y^*<0.5$) x $10^0$',
                    ],
        'texts_y': [0.98,0.94,0.90,0.86],
        'texts_size': [20],
        'x_errors': [0]*15+[1]*30,
        'scale_nicks': [    'datyb0ys0','datyb0ys1','datyb0ys2','datyb0ys3','datyb0ys4','datyb1ys0','datyb1ys1','datyb1ys2','datyb1ys3','datyb2ys0','datyb2ys1','datyb2ys2','datyb3ys0','datyb3ys1','datyb4ys0',
                            'amcyb0ys0','amcyb0ys1','amcyb0ys2','amcyb0ys3','amcyb0ys4','amcyb1ys0','amcyb1ys1','amcyb1ys2','amcyb1ys3','amcyb2ys0','amcyb2ys1','amcyb2ys2','amcyb3ys0','amcyb3ys1','amcyb4ys0'],
        'scales':[1e9/35.8*4/1000]*5+[1e6/35.8*4/1000]*4+[1e3/35.8*4/1000]*3+[1e1/35.8*4/1000]*2+[1e0/35.8*4/1000]*1
                +[1e9/1.0*4/1000]*5+[1e6/1.0*4/1000]*4+[1e3/1.0*4/1000]*3+[1e1/1.0*4/1000]*2+[1e0/1.0*4/1000]*1,
        'www': 'crossection'+cut,
        #'markers': ['d','o','v','_','_','_'],
        'markers': ['d']*5+['o']*4+['v']*3+['^']*2+['p']+['_']*15,
        'colors': ['red','blue','green','orange','purple','lime','salmon','teal','yellow','cyan','violet','brown','royalblue','olive','grey'],
        'y_lims': [1e-6,1e14],
        'y_label': r'$ \\frac{d^3\\mathit{\\sigma}}{d\\mathit{p}_T^Z d\\mathit{y_b} d\\mathit{y^*}}/(\\frac{p\\mathit{b}}{GeV})$',
    })
    plots.append(d)
    return [PlottingJob(plots=plots, args=args)]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
