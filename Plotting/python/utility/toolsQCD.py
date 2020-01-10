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
        '17Jul2018' : '/ceph/tberger/excalibur_results/2019-09-03/data16_mm_BCDEFGH_SiMu17Jul2018.root',
        #'GH':       '/storage/8/tberger/excalibur_work/excalibur/data16_mm_GH_SiMu07Aug17_2019-05-31_10-49/out.root',
        #'amc' :     '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_DYtoLLamcatnlo.root',
        #'hpp' :     '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_DYtoLLherwigpp.root',
        #'mad' :     '/storage/8/tberger/excalibur_results/2019-06-17/mc16_mm_BCDEFGH_DYtoLLmadgraph.root',
        'amc' :     '/ceph/tberger/excalibur_results/2019-09-03/mc16_mm_BCDEFGH_DYtoLLamcatnlo.root',
        #'hpp' :     '/ceph/tberger/excalibur_results/2019-09-03/mc16_mm_BCDEFGH_DYtoLLherwigpp.root',
        #'mad' :     '/ceph/tberger/excalibur_results/2019-09-03/mc16_mm_BCDEFGH_DYtoLLmadgraph.root',
        'hpp' :     '/ceph/tberger/excalibur_results/2019-11-06/mc16_mm_BCDEFGH_DYtoLLherwigpp.root',
        'mad' :     '/ceph/tberger/excalibur_results/2019-11-06/mc16_mm_BCDEFGH_DYtoLLmadgraph.root',
        #'pow' :     '/storage/8/tberger/excalibur_results/2019-06-13/mc16_mm_BCDEFGH_ZtoMMpowheg.root',
        #'ptz' :     '/storage/8/tberger/excalibur_results/2019-06-13/mc16_mm_BCDEFGH_DYtoLLamcatnlo_Pt0ToInf.root',
        'TT' :      '/ceph/tberger/excalibur_results/2019-09-03/mc16_mm_BCDEFGH_TTJetsmadgraph.root',
        'ZZ' :      '/ceph/tberger/excalibur_results/2019-09-03/mc16_mm_BCDEFGH_ZZpythia8.root',
        'WZ' :      '/ceph/tberger/excalibur_results/2019-09-03/mc16_mm_BCDEFGH_WZJToLLLNu.root',
        'WW' :      '/ceph/tberger/excalibur_results/2019-09-03/mc16_mm_BCDEFGH_WWTo2L2Nupowheg.root',
        'TW':       '/ceph/tberger/excalibur_results/2019-09-03/mc16_mm_BCDEFGH_TW.root',
        'test':     '/portal/ekpbms1/home/mschnepf/QCD/NP_corrections/runtime/CMSSW_10_6_2/src/official_1mio.root',
    })
    return datasets

def prepare_3Dhists(args=None, obs='zpt'):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, '', '', '', yboostbin=None, ystarbin=None)
    l_ybinedges = [0,5,9,12,14,0]
    l_obshists,l_obsbinedges,counter = [],[0],0
    for index in xrange(15):
        name = obs+"_{}".format(index)
        if index in [14]:
            rebinning(args,d,obs,(0.0,0.5),(2.0,2.5))
            l_bins = [float(x) for x in d['x_bins'][0].split(' ')]
            l_obshists.append(ROOT.TH1D(name,"",len(l_bins)-1, array('d',l_bins)))
        elif index in [4,8,11,12,13]:
            rebinning(args,d,obs,(0.0,0.5),(1.5,2.0))
            l_bins = [float(x) for x in d['x_bins'][0].split(' ')]
            l_obshists.append(ROOT.TH1D(name,"",len(l_bins)-1, array('d',l_bins)))
        else:
            rebinning(args,d,obs,(0.0,0.5),(0.0,0.5))
            l_bins = [float(x) for x in d['x_bins'][0].split(' ')]
            l_obshists.append(ROOT.TH1D(name,"",len(l_bins)-1, array('d',l_bins)))
        counter+=l_obshists[index].GetNbinsX()
        l_obsbinedges.append(counter)
    h_reco = ROOT.TH1D(obs,"",counter,0,counter)
    h_gen = ROOT.TH1D("gen"+obs,"",counter,0,counter)
    h_response = ROOT.TH2D("response","",counter,0,counter,counter,0,counter)
    return [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges]

