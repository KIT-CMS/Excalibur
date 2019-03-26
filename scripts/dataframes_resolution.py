# -*- coding: utf-8 -*-

# script to estimate zpt, phistareta, jet1y and zy resolution using ROOT dataframes. To be optimized!
# need

import os
import ROOT
import numpy as np
from array import array
from copy import deepcopy

ROOT.gROOT.SetBatch()
#ROOT.TH1D.StatOverflows(True)

def error(a,b,c):
    # gives the root of the squared sum of a,b,c
    return np.sqrt(a**2+b**2+c**2)

def generate_basiccutstring(cut='_jet1pt20',yboostbin=None,ystarbin=None):
    basicrecocutstring='(abs(mupluseta)<2.4)&&(abs(muminuseta)<2.4)&&(mupluspt>25)&&(muminuspt>25)&&(abs(zmass-91.1876)<20)'
    basicgencutstring='(abs(genmupluseta)<2.4)&&(abs(genmuminuseta)<2.4)&&(genmupluspt>25)&&(genmuminuspt>25)&&(abs(genzmass-91.1876)<20)'
    cut=cut.split('_')
    if 'gen' in cut:
        basiccutstring = basicgencutstring
    else:
        basiccutstring = basicrecocutstring
    if 'jet1pt10' in cut:
        basiccutstring+='&&('+cut[0]+'jet1pt>10)'
    if 'jet1pt15' in cut:
        basiccutstring+='&&('+cut[0]+'jet1pt>15)'
    if 'jet1pt20' in cut:
        basiccutstring+='&&('+cut[0]+'jet1pt>20)'
    if 'jet1pt30' in cut:
        basiccutstring+='&&('+cut[0]+'jet1pt>30)'
    if 'zpt30' in cut:
        basiccutstring+='&&('+cut[0]+'zpt>30)'
    if 'phistareta04' in cut:
        basiccutstring+='&&('+cut[0]+'phistareta>0.4)'
    if 'backtoback' in cut:
        basiccutstring+='&&(abs(abs('+cut[0]+'zphi-'+cut[0]+'jet1phi)-3.14159)<1.57)'
    if 'alpha05' in cut:
        basiccutstring+='&&('+cut[0]+'jet2pt/'+cut[0]+'zpt<0.5)'
    if yboostbin and ystarbin:
        basiccutstring+=('&&('+cut[0]+'yboost>{})&&('+cut[0]+'yboost<{})&&('+cut[0]+'ystar>{})&&('+cut[0]+'ystar<{})').format(yboostbin[0],yboostbin[1],ystarbin[0],ystarbin[1])
    return basiccutstring

def rebinning(obs,yboostbin,ystarbin):
    if obs == 'mupluspt' or obs == 'muminuspt':
        binning = ' '.join(['{}'.format(x) for x in range(25,300,(300-25)/11)])+' 350'
    if obs in ['zy','jet1y','mupluseta','muminuseta','mu1eta','mu2eta','matchedjet1y']:
        binning = '-2.4 -2.2 -2.0 -1.8 -1.6 -1.4 -1.2 -1.00 -0.8 -0.6 -0.4 -0.2 0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8 2.0 2.2 2.4'
    if obs == 'jet1pt':
        binning = '5 10 12 15 20 30 50 75 125 175 225 300 400'
    if obs in ['yboost','ystar','matchedyboost','matchedystar']:
        binning = '0.0 0.5 1.0 1.5 2.0 2.5'
    if obs == 'deltaphizjet1':
        binning = '0.0 0.4 0.8 1.2 1.6 2.0 2.4 2.8 3.2'
    if obs=='zpt':
        if (yboostbin==(0.0,0.5) and ystarbin==(2.0,2.5)):
            print obs+" binning changed"
            binning = '25 30 40 50 70 90 110 150 250'
        elif ( (yboostbin==(0.0,0.5) and ystarbin==(1.5,2.0))
            or (yboostbin==(0.5,1.0) and ystarbin==(1.5,2.0))
            or (yboostbin==(1.0,1.5) and ystarbin==(1.0,1.5))
            or (yboostbin==(1.5,2.0) and ystarbin==(0.5,1.0))
            or (yboostbin==(2.0,2.5) and ystarbin==(0.0,0.5))
            ):
            print obs+" binning changed"
            binning = '25 30 35 40 45 50 60 70 80 90 100 110 130 150 170 190 250 1000'
        else: # use standard binning
            binning = '25 30 35 40 45 50 60 70 80 90 100 110 130 150 170 190 220 250 400 1000'
    if obs=='phistareta':
        if (yboostbin==(0.0,0.5) and ystarbin==(2.0,2.5)):
            print obs+" binning changed"
            binning = '0.4 0.6 0.8 1.0 5'
        elif ( (yboostbin==(0.0,0.5) and ystarbin==(1.5,2.0))
            or (yboostbin==(0.5,1.0) and ystarbin==(1.5,2.0))
            or (yboostbin==(1.0,1.5) and ystarbin==(1.0,1.5))
            or (yboostbin==(1.5,2.0) and ystarbin==(0.5,1.0))
            or (yboostbin==(2.0,2.5) and ystarbin==(0.0,0.5))
            ):
            print obs+" binning changed"
            binning = '0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.2 1.5 2 3 5 10 50'
        else: # use standard binning            
            binning = '0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.2 1.5 2 3 4 5 7 10 15 20 30 50'
    return [float(x) for x in binning.split(' ')]

