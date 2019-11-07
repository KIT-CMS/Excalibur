# -*- coding: utf-8 -*-

# script to estimate zpt, phistareta, jet1y and zy resolution using ROOT dataframes. To be optimized!

# To get it running, you need to source:
#   'export LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64'
#   'source /cvmfs/sft.cern.ch/lcg/views/dev3/latest/x86_64-slc6-gcc8-opt/setup.sh'
# Suggestion: takes a while, use 'nice -n10 python scripts/dataframes_resolution.py' to run the script

import os
import ROOT
import numpy as np
from array import array
from copy import deepcopy
import scipy.stats

ROOT.gROOT.SetBatch()
#ROOT.TH1D.StatOverflows(True)

def error(a,b,c):
    # gives the root of the squared sum of a,b,c
    return np.sqrt(a**2+b**2+c**2)


def betainverse(alpha,N1,N2):
    return scipy.stats.beta.ppf(alpha,N1+1,N2+1)


def generate_basiccutstring(cut='_jet1pt20',yboostbin=None,ystarbin=None):
    # Sets cutstring according to chosen kinematic selection.
    # Basic selection is always applied for gen and reco, respectively:
    basicrecocutstring='(abs(mupluseta)<2.4)&&(abs(muminuseta)<2.4)&&(mupluspt>25)&&(muminuspt>25)&&(abs(zmass-91.1876)<20)'
    basicgencutstring='(abs(genmupluseta)<2.4)&&(abs(genmuminuseta)<2.4)&&(genmupluspt>25)&&(genmuminuspt>25)&&(abs(genzmass-91.1876)<20)'
    cut=cut.split('_')
    if 'gen' in cut:
        basiccutstring = basicgencutstring
    else:
        basiccutstring = basicrecocutstring
    # Additional selection criteria. (Default is jet1pt>20)
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
        #basiccutstring+=('&&(abs('+cut[0]+'zy)>{})&&(abs('+cut[0]+'zy)<{})&&(abs('+cut[0]+'jet1y)>{})&&(abs('+cut[0]+'jet1y)<{})').format(yboostbin[0],yboostbin[1],ystarbin[0],ystarbin[1])
    return basiccutstring

def rebinning(obs,yboostbin=None,ystarbin=None):
    # Adapt histogram binning dependent on rapidity bin.
    if obs == 'mupluspt' or obs == 'muminuspt':
        binning = ' '.join(['{}'.format(x) for x in range(25,300,(300-25)/11)])+' 350'
    if obs in ['zy','jet1y','mupluseta','muminuseta','mu1eta','mu2eta','matchedjet1y','switchedjet1y']:
        binning = '-2.4 -2.2 -2.0 -1.8 -1.6 -1.4 -1.2 -1.00 -0.8 -0.6 -0.4 -0.2 0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8 2.0 2.2 2.4'
    if obs in ['muplusphi','muminusphi','mu1phi','mu2phi']:
        binning = '-3.2 -2.8 -2.4 -2.0 -1.6 -1.2 -0.8 -0.4 0.0 0.4 0.8 1.2 1.6 2.0 2.4 2.8 3.2'
    if obs in ['abszy','absjet1y']:
        binning = '0.0 0.4 0.8 1.2 1.6 2.0 2.4'
    if obs == 'jet1pt':
        binning = '5 10 12 15 20 30 50 75 125 175 225 300 400'
    if obs in ['yboost','ystar','matchedyboost','matchedystar']:
        binning = '0.0 0.5 1.0 1.5 2.0 2.5'
    if obs == 'deltaphizjet1':
        binning = '0.0 0.4 0.8 1.2 1.6 2.0 2.4 2.8 3.2'
    if obs=='zpt':
        if (yboostbin==(0.0,0.5) and ystarbin==(2.0,2.5)):
            print obs+" binning changed"
            binning = '25 30 40 50 70 90 110 150 250 1000'
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
            binning = '0.4 0.6 0.8 1.0 5 50'
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
        'amc' :     '/ceph/tberger/excalibur_results/2019-09-03/mc16_mm_BCDEFGH_DYtoLLamcatnlo.root',
        #'hpp' :     '/ceph/tberger/excalibur_results/2019-09-03/mc16_mm_BCDEFGH_DYtoLLherwigpp.root',
        #'mad' :     '/ceph/tberger/excalibur_results/2019-09-03/mc16_mm_BCDEFGH_DYtoLLmadgraph.root',
        'hpp' :     '/ceph/tberger/excalibur_results/2019-11-06/mc16_mm_BCDEFGH_DYtoLLherwigpp.root',
        'mad' :     '/ceph/tberger/excalibur_results/2019-11-06/mc16_mm_BCDEFGH_DYtoLLmadgraph.root',
        })