def invert_3Dhists(args=None, filename = '',PLOTSFOLDER = '', BUFFERFOLDER = ''):
    if '' in [filename,PLOTSFOLDER,BUFFERFOLDER]:
        print "WARNING: inputs must be specified!"
        return
    if not os.path.exists(BUFFERFOLDER):
        os.makedirs(BUFFERFOLDER)
        print 'The directory',BUFFERFOLDER,'has been created'
    if 'phistareta' in filename:
        obs = 'phistareta'
        [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhists(args,'phistareta')
    elif 'zpt' in filename:
        obs = 'zpt'
        [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhists(args,'zpt')
    file_in = ROOT.TFile(PLOTSFOLDER+'/'+filename,"READ")
    namelist = [key.GetName() for key in file_in.GetListOfKeys()]
    print namelist
    output_file = BUFFERFOLDER+'/'+filename.replace('.root','_binned.root')
    file_out = ROOT.TFile(output_file,"RECREATE")
    for histname in namelist:
      hist = file_in.Get(histname)
      if isinstance(hist,ROOT.TH1D):
        hist_index, bin_index = 0,0
        genybmin,genybmax,genysmin,genysmax = 0.0,0.5,0.0,0.5
        for obsbin in xrange(h_gen.GetNbinsX()):
            if obsbin in l_obsbinedges:
                if not obsbin==0:
                    hist_bin.Write(histname+namestring)
                    bin_index = 0
                    hist_index += 1
                    genybmin += 0.5
                    genybmax += 0.5
                    if obsbin in ([93,167,222,256] if obs=='zpt' else [85,152,201,227]):
                    #if obsbin in ([93,167,222,256] if obs=='zpt' else [81,145,192,218]):
                        genysmin += 0.5
                        genysmax += 0.5
                        genybmin,genybmax = 0.0,0.5
                namestring = "_yb{}_ys{}".format(int(2*genybmin),int(2*genysmin))
                hist_bin  = l_obshists[hist_index].Clone(histname+namestring)
                if genysmin==2.0:
                    if obs == 'zpt':
                        hist_bin = ROOT.TH1D(histname+namestring,"",8,array('d',[25,30,40,50,70,90,110,150,250]))
                    if obs == 'phistareta':
                        hist_bin = ROOT.TH1D(histname+namestring,"",4,array('d',[0.4,0.6,0.8,1.0,5]))
            bin_index += 1
            hist_bin.SetBinContent(bin_index,hist.GetBinContent(obsbin+1))
            hist_bin.SetBinError(bin_index,hist.GetBinError(obsbin+1))
        hist_bin.Write(histname+namestring)
      elif isinstance(hist,ROOT.TGraphAsymmErrors):
        x,y = ROOT.Double(0),ROOT.Double(0)
        g_reco, g_gen = ROOT.TGraphAsymmErrors(h_reco), ROOT.TGraphAsymmErrors(h_gen)
        l_obsgraphs = [ROOT.TGraphAsymmErrors(g) for g in l_obshists]
        graph_index, bin_index = 0,0
        genybmin,genybmax,genysmin,genysmax = 0.0,0.5,0.0,0.5
        for obsbin in xrange(g_gen.GetN()-1):
            if obsbin in l_obsbinedges:
                if not obsbin==0:
                    graph_bin.Write(histname+namestring)
                    bin_index = 0
                    graph_index += 1
                    genybmin += 0.5
                    genybmax += 0.5
                    if obsbin in ([93,167,222,256] if obs=='zpt' else [85,152,201,227]):
                    #if obsbin in ([93,167,222,256] if obs=='zpt' else [81,145,192,218]):
                        genysmin += 0.5
                        genysmax += 0.5
                        genybmin,genybmax = 0.0,0.5
                namestring = "_yb{}_ys{}".format(int(2*genybmin),int(2*genysmin))
                graph_bin  = l_obsgraphs[graph_index].Clone(histname+namestring)
                if genysmin==2.0:
                    if obs == 'zpt':
                        hist_bin = ROOT.TH1D(histname+namestring,"",8,array('d',[25,30,40,50,70,90,110,150,250]))
                    if obs == 'phistareta':
                        hist_bin = ROOT.TH1D(histname+namestring,"",4,array('d',[0.4,0.6,0.8,1.0,5]))
                    graph_bin = ROOT.TGraphAsymmErrors(hist_bin)
            graph_bin.GetPoint(bin_index,x,y)
            x0 = copy.deepcopy(x)
            hist.GetPoint(obsbin,x,y)
            graph_bin.SetPoint(bin_index,x0,y)
            graph_bin.SetPointEYhigh(bin_index,hist.GetErrorYhigh(obsbin))
            graph_bin.SetPointEYlow(bin_index,hist.GetErrorYlow(obsbin))
            bin_index += 1
        graph_bin.Write(histname+namestring)
    print "histograms written to",output_file

def closure_chi2(args=None, unffilename='', genfilename='' ,PLOTSFOLDER='', BUFFERFOLDER='', ybindex=None, ysindex=None):
    obs  = unffilename.split('_')[0]
    data = genfilename.split('_')[1].split('.')[0]
    mc   = unffilename.split('.')[0].split('_')[-1]
    varlist = ['stats_'+mc]
    if 'toy' in unffilename:
        varlist = ['stats_'+mc,'model_toy','Robs','Ryj','Ryz','switch','F','A']
    f_unf = ROOT.TFile(PLOTSFOLDER+'/'+unffilename,"READ")
    print PLOTSFOLDER+'/'+unffilename
    f_gen = ROOT.TFile(PLOTSFOLDER+'/'+genfilename,"READ")
    print PLOTSFOLDER+'/'+genfilename
    h_unf = f_unf.Get("unfolded"+obs)
    h_gen = f_gen.Get("gen"+obs)
    h_unc = h_gen.Clone("uncertainty")
    h_unc.Reset()
    for var in varlist:
        f_var = ROOT.TFile(PLOTSFOLDER+'/uncertainty/'+obs+'_17Jul2018_'+var+'.root',"READ")
        h_var = f_var.Get("uncertainty_"+var)
        for i in xrange(h_unc.GetNbinsX()):
            h_unc.SetBinContent(i+1,np.sqrt(h_unc[i+1]**2+h_var[i+1]**2))
    chi2 = 0
    if not (ybindex==None or ysindex==None):
        [l_ybinedges, l_obsbinedges] = prepare_3Dhists(args,obs)[4:6]
        obsindexmin, obsindexmax = l_obsbinedges[l_ybinedges[ysindex]+int(ybindex)],l_obsbinedges[l_ybinedges[ysindex]+int(ybindex)+1]
    else:
        obsindexmin, obsindexmax = 0,h_unc.GetNbinsX()
    h_chi2 = h_unc.Clone("chi2")
    for i in xrange(obsindexmin, obsindexmax):
        chi2 += (h_unf[i+1]-h_gen[i+1])**2/((h_unc[i+1]*h_unf[i+1])**2+h_unf.GetBinError(i+1)**2)
        h_chi2.SetBinContent(i+1,(h_unf[i+1]-h_gen[i+1])/np.sqrt((h_unc[i+1]*h_unf[i+1])**2+h_unf.GetBinError(i+1)**2))
        h_chi2.SetBinError(i+1,0)
    print "chi2/ndf between gen",data,"and reco",data,"unfolded by",mc,"is",chi2/(obsindexmax-obsindexmin)
    return chi2/(obsindexmax-obsindexmin)

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

    
    
    
    
    