datasets = ({
        'amc' :     '/ceph/tberger/excalibur_results/2019-01-28/mc16_mm_BCDEFGH_DYtoLLamcatnlo.root',
        'hpp' :     '/ceph/tberger/excalibur_results/2019-01-28/mc16_mm_BCDEFGH_DYtoLLherwigpp.root',
        'mad' :     '/ceph/tberger/excalibur_results/2019-01-28/mc16_mm_BCDEFGH_DYtoLLmadgraph.root',
        })

ybins = [0.0,0.5,1.0,1.5,2.0,2.5]

'''
obs='zpt'
cut='_jet1pt20'
mc='amc'
yboostbin=(0.0,0.5)
ystarbin=(0.0,0.5)
match=''
dressed=''
puid=''
binsof=''
'''

def write_resolution(obs='zpt', cut='_jet1pt20', mc='amc', yboostbin=None, ystarbin=None,
        match='', dressed='', puid='', binsof=''):
    cutstring,gencutstring = generate_basiccutstring(cut),generate_basiccutstring('gen'+cut)
    weightstring = "(leptonIDSFWeight)*(leptonIsoSFWeight)*(leptonTriggerSFWeight)"
    if yboostbin and ystarbin:
        ycutstring,genycutstring = generate_basiccutstring('',yboostbin,ystarbin),generate_basiccutstring('gen',yboostbin,ystarbin)
        #namestring = "_yboost_{}-{}_ystar_{}-{}".format(yboostbin[0],yboostbin[1],ystarbin[0],ystarbin[1]).replace('.','')
        namestring = "_yb{}_ys{}".format(int(2*yboostbin[0]),int(2*ystarbin[0]))
    else:
        ycutstring,genycutstring,namestring = '1','1',""
    
    #print cutstring
    #print gencutstring
    #print ycutstring
    #print genycutstring
    input_file = datasets[mc].replace('.root',dressed+puid+'.root')
    #file_in = ROOT.TFile(input_file,"READ")
    print "resolution information will be estimated from ",input_file
    #output_path = plots_folder+cut+dressed+puid+"/resolution_test/"
    #output_path = plots_folder+cut+dressed+puid+"/resolution_new"
    output_path = plots_folder+cut+dressed+puid+"/resolution"
    filename = obs+'_'+mc+namestring+".root"
    if not binsof=='':
        filename = obs+'_'+mc+namestring+"_bins_of_"+binsof+".root"
    output_file = output_path+"/"+filename
    # safety step to avoid overwriting of existing files
    if not os.path.exists(output_path):
        print "create folder",output_path
        os.makedirs(output_path)
    if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        return
    
    print "resolution information will be written to "+output_file
    N = 100
    hmin, hmax = -0.2,0.2
    if obs =='phistareta':
        hmin, hmax = -0.01,0.01
    if obs == 'zy':
        hmin, hmax = -0.1,0.1
    obs_exp = obs
    genobs_exp = 'gen'+obs
    res_exp = "(("+obs_exp+")/("+genobs_exp+")-1)"
    bin_exp = "&&("+genobs_exp+">{})&&("+genobs_exp+"<{})"
    reco_bin_exp = "&&("+obs_exp+">{})&&("+obs_exp+"<{})"
    bins = rebinning(obs,yboostbin,ystarbin)
    if obs in ['yboost','ystar','zy','jet1y']:
        res_exp="("+obs+"-gen"+obs+")"
        if binsof=='zpt':
            bin_exp="&&(genzpt>{})&&(genzpt<{})"
            reco_bin_exp="&&(zpt>{})&&(zpt<{})"
            bins = rebinning('zpt',yboostbin,ystarbin)
        elif binsof=='phistareta':
            bin_exp="&&(genphistareta>{})&&(genphistareta<{})"
            reco_bin_exp="&&(phistareta>{})&&(phistareta<{})"
            bins = rebinning('phistareta',yboostbin,ystarbin)
    print bins
    df_gen, df_reco = ROOT.RDataFrame("genzjetcuts_L1L2L3/ntuple",input_file), ROOT.RDataFrame("zjetcuts_L1L2L3/ntuple",input_file)
    df_gen  = df_gen.Define("res",res_exp)
    df_reco = df_reco.Define("SF",weightstring)
    df_gen  = df_gen.Filter(gencutstring)
    df_reco = df_reco.Filter(cutstring)
    
    file_out = ROOT.TFile(output_file,"RECREATE")
    histlist = ["rms","sigma","sigma1","sigma2","alpha","SF","fakerate","acceptance","stability","purity","PU","matched","switched","truncation"]
    h_gen = ROOT.TH1D("gen"+obs, "", len(bins)-1, array('d',bins))
    [h_rms,h_sigma,h_sigma1,h_sigma2,h_alpha,
        h_SF,h_fake,h_acceptance,h_stability,h_purity,h_PU,h_match,h_switch,h_trunc
    ] = [h_gen.Clone(name) for name in histlist]
    doublegaus = ROOT.TF1("doublegaus","[0]*(TMath::Exp(-x**2/[1]**2)+[2]*TMath::Exp(-x**2/[3]**2))",hmin,hmax)
    obs_histo = ROOT.RDF.TH1DModel("gen"+obs, "", len(bins)-1, array('d',bins))
    jety_histo = ROOT.RDF.TH1DModel("jet1y", "", 24,-2.4,2.4)
    weight_histo = ROOT.RDF.TH1DModel("weight","",4,-2,2)
    df_switch      = df_gen.Filter(cutstring+"&&"+genycutstring+"&&(matchedgenjet1pt>0)&&(matchedgenjet1pt<genjet1pt)")
    h_jet1y_switch = df_switch.Histo1D(jety_histo,'jet1y','weight')
    h_jet1y_switch.Fit("gaus")
    h_jet1y_switch.Write("switchwidth")
    for j in xrange(len(bins)-1):
        genmin, genmax = 1.0*bins[j], 1.0*bins[j+1]
        print "resolution estimation in", genmin, "to", genmax
        binname = "_{}_{}".format(int(genmin),int(genmax))
        if obs =='phistareta' or binsof=='phistareta':
            binname = "_{}_{}".format(int(genmin*10),int(genmax*10))
        print 'fill histograms'
        res_histo = ROOT.RDF.TH1DModel("resolution"+binname,"",N,hmin,hmax)
        df_gen_binned  = df_gen.Filter(genycutstring
                                        +bin_exp.format(genmin,genmax))
        df_reco_binned = df_reco.Filter(ycutstring
                                        +reco_bin_exp.format(genmin,genmax))
        df_gen_binned_res = df_gen_binned.Filter("("+obs_exp+">-990)&&("+genobs_exp+">-990)")
        h_resolution = df_gen_binned_res.Histo1D(res_histo,'res','weight')
        h_SFweight = df_reco_binned.Histo1D(weight_histo,'SF')
        h_genweight = df_gen_binned.Histo1D(weight_histo,'weight')
        #if h_resolution.GetEntries()>0:
        h_trunc.SetBinContent(j+1,h_resolution.Integral()/h_resolution.GetEntries())
        h_trunc.SetBinError(j+1,0)
        h_resolution.Fit("gaus","","")
        sigma = h_resolution.GetFunction("gaus").GetParameter(2)
        rms = h_resolution.GetRMS()
        print "RMS:",rms,"Sigma:",sigma
        h_sigma.SetBinContent(j+1,h_resolution.GetFunction("gaus").GetParameter(2))
        h_sigma.SetBinError(j+1,h_resolution.GetFunction("gaus").GetParError(2))
        h_rms.SetBinContent(j+1,h_resolution.GetRMS())
        h_rms.SetBinError(j+1,h_resolution.GetRMSError())
        doublegaus.SetParameters(h_resolution.GetMaximum(),sigma,0.1,10*rms)
        doublegaus.SetParLimits(1,0,rms)
        doublegaus.SetParLimits(2,0,1)
        doublegaus.SetParLimits(3,rms,1)
        h_resolution.Fit("doublegaus","+","")#,-rms,rms)
        h_sigma1.SetBinContent(j+1,h_resolution.GetFunction("doublegaus").GetParameter(1))
        h_sigma1.SetBinError(j+1,h_resolution.GetFunction("doublegaus").GetParError(1))
        h_alpha.SetBinContent(j+1,h_resolution.GetFunction("doublegaus").GetParameter(2))
        h_alpha.SetBinError(j+1,h_resolution.GetFunction("doublegaus").GetParError(2))
        h_sigma2.SetBinContent(j+1,h_resolution.GetFunction("doublegaus").GetParameter(3))
        h_sigma2.SetBinError(j+1,h_resolution.GetFunction("doublegaus").GetParError(3))
        h_resolution.Write()
        if binsof == '':
            print 'count events'
            N_genbin_recobin = 1.0*df_gen_binned.Filter(cutstring+"&&"+ycutstring
                                                                +("&&("+obs_exp+">{})&&("+obs_exp+"<{})").format(genmin,genmax)).Sum('weight').GetValue()
            N_recobin_genbin = 1.0*df_reco_binned.Filter(gencutstring+"&&"+genycutstring
                                                                +("&&("+genobs_exp+">{})&&("+genobs_exp+"<{})").format(genmin,genmax)).Sum('weight').GetValue()
            N_reco_genbin = 1.0*df_gen_binned.Filter(cutstring).Sum('weight').GetValue()
            N_gen_recobin = 1.0*df_reco_binned.Filter(gencutstring).Sum('weight').GetValue()
            N_genbin, N_recobin = 1.0*df_gen_binned.Sum('weight').GetValue(), 1.0*df_reco_binned.Sum('weight').GetValue()
            N_gen, N_reco = 1.0*df_gen.Sum('weight').GetValue(), 1.0*df_reco.Sum('weight').GetValue()
            print N_gen, N_reco, N_genbin,N_recobin
            df_reco_binned_match    = df_reco_binned.Filter(("(matchedgenjet1pt>0)&&(matchedgenjet1pt==genjet1pt)&&("+obs_exp+">{})&&("+obs_exp+"<{})").format(genmin,genmax))
            N_match             = 1.0*df_reco_binned_match.Sum('weight').GetValue()
            df_reco_binned_switch   = df_reco_binned.Filter(("(matchedgenjet1pt>0)&&(matchedgenjet1pt<genjet1pt)&&("+obs_exp+">{})&&("+obs_exp+"<{})").format(genmin,genmax))
            N_switch            = 1.0*df_reco_binned_switch.Sum('weight').GetValue()
            df_reco_binned_PU       = df_reco_binned.Filter(("(matchedgenjet1pt<0)&&("+obs_exp+">{})&&("+obs_exp+"<{})").format(genmin,genmax))
            N_PU                = 1.0*df_reco_binned_PU.Sum('weight').GetValue()
            print N_match/N_recobin, N_switch/N_recobin, N_PU/N_recobin, N_match+N_switch+N_PU-N_recobin
            genweight = h_genweight.GetMean()
            h_gen.SetBinContent(j+1,genweight*N_genbin)
            h_gen.SetBinError(j+1,error(h_genweight.GetMeanError()*N_genbin,genweight*np.sqrt(N_genbin),0))
            h_SF.SetBinContent(j+1,h_SFweight.GetMean())
            h_SF.SetBinError(j+1,h_SFweight.GetMeanError())
            try:
                h_fake.SetBinContent(j+1,1-N_gen_recobin/N_recobin)
                h_fake.SetBinError(j+1,np.sqrt(N_gen_recobin/N_recobin*(1-N_gen_recobin/N_recobin)/N_recobin))
                print 'fakerate:',1-N_gen_recobin/N_recobin,N_gen_recobin,N_recobin
                h_purity.SetBinContent(j+1,N_genbin_recobin/N_recobin)
                h_purity.SetBinError(j+1,np.sqrt(N_genbin_recobin/N_recobin*(1-N_genbin_recobin/N_recobin)/N_recobin))
                print 'purity:',N_genbin_recobin/N_recobin,N_genbin_recobin,N_recobin
                h_PU.SetBinContent(j+1,N_PU/N_recobin)
                h_PU.SetBinError(j+1,np.sqrt(N_PU/N_recobin*(1-N_PU/N_recobin)/N_recobin))
                h_match.SetBinContent(j+1,N_match/N_recobin)
                h_match.SetBinError(j+1,np.sqrt(N_match/N_recobin*(1-N_match/N_recobin)/N_recobin))
                h_switch.SetBinContent(j+1,N_switch/N_recobin)
                h_switch.SetBinError(j+1,np.sqrt(N_switch/N_recobin*(1-N_switch/N_recobin)/N_recobin))
            except ZeroDivisionError:
                h_fake.SetBinContent(j+1,0)
                h_purity.SetBinContent(j+1,0)
                h_PU.SetBinContent(j+1,0)
                h_match.SetBinContent(j+1,0)
                h_switch.SetBinContent(j+1,0)
                
            try:
                h_acceptance.SetBinContent(j+1,N_reco_genbin/N_genbin)
                h_acceptance.SetBinError(j+1,np.sqrt(N_reco_genbin/N_genbin*(1-N_reco_genbin/N_genbin)/N_genbin))
                print 'acceptance:',N_reco_genbin/N_genbin,N_reco_genbin,N_genbin
                h_stability.SetBinContent(j+1,N_genbin_recobin/N_genbin)
                h_stability.SetBinError(j+1,np.sqrt(N_genbin_recobin/N_genbin*(1-N_genbin_recobin/N_genbin)/N_genbin))
                print 'stability:',N_genbin_recobin/N_genbin,N_genbin_recobin,N_genbin
            except ZeroDivisionError:
                print 'ZeroDivisionError occurred'
                h_acceptance.SetBinContent(j+1,0)
                h_stability.SetBinContent(j+1,0)
    h_resolution.Delete()
    file_out.Write()
    file_out.Close()
    return