'''
obs='zpt'
cut='_jet1pt20'
mc='amc'
yboostbin=(0.0,0.5)
ystarbin=(0.0,0.5)
match=''
postfix=''
binsof=''
'''

def write_resolution(obs='zpt', cut='_jet1pt20', mc='mad', yboostbin=None, ystarbin=None,
        match='', postfix='', binsof='',trunc=''):
    # Script to write obs-resolution to files
    cutstring,gencutstring = generate_basiccutstring(cut),generate_basiccutstring('gen'+cut)
    weightstring = "1"#(leptonIDSFWeight)*(leptonIsoSFWeight)*(leptonTriggerSFWeight)"
    if yboostbin and ystarbin:
        ycutstring,genycutstring = generate_basiccutstring('',yboostbin,ystarbin),generate_basiccutstring('gen',yboostbin,ystarbin)
        namestring = "_yb{}_ys{}".format(int(2*yboostbin[0]),int(2*ystarbin[0]))
        #namestring = "_yz{}_yj{}".format(int(yboostbin[0]/0.5),int(ystarbin[0]/0.5))
    else:
        ycutstring,genycutstring,namestring = '1','1',""
    
    input_file = datasets[mc].replace('.root',postfix+'.root')
    #file_in = ROOT.TFile(input_file,"READ")
    print "resolution information will be estimated from ",input_file
    output_path = plots_folder+cut+postfix+"/resolution"+trunc
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
    N = 50
    hmin, hmax = 0,2
    if obs in ['matchedjet1y','switchedjet1y']:
        obs_exp = 'jet1y'
        genobs_exp = 'genjet1y'
    else:
        obs_exp = obs
        genobs_exp = 'gen'+obs
    res_exp = "(("+obs_exp+")/("+genobs_exp+")-1)"
    bin_exp = "&&("+genobs_exp+">{})&&("+genobs_exp+"<{})"
    reco_bin_exp = "&&("+obs_exp+">{})&&("+obs_exp+"<{})"
    #bins = rebinning(obs)
    bins = rebinning(obs,yboostbin,ystarbin)
    if obs in ['zy','jet1y','switchedjet1y','mupluseta','muplusphi','muminuseta','muminusphi']:
        res_exp="("+obs_exp+"-"+genobs_exp+")"
    if binsof=='zpt':
        bin_exp="&&(genzpt>{})&&(genzpt<{})"
        reco_bin_exp="&&(zpt>{})&&(zpt<{})"
        bins = rebinning('zpt',yboostbin,ystarbin)
    elif binsof=='phistareta':
        bin_exp="&&(genphistareta>{})&&(genphistareta<{})"
        reco_bin_exp="&&(phistareta>{})&&(phistareta<{})"
        bins = rebinning('phistareta',yboostbin,ystarbin)
    if obs in ['matchedjet1y']:
        res_exp="("+obs_exp+"-matched"+genobs_exp+")"
        #bin_exp+="&&(matchedgenjet1pt==genjet1pt)"
    if obs in ['switchedjet1y']:
        bin_exp+="&&(matchedgenjet1pt<genjet1pt)&&(matchedgenjet1pt>0)"
    print bins
    df_gen, df_reco = ROOT.RDataFrame("genzjetcuts_L1L2L3/ntuple",input_file), ROOT.RDataFrame("zjetcuts_L1L2L3/ntuple",input_file)
    df_gen  = df_gen.Define("res",res_exp)
    df_reco = df_reco.Define("SF",weightstring)
    df_gen  = df_gen.Filter(gencutstring)
    df_reco = df_reco.Filter(cutstring)
    
    file_out = ROOT.TFile(output_file,"RECREATE")
    histlist = ["rms","sigma0","sigma","chi2",
        "fakes","losses","stability","purity","PU","matched","switched",
        "gg","qg","aqg","qq","qaq","aqaq"]
    h_gen = ROOT.TH1D("gen"+obs, "", len(bins)-1, array('d',bins))
    [h_rms,h_sigma0,h_sigma,h_chi2,
        h_fake,h_loss,h_stability,h_purity,h_PU,h_match,h_switch,
        h_gg,h_qg,h_aqg,h_qq,h_qaq,h_aqaq
    ] = [h_gen.Clone(name) for name in histlist]
    #doublegaus = ROOT.TF1("doublegaus","[0]*(TMath::Exp(-x**2/[1]**2)+[2]*TMath::Exp(-x**2/[3]**2))",hmin,hmax)
    cryb = ROOT.TF1("cryb","[0]*ROOT::Math::crystalball_function(-abs(x), [1], [3], [2], 0)",hmin,hmax)
    obs_histo = ROOT.RDF.TH1DModel("gen"+obs, "", len(bins)-1, array('d',bins))
    #jety_histo = ROOT.RDF.TH1DModel("jet1y", "", 24,-2.4,2.4)
    weight_histo = ROOT.RDF.TH1DModel("weight","",4,-2,2)
    #df_switch      = df_gen.Filter(cutstring+"&&"+genycutstring+"&&(matchedgenjet1pt>0)&&(matchedgenjet1pt<genjet1pt)")
    #h_jet1y_switch = df_switch.Histo1D(jety_histo,'jet1y','weight')
    #h_jet1y_switch.Fit("gaus")
    #h_jet1y_switch.Write("switchwidth")
    xq = array('d',[0.0,1.0])
    yq = array('d',[0,0])
    if trunc == '_98':
        xq = array('d',[0.01,0.99])
    elif trunc == '_985':
        xq = array('d',[0.0075,0.9925])
    elif trunc == '_95':
        xq = array('d',[0.025,0.975])
    for j in xrange(len(bins)-1):
        genmin, genmax = 1.0*bins[j], 1.0*bins[j+1]
        print "resolution estimation in", genmin, "to", genmax
        binname = "_{}_{}".format(int(genmin),int(genmax))
        if obs =='phistareta' or binsof=='phistareta':
            binname = "_{}_{}".format(int(genmin*10),int(genmax*10))
        print 'fill histograms'
        df_gen_binned  = df_gen.Filter(genycutstring+bin_exp.format(genmin,genmax))
        df_reco_binned = df_reco.Filter(ycutstring+reco_bin_exp.format(genmin,genmax))
        df_gen_binned_res = df_gen_binned.Filter("("+obs_exp+">-990)&&("+genobs_exp+">-990)")
        test_histo = ROOT.RDF.TH1DModel("test","",1000,-10,10)
        h_test = df_gen_binned_res.Histo1D(test_histo,'res','weight')
        h_test.GetQuantiles(2,yq,xq)
        hmin, hmax = yq[0],yq[1]
        print hmin, hmax
        N = max(min(200,int(h_test.GetEntries()/50)),15)
        res_histo = ROOT.RDF.TH1DModel("resolution"+binname,"",N,hmin,hmax)
        h_resolution = df_gen_binned_res.Histo1D(res_histo,'res','weight')
        h_genweight = df_gen_binned.Histo1D(weight_histo,'weight')
        if not h_resolution.GetEntries() > 0:
            print "WARNING: bin does not contain any events!"
            continue
        h_resolution.Fit("gaus","","")
        sigma = h_resolution.GetFunction("gaus").GetParameter(2)
        rms = h_resolution.GetRMS()
        print "RMS:",rms,"Sigma:",sigma,"chi2 / NDF:",h_resolution.GetFunction("gaus").GetChisquare(),"/",h_resolution.GetFunction("gaus").GetNDF()
        h_sigma0.SetBinContent(j+1,sigma)
        h_sigma0.SetBinError(j+1,h_resolution.GetFunction("gaus").GetParError(2))
        h_rms.SetBinContent(j+1,rms)
        h_rms.SetBinError(j+1,h_resolution.GetRMSError())
        cryb.SetParameters(h_resolution.GetMaximum(),1,sigma,1)
        #cryb.SetParLimits(1,0.1,10)
        cryb.SetParLimits(2,sigma/10,1)
        #doublegaus.SetParameters(h_resolution.GetMaximum(),sigma,0.1,10*rms)
        #doublegaus.SetParLimits(1,0,rms)
        #doublegaus.SetParLimits(2,0,1)
        #doublegaus.SetParLimits(3,rms,1)
        #h_resolution.Fit("doublegaus","+","")#,-rms,rms)
        #h_sigma1.SetBinContent(j+1,h_resolution.GetFunction("doublegaus").GetParameter(1))
        #h_sigma1.SetBinError(j+1,h_resolution.GetFunction("doublegaus").GetParError(1))
        #h_alpha.SetBinContent(j+1,h_resolution.GetFunction("doublegaus").GetParameter(2))
        #h_alpha.SetBinError(j+1,h_resolution.GetFunction("doublegaus").GetParError(2))
        #h_sigma2.SetBinContent(j+1,h_resolution.GetFunction("doublegaus").GetParameter(3))
        #h_sigma2.SetBinError(j+1,h_resolution.GetFunction("doublegaus").GetParError(3))
        h_resolution.Fit("cryb","+","")
        h_sigma.SetBinContent(j+1,h_resolution.GetFunction("cryb").GetParameter(2))
        h_sigma.SetBinError(j+1,h_resolution.GetFunction("cryb").GetParError(2))
        print "chi2 / NDF:",h_resolution.GetFunction("cryb").GetChisquare(),"/",h_resolution.GetFunction("cryb").GetNDF()
        try:
            h_chi2.SetBinContent(j+1,h_resolution.GetFunction("cryb").GetChisquare()/h_resolution.GetFunction("cryb").GetNDF())
        except ZeroDivisionError:
            h_chi2.SetBinContent(j+1,0)
        h_chi2.SetBinError(j+1,0)
        h_resolution.Write()
        if binsof == '':
            print 'count events'
            w_genbin_recobin = 1.0*df_gen_binned.Filter(cutstring+"&&"+ycutstring
                                                        +reco_bin_exp.format(genmin,genmax)).Sum('weight').GetValue()
                                                        #+("&&("+obs_exp+">{})&&("+obs_exp+"<{})").format(genmin,genmax)).Sum('weight').GetValue()
            w_recobin_genbin = 1.0*df_reco_binned.Filter(gencutstring+"&&"+genycutstring
                                                        +bin_exp.format(genmin,genmax)).Sum('weight').GetValue()
                                                        #+("&&("+genobs_exp+">{})&&("+genobs_exp+"<{})").format(genmin,genmax)).Sum('weight').GetValue()
            w_reco_genbin = 1.0*df_gen_binned.Filter(cutstring).Sum('weight').GetValue()
            w_gen_recobin = 1.0*df_reco_binned.Filter(gencutstring).Sum('weight').GetValue()
            w_genbin, w_recobin = 1.0*df_gen_binned.Sum('weight').GetValue(), 1.0*df_reco_binned.Sum('weight').GetValue()
            w_gen, w_reco = 1.0*df_gen.Sum('weight').GetValue(), 1.0*df_reco.Sum('weight').GetValue()
            print w_gen, w_reco, w_genbin,w_recobin
            #df_reco_binned_match    = df_reco_binned.Filter(("(matchedgenjet1pt>0)&&(matchedgenjet1pt==genjet1pt)&&("+obs_exp+">{})&&("+obs_exp+"<{})").format(genmin,genmax))
            #N_match             = 1.0*df_reco_binned_match.Sum('weight').GetValue()
            #df_gen_binned_match    = df_gen_binned.Filter(cutstring+"&&(matchedgenjet1pt>0)&&(matchedgenjet1pt==genjet1pt)")
            #df_reco_binned_switch   = df_reco_binned.Filter(("(matchedgenjet1pt>0)&&(matchedgenjet1pt<genjet1pt)&&("+obs_exp+">{})&&("+obs_exp+"<{})").format(genmin,genmax))
            #N_switch            = 1.0*df_reco_binned_switch.Sum('weight').GetValue()
            #df_gen_binned_switch   = df_gen_binned.Filter(cutstring+"&&(matchedgenjet1pt>0)&&(matchedgenjet1pt<genjet1pt)")
            #N_switch            = 1.0*df_gen_binned_switch.Sum('weight').GetValue()
            #df_reco_binned_PU       = df_reco_binned.Filter(("(matchedgenjet1pt<0)&&("+obs_exp+">{})&&("+obs_exp+"<{})").format(genmin,genmax))
            #N_PU                = 1.0*df_reco_binned_PU.Sum('weight').GetValue()
            #df_gen_binned_PU       = df_gen_binned.Filter(cutstring+"&&(matchedgenjet1pt<0)")
            #N_PU                = 1.0*df_gen_binned_PU.Sum('weight').GetValue()
            w_match             = 1.0*df_gen_binned.Filter(cutstring+"&&(matchedgenjet1pt>0)&&(matchedgenjet1pt==genjet1pt)").Sum('weight').GetValue()
            w_switch            = 1.0*df_gen_binned.Filter(cutstring+"&&(matchedgenjet1pt>0)&&(matchedgenjet1pt<genjet1pt)").Sum('weight').GetValue()
            w_PU                = 1.0*df_gen_binned.Filter(cutstring+"&&(matchedgenjet1pt<0)").Sum('weight').GetValue()
            w_sum = w_match+w_switch+w_PU
            genweight = h_genweight.GetMean()
            h_gen.SetBinContent(j+1,w_genbin)
            N_recobin     = df_reco_binned.Count().GetValue()
            N_genbin      = df_gen_binned.Count().GetValue()
            N_reco_genbin = df_gen_binned.Filter(cutstring).Count().GetValue()
            #print N_genbin,N_recobin
            w_gg = 1.0*df_gen_binned.Filter("(parton1flavour==21)&&(parton2flavour==21)").Sum('weight').GetValue()
            w_aqaq = 1.0*df_gen_binned.Filter("(parton1flavour<0)&&(parton2flavour<0)").Sum('weight').GetValue()
            w_qq = 1.0*df_gen_binned.Filter("(parton1flavour>0)&&(parton1flavour<10)&&(parton2flavour>0)&&(parton2flavour<10)").Sum('weight').GetValue()
            w_qaq = 1.0*df_gen_binned.Filter("((parton1flavour>0&&parton1flavour<10&&parton2flavour<0)||(parton1flavour<0&&parton2flavour>0&&parton2flavour<10))").Sum('weight').GetValue()
            w_qg  = 1.0*df_gen_binned.Filter("((parton1flavour>0&&parton1flavour<10&&parton2flavour==21)||(parton1flavour==21&&parton2flavour>0&&parton2flavour<10))").Sum('weight').GetValue()
            w_aqg  = 1.0*df_gen_binned.Filter("((parton1flavour<0&&parton2flavour==21)||(parton1flavour==21&&parton2flavour<0))").Sum('weight').GetValue()
            try:
                h_fake.SetBinContent(       j+1,w_gen_recobin/w_recobin)
                h_fake.SetBinError(         j+1,np.sqrt(w_gen_recobin/w_recobin*(1-w_gen_recobin/w_recobin)/N_recobin))
                print 'fakes:',1-w_gen_recobin/w_recobin,w_gen_recobin,w_recobin
                h_purity.SetBinContent(     j+1,w_genbin_recobin/w_recobin)
                h_purity.SetBinError(       j+1,np.sqrt(w_genbin_recobin/w_recobin*(1-w_genbin_recobin/w_recobin)/N_recobin))
                print 'purity:',w_genbin_recobin/w_recobin,w_genbin_recobin,w_recobin
            except ZeroDivisionError:
                h_fake.SetBinContent(       j+1,0)
                h_purity.SetBinContent(     j+1,0)
                h_PU.SetBinContent(         j+1,0)
                h_match.SetBinContent(      j+1,0)
                h_switch.SetBinContent(     j+1,0)
                
            try:
                h_loss.SetBinContent(       j+1,w_reco_genbin/w_genbin)
                h_loss.SetBinError(         j+1,np.sqrt(w_reco_genbin/w_genbin*(1-w_reco_genbin/w_genbin)/N_genbin))
                print 'losses:',w_reco_genbin/w_genbin,w_reco_genbin,w_genbin
                h_stability.SetBinContent(  j+1,w_genbin_recobin/w_genbin)
                h_stability.SetBinError(    j+1,np.sqrt(w_genbin_recobin/w_genbin*(1-w_genbin_recobin/w_genbin)/N_genbin))
                print 'stability:',w_genbin_recobin/w_genbin,w_genbin_recobin,w_genbin
                h_PU.SetBinContent(         j+1,w_PU/w_sum)
                h_PU.SetBinError(           j+1,np.sqrt(w_PU/w_sum*(1-w_PU/w_sum)/N_reco_genbin))
                h_match.SetBinContent(      j+1,w_match/w_sum)
                h_match.SetBinError(        j+1,np.sqrt(w_match/w_sum*(1-w_match/w_sum)/N_reco_genbin))
                h_switch.SetBinContent(     j+1,w_switch/w_sum)
                h_switch.SetBinError(       j+1,np.sqrt(w_switch/w_sum*(1-w_switch/w_sum)/N_reco_genbin))
                print "matched:",w_match/w_sum,'switched:',w_switch/w_sum,'pileup:',w_PU/w_sum,'all:',w_reco_genbin/w_sum
                h_gg.SetBinContent(         j+1,w_gg/w_genbin)
                h_gg.SetBinError(           j+1,np.sqrt(w_gg/w_genbin*(1-w_gg/w_genbin)/N_genbin))
                h_qg.SetBinContent(         j+1,w_qg/w_genbin)
                h_qg.SetBinError(           j+1,np.sqrt(w_qg/w_genbin*(1-w_qg/w_genbin)/N_genbin))
                h_aqg.SetBinContent(        j+1,w_aqg/w_genbin)
                h_aqg.SetBinError(          j+1,np.sqrt(w_aqg/w_genbin*(1-w_aqg/w_genbin)/N_genbin))
                h_qq.SetBinContent(         j+1,w_qq/w_genbin)
                h_qq.SetBinError(           j+1,np.sqrt(w_qq/w_genbin*(1-w_qq/w_genbin)/N_genbin))
                h_qaq.SetBinContent(        j+1,w_qaq/w_genbin)
                h_qaq.SetBinError(          j+1,np.sqrt(w_qaq/w_genbin*(1-w_qaq/w_genbin)/N_genbin))
                h_aqaq.SetBinContent(       j+1,w_aqaq/w_genbin)
                h_aqaq.SetBinError(         j+1,np.sqrt(w_aqaq/w_genbin*(1-w_aqaq/w_genbin)/N_genbin))
                print "gg:",w_gg/w_genbin,"aqaq:",w_aqaq/w_genbin,"qq:",w_qq/w_genbin,"qaq:",w_qaq/w_genbin,"qg:",w_qg/w_genbin,"aqg:",w_aqg/w_genbin,"all:",(w_gg+w_aqaq+w_qq+w_qaq+w_qg+w_aqg)/w_genbin
            except ZeroDivisionError:
                print 'ZeroDivisionError occurred'
                h_loss.SetBinContent(       j+1,0)
                h_stability.SetBinContent(  j+1,0)
    h_resolution.Delete()
    file_out.Write()
    file_out.Close()
    return