#plots_folder = '/ceph/tberger/ZJtriple/ZJtriple'
plots_folder = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple'
for obs in ['zpt','phistareta',
            #'deltaphizjet1',
            #'yboost','ystar',
            'jet1y','zy',
            #'mupluspt','muplusphi','mupluseta','muminuspt','muminuseta','muminusphi','jet1pt',
            ]:
  for cut in ['_jet1pt10',#'_jet1pt10_backtoback',#'_jet1pt10_alpha05',
              '_jet1pt15',#'_jet1pt15_backtoback',#'_jet1pt15_alpha05',
              '_jet1pt20',#'_jet1pt20_backtoback',#'_jet1pt20_alpha05',
              ]:
    for mc in ['mad']:#,'hpp']:
     for match in ['']:
      for dressed in ['_FSR01']:#,'_FSR02','_FSR03','_FSR04']:
       for puid in [   '',#'_puppi',
                    #'_puidloose','_puidmedium','_puidtight'
                    ]:
        for yboostbin in zip(ybins[:-1],ybins[1:]):
         for ystarbin in zip(ybins[:-1],ybins[1:]):
          if not yboostbin[0]+ystarbin[0]>2:
           if obs in ['zpt','phistareta']:
            write_resolution(obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin, dressed=dressed, puid=puid)
           else:
            write_resolution(obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin, dressed=dressed, puid=puid,binsof = 'zpt')
            write_resolution(obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin, dressed=dressed, puid=puid,binsof = 'phistareta')