ybins = [0.0,0.5,1.0,1.5,2.0,2.5]

# Select output folder:
#plots_folder = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple_2019-08-02'
#plots_folder = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple_2019-09-05'
#plots_folder = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple_2019-09-12'
plots_folder = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple_2019-11-06'

# The following loop loops over all observables (obs), selection criteria (cut), simulations (mc), histogram truncation (trunc), additional attributes (postfix) and rapidity bins (yboostbin,ystarbin):
for obs in ['zpt','phistareta',
            #'jet1y',
            'zy',
            'matchedjet1y',#'switchedjet1y',
            ]:
 for cut in [#'_jet1pt10',#'_jet1pt10_backtoback',#'_jet1pt10_alpha05',
              #'_jet1pt15',#'_jet1pt15_backtoback',#'_jet1pt15_alpha05',
              '_jet1pt20',#'_jet1pt20_backtoback',#'_jet1pt20_alpha05',
              ]:
  for mc in ['mad']:
   for trunc in ['_985']:#,'_95']:#,'_98','_95']:
    for postfix in ['',#'_puppi','_ak8',
                    #'_puidloose','_puidmedium','_puidtight'
                    #'_R02',#'_R04','_R06','_R09'
                    ]:
     for yboostbin in zip(ybins[:-1],ybins[1:]):
      for ystarbin in zip(ybins[:-1],ybins[1:]):
       if not yboostbin[0]+ystarbin[0]>2:
        if obs in ['zpt','phistareta']:
            write_resolution(obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin, postfix=postfix,trunc=trunc)
        elif obs in ['mupluspt','mupluseta','muplusphi']:
            write_resolution(obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin, postfix=postfix, binsof = 'zpt', trunc=trunc)
            write_resolution(obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin, postfix=postfix, binsof = 'phistareta', trunc=trunc)
        else:
            write_resolution(obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin, postfix=postfix, binsof = 'zpt', trunc=trunc)
            write_resolution(obs, cut, mc=mc, yboostbin=yboostbin, ystarbin=ystarbin, postfix=postfix, binsof = 'phistareta', trunc=trunc)

# Continue with plotting script Plotting/configs/qcd_cross_section_3Dhist.py
