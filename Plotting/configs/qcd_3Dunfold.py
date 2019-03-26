# -*- coding: utf-8 -*-

from Excalibur.Plotting.utility.toolsZJet import PlottingJob
from Excalibur.Plotting.utility.binningsZJet import rebinning
from Excalibur.Plotting.utility.toolsQCD import error, basic_xsec, generate_datasets, generate_ylims, generate_variationstring
import Excalibur.Plotting.utility.colors as colors

from copy import deepcopy
import ROOT
import numpy as np
import os
from array import array

'''
if os.environ["CMSSW_BASE"] == "/portal/ekpbms2/home/tberger/Excalibur/CMSSW_9_4_2":
    from scipy.integrate import quad
    from pynverse import inversefunc
    S1,S2,Al = 0.0215797029742, 0.0554388992754, 0.307163970595
    def doublegauss(x,S1,S2,Al):
        return (np.exp(-x**2/2/S1**2)+Al*np.exp(-x**2/2/S2**2))/np.sqrt(2*np.pi)/(S1+S2*Al)
    print 2*np.sqrt(2*np.pi)/(1+0.1*10)
    print [doublegauss(x,S1,S2,Al) for x in [-1,0,1]]
    def doubleerf(x,S1,S2,Al):
    #def doubleerf(x):
        return quad(doublegauss,-np.inf,x,args=(S1,S2,Al))[0]
        #return quad(doublegauss,-np.inf,x,args=(1,10,0.1))[0]
    print [doubleerf(x,S1,S2,Al) for x in [-1,0,1]]
    def invdoubleerf(x,S1,S2,Al):
        inv = inversefunc(doubleerf,args=(S1,S2,Al))
        #inv = inversefunc(doubleerf)
        return 1*inv(x)
    print [invdoubleerf(x,S1,S2,Al) for x in [0.1, 0.5, 0.9]]
'''

datasets = generate_datasets(args=None)
ylims = generate_ylims(args=None)
variationstring = generate_variationstring(args=None)
#plots_folder = '/ceph/tberger/ZJtriple_2018/ZJtriple'
#plots_folder = '/ceph/tberger/ZJtriple/ZJtriple'
plots_folder = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple'

def prepare_3Dhist(args=None, obs='zpt'):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, '', '', '', yboostbin=None, ystarbin=None)
    l_ybinedges = [0,5,9,12,14,0]
    l_obshists,l_obsbinedges,counter = [],[],0
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
        l_obsbinedges.append(counter)
        counter+=l_obshists[index].GetNbinsX()
    h_reco = ROOT.TH1D(obs,"",counter,0,counter)
    h_gen = ROOT.TH1D("gen"+obs,"",counter,0,counter)
    h_response = ROOT.TH2D("response","",counter,0,counter,counter,0,counter)
    return [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges]

def invert_3Dhists(args=None, filename = ''):
    if filename == '':
        print "WARNING: filename must be specified!"
        return
    if 'phistareta' in filename:
        obs = 'phistareta'
        [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,'phistareta')
    elif 'zpt' in filename:
        obs = 'zpt'
        [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,'zpt')
    file_in = ROOT.TFile(filename,"READ")
    namelist = [key.GetName() for key in file_in.GetListOfKeys()]
    print namelist
    output_file = filename.replace('.root','_binned.root')
    file_out = ROOT.TFile(output_file,"RECREATE")
    for histname in namelist:
        hist = file_in.Get(histname)
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
                        genysmin += 0.5
                        genysmax += 0.5
                        genybmin,genybmax = 0.0,0.5
                namestring = "_yb{}_ys{}".format(int(2*genybmin),int(2*genysmin))
                hist_bin  = l_obshists[hist_index].Clone(histname+namestring)
            bin_index += 1
            hist_bin.SetBinContent(bin_index,hist.GetBinContent(obsbin+1))
            hist_bin.SetBinError(bin_index,hist.GetBinError(obsbin+1))
        hist_bin.Write(histname+namestring)
    print "histograms written to",output_file

def loop_3Dhist(args=None):
    plots = []
    for obs in ['zpt']:
     for cut in [#'_jet1pt10',
                 #'_jet1pt15',
                 '_jet1pt20',
                 ]:
      #for data in [ 'amc',#'hpp','mad',
      #              #'BCDEFGH',
      #              #'TTJets','TW','ZZ','WZ','WW'
      #              #'TTJets','ST','ZZ','WZ','WW','WJets'
      #              ]:
      for (data,mc) in [#('BCDEFGH','toy'),#('BCDEFGH','amc'),('BCDEFGH','mad'),('BCDEFGH','hpp'),
                        ('amc','toy'),('amc','amc'),('amc','mad'),('amc','hpp'),
                        ('mad','toy'),('mad','amc'),('mad','mad'),('mad','hpp'),
                        ('hpp','toy'),('hpp','amc'),('hpp','mad'),('hpp','hpp'),
                        ]:
       for match in ['',
                     #'_matched',#'_switched',
                     ]:#,'_PU']:
        for dressed in ['',
                        #'_FSR01'
                        ]:
         for puid in ['',
                    #'_puppi','_puidloose','_puidmedium','_puidtight'
                    ]:
          for varquantity in [#'',
                            '_stats',#'_toy','_SF'
                            #'_switch',#'_Robs','_Ryz','_Ryj',#'_w1',
                            #'_IDSF','_IsoSF','_TriggerSF',
                            ]:
           for variation in [0,
                            #-1,1
                            ]:
            #create_3Dhist(args, obs, cut, data, match,dressed,puid,varquantity=varquantity,variation=variation)
            uncertainties_3Dhist(args,obs,cut,data,match,dressed,puid,varquantity)
            
  #          invert_3Dhist(args, obs, cut, data, mc,match,dressed,puid,varquantity,variation)

    if plots==[]:
        return
    else:
        return [PlottingJob(plots=plots, args=args)]

def create_3Dhist(args=None, obs='zpt', cut='_jet1pt15', data='BCDEFGH', match='', dressed='_FSR01', puid='', varquantity='', variation=0):
    if data == 'toy':
        print "toy mc not created by this function."
        return 
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, data, yboostbin=None, ystarbin=None)
    [l_obshists, h_reco, h_gen, h_recoresponse, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args, obs)
    # simulations are always scaled to match data comparison (weight, lumi)
    if data == 'BCDEFGH':
        lumi = 1
        match = ''
    else:
        lumi = d['lumis'][0]
    h_genresponse = deepcopy(h_recoresponse)
    if varquantity == '_JEC':
        input_file = '/ceph/tberger/excalibur_results/2019-03-20/data16_mm_BCDEFGH_SiMu07Aug17'+dressed+varquantity+variationstring[variation]+'.root'
    elif varquantity == '_JER':
        input_file = '/ceph/tberger/excalibur_results/2019-03-20/data16_mm_BCD_SiMu07Aug17'+dressed+'_smearedJets.root'
    else:
        input_file = datasets[data].replace('.root',dressed+puid+'.root')
    f_in = ROOT.TFile(input_file,"READ")
    print "use file",input_file
    output_file = plots_folder+cut+dressed+puid+'/'+obs+"_"+data+match+".root"
    if not varquantity in ['_IDSF','_IsoSF','_TriggerSF','_JEC']:
        variation = 0
    if varquantity=='_JER' or not variation == 0:
        output_file = plots_folder+cut+dressed+puid+'/variations/'+obs+"_"+data+match+varquantity+variationstring[variation]+".root"
    print "response will be written to", output_file
    if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        return
    ntuple_gen, ntuple_reco = f_in.Get("genzjetcuts_L1L2L3/ntuple"), f_in.Get("zjetcuts_L1L2L3/ntuple")
    if data == 'BCDEFGH':
        ntuple_reco = f_in.Get("zjetcuts_L1L2L3Res/ntuple")
    f_out = ROOT.TFile(output_file,"RECREATE")
    print 'Fill 3D reco histogram'
    obsmin, obsmax = l_obshists[0].GetXaxis().GetXbins()[0],l_obshists[0].GetXaxis().GetXbins()[l_obshists[0].GetNbinsX()]
    for entry in ntuple_reco:
        #yb,ys,event,weight = entry.yboost,entry.ystar,entry.event,entry.weight
        zy,jet1y,event,weight = entry.zy,entry.jet1y,entry.event,entry.weight
        recocutweight = ( (entry.mupluspt >25) & (abs(entry.mupluseta) <2.4)
                        & (entry.muminuspt>25) & (abs(entry.muminuseta)<2.4)
                        & (abs(entry.zmass-91.1876)<20) )
        #genyb,genys = ((entry.genyboost,entry.genystar) if not data == 'BCDEFGH' else (yb,ys))
        genzy,genjet1y = ( (entry.genzy, entry.genjet1y) if not data == 'BCDEFGH' else (zy,jet1y))
        gencutweight = (  (entry.genmupluspt >25) & (abs(entry.genmupluseta) <2.4)
                        & (entry.genmuminuspt>25) & (abs(entry.genmuminuseta)<2.4)
                        & (abs(entry.genzmass-91.1876)<20) 
                        if not data == 'BCDEFGH' else recocutweight)
        jet1pt = entry.jet1pt
        genjet1pt = (entry.genjet1pt if not data == 'BCDEFGH' else jet1pt)
        #jet2pt = entry.jet2pt
        #jet3pt = entry.jet3pt
        if varquantity == '_JetPt':
            jet1pt *= (1+0.1*np.random.randn())
            jet2pt *= (1+0.1*np.random.randn())
            jet3pt *= (1+0.1*np.random.randn())
            if jet1pt<0:
                print "jet1 switched below 0",entry.jet1pt
                break
            if jet2pt>jet1pt:
                #print "jet1 switched to jet2:",entry.jet1pt,entry.jet2pt
                jet1pt = jet2pt
                jet1y  = entry.jet2y
            if jet3pt>jet1pt:
                #print "jet3 switched to jet1:",entry.jet1pt,entry.jet2pt,entry.jet3pt,jet1pt,jet2pt,jet3pt
                jet1pt = jet2pt
                jet1y  = entry.jet2y
        yb,ys = 0.5*abs(zy+jet1y),0.5*abs(zy-jet1y)
        genyb,genys = 0.5*abs(genzy+genjet1y),0.5*abs(genzy-genjet1y)
        if 'jet1pt20' in cut.split('_'):
            gencutweight  &= ((genjet1pt>20) if not data == 'BCDEFGH' else 1)
            recocutweight &= (jet1pt>20)
        if 'jet1pt15' in cut.split('_'):
            gencutweight  &= ((genjet1pt>15) if not data == 'BCDEFGH' else 1)
            recocutweight &= (jet1pt>15)
        if 'jet1pt10' in cut.split('_'):
            gencutweight  &= ((genjet1pt>10) if not data == 'BCDEFGH' else 1)
            recocutweight &= (jet1pt>10)
        if not recocutweight:
            continue
        SFweight = entry.leptonIDSFWeight * entry.leptonIsoSFWeight * entry.leptonTriggerSFWeight
        if varquantity == '_IDSF':
          if variation == -1:
            SFweight = entry.leptonIDSFWeightDown * entry.leptonIsoSFWeight * entry.leptonTriggerSFWeight
          if variation == 1:
            SFweight = entry.leptonIDSFWeightUp * entry.leptonIsoSFWeight * entry.leptonTriggerSFWeight
        if varquantity == '_IsoSF':
          if variation == -1:
            SFweight = entry.leptonIDSFWeight * entry.leptonIsoSFWeightDown * entry.leptonTriggerSFWeight
          if variation == 1:
            SFweight = entry.leptonIDSFWeight * entry.leptonIsoSFWeightUp * entry.leptonTriggerSFWeight
        if varquantity == '_TriggerSF':
          if variation == -1:
            SFweight = entry.leptonIDSFWeight * entry.leptonIsoSFWeight * entry.leptonTriggerSFWeightDown
          if variation == 1:
            SFweight = entry.leptonIDSFWeight * entry.leptonIsoSFWeight * entry.leptonTriggerSFWeightUp
        if match == '_matched':
            gencutweight  &= (entry.matchedgenjet1pt==entry.genjet1pt)
            recocutweight &= (entry.matchedgenjet1pt==entry.genjet1pt)
        if match == '_switched':
            gencutweight  &= ((entry.matchedgenjet1pt<entry.genjet1pt) & (entry.matchedgenjet1pt>0))
            recocutweight &= ((entry.matchedgenjet1pt<entry.genjet1pt) & (entry.matchedgenjet1pt>0))
        if match == '_PU':
            gencutweight  &= (entry.matchedgenjet1pt<0)
            recocutweight &= (entry.matchedgenjet1pt<0)
        if obs =='zpt':
            recoobs,genobs = entry.zpt,(entry.genzpt if not data == 'BCDEFGH' else entry.zpt)
        elif obs =='phistareta':
            recoobs,genobs = entry.phistareta,(entry.genphistareta if not data == 'BCDEFGH' else entry.phistareta)
        else:
            print "WARNING: creation of 3D histogram for observable not implemented!"
            return
        if abs(yb+ys)>2.5 or recoobs<obsmin or recoobs>obsmax:
            continue
        y_index = l_ybinedges[int(ys/0.5)]+int(yb/0.5)
        obs_index = l_obsbinedges[y_index]+l_obshists[y_index].FindBin(recoobs)-1
        if abs(genyb+genys)>2.5 or genobs<obsmin or genobs>obsmax:
            geny_index,genobs_index = 0,-1
        else:
            geny_index = l_ybinedges[int(genys/0.5)]+int(genyb/0.5)
            genobs_index = l_obsbinedges[geny_index]+l_obshists[geny_index].FindBin(genobs)-1
        h_reco.Fill(obs_index,recocutweight*weight*SFweight*lumi)
        h_recoresponse.Fill(obs_index,genobs_index,recocutweight*gencutweight*weight*SFweight*lumi)
    
    print 'Fill 3D gen histogram'
    if not data == 'BCDEFGH':
      for entry in ntuple_gen:
        #yb,ys,event,weight = entry.yboost,entry.ystar,entry.event,entry.weight
        yb,ys,event,weight = 0.5*abs(entry.zy+entry.jet1y),0.5*abs(entry.zy-entry.jet1y),entry.event,entry.weight
        gencutweight = ((entry.genmupluspt>25) & (abs(entry.genmupluseta)<2.4)
                        & (entry.genmuminuspt>25) & (abs(entry.genmuminuseta)<2.4)
                        & (abs(entry.genzmass-91.1876)<20))
        genyb,genys = entry.genyboost,entry.genystar
        genyb,genys = 0.5*abs(entry.genzy+entry.genjet1y),0.5*abs(entry.genzy-entry.genjet1y)
        recocutweight = ((entry.mupluspt>25) & (abs(entry.mupluseta)<2.4) 
                        & (entry.muminuspt>25) & (abs(entry.muminuseta)<2.4)
                        & (abs(entry.zmass-91.1876)<20))
        if 'jet1pt20' in cut.split('_'):
            gencutweight  &= (entry.genjet1pt>20)
            recocutweight &= (entry.jet1pt>20)
        if 'jet1pt10' in cut.split('_'):
            gencutweight  &= (entry.genjet1pt>10)
            recocutweight &= (entry.jet1pt>10)
        if not gencutweight:
            continue
        SFweight = entry.leptonIDSFWeight * entry.leptonIsoSFWeight * entry.leptonTriggerSFWeight
        if match == '_matched':
            gencutweight  &= (entry.matchedgenjet1pt==entry.genjet1pt)
            recocutweight &= (entry.matchedgenjet1pt==entry.genjet1pt)
        if match == '_switched':
            gencutweight  &= ((entry.matchedgenjet1pt<entry.genjet1pt) & (entry.matchedgenjet1pt>0))
            recocutweight &= ((entry.matchedgenjet1pt<entry.genjet1pt) & (entry.matchedgenjet1pt>0))
        if match == '_PU':
            gencutweight  &= (entry.matchedgenjet1pt<0)
            recocutweight &= (entry.matchedgenjet1pt<0)
        if obs =='zpt':
            recoobs,genobs = entry.zpt,entry.genzpt
        elif obs =='phistareta':
            recoobs,genobs = entry.phistareta,entry.genphistareta
        else:
            print "WARNING: creation of 3D histogram for observable not implemented!"
            return
        if abs(genyb+genys)>2.5  or genobs<obsmin or genobs>obsmax:
            continue
        geny_index = l_ybinedges[int(genys/0.5)]+int(genyb/0.5)
        genobs_index = l_obsbinedges[geny_index]+l_obshists[geny_index].FindBin(genobs)-1
        if abs(yb+ys)>2.5 or recoobs<obsmin or recoobs>obsmax:
            y_index,obs_index= 0,-1
        else:
            y_index = l_ybinedges[int(ys/0.5)]+int(yb/0.5)
            obs_index = l_obsbinedges[y_index]+l_obshists[y_index].FindBin(recoobs)-1
        h_gen.Fill(genobs_index,gencutweight*weight*lumi)
        h_genresponse.Fill(obs_index,genobs_index,recocutweight*gencutweight*weight*lumi)
    print "response written to", output_file
    h_reco.Write()
    h_gen.Write()
    h_recoresponse.Write()
    h_genresponse.Write("response_2")
    return

'''
args=None
obs='zpt'
cut='_jet1pt20'
mc='mad'
match=''
dressed='_FSR01'
puid=''
varquantity=''
variation=0
N_toys=1000000
'''

def toyloop_3D(args=None):
    N_toys = 100000000
    for cut in ['_jet1pt10','_jet1pt15','_jet1pt20']:
     #for data in ['BCDEFGH','amc','hpp','mad','TTJets','TW','WW','WZ','ZZ']:
     #   create_3Dhist(obs='zpt',       cut=cut,data=data)
     #   create_3Dhist(obs='phistareta',cut=cut,data=data)
     create_toy3Dhist(obs='zpt',       cut=cut,N_toys=N_toys)
     create_toy3Dhist(obs='phistareta',cut=cut,N_toys=N_toys)
     for varquantity in ['_Robs','_Ryj','_Ryz','_A','_F']:#,'_switch','_SF'
      for variation in [-1,1]:
        create_toy3Dhist(obs='zpt',       cut=cut,varquantity=varquantity,variation=variation,N_toys=N_toys)
        create_toy3Dhist(obs='phistareta',cut=cut,varquantity=varquantity,variation=variation,N_toys=N_toys)
    return


def create_toy3Dhist(args=None, obs='phistareta', cut='_jet1pt20', mc='mad', match='', dressed='_FSR01', puid='', varquantity='_Robs', variation=0, N_toys=100000000):
    if mc == 'BCDEFGH':
        print "Can not create toy mc from data."
        return
    if varquantity in ['','_stats','_IDSF','_IsoSF','_TriggerSF']:
        variation = 0
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, '', mc, yboostbin=None, ystarbin=None)
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    h_genresponse = h_response.Clone("response_2")
    l_RMSobs,l_RMSyz,l_RMSyj,l_switch,l_weight,l_A,l_F,l_SF,l_swwidth= [],[],[],[],[],[],[],[],[]
    l_genobsmin,l_genobsmax,l_genobscenter,l_genybmin,l_genybmax,l_genysmin,l_genysmax = [],[],[],[],[],[],[]
    #input_path = "/ceph/tberger/plots/resolution_dataframes/resolution_"+mc+cut+dressed+puid
    input_path  = plots_folder+cut+dressed+puid+'/resolution'
    #output_file = plots_folder+cut+dressed+puid+'/'+obs+'_toy_from_'+mc+match+'.root'
    output_file = plots_folder+cut+dressed+puid+'/'+obs+'_toy'+match+'.root'
    if not variation == 0:
        output_file = plots_folder+cut+dressed+puid+'/variations/'+obs+'_toy'+match+varquantity+variationstring[variation]+'.root'
    # safety step to avoid overwriting of existing files
    if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        return
    print "3DtoyMC will be written to "+output_file
    f_out = ROOT.TFile(output_file,"RECREATE")
    hist_index, bin_index = 0,0
    
    genybmin,genybmax,genysmin,genysmax = 0.0,0.5,0.0,0.5
    obsmin, obsmax = l_obshists[0].GetXaxis().GetXbins()[0],l_obshists[0].GetXaxis().GetXbins()[l_obshists[0].GetNbinsX()]
    for obsbin in xrange(h_gen.GetNbinsX()):
        if obsbin in l_obsbinedges:
            if not obsbin==0:
                bin_index = 0
                hist_index += 1
                genybmin += 0.5
                genybmax += 0.5
                if obsbin in ([93,167,222,256] if obs=='zpt' else [85,152,201,227]):
                    genysmin += 0.5
                    genysmax += 0.5
                    genybmin,genybmax = 0.0,0.5
            namestring = "_yb{}_ys{}".format(int(2*genybmin),int(2*genysmin))
            print input_path+"/"+obs+"_"+mc+namestring+".root"
            f_in_obs = ROOT.TFile(input_path+"/"+obs+"_"+mc+namestring+".root","READ")
            f_in_yz = ROOT.TFile(input_path+"/zy_"+mc+namestring+"_bins_of_"+obs+".root","READ")
            f_in_yj = ROOT.TFile(input_path+"/jet1y_"+mc+namestring+"_bins_of_"+obs+".root","READ")
            h_weight = f_in_obs.Get("gen"+obs)
            #x_bins = [np.sqrt(h_weight.GetBinLowEdge(i+1)*(h_weight.GetBinLowEdge(i+1)+h_weight.GetBinWidth(i+1))) for i in xrange(h_weight.GetNbinsX())]
            x_bins = [h_weight.GetBinLowEdge(i+1)+h_weight.GetBinWidth(i+1)/2 for i in xrange(h_weight.GetNbinsX())]
            #print x_bins
            h_rms_obs= f_in_obs.Get("rms")
            h_rms_yz = f_in_yz.Get("rms")
            h_rms_yj = f_in_yj.Get("rms")
            h_switched = f_in_obs.Get("switched")
            h_fake =f_in_obs.Get("fakerate")
            h_acceptance = f_in_obs.Get("acceptance")
            fit1 = ROOT.TF1("fit1","[0]+[1]*sqrt(x)+[2]/sqrt(x)",obsmin,obsmax)
            fit2 = ROOT.TF1("fit2","[0]-[1]/x**2",obsmin,obsmax)
            fit3 = ROOT.TF1("fit3","[0]+[1]/x**3",obsmin,obsmax)
            fit3.SetParLimits(0,0,1)
            
            fit_obs = h_rms_obs.Fit("fit1","S N")
            v_obs = [fit1(x_bins[i]) for i in xrange(h_rms_obs.GetNbinsX())]
            conf_obs = array('d',[0]*len(x_bins))
            fit_obs.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_obs,0.683)
            
            fit_yz = h_rms_yz.Fit("fit1","S N")
            v_yz = [fit1(x_bins[i]) for i in xrange(h_rms_yz.GetNbinsX())]
            conf_yz = array('d',[0]*len(x_bins))
            fit_yz.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_yz,0.683)
            
            fit_yj = h_rms_yj.Fit("fit1","S N")
            v_yj = [fit1(x_bins[i]) for i in xrange(h_rms_yj.GetNbinsX())]
            conf_yj = array('d',[0]*len(x_bins))
            fit_yj.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_yj,0.683)
            
            fit_A = h_acceptance.Fit("fit2","S N")
            v_A = [fit2(x_bins[i]) for i in xrange(h_acceptance.GetNbinsX())]
            conf_A = array('d',[0]*len(x_bins))
            fit_A.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_A,0.683)
            
            fit_F = h_fake.Fit("fit3","S N")
            v_F = [fit3(x_bins[i]) for i in xrange(h_fake.GetNbinsX())]
            conf_F = array('d',[0]*len(x_bins))
            fit_F.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_F,0.683)
            
            h_pu = f_in_obs.Get("PU")
            h_SF =f_in_obs.Get("SF")
            #h_stability = f_in.Get("stability")
            #h_purity = f_in.Get("purity")
        bin_index += 1
        l_genobsmin.append(h_weight.GetBinLowEdge(bin_index))
        l_genobsmax.append(h_weight.GetBinLowEdge(bin_index)+h_weight.GetBinWidth(bin_index))
        l_genobscenter.append(np.sqrt(l_genobsmin[obsbin]*l_genobsmax[obsbin]))
        l_genybmin.append(genybmin)
        l_genybmax.append(genybmax)
        l_genysmin.append(genysmin)
        l_genysmax.append(genysmax)
        #l_RMSobs.append( v_obs[bin_index-1] +(    variation*conf_obs[bin_index-1] if varquantity in ['_Robs'] else 0))
        #l_RMSyz.append(  v_yz[bin_index-1]  +(    variation*conf_yz[bin_index-1] if varquantity in ['_Ryz'] else 0))
        #l_RMSyj.append(  v_yj[bin_index-1]  +(    variation*conf_yj[bin_index-1] if varquantity in ['_Ryj'] else 0))
        l_A.append(      v_A[bin_index-1]   +(    variation*conf_A[bin_index-1] if varquantity in ['_A'] else 0))
        l_F.append(    1-v_F[bin_index-1]   -(    variation*conf_F[bin_index-1] if varquantity in ['_F'] else 0))
        l_RMSobs.append( h_rms_obs[bin_index]+(   variation*h_rms_obs.GetBinError(bin_index) if varquantity in ['_Robs'] else 0))
        l_RMSyz.append(   h_rms_yz[bin_index]+(    variation*h_rms_yz.GetBinError(bin_index) if varquantity in ['_Ryz'] else 0))
        l_RMSyj.append(   h_rms_yj[bin_index]+(    variation*h_rms_yj.GetBinError(bin_index) if varquantity in ['_Ryj'] else 0))
        #l_A.append(   h_acceptance[bin_index]+(variation*h_acceptance.GetBinError(bin_index) if varquantity in ['_A'] else 0))
        #l_F.append(       1-h_fake[bin_index]-(      variation*h_fake.GetBinError(bin_index) if varquantity in ['_F'] else 0))
        l_switch.append(h_switched[bin_index]+(variation*h_switched.GetBinError(bin_index) if varquantity in ['_switch'] else 0))
        l_swwidth.append(2.2)
        l_weight.append(h_weight[bin_index])
        l_SF.append(          h_SF[bin_index]+(        variation*h_SF.GetBinError(bin_index) if varquantity in ['_SF'] else 0))
    if match == '_matched':
        l_switch = [0]*h_gen.GetNbinsX()
    elif match == '_switched':
        l_switch = [1]*h_gen.GetNbinsX()
    h_rand = h_gen.Clone("weight")
    for i in xrange(h_rand.GetNbinsX()):
        h_rand.SetBinContent(i+1,max(l_weight[i],0))
    #l_RMSyz = [0]*h_gen.GetNbinsX()
    #l_RMSyj = [0]*h_gen.GetNbinsX()
    l_switch = [0]*h_gen.GetNbinsX()
    #l_A  = [1]*h_gen.GetNbinsX()
    #l_F  = [1]*h_gen.GetNbinsX()
    #l_SF = [1]*h_gen.GetNbinsX()
    print obs+" resolution in each bin:",[l_RMSobs[i+100] for i in range(5)]
    print "yz resolution in each bin:",[l_RMSyz   [i+100] for i in range(5)]
    print "yj resolution in each bin:",[l_RMSyj   [i+100] for i in range(5)]
    print "acceptance in each bin:",[l_A          [i+100] for i in range(5)]
    print "fake corr. in each bin:",[l_F          [i+100] for i in range(5)]
    #r_switch = 2.2
    gencounter = 0
    recocounter = 0
    print "3DtoyMC will be written to "+output_file
    print "create toys"
    for i in xrange(N_toys):
        if i%(N_toys/10) == 0:
            print "toy MC creation finished to "+str(100.*i/N_toys)+"%"
        index = int(h_rand.GetRandom())
        genobs = l_genobsmin[index]+(l_genobsmax[index]-l_genobsmin[index])*np.random.random()
        while True:
            genyb  = l_genybmin[index]+(l_genybmax[index]-l_genybmin[index])*np.random.random()
            genys  = l_genysmin[index]+(l_genysmax[index]-l_genysmin[index])*np.random.random()
            if genyb+genys<2.5:
                break
        sgn1 = np.sign(np.random.randn())
        sgn2 = np.sign(np.random.randn())
        genyz = sgn1 * (genyb + sgn2*genys)
        genyj = sgn1 * (genyb - sgn2*genys)
        geny_index = l_ybinedges[int(genys/0.5)]+int(genyb/0.5)
        genobs_index = l_obsbinedges[geny_index]+l_obshists[geny_index].FindBin(genobs)-1
        #print l_S1obs[genobs_index],l_S2obs[genobs_index],l_Alobs[genobs_index]
        recoobs= genobs * (1+l_RMSobs[genobs_index]*np.random.randn())
        recoyz = genyz+l_RMSyz[genobs_index]*np.random.randn()
        recoyj = genyj+l_RMSyj[genobs_index]*np.random.randn()
        if np.random.random() < l_switch[genobs_index]:
            #recoyj = 4.8*np.random.random()-2.4
            while True:
                recoyj = l_swwidth[genobs_index]*np.random.randn()
                if abs(recoyj)<2.4:
                    break
        recoyb = abs(recoyj+recoyz)/2
        recoys = abs(recoyj-recoyz)/2
        if obs=='zpt' and (recoyb+recoys > 2.5 or recoobs>1000 or recoobs<25 or (recoobs>250 and recoys>2)):
            continue
        if obs=='phistareta' and (recoyb+recoys > 2.5 or recoobs>50 or recoobs<0.4 or (recoobs>5 and recoys>2)):
            continue
        y_index = l_ybinedges[int(recoys/0.5)]+int(recoyb/0.5)
        recoobs_index = l_obsbinedges[y_index]+l_obshists[y_index].FindBin(recoobs)-1
        if recoobs_index == 75:
            recocounter += 1
        randF,randA = np.random.random(),np.random.random()
        if randF < l_F[genobs_index]:
            h_gen.Fill(genobs_index)
        if randA < l_A[genobs_index]:
            h_reco.Fill(recoobs_index,l_SF[recoobs_index])
        if randA < l_A[genobs_index] and randF < l_F[genobs_index]:
            h_response.Fill(recoobs_index,genobs_index,l_SF[recoobs_index])
            h_genresponse.Fill(recoobs_index,genobs_index)
    f_out.cd()
    h_reco.Write()
    h_gen.Write()
    h_response.Write()
    h_genresponse.Write()
    print "3DtoyMC written to "+output_file
    return

'''
def create_toy3Dhist(args=None, obs='zpt', cut='_jet1pt20', mc='mad', match='', dressed='', puid='', varquantity='', variation=0, N_toys=10):
    if mc == 'BCDEFGH':
        print "Can not create toy mc from data."
        return
    if varquantity in ['','_stats','_IDSF','_IsoSF','_TriggerSF']:
        variation = 0
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, '', mc, yboostbin=None, ystarbin=None)
    [l_obshists, h_reco, h_gen, responsehist, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    l_switch = []
    lumi = d['lumis'][0]
    #input_path = "/ceph/tberger/plots/resolution/resolution_"+mc+cut+dressed+puid
    #input_path = "/ceph/tberger/plots/resolution_dataframes/resolution_"+mc+cut+dressed+puid
    input_path  = plots_folder+cut+dressed+puid+'/resolution'
    #output_file = plots_folder+cut+dressed+puid+'/'+obs+'_toy_from_'+mc+match+'.root'
    #if RMS:
    output_file = plots_folder+cut+dressed+puid+'/'+obs+'_toy'+match+'.root'
    #else:
    #    output_file = plots_folder+cut+dressed+puid+'/'+obs+'_toy'+match+'_DG.root'
    if not variation == 0:
        output_file = plots_folder+cut+dressed+puid+'/variations/'+obs+'_toy'+match+varquantity+str(variation)+'.root'
    # safety step to avoid overwriting of existing files
    if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        return
    print "3DtoyMC will be written to "+output_file
    f_out = ROOT.TFile(output_file,"RECREATE")
    hist_index, bin_index = 0,0
    genybmin,genybmax,genysmin,genysmax = 0.0,0.5,0.0,0.5
    obsmin, obsmax = l_obshists[0].GetXaxis().GetXbins()[0],l_obshists[0].GetXaxis().GetXbins()[l_obshists[0].GetNbinsX()]
    doublegauss = ROOT.TF1("doublegauss","[0]*(TMath::Exp(-x**2/[1]**2)+[2]*TMath::Exp(-x**2/[3]**2))",-2,2)
    r_obs = doublegauss.Clone("doublegauss_obs")
    r_yz  = doublegauss.Clone("doublegauss_zy")
    r_yj  = doublegauss.Clone("doublegauss_jet1y")
    N=0
    for obsbin in xrange(h_gen.GetNbinsX()):
        if obsbin in l_obsbinedges:
            print N,"events created"
            if not obsbin==0:
                bin_index = 0
                hist_index += 1
                genybmin += 0.5
                genybmax += 0.5
                if obsbin in [93,167,222,256]:
                    genysmin += 0.5
                    genysmax += 0.5
                    genybmin,genybmax = 0.0,0.5
            namestring = "_yb{}_ys{}".format(int(2*genybmin),int(2*genysmin))
            print input_path+"/"+obs+"_"+mc+namestring+".root"
            #f_in_obs = ROOT.TFile(input_path+"/"+obs+""+namestring+".root","READ")
            #f_in_yz = ROOT.TFile(input_path+"/zy"+namestring+".root","READ")
            #f_in_yj = ROOT.TFile(input_path+"/jet1y"+namestring+".root","READ")
            f_in_obs = ROOT.TFile(input_path+"/"+obs+"_"+mc+namestring+".root","READ")
            f_in_yz = ROOT.TFile(input_path+"/zy_"+mc+namestring+"_bins_of_"+obs+".root","READ")
            f_in_yj = ROOT.TFile(input_path+"/jet1y_"+mc+namestring+"_bins_of_"+obs+".root","READ")
            h_rms_obs= f_in_obs.Get("sigma")
            h_rms_yz = f_in_yz.Get("sigma")
            h_rms_yj = f_in_yj.Get("sigma")
            h_weight = f_in_obs.Get("gen"+obs)
            h_matched = f_in_obs.Get("matched")
            h_switched = f_in_obs.Get("switched")
            h_pu = f_in_obs.Get("PU")
            h_SF =f_in_obs.Get("SF")
            h_fake =f_in_obs.Get("fakerate")
            h_acceptance = f_in_obs.Get("acceptance")
            h_si1_obs,h_si2_obs,h_alp_obs = f_in_obs.Get("sigma1"),f_in_obs.Get("sigma2"),f_in_obs.Get("alpha")
            h_si1_yz ,h_si2_yz ,h_alp_yz  = f_in_yz.Get("sigma1") ,f_in_yz.Get("sigma2") ,f_in_yz.Get("alpha")
            h_si1_yj ,h_si2_yj ,h_alp_yj  = f_in_yj.Get("sigma1") ,f_in_yj.Get("sigma2") ,f_in_yj.Get("alpha")
            #h_stability = f_in.Get("stability")
            #h_purity = f_in.Get("purity")
            r_switch = 2.2#l_switch[hist_index]
        bin_index += 1
        rms_obs  = h_rms_obs[bin_index]+(      h_rms_obs.GetBinError(bin_index)*np.random.randn() if varquantity in ['_Robs',  '_Toy'] else 0)
        si1_obs  = h_si1_obs[bin_index]+(      h_si1_obs.GetBinError(bin_index)*np.random.randn() if varquantity in ['_Robs',  '_Toy'] else 0)
        si2_obs  = h_si2_obs[bin_index]+(      h_si2_obs.GetBinError(bin_index)*np.random.randn() if varquantity in ['_Robs',  '_Toy'] else 0)
        alp_obs  = h_alp_obs[bin_index]+(      h_alp_obs.GetBinError(bin_index)*np.random.randn() if varquantity in ['_Robs',  '_Toy'] else 0)
        rms_yz   = h_rms_yz[bin_index] +(       h_rms_yz.GetBinError(bin_index)*np.random.randn() if varquantity in ['_Ryz',   '_Toy'] else 0)
        si1_yz   = h_si1_yz[bin_index] +(       h_si1_yz.GetBinError(bin_index)*np.random.randn() if varquantity in ['_Ryz',   '_Toy'] else 0)
        si2_yz   = h_si2_yz[bin_index] +(       h_si2_yz.GetBinError(bin_index)*np.random.randn() if varquantity in ['_Ryz',   '_Toy'] else 0)
        alp_yz   = h_alp_yz[bin_index] +(       h_alp_yz.GetBinError(bin_index)*np.random.randn() if varquantity in ['_Ryz',   '_Toy'] else 0)
        rms_yj   = h_rms_yj[bin_index] +(       h_rms_yj.GetBinError(bin_index)*np.random.randn() if varquantity in ['_Ryj',   '_Toy'] else 0)
        si1_yj   = h_si1_yj[bin_index] +(       h_si1_yj.GetBinError(bin_index)*np.random.randn() if varquantity in ['_Ryj',   '_Toy'] else 0)
        si2_yj   = h_si2_yj[bin_index] +(       h_si2_yj.GetBinError(bin_index)*np.random.randn() if varquantity in ['_Ryj',   '_Toy'] else 0)
        alp_yj   = h_alp_yj[bin_index] +(       h_alp_yj.GetBinError(bin_index)*np.random.randn() if varquantity in ['_Ryj',   '_Toy'] else 0)
        switch   = h_switched[bin_index]+(    h_switched.GetBinError(bin_index)*np.random.randn() if varquantity in ['_switch','_Toy'] else 0)
        weight   = h_weight[bin_index]+(        h_weight.GetBinError(bin_index)*np.random.randn() if varquantity in ['_weight','_Toy'] else 0)
        pu       = h_pu[bin_index]
        A        = h_acceptance[bin_index]+(h_acceptance.GetBinError(bin_index)*np.random.randn() if varquantity in ['_A',     '_Toy'] else 0)
        F        = 1-h_fake[bin_index]-(          h_fake.GetBinError(bin_index)*np.random.randn() if varquantity in ['_F',     '_Toy'] else 0)
        SF       = h_SF[bin_index]+(                h_SF.GetBinError(bin_index)*np.random.randn() if varquantity in ['_SF',    '_Toy'] else 0)
        #weight /= h_weight.Integral()
        if match == '_matched':
            switch = 0
        elif match == '_switched':
            switch = 1
        N += int(N_toys*weight)
        genobsmin = l_obshists[hist_index].GetBinLowEdge(bin_index)
        genobsmax = genobsmin + l_obshists[hist_index].GetBinWidth(bin_index)
        r_obs.SetParameters(1,si1_obs,alp_obs,si2_obs)
        r_yz.SetParameters( 1,si1_yz ,alp_yz ,si2_yz )
        r_yj.SetParameters( 1,si1_yj ,alp_yj ,si2_yj )
        #h_obs = ROOT.TH1D(obs,"",50,-0.2,0.2)
        #h_yz  = ROOT.TH1D("zy","",50,-0.2,0.2)
        #h_yj  = ROOT.TH1D("jet1y","",50,-0.2,0.2)
        binname = "_{}_{}".format(int(genobsmin),int(genobsmax))+namestring
        for i in xrange(int(N_toys*weight)):
            genobs = genobsmin+(genobsmax-genobsmin)*np.random.random()
            while True:
                genyb  = genybmin+(genybmax-genybmin)*np.random.random()
                genys  = genysmin+(genysmax-genysmin)*np.random.random()
                if genyb+genys<2.5:
                    break
            if (genys>2.0 and genobs>250):
                print "obs out of range!"
            sgn1 = np.sign(np.random.randn())
            sgn2 = np.sign(np.random.randn())
            genyz = sgn1 * (genyb + sgn2*genys)
            genyj = sgn1 * (genyb - sgn2*genys)
            geny_index = l_ybinedges[int(genys/0.5)]+int(genyb/0.5)
            genobs_index = l_obsbinedges[geny_index]+l_obshists[geny_index].FindBin(genobs)-1
            recoobs= genobs * (1+rms_obs*np.random.randn())
            recoyz = genyz+rms_yz *np.random.randn()
            recoyj = genyj+rms_yj *np.random.randn()
            #recoobs= genobs * (1+r_obs.GetRandom())
            #recoyz = genyz+r_yz.GetRandom()
            #recoyj = genyj+r_yj.GetRandom()
            if np.random.random() < switch:
                recoyj = 4.8*np.random.random()-2.4
                #while True:
                #    recoyj = r_switch*np.random.randn()
                #    if abs(recoyj)<2.4:
                #        break
            recoyb = abs(recoyj+recoyz)/2
            recoys = abs(recoyj-recoyz)/2
            if recoyb+recoys > 2.5 or recoobs>1000 or recoobs<25 or (recoobs>250 and recoys>2):
                continue
            y_index = l_ybinedges[int(recoys/0.5)]+int(recoyb/0.5)
            recoobs_index = l_obsbinedges[y_index]+l_obshists[y_index].FindBin(recoobs)-1
         #   h_obs.Fill((genobs-recoobs)/genobs)
         #   h_yz.Fill(genyz-recoyz)
         #   h_yj.Fill(genyj-recoyj)
            if np.random.rand()<F:
                h_gen.Fill(genobs_index)
            if np.random.rand()<A:
                h_reco.Fill(recoobs_index,SF)
            if np.random.rand()<A and np.random.rand()<F:
                responsehist.Fill(genobs_index,recoobs_index,SF)
        f_out.cd()
        #h_obs.Write(obs+"{}".format(obsbin))
        #h_yz.Write("zy"+binname)
        #h_yj.Write("jet1y"+binname)
    print N,"events created"
    h_reco.Write()
    h_gen.Write()
    responsehist.Write()
    print "3DtoyMC written to "+output_file
    return
'''

'''
def create_toy3Dhist(args=None, obs='zpt', cut='_jet1pt20', mc='amc', match='', dressed='', puid='', varquantity='', variation=0, N_toys=1000):
    if mc == 'BCDEFGH':
        print "Can not create toy mc from data."
        return
    if varquantity in ['','_stats','_IDSF','_IsoSF','_TriggerSF']:
        variation = 0
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, '', mc, yboostbin=None, ystarbin=None)
    [l_obshists, h_reco, h_gen, responsehist, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    lumi = d['lumis'][0]
    input_path = "/ceph/tberger/plots/resolution_dataframes/resolution_"+mc+cut+dressed+puid
    #input_path = "/ceph/tberger/plots/resolution/resolution_"+mc+cut+dressed+puid
    output_file = plots_folder+cut+dressed+puid+'/'+obs+'_toy'+match+'_test.root'
    if not variation == 0:
        output_file = plots_folder+cut+dressed+puid+'/variations/'+obs+'_toy'+match+varquantity+variationstring[variation]+'.root'
    # safety step to avoid overwriting of existing files
    if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        return
    print "3DtoyMC will be written to "+output_file
    f_out = ROOT.TFile(output_file,"RECREATE")
    hist_index, bin_index = 0,0
    genybmin,genybmax,genysmin,genysmax = 0.0,0.5,0.0,0.5
    obsmin, obsmax = l_obshists[0].GetXaxis().GetXbins()[0],l_obshists[0].GetXaxis().GetXbins()[l_obshists[0].GetNbinsX()]
    for obsbin in xrange(h_gen.GetNbinsX()):
        if obsbin in l_obsbinedges:
            if not obsbin==0:
                bin_index = 0
                hist_index += 1
                genybmin += 0.5
                genybmax += 0.5
                if obsbin in [93,167,222,256]:
                    genysmin += 0.5
                    genysmax += 0.5
                    genybmin,genybmax = 0.0,0.5
            #namestring = "_yboost_{}-{}_ystar_{}-{}".format(genybmin,genybmax,genysmin,genysmax).replace(".","")
            namestring = "_yb{}_ys{}".format(int(2*genybmin),int(2*genysmin))
            print input_path+"/"+obs+namestring+".root"
            #f_in = ROOT.TFile(input_path.replace("_doublegauss","")+"/"+obs+namestring+".root","READ")
            f_in_obs = ROOT.TFile(input_path+"/"+obs+namestring+".root","READ")
            f_in_yz = ROOT.TFile(input_path+"/zy"+namestring+".root","READ")
            f_in_yj = ROOT.TFile(input_path+"/jet1y"+namestring+".root","READ")
            sigma1_obs,sigma2_obs,alpha_obs,sigma_obs,rms_obs= f_in_obs.Get("sigma1"),f_in_obs.Get("sigma2"),f_in_obs.Get("alpha"),f_in_obs.Get("sigma"),f_in_obs.Get("rms")
            sigma1_yz, sigma2_yz, alpha_yz, sigma_yz, rms_yz = f_in_yz.Get("sigma1"), f_in_yz.Get("sigma2"), f_in_yz.Get("alpha"), f_in_yz.Get("sigma"), f_in_yz.Get("rms")
            sigma1_yj, sigma2_yj, alpha_yj, sigma_yj, rms_yj = f_in_yj.Get("sigma1"), f_in_yj.Get("sigma2"), f_in_yj.Get("alpha"), f_in_yj.Get("sigma"), f_in_yj.Get("rms")
            #sigma1_yb, sigma2_yb, alpha_yb, sigma_yb, rms_yb =f_in_yb.Get("sigma1"), f_in_yb.Get("sigma2"), f_in_yb.Get("alpha"), f_in_yb.Get("sigma"), f_in_yb.Get("rms")
            #sigma1_ys, sigma2_ys, alpha_ys, sigma_ys, rms_ys =f_in_ys.Get("sigma1"), f_in_ys.Get("sigma2"), f_in_ys.Get("alpha"), f_in_ys.Get("sigma"), f_in_ys.Get("rms")
            h_weight = f_in_obs.Get("gen"+obs)
            h_switched = f_in_obs.Get("switched")
            h_pu = f_in_obs.Get("PU")
            h_SF =f_in_obs.Get("SF")
            h_fake =f_in_obs.Get("fakerate")
            h_acceptance = f_in_obs.Get("acceptance")
            #h_stability = f_in.Get("stability")
            #h_purity = f_in.Get("purity")
            
        bin_index += 1
        genobsmin = l_obshists[hist_index].GetBinLowEdge(bin_index)
        genobsmax = genobsmin + l_obshists[hist_index].GetBinWidth(bin_index)
        binname = "_{}_{}".format(int(genobsmin),int(genobsmax))+namestring
        Robs = [sigma1_obs[bin_index], alpha_obs[bin_index], sigma2_obs[bin_index], sigma_obs[bin_index], rms_obs[bin_index]]
        Ryz  = [ sigma1_yz[bin_index],  alpha_yz[bin_index],  sigma2_yz[bin_index],  sigma_yz[bin_index],  rms_yz[bin_index]]
        Ryj  = [ sigma1_yj[bin_index],  alpha_yj[bin_index],  sigma2_yj[bin_index],  sigma_yj[bin_index],  rms_yj[bin_index]]
       #Ryb  = [ sigma1_yb[bin_index],  alpha_yb[bin_index],  sigma2_yb[bin_index],  sigma_yb[bin_index],  rms_yb[bin_index]]
       #Rys  = [ sigma1_ys[bin_index],  alpha_ys[bin_index],  sigma2_ys[bin_index],  sigma_ys[bin_index],  rms_ys[bin_index]]
        #if varquantity == '_Robs':
        #    #Robs[0] += variation*sigma1_obs.GetBinError(bin_index)
        #    #Robs[1] += variation*alpha_obs.GetBinError(bin_index)
        #    #Robs[2] += variation*sigma2_obs.GetBinError(bin_index)
        #    #Robs[3] += variation*sigma_obs.GetBinError(bin_index)
        #    Robs[4] += variation*rms_obs.GetBinError(bin_index)
        #if varquantity == '_Ryz':
        #    #Ryz[0] += variation*sigma1_yz.GetBinError(bin_index)
        #    #Ryz[1] += variation* alpha_yz.GetBinError(bin_index)
        #    #Ryz[2] += variation*sigma2_yz.GetBinError(bin_index)
        #    #Ryz[3] += variation* sigma_yz.GetBinError(bin_index)
        #    Ryz[4] += variation*   rms_yz.GetBinError(bin_index)
        #if varquantity == '_Ryj':
        #    #Ryj[0] += variation*sigma1_yj.GetBinError(bin_index)
        #    #Ryj[1] += variation* alpha_yj.GetBinError(bin_index)
        #    #Ryj[2] += variation*sigma2_yj.GetBinError(bin_index)
        #    #Ryj[3] += variation* sigma_yj.GetBinError(bin_index)
        #    Ryj[4] += variation*   rms_yj.GetBinError(bin_index)
        switch = h_switched[bin_index]
        if match == '_matched':
            switch = 0
        elif match == '_switched':
            switch = 1
        if varquantity == '_switch':
            switch += variation*h_switched.GetBinError(bin_index)
        w1 = h_weight[bin_index]/N_toys*lumi
        if varquantity == '_w1':
            w1 += variation*h_weight.GetBinError(bin_index)/N_toys
        w2 = h_acceptance[bin_index]/(1-h_fake[bin_index])
        if varquantity == '_w2':
            w2 += variation*error(h_acceptance.GetBinError(bin_index)/(1-h_fake[bin_index]),h_acceptance[bin_index]/(1-h_fake[bin_index])**2*h_fake.GetBinError(bin_index),0)
   #     print obsbin,bin_index,hist_index,genobsmin,genobsmax,w1,w2,switch,obs+namestring+".root"
        doublegauss = ROOT.TF1("doublegauss","[0]*(TMath::Exp(-x**2/[1]**2)+[2]*TMath::Exp(-x**2/[3]**2))",-0.2,0.2)
        r_obs = doublegauss.Clone("doublegauss_obs")
        r_yz  = doublegauss.Clone("doublegauss_zy")
        r_yj  = doublegauss.Clone("doublegauss_jet1y")
        #r_obs.SetParameters(1,Robs[0],Robs[1],Robs[2])
        #r_yz.SetParameters( 1, Ryz[0], Ryz[1], Ryz[2])
        #r_yj.SetParameters( 1, Ryj[0], Ryj[1], Ryj[2])
        #r_obs.SetParameters(1,Robs[4],0,1)
        #r_yz.SetParameters( 1, Ryz[4],0,1)
        #r_yj.SetParameters( 1, Ryj[4],0,1)
        #h_obs = ROOT.TH1D(obs,"",100,-0.2,0.2)
        #h_yz  = ROOT.TH1D("zy","",50,-2.5,2.5)
        #h_yj  = ROOT.TH1D("jet1y","",50,-2.5,2.5)
        switching = ROOT.TF1("switch","[0]*TMath::Exp(-x**2/[1]**2/2)",-2.4,2.4)
        switching.SetParameters(1,1.8)
        for i in xrange(int(N_toys*w1)):
            print int(N_toys*w1)
            genobs = genobsmin+(genobsmax-genobsmin)*np.random.random()
            genyb  = genybmin +(genybmax -genybmin) *np.random.random()
            genys  = genysmin +(genysmax -genysmin) *np.random.random()
            while genyb+genys > 2.5:
                genyb  = genybmin +(genybmax -genybmin) *np.random.random()
                genys  = genysmin +(genysmax -genysmin) *np.random.random()
            sgn1 = np.sign(np.random.randn())
            sgn2 = np.sign(np.random.randn())
            genyz = sgn1 * (genyb + sgn2*genys)
            genyj = sgn1 * (genyb - sgn2*genys)
            geny_index = l_ybinedges[int(genys/0.5)]+int(genyb/0.5)
            genobs_index = l_obsbinedges[geny_index]+l_obshists[geny_index].FindBin(genobs)-1
            #recoobs= genobs * (1+r_obs.GetRandom())
            #recoyz = genyz+r_yz.GetRandom()
            #recoyj = genyj+r_yj.GetRandom()
            recoobs= genobs * (1+Robs[4]*np.random.randn())
            recoyz = genyz+Ryz[4]*np.random.randn()
            recoyj = genyj+Ryj[4]*np.random.randn()
            if np.random.random() < switch:
                #recoyj = 1.8*np.random.randn()
                #while abs(recoyj)>2.4:
                    #recoyj = switching.GetRandom()
                    recoyj = 4.8*np.random.random()-2.4
            recoyb = 0.5*abs(recoyj+recoyz)
            recoys = 0.5*abs(recoyj-recoyz)
            #while recoyb+recoys > 2.5:
            #    recoyz = genyz+r_yz.GetRandom()
            #    recoyj = genyj+r_yj.GetRandom()
            #    if np.random.random() < switch:
            #        recoyj = 4.8*np.random.random()-2.4
            #    recoyb = 0.5*abs(recoyj+recoyz)
            #    recoys = 0.5*abs(recoyj-recoyz)
            #    print recoyb+recoys
            #print "check"
            if recoyb+recoys > 2.5:
                continue
            if recoobs<obsmin or recoobs>obsmax:
                continue
            w3 = h_SF.GetBinContent(h_SF.FindBin(recoobs))
            y_index = l_ybinedges[int(recoys/0.5)]+int(recoyb/0.5)
            recoobs_index = l_obsbinedges[y_index]+l_obshists[y_index].FindBin(recoobs)-1
            h_gen.Fill(genobs_index)
            h_reco.Fill(recoobs_index)
            responsehist.Fill(recoobs_index,genobs_index)
        f_out.cd()
        #h_obs.Write(obs+"{}".format(obsbin))
        #h_yz.Write("zy"+binname)
        #h_yj.Write("jet1y"+binname)
    
    #f_out = ROOT.TFile(output_file,"RECREATE")
    h_reco.Write()
    h_gen.Write()
    responsehist.Write()
    print "3DtoyMC written to "+output_file
    return
'''

def unfold_3Dhist_by_inversion(args=None,obs='zpt',cut='_jet1pt20',data='BCDEFGH',mc='toy',match='',dressed='_FSR01', puid='',varquantity='',variation=0):
    if varquantity in ['','_IDSF','_IsoSF','_TriggerSF'] and not variation==0:
        print "WARNING: variations can not be computed for these variation quantities"
        variation = 0
    if not 'toy' in mc and not varquantity == '_stats':
        variation = 0
        print "WARNING: only statistical variations can be computed for this MC"
    input_file_data = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
    input_file_mc   = plots_folder+cut+dressed+puid+'/'+obs+'_'+mc+match+'.root'
    output_file = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    if not variation == 0:
      if not varquantity == '_stats':
        input_file_mc = plots_folder+cut+dressed+puid+'/variations/'+obs+'_'+mc+match+varquantity+variationstring[variation]+'.root'
        output_file    = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+varquantity+variationstring[variation]+'.root'
      else:
        output_file    = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+varquantity+'.root'
    print "response will be written to", output_file
    #if os.path.exists(output_file):
    #    print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
    #    return
    f_in_mc, f_in_data  = ROOT.TFile(input_file_mc,"READ"), ROOT.TFile(input_file_data,"READ")
    h_reco, h_gen, h_data, h_closure  = f_in_mc.Get(obs), f_in_mc.Get("gen"+obs), f_in_data.Get(obs), f_in_data.Get("gen"+obs)
    h_response, h_genresponse = f_in_mc.Get("response"),f_in_mc.Get("response_2")
    Nx,Ny = h_response.GetNbinsX(),h_response.GetNbinsY()
    print Nx,Ny
    [m_reco, m_gen, m_data, m_closure] = 4*[ROOT.TMatrixD(Nx,1)]
    [a_reco, a_gen, a_data, a_closure] = 4*[ROOT.TArrayD(Nx)]
    m_response = ROOT.TMatrixD(Nx,Ny)
    a_response = ROOT.TArrayD(Nx*Ny)
    m_unfold, m_data_e, m_unfold_e = ROOT.TMatrixD(1,Ny), ROOT.TMatrixD(Nx,Ny), ROOT.TMatrixD(Nx,Ny)
    a_edge, a_data_e = ROOT.TArrayD(Ny), ROOT.TArrayD(Nx*Ny)
    #print "Set acceptance rate to 1"
    h_prox = h_response.ProjectionX("projectionx",1,Nx,"e")
    h_proy = h_response.ProjectionY("projectiony",1,Ny,"e")
    h_loss = h_gen.Clone("loss")
    h_fake = h_reco.Clone("fake")
    h_loss.Add(h_proy,-1)
    h_fake.Add(h_prox,-1)
    print "data distribution:",[h_data[i+1] for i in xrange(6)]
    print "reco distribution:",[h_reco[i+1] for i in xrange(6)]
    print "gen  distribution:",[h_gen[i+1]  for i in xrange(6)]
    print "projection on X:",[h_prox[i+1] for i in xrange(6)]
    print "projection on Y:",[h_proy[i+1] for i in xrange(6)]
    
    print "fake distribution:",[h_fake[i+1] for i in xrange(6)]
    print "loss distribution:",[h_loss[i+1] for i in xrange(6)]
    if varquantity=='_stats' and not variation == 0:
        print "Statistical variation of response matrix"
        h_proy = h_genresponse.ProjectionY("projectiony",1,Ny,"e")
        for j in xrange(Ny):
            #print h_reco.GetBinError(j+1)**2-h_prox.GetBinError(j+1)**2,np.sqrt(abs(h_reco.GetBinError(j+1)**2-h_prox.GetBinError(j+1)**2))
            #print h_gen.GetBinError(j+1)**2-h_proy.GetBinError(j+1)**2,np.sqrt(h_gen.GetBinError(j+1)**2-h_proy.GetBinError(j+1)**2)
            h_fake.SetBinError(j+1,np.sqrt(abs(h_reco.GetBinError(j+1)**2-h_prox.GetBinError(j+1)**2)))
            h_loss.SetBinError(j+1,np.sqrt(abs(h_gen.GetBinError(j+1)**2-h_proy.GetBinError(j+1)**2)))
            #if h_gen.GetBinError(j+1)**2-h_proy.GetBinError(j+1)**2 < 0:
            #    print h_gen.GetBinError(j+1)**2-h_proy.GetBinError(j+1)**2
            #if h_reco.GetBinError(j+1)**2-h_prox.GetBinError(j+1)**2 < 0:
            #    print h_gen.GetBinError(j+1)**2-h_proy.GetBinError(j+1)**2
        for j in xrange(Ny):
          for i in xrange(Nx):
            h_response.SetBinContent(i+1,j+1,h_response.GetBinContent(i+1,j+1)+h_response.GetBinError(i+1,j+1)*np.random.randn())
          h_loss.SetBinContent(j+1,h_loss[j+1]+h_loss.GetBinError(j+1)*np.random.randn())
          h_fake.SetBinContent(j+1,h_fake[j+1]+h_fake.GetBinError(j+1)*np.random.randn())
        h_prox = h_response.ProjectionX("projectionx",1,Nx,"e")
        h_proy = h_response.ProjectionY("projectiony",1,Ny,"e")
        h_gen = h_loss.Clone("gen"+obs)
        h_reco = h_loss.Clone(obs)
        h_gen.Add(h_prox)
        h_reco.Add(h_proy)
        #print "gen  distribution after variation:",[h_gen[i+1]  for i in xrange(6)]
        #print "reco distribution after variation:",[h_reco[i+1] for i in xrange(6)]
    if data == 'BCDEFGH':
        #h_data.Scale(1/35.9)
        l_bkg = ['TTJets','TW','WW','WZ','ZZ']
        #l_bkg = ['TTJets','ST','WW','WZ','ZZ','WJets']
        print "subtract backgrounds ",l_bkg
        for bkg in l_bkg:
            f_bkg = ROOT.TFile(plots_folder+cut+dressed+puid+'/'+obs+'_'+bkg+match+'.root',"READ")
            print plots_folder+cut+dressed+puid+'/'+obs+'_'+bkg+match+'.root'
            h_bkg = f_bkg.Get(obs)
            h_data.Add(h_bkg,-1)
            print "data distribution:",[h_data.GetBinContent(i+1) for i in xrange(6)]
    for i in xrange(Nx*Ny):
        # normalize matrix rows to correct for losses
        #a_response[i]=h_response.GetBinContent(i/Nx+1,i%Ny+1)/h_edge[i%Ny+1]
        try:
            a_response[i]=h_response.GetBinContent(i/Nx+1,i%Ny+1)/h_gen[i%Ny+1]
        except ZeroDivisionError:
            a_response[i]=0
    for i in xrange(Nx):
        a_reco[i]        = h_reco.GetBinContent(i+1)
        a_gen[i]         = h_gen.GetBinContent(i+1)
        #print a_data[i], h_data.GetBinContent(i+1)
        a_closure[i]     = h_closure.GetBinContent(i+1)
        a_data_e[i*Nx+i] = h_data.GetBinError(i+1)**2
        #print "fakerate",h_fake[i+1]/h_reco[i+1]
        # correct for fakes
        try:
            a_data[i]    = h_data.GetBinContent(i+1)*(1-h_fake[i+1]/h_reco[i+1])
        except ZeroDivisionError:
            a_data[i]    = h_data.GetBinContent(i+1)
        
        
    print "data distribution:",[a_data[i] for i in xrange(6)]
    m_response.SetMatrixArray(a_response.GetArray())
    m_reco.SetMatrixArray(a_reco.GetArray())
    m_gen.SetMatrixArray(a_gen.GetArray())
    m_data.SetMatrixArray(a_data.GetArray())
    m_data_e.SetMatrixArray(a_data_e.GetArray())
    m_closure.SetMatrixArray(a_closure.GetArray()) 
    m_inv    = deepcopy(m_response)
    m_dummy1 = deepcopy(m_response)
    m_dummy2 = deepcopy(m_response)
    m_inv.Invert()
    print [m_response(i,0) for i in xrange(7)]
    #print [m_inv(i,0) for i in xrange(7)]
    m_unfold.Mult(m_inv,m_data)
    m_dummy1.Transpose(m_inv)
    m_dummy2.Mult(m_data_e,m_dummy1)
    m_unfold_e.Mult(m_inv,m_dummy2)
    svd = ROOT.TDecompSVD(m_response)
    print "Response matrix Condition number is given as",svd.Condition()
    h_covariance  = h_response.Clone("covariance")
    h_correlation = h_response.Clone("correlation")
    h_unfold      = h_closure.Clone("unfolded"+obs)
    for j in xrange(Ny):
        for i in xrange(Nx):
            h_covariance.SetBinContent(i+1,j+1,m_unfold_e(i,j))
            h_response.SetBinContent(i+1,j+1,m_response(i,j))
            h_correlation.SetBinContent(i+1,j+1,m_unfold_e(i,j)/np.sqrt(m_unfold_e(i,i)*m_unfold_e(j,j)))
        h_unfold.SetBinContent(j+1,m_unfold(0,j))
        h_unfold.SetBinError(j+1,np.sqrt(m_unfold_e(j,j)))
    print "unfold distribution:",[h_unfold[i+1] for i in xrange(6)]
    print [h_correlation.GetBinContent(i+1,1) for i in xrange(7)]
    f_out = ROOT.TFile(output_file,"RECREATE")
    h_unfold.Write()
    h_reco.Write()
    h_gen.Write()
    h_data.Write("signal"+obs)
    h_response.Write()
    h_covariance.Write()
    h_correlation.Write()
    print "unfolding results written to",output_file
    return

def unfold_3Dhist_by_tunfold(args=None,obs='zpt',cut='_jet1pt20',data='amc',mc='toy',match='',dressed='', puid='',varquantity='',variation=0):
    if varquantity in ['','_IDSF','_IsoSF','_TriggerSF']:
        print "WARNING: variations can not be computed for these variation quantities"
        variation = 0
    if not 'toy' in mc and not varquantity == '_stats':
        variation = 0
        print "WARNING: only statistical variations can be computed for this MC"
    input_file_data = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
    input_file_mc   = plots_folder+cut+dressed+puid+'/'+obs+'_'+mc+match+'.root'
    output_file = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    if not variation == 0:
      if not varquantity == '_stats':
        input_file_mc = plots_folder+cut+dressed+puid+'/variations/'+obs+'_'+mc+match+varquantity+str(variation)+'.root'
      output_file    = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+varquantity+'.root'
    print "response will be written to", output_file
    #if os.path.exists(output_file):
    #    print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
    #    return
    f_in_mc, f_in_data  = ROOT.TFile(input_file_mc,"READ"), ROOT.TFile(input_file_data,"READ")
    h_reco, h_gen, h_data, h_closure  = f_in_mc.Get(obs), f_in_mc.Get("gen"+obs), f_in_data.Get(obs), f_in_data.Get("gen"+obs)
    h_response = f_in_mc.Get("response")
    Nx,Ny = h_response.GetNbinsX(),h_response.GetNbinsY()
    f_out = ROOT.TFile(output_file,"RECREATE")
    
    h_edge = h_gen.Clone("edge")
    h_fake = h_reco.Clone("fake")
    print Nx,h_edge.GetNbinsX()
    print Ny,h_gen.GetNbinsX()
    for j in xrange(Ny):
        edge_gen =0
        edge_reco =0
        for i in xrange(Nx):
            edge_gen +=h_response.GetBinContent(i+1,j+1)
            edge_reco+=h_response.GetBinContent(j+1,i+1)
        h_edge.SetBinContent(j+1,edge_gen)
        h_fake.SetBinContent(j+1,edge_reco-h_reco[j+1])
    print "data distribution:",[h_data[i+1] for i in xrange(6)]
    print "gen  distribution:",[h_gen[i+1]  for i in xrange(6)]
    print "reco distribution:",[h_reco[i+1] for i in xrange(6)]
    print "edge distribution:",[h_edge[i+1] for i in xrange(6)]
    print "fake distribution:",[h_fake[i+1] for i in xrange(6)]
    #for i in xrange(Nx):
    #  for j in xrange(Ny):
    #    h_response.SetBinContent(i+1,j+1,h_response.GetBinContent(i+1,j+1)/h_edge[j+1])
    #    #try:
    #    #    h_response.SetBinContent(i+1,j+1,h_response.GetBinContent(i+1,j+1)/h_gen[j+1])
    #    #except ZeroDivisionError:
    #    #    h_response.SetBinContent(i+1,j+1,0)
    for i in xrange(Nx):
        # correct for fakes
        h_data.SetBinContent(i+1,h_data.GetBinContent(i+1)+h_data[i+1]*h_fake[i+1]/h_reco[i+1])
        #h_response.SetBinContent(i+1,0,h_reco[i+1])#-h_fake[i+1])
        # set underflow bin to correct for losses
        h_response.SetBinContent(0,i+1, h_gen[i+1]-h_edge[i+1])
    print [h_response.GetBinContent(i+1,1) for i in xrange(7)]
    print "data distribution:",[h_data[i+1] for i in xrange(6)]
    unfold = ROOT.TUnfoldDensity(h_response,1,
                    ROOT.TUnfold.ERegMode(2),
                    ROOT.TUnfold.EConstraint(0),
                    ROOT.TUnfoldDensity.EDensityMode(0),
                    0,0,
                    "0","*[B]")
    print unfold
    unfold.DoUnfold(1,h_data)
    h_unfold = unfold.GetOutput("unfolded"+obs)
    h_covariance = unfold.GetEmatrixInput("covariance")
    h_correlation = h_covariance.Clone("correlation")
    for j in xrange(Ny):
        for i in xrange(Nx):
            h_correlation.SetBinContent(i+1,j+1,h_covariance.GetBinContent(i+1,j+1)
                                                /np.sqrt(h_covariance.GetBinContent(i+1,i+1)*h_covariance.GetBinContent(j+1,j+1)))
    #h_covariance = unfold.GetEmatrixTotal("covariance")
    print "unfold distribution:",[h_unfold[i+1] for i in xrange(6)]
    print [h_correlation.GetBinContent(i+1,1) for i in xrange(7)]
    f_out.cd()
    h_unfold.Write()
    h_covariance.Write()
    h_reco.Write()
    h_gen.Write()
    h_data.Write("signal"+obs)
    print "unfolding results written to",output_file
    return

def uncloop(args=None):
    #for cut in ['_jet1pt10','_jet1pt15','_jet1pt20']:
    for cut in ['_jet1pt20']:
     for dressed in [#'',
                    '_FSR01'
                    ]:
      for varquantity in [  #'_stats_amc','_stats_hpp','_stats_mad',
                            #'_stats_toy',
                            '_Robs','_Ryj','_Ryz','_F','_A',#'_weight','_switch','_SF',
                            '_IDSF','_IsoSF','_TriggerSF',
                            '_bkg','_lumi',
                            '_JEC',#'_JER',
                            '_statistical',
                            ]:
        for data in [   #'amc','hpp','mad',
                        'BCDEFGH'
                        ]:
          uncertainties_3Dhist(obs='zpt',       cut=cut,data=data,dressed=dressed,varquantity=varquantity)
          uncertainties_3Dhist(obs='phistareta',cut=cut,data=data,dressed=dressed,varquantity=varquantity)
    return

def uncertainties_3Dhist(args=None, obs='zpt', cut='_jet1pt20', data='BCDEFGH',match='',dressed='_FSR01',puid='',varquantity='_total',N_toys=1000):
    var=varquantity
    output_file = plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+varquantity+'.root'
    print "write uncertainty to file",output_file
    if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        return
    f_out = ROOT.TFile(output_file,"RECREATE")
    if varquantity in ['_stats_toy','_stats_amc','_stats_mad','_stats_hpp']:
            mc = varquantity.split('_')[-1]
            input_file = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
            f_in      = ROOT.TFile(input_file,"READ")
            h_central = f_in.Get(obs)
            h_uncertainty = h_central.Clone('uncertainty'+var)
            h_uncertainty.Reset()
            h_sum = h_uncertainty.Clone('mean_'+mc)
            h_sqr = f_in.Get('response')
            h_sqr.Reset()
            h_cov = h_sqr.Clone("covariance_"+mc)
            for i in xrange(N_toys):
                unfold_3Dhist_by_inversion(args,obs,cut,data,mc,match,dressed,puid,varquantity='_stats',variation=i+1)
                input_file_var   = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'_stats'+'.root'
                f_in_var   = ROOT.TFile(input_file_var,"READ")
                h_var   = f_in_var.Get('unfolded'+obs)
                for i in xrange(h_uncertainty.GetNbinsX()):
                    h_sum.SetBinContent(i+1, h_sum[i+1]+h_var[i+1])
                    for j in xrange(h_uncertainty.GetNbinsX()):
                       h_sqr.SetBinContent(i+1,j+1,h_sqr.GetBinContent(i+1,j+1)+h_var[i+1]*h_var[j+1])
            f_out.cd()
            for i in xrange(h_uncertainty.GetNbinsX()):
                h_central.SetBinContent(i+1,h_sum[i+1]/N_toys)
                for j in xrange(h_uncertainty.GetNbinsX()):
                    h_cov.SetBinContent(i+1,j+1,h_sqr.GetBinContent(i+1,j+1)/N_toys-h_central[i+1]*h_central[j+1])
                    h_cov.SetBinError(i+1,j+1,0)
                h_central.SetBinError(i+1,np.sqrt(h_cov.GetBinContent(i+1,i+1)))
                h_uncertainty.SetBinContent(i+1,h_central.GetBinError(i+1)/h_central[i+1])
                h_uncertainty.SetBinError(i+1,0)
            h_uncertainty.Write()
            h_cov.Write()
            h_central.Write('unfolded'+obs+'_by_'+mc)
    elif varquantity in ['_Robs','_Ryz','_Ryj','_switch','_weight','_A','_F','_SF','_Toy']:
            create_toy3Dhist(args,obs,cut,'mad',match,dressed,puid,varquantity='',variation=0)
            unfold_3Dhist_by_inversion(args,obs,cut,data,'toy',match,dressed,puid)
            input_file = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_toy'+match+'.root'
            f_in      = ROOT.TFile(input_file,"READ")
            h_central = f_in.Get('unfolded'+obs)
            h_uncertainty = h_central.Clone('uncertainty'+var)
            h_uncertainty.Reset()
            create_toy3Dhist(args,obs,cut,'mad',match,dressed,puid,varquantity=var,variation=1)
            create_toy3Dhist(args,obs,cut,'mad',match,dressed,puid,varquantity=var,variation=-1)
            unfold_3Dhist_by_inversion(args,obs,cut,data,'toy',match,dressed,puid,varquantity=var,variation=1)
            unfold_3Dhist_by_inversion(args,obs,cut,data,'toy',match,dressed,puid,varquantity=var,variation=-1)
            input_file_up   = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_toy'+match+var+'Up.root'
            input_file_down = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_toy'+match+var+'Down.root'
            f_in_up   = ROOT.TFile(input_file_up,  "READ")
            f_in_down = ROOT.TFile(input_file_down,"READ")
            h_up      = f_in_up.Get('unfolded'+obs)
            h_down    = f_in_down.Get('unfolded'+obs)
            for i in xrange(h_uncertainty.GetNbinsX()):
                h_uncertainty.SetBinContent(i+1,max(abs(h_central[i+1]-h_up[i+1]),abs(h_central[i+1]-h_down[i+1]))/h_central[i+1])
                h_uncertainty.SetBinError(i+1,0)
            f_out.cd()
            h_uncertainty.Write()
            h_central.Write('unfolded'+obs+var)
    elif varquantity in ['_IDSF','_IsoSF','_TriggerSF']:
        input_file = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
        create_3Dhist(args,obs,cut,data,match,dressed,puid,varquantity=var,variation=1)
        create_3Dhist(args,obs,cut,data,match,dressed,puid,varquantity=var,variation=-1)
        f_in      = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get(obs)
        h_uncertainty = h_central.Clone('uncertainty'+var)
        h_uncertainty.Reset()
        input_file_up   = plots_folder+cut+dressed+puid+'/variations/'+obs+'_'+data+match+var+'Up.root'
        input_file_down = plots_folder+cut+dressed+puid+'/variations/'+obs+'_'+data+match+var+'Down.root'
        f_in_up   = ROOT.TFile(input_file_up,"READ")
        f_in_down = ROOT.TFile(input_file_down,"READ")
        h_up      = f_in_up.Get(obs)
        h_down    = f_in_down.Get(obs)
        for i in xrange(h_uncertainty.GetNbinsX()):
            h_uncertainty.SetBinContent(i+1,max(max(abs(h_up[i+1]-h_central[i+1]),abs(h_down[i+1]-h_central[i+1]))/h_central[i+1],0))
            h_uncertainty.SetBinError(i+1,0)
        f_out.cd()
        h_uncertainty.Write()
        h_central.Write(obs)
    elif varquantity in ['_JEC']:
        input_file = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
        f_in      = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get(obs)
        h_uncertainty = h_central.Clone('uncertainty'+var)
        h_uncertainty.Reset()
        input_file_up   = plots_folder+cut+dressed+puid+'/variations/'+obs+'_'+data+match+var+'Up.root'
        input_file_down = plots_folder+cut+dressed+puid+'/variations/'+obs+'_'+data+match+var+'Down.root'
        f_in_up   = ROOT.TFile(input_file_up,"READ")
        f_in_down = ROOT.TFile(input_file_down,"READ")
        h_up      = f_in_up.Get(obs)
        h_down    = f_in_down.Get(obs)
        for i in xrange(h_uncertainty.GetNbinsX()):
            h_uncertainty.SetBinContent(i+1,max(abs(h_up[i+1]-h_central[i+1]),abs(h_down[i+1]-h_central[i+1]))/h_central[i+1])
            h_uncertainty.SetBinError(i+1,0)
        f_out.cd()
        h_uncertainty.Write()
        h_central.Write(obs)
    elif varquantity in ['_JER']:
        input_file = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
        f_in      = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get(obs)
        h_uncertainty = h_central.Clone('uncertainty'+var)
        h_uncertainty.Reset()
        input_file_var   = plots_folder+cut+dressed+puid+'/variations/'+obs+'_'+data+match+var+'.root'
        f_in_var   = ROOT.TFile(input_file_var,"READ")
        h_var      = f_in_var.Get(obs)
        for i in xrange(h_uncertainty.GetNbinsX()):
            h_uncertainty.SetBinContent(i+1,(h_var[i+1]-h_central[i+1])/h_central[i+1])
            h_uncertainty.SetBinError(i+1,0)
        f_out.cd()
        h_uncertainty.Write()
        h_central.Write(obs)
    elif varquantity in ['_bkg']:
        if not data=='BCDEFGH':
            print "WARNING: bkg uncertainty only defined for data"
            return
        input_file = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
        f_in      = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get(obs)
        h_uncertainty = h_central.Clone('uncertainty'+var)
        l_bkg = ['TTJets','TW','WW','WZ','ZZ']
        for bkg in l_bkg:
            f_bkg = ROOT.TFile(plots_folder+cut+dressed+puid+'/'+obs+'_'+bkg+match+'.root',"READ")
            h_bkg = f_bkg.Get(obs)
            h_bkg.Add(h_bkg)
        for i in xrange(h_uncertainty.GetNbinsX()):
            h_uncertainty.SetBinContent(i+1,h_bkg[i+1]/h_central[i+1]/2)
            h_uncertainty.SetBinError(i+1,0)
        f_out.cd()
        h_uncertainty.Write('uncertainty'+var)
    elif varquantity in ['_lumi']:
        input_file = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
        f_in      = ROOT.TFile(input_file,"READ")
        h_uncertainty = f_in.Get(obs)
        for i in xrange(h_uncertainty.GetNbinsX()):
            h_uncertainty.SetBinContent(i+1,0.025)
            h_uncertainty.SetBinError(i+1,0)
        f_out.cd()
        h_uncertainty.Write('uncertainty'+var)
    elif varquantity in ['_statistical']:
        unfold_3Dhist_by_inversion(args,obs,cut,data,'toy',match,dressed,puid)
        input_file = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_toy'+match+'.root'
        f_in       = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get('unfolded'+obs)
        h_uncertainty = h_central.Clone('uncertainty'+var)
        for i in xrange(h_uncertainty.GetNbinsX()):
            h_uncertainty.SetBinContent(i+1,h_central.GetBinError(i+1)/h_central[i+1])
            h_uncertainty.SetBinError(i+1,0)
        f_out.cd()
        h_uncertainty.Write()
    elif varquantity in ['_total']:
        input_file = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
        f_in       = ROOT.TFile(input_file,"READ")
        h_uncertainty = f_in.Get(obs)
        h_uncertainty.Reset()
        varlist = ({'stat': ['_statistical'],
                    'lumi': ['_lumi'],
                    'bkg' : ['_bkg'],
                    'eff' : ['_IDSF','_IsoSF','_TriggerSF'],
                    'unf' : ['_stats_mad'],
                    #'jec' : ['_JEC'],
                    #'mod' : ['_Robs','_Ryz','_Ryj','_A','_F'],
                    })
        for vkey in varlist:
          h_unc = h_uncertainty.Clone("uncertainty_"+vkey)
          h_unc.Reset()
          for v in varlist[vkey]:
            input_file_unc = plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+v+'.root'
            f_in_unc       = ROOT.TFile(input_file_unc,"READ")
            h_v            = f_in_unc.Get('uncertainty'+v)
            for i in xrange(h_uncertainty.GetNbinsX()):
                h_unc.SetBinContent(i+1,np.sqrt(h_unc[i+1]**2+h_v[i+1]**2))
                h_unc.SetBinError(i+1,0)
          if not vkey == 'stat':
            for i in xrange(h_uncertainty.GetNbinsX()):
                h_uncertainty.SetBinContent(i+1,np.sqrt(h_uncertainty[i+1]**2+h_unc[i+1]**2))
                h_uncertainty.SetBinError(i+1,0)
          f_out.cd()
          h_unc.Write()
        h_uncertainty.Write('uncertainty'+var)
    else:
        print "WARNING: uncertainty does not exist! Please remove",output_file
        return
    print "uncertainties written to",output_file
    return


'''
def invert_3Dhist(args=None, obs='zpt', cut='_jet1pt20', data='amc', mc='amc',match='',dressed='',puid='',varquantity='',variation=0,
      #  folder='unfolded',method=''):
        folder='',method=''):
#def invert_3Dhist(args=None, obs='zpt', cut='_jet1pt20', data='amc', mc='',match='',dressed='',puid='',varquantity='',variation=0,prefix=''):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args,obs,cut,data,data)
    [l_obshists, h_reco, h_gen, responsehist, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    #if not method == '' and not folder == 'unfolded':
    #    print "WARNING: unfolding methods need the matching prefix!"
    #    return
    if varquantity == '':
        variation = 0
    input_file  = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
    output_file = plots_folder+cut+dressed+puid+'/binned/'+obs+'_'+data+match+'.root'
    histname_gen  = 'gen'+obs
    histname_reco = obs
    if folder == 'unfolded':
        input_file  = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
        output_file = plots_folder+cut+dressed+puid+'/binned/unfolded'+obs+'_'+data+'_by_'+mc+match+'.root'
        histname_gen  = 'unfolded'+obs
        histname_reco = 'signal'+obs
    if folder == 'uncertainty':
        if varquantity == '':
            print "WARNING: uncertainty needs a variated quantity!"
            return
        input_file  = plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+varquantity+'.root'
        output_file = plots_folder+cut+dressed+puid+'/binned/uncertainty'+obs+'_'+data+match+varquantity+'.root'
        histname_gen  = 'unfolded'+obs+'_by_'+mc
        histname_reco = 'uncertainty_'+data
    print input_file
    print histname_gen,histname_reco
    f_in = ROOT.TFile(input_file,"READ")
    h_gen = f_in.Get(histname_gen)
    h_reco = f_in.Get(histname_reco)
    f_out = ROOT.TFile(output_file,"RECREATE")
    hist_index, bin_index = 0,0
    
    genybmin,genybmax,genysmin,genysmax = 0.0,0.5,0.0,0.5
    for obsbin in xrange(h_gen.GetNbinsX()):
        if obsbin in l_obsbinedges:
            if not obsbin==0:
                h_genbin.Write(histname_gen+namestring)
                h_recobin.Write(histname_reco+namestring)
                bin_index = 0
                hist_index += 1
                genybmin += 0.5
                genybmax += 0.5
                if obsbin in [93,167,222,256]:
                    genysmin += 0.5
                    genysmax += 0.5
                    genybmin,genybmax = 0.0,0.5
            namestring = "_yb{}_ys{}".format(int(2*genybmin),int(2*genysmin))
            h_genbin  = l_obshists[hist_index].Clone(histname_gen+namestring)
            h_recobin = l_obshists[hist_index].Clone(histname_reco+namestring)
        bin_index += 1
        h_genbin.SetBinContent(bin_index,h_gen.GetBinContent(obsbin+1))
        h_genbin.SetBinError(bin_index,h_gen.GetBinError(obsbin+1))
        h_recobin.SetBinContent(bin_index,h_reco.GetBinContent(obsbin+1))
        h_recobin.SetBinError(bin_index,h_reco.GetBinError(obsbin+1))
    h_genbin.Write(histname_gen+namestring)
    h_recobin.Write(histname_reco+namestring)
    print "histograms written to",output_file
'''


def plot_compare_datamc_3D(args=None, obs='zpt', cut='_jet1pt20', data='BCDEFGH', mc='amc',match='',dressed='_FSR01',puid=''):
#def plot_compare_datamc_3D(args=None, obs='zpt', cut='_jet1pt20', data='BCDEFGH', mc='amc',match='',dressed='_FSR01',puid=''):
    
    bkg_list = ['TTJets','WZ','ZZ','TW','WW']
    
    data_source = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
    mc_source   = plots_folder+cut+dressed+puid+'/'+obs+'_'+mc+match+'.root'
    bkg_source  =[plots_folder+cut+dressed+puid+'/'+obs+'_'+bkg+match+'.root' for bkg in bkg_list]
    
    filelist = [data_source,mc_source]+bkg_source
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
        
    plots=[]
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'files': filelist_binned,
                'x_expressions': [obs+namestring],
                'folders': [''],
                'nicks': ['Data','DY']+bkg_list,
                'analysis_modules': ['SumOfHistograms','NormalizeByBinWidth','Ratio'],#
                'sum_nicks' : ['DY '+' '.join(bkg_list)],
                'sum_result_nicks' : ['sim'],
                'ratio_numerator_nicks': ['Data'],
                'ratio_denominator_nicks': ['sim'],
                'ratio_result_nicks':['ratio'],
                'ratio_denominator_no_errors': False,
                'stacks':['data','mc']+len(bkg_list)*['mc']+['ratio'],
                'www': 'comparison_datamc'+cut+dressed+puid+'_'+data+'_vs_'+mc+match+'/datamc'+namestring,
                'filename': obs,
                'x_label': obs,
                'x_log': True,
                'x_errors': [1],
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'y_log': True,
                'y_lims': [1e-2,1e5] if obs =='zpt' else [1e0,1e7],
                'y_label': 'Events per binsize',
                'nicks_blacklist': ['sim'],
                'y_subplot_label': 'Data/Sim',
                'y_subplot_lims': [0.75,1.25],
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                 #'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{6.2}}$",
            })
            plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def plot_resolution_3D(args=None, obs='zpt', cut='_jet1pt15', mc='mad',match='',dressed='_FSR01',puid=''):
    plots=[]
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
       for cut in ['_jet1pt10','_jet1pt15','_jet1pt20']:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'files': [plots_folder+cut+dressed+puid+'/resolution_old/'+obs+'_'+mc+match+namestring+'.root'],
                'www': 'resolutions'+cut+dressed+puid+'_'+mc+match+'/resolution'+namestring,
                'folders': [''],
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'x_log': True,
                'x_label': obs,
                'x_errors': [1],
                'markers': ['.'],
            })
            d1 = deepcopy(d)
            d1.update({
                'x_expressions': ['sigma','rms'],
                'texts_x': [0.03,0.7],
                'filename': obs+'_resolution',
                'nicks': ['sigma','rms'],
                'legend': None,
                'analysis_modules': ['FunctionPlot'],
                'function_fit': ['sigma','rms'],
                'functions': ['[0]+[1]*sqrt(x)+[2]/sqrt(x)'],
                #'functions': ['[0]+[1]*x+[2]*sqrt(x)'],
                'function_parameters': ['1,1,1'],
                'function_display_result': True,
                'function_nicknames': ['sigma_fit','rms_fit'],
                'function_fit_parameter_names': ['p_0',r'p_1',r'p_2'],
                'colors': ['green','blue','darkgreen','darkblue'],
            })
            if obs == 'zpt':
                d1['y_lims'] = [0,0.03]
                d1['y_label'] = r'Relative $p_T^Z$ resolution'
            if obs == 'phistareta':
                d1['y_lims'] = [0,0.005]
                d1['y_label'] = r'Relative $\\Phi^*_\\eta$ resolution'
            d2 = deepcopy(d1)
            d2.update({
                'files': [plots_folder+cut+dressed+puid+'/resolution_old/jet1y_'+mc+match+namestring+'_bins_of_'+obs+'.root'],
                'filename': 'jet1y_resolution_bins_of_'+obs,
                'y_lims': [0,0.05],
                'y_label': r'$y^{jet1}$ resolution',
            })
            d3 = deepcopy(d1)
            d3.update({
                'files': [plots_folder+cut+dressed+puid+'/resolution_old/zy_'+mc+match+namestring+'_bins_of_'+obs+'.root'],
                'filename': 'zy_resolution_bins_of_'+obs,
                'y_lims': [0,0.01] if obs=='zpt' else [0,0.02],
                'y_label': r'$y^{Z}$ resolution',
            })
            d4 = deepcopy(d)
            d4.update({
                'x_expressions': ['PU','matched','switched'],
                'nicks': ['PU','matched','switched'],
                'analysis_modules':['ScaleHistograms'],
                'scale_nicks': ['PU','matched','switched'],
                'scales': [100],
                'markers': ['fill'],
                'filename': obs+'_fractions',
                'y_lims': [0,125],
                'y_label': 'Fraction / %',
                'stacks': ['fraction'],
                'colors': ['grey','steelblue','orange'],
                'lines': [100],
                'y_ticks': [0,10,20,30,40,50,60,70,80,90,100],
            })
            d5 = deepcopy(d)
            d5.update({
                'x_expressions': ['fakerate','acceptance','purity','stability'],
                'nicks': ['fakerate','acceptance','purity','stability'],
                'scale_nicks': ['fakerate','acceptance','purity','stability'],
                'analysis_modules':['ScaleHistograms','FunctionPlot'],
                'scales': [100],
                'filename': obs+'_rates',
                'y_lims': [0,130],
                'y_label': 'Fraction / %',
                'y_ticks': [0,10,20,30,40,50,60,70,80,90,100],
                'lines': [100],
                'function_fit': ['acceptance','fakerate'],
                'functions': ['[0]-[1]/x**2','[0]+[1]/x**3'],
                'function_parameters': ['1,1,1','1,1'],
                'function_display_result': True,
                'function_nicknames': ['acc_fit','fak_fit'],
                'texts_x':[0.03,0.01,0.35],
                'texts_y':[0.97,0.92,0.92],
            })
            plots.append(d1)
            plots.append(d2)
            plots.append(d3)
            plots.append(d4)
            plots.append(d5)
    return [PlottingJob(plots=plots, args=args)]

def plot_compare_unfolding_methods_3D(args=None, obs='zpt', cut='_jet1pt20', data='amc', mc='mad',match='',dressed='',puid=''):
    signal_source  = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
    unfold_source1 = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'_dagostini.root'
    unfold_source2 = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'_inversion.root'
    unfold_source3 = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'_tunfold.root'
    unfold_source4 = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    
    #unfold_source4 = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_toy'+match+'.root'
    
    unc_source     = plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+'BCDEFGH'+match+'_stats_'+mc+'.root'
    
    filelist = [signal_source,unfold_source1,unfold_source2,unfold_source3,unfold_source4,unc_source]
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
        
    plots=[]
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
        for ysmin in [0.0,0.5,1.0,1.5,2.0]:
          if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            #filelist_binned.insert(3,plots_folder+cut+dressed+puid+'/resolution/'+obs+'_'+mc+namestring+'.root')
            #filelist_binned[4] = plots_folder+cut+dressed+puid+'/resolution/'+obs+'_amc'+namestring+'.root'
            d = ({ 
                #'files': filelist_binned[:4]+[plots_folder+cut+dressed+puid+'/resolution/'+obs+'_amc'+namestring+'.root']+filelist_binned[5:],
                #'x_expressions': ['gen'+obs+namestring]+3*['gen'+obs+namestring]+['gen'+obs]+['uncertainty_'+mc+namestring],
                'files': filelist_binned,
                'x_expressions': ['gen'+obs+namestring]+4*['unfolded'+obs+namestring]+['uncertainty_'+mc+namestring],
                'folders': [''],
                'nicks': ['gen','dagostini','inversion','tunfold','matrix','unc'],
                'analysis_modules': ['MultiplyHistograms','SumOfHistograms','Ratio'],
                'multiply_nicks': ['gen unc'],
                'multiply_result_nicks': ['fac'],
                'sum_nicks' : ['gen fac','gen fac'],
                'sum_result_nicks' : ['up','down'],
                'sum_scale_factors' : ['1 1', '1 -1'],
                'ratio_numerator_nicks': ['dagostini','inversion','tunfold','matrix','up','down'],
                'ratio_denominator_nicks': ['gen'],
                'ratio_denominator_no_errors': False,
                'labels': ["Gen","D`Agostini (4x)","Inversion (RooUnfold)","TUnfold (1e-6)","Matrix Inversion","","","","","Response Stat. Unc."," "],
                'subplot_legend': 'upper left',
                'subplot_fraction': 45,
                'y_subplot_label': 'Ratio to Gen',
                'www': 'comparison_unfolding_methods'+cut+dressed+puid+'_'+data+'_by_'+mc+match+'/unfolded'+namestring,
                'filename': obs,
                'x_label': 'zpt',
                'x_log': True,
                'x_errors': 4*[0]+[1,0,0,0,1,0,0],
                'y_log': True,
                'y_errors': [True]+10*[False],
                'markers': ['.']+2*['s','D','o','.']+['fill']*2,
                'nicks_whitelist': ['^gen$','^dagostini$','^inversion$','^tunfold$','^matrix$','ratio'],
                'colors': ['black','red','blue','green','purple','red','blue','green','purple','yellow','white'],
                'y_subplot_lims': [0.8,1.2],
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
            })
            plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

#def plot_compare_unfolding_samples_3D(args=None, obs='phistareta', cut='_jet1pt20', data='BCDEFGH', mc='amc',match='',dressed='_FSR01',puid=''):
#def plot_compare_unfolding_samples_3D(args=None, obs='zpt', cut='_jet1pt20', data='BCDEFGH', mc='amc',match='',dressed='_FSR01',puid=''):
#def plot_compare_unfolding_samples_3D(args=None, obs='phistareta', cut='_jet1pt20', data='BCDEFGH', mc='mad',match='',dressed='_FSR01',puid=''):
#def plot_compare_unfolding_samples_3D(args=None, obs='zpt', cut='_jet1pt20', data='BCDEFGH', mc='mad',match='',dressed='_FSR01',puid=''):
#def plot_compare_unfolding_samples_3D(args=None, obs='phistareta', cut='_jet1pt20', data='BCDEFGH', mc='toy',match='',dressed='_FSR01',puid=''):
def plot_compare_unfolding_samples_3D(args=None, obs='zpt', cut='_jet1pt10', data='BCDEFGH', mc='toy',match='',dressed='_FSR01',puid=''):
    create_3Dhist(args,obs,cut,'amc',match,dressed,puid)
    create_3Dhist(args,obs,cut,'hpp',match,dressed,puid)
    create_3Dhist(args,obs,cut,'mad',match,dressed,puid)
    create_toy3Dhist(args,obs,cut,'mad',match,dressed,puid)
    unfold_3Dhist_by_inversion(args,obs,cut,'amc',mc,match,dressed,puid)
    unfold_3Dhist_by_inversion(args,obs,cut,'hpp',mc,match,dressed,puid)
    unfold_3Dhist_by_inversion(args,obs,cut,'mad',mc,match,dressed,puid)
    
    signal_source1 = plots_folder+cut+dressed+puid+'/'+obs+'_amc'+match+'.root'
    signal_source2 = plots_folder+cut+dressed+puid+'/'+obs+'_mad'+match+'.root'
    signal_source3 = plots_folder+cut+dressed+puid+'/'+obs+'_hpp'+match+'.root'
    unfold_source1 = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_amc_by_'+mc+match+'.root'
    unfold_source2 = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_mad_by_'+mc+match+'.root'
    unfold_source3 = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_hpp_by_'+mc+match+'.root'
    unc_source     = plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+'_stats_'+mc+'.root'
    varlist = ['Robs','Ryj','Ryz','F','A']
    #varlist = ['Ryj']#,'switch'
    filelist = [signal_source1,unfold_source1,signal_source2,unfold_source2,signal_source3,unfold_source3,unc_source]+[
                plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+'_'+var+'.root' for var in varlist]
    
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
        
    plots=[]
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
        for ysmin in [0.0,0.5,1.0,1.5,2.0]:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'files': filelist_binned,
                'x_expressions': 3*['gen'+obs+namestring,'unfolded'+obs+namestring]+['uncertainty_stats_'+mc+namestring]+['uncertainty_'+x+namestring for x in varlist],
                'folders': [''],
                'nicks': ['amcgen','amcunf','madgen','madunf','hppgen','hppunf','unc_mc']+['unc_'+x for x in varlist],
                'analysis_modules': ['QuadraticSumOfHistograms','Ratio','SumOfHistograms'],#,'MultiplyHistograms'
                'quad_sum_nicks': ['unc_'+' unc_'.join(varlist)],
                'quad_sum_result_nicks': ['unc_toy'],
                #'multiply_nicks': ['madgen unc_mc','madgen unc_toy'],
                #'multiply_result_nicks': ['fac_mc','fac_toy'],
                #'sum_nicks' : ['madgen fac_mc','madgen fac_mc','madgen fac_toy','madgen fac_toy'],
                #'sum_result_nicks' : ['mc_up','mc_down','toy_up','toy_down'],
                #'sum_scale_factors' : ['1 1', '1 -1','1 1', '1 -1'],
                #'ratio_numerator_nicks': ['amcunf','madunf','hppunf','mc_up','mc_down','toy_up','toy_down'],
                #'ratio_denominator_nicks': ['amcgen','madgen','hppgen']+4*['madgen'],
                'ratio_numerator_nicks': ['unc_mc','amcunf','madunf','hppunf'],
                'ratio_denominator_nicks': ['unc_mc','amcgen','madgen','hppgen'],
                'ratio_result_nicks': ['unity','ratio_amc','ratio_mad','ratio_hpp'],
                'sum_nicks' : ['unity unc_mc','unity unc_mc','unity unc_toy','unity unc_toy'],
                'sum_scale_factors' : ['1 1', '1 -1','1 1', '1 -1'],
                'sum_result_nicks': ['mc_up','mc_down','toy_up','toy_down'],
                'ratio_denominator_no_errors': False,
                'labels': ["aMC@NLO","aMC@NLO","","Herwig++","Herwig++","","Madgraph","Madgraph","","Toy Stat. Unc.","","Toy Syst. Unc.",""],
                'subplot_legend': 'upper left',
                'subplot_fraction': 45,
                'subplot_nicks': ['up','down','ratio'], 
                'y_subplot_label': 'Unfolded/Gen',
                'www': 'comparison_unfolding_samples'+cut+dressed+puid+'_'+data+'_by_'+mc+match+'/unfolded'+namestring,
                'filename': obs,
                'x_label': obs,
                'x_log': True,
                'x_errors': 3*[1,0,0]+4*[0],
                'y_log': True,
                'y_errors': 9*[True]+4*[False],
                'step': [False]*11+[True]*2,
                'line_styles': ['']*11+['-']*2,
                'markers': ['.','s','s','.','D','D','.','o','o']+['fill']*2+['']*2,
                #'nicks_whitelist': ['^gen$','^amc$','^mad$','^hpp$','^toy$','ratio'],
                'nicks_whitelist': ['amc','hpp','mad','mc','toy'],
                'nicks_blacklist': ['unity','unc'],
                'colors': ['darkred','red','red','darkblue','blue','blue','darkgreen','green','green','yellow','white','black','black'],
                'y_subplot_lims': [0.9,1.1],
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
            })
            if not mc=='toy':
                d['nicks_blacklist']+=['toy']
                d['labels'].pop(9)
                d['labels'].insert(9," ")
                d['labels'].pop(10)
            if mc=='amc':
                d['labels'].insert(9,"aMC@NLO Stat. Unc.")
            elif mc=='hpp':
                d['labels'].insert(9,"Herwig++ Stat. Unc.")
            elif mc=='mad':
                d['labels'].insert(9,"Madgraph Stat. Unc.")
            if not ybmin+ysmin>2:
                plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def plot_uncertainties_3D(args=None, obs='zpt', cut='_jet1pt15', data='BCDEFGH', mc='toy', match='',dressed='_FSR01',puid=''):
#def plot_uncertainties_3D(args=None, obs='phistareta', cut='_jet1pt15', data='BCDEFGH', mc='mad', match='',dressed='_FSR01',puid=''):
    if not data == 'BCDEFGH':
        print "WARNING: uncertainties are meant for data only!"
        return
    unf_source = plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+'_statistical.root'
    unc_source = plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+'_stats_'+mc+'.root'
    varlist = ['lumi','bkg','IDSF','IsoSF','TriggerSF','JEC','Robs','Ryj','Ryz','F','A']#,'switch','SF','weight']
    filelist = [unf_source,unc_source]+[plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+'_'+var+'.root' for var in varlist]
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    plots = []
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
        for ysmin in [0.0,0.5,1.0,1.5,2.0]:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'files': filelist_binned,
                'folders': [''],
                'nicks': ['unf','stats']+varlist,
                'x_expressions': ['uncertainty_statistical'+namestring]+['uncertainty_stats_'+mc+namestring]+['uncertainty_'+var+namestring for var in varlist],
                'analysis_modules': ['QuadraticSumOfHistograms'],
                'quad_sum_nicks': ['IDSF IsoSF TriggerSF','Robs Ryz Ryj F A','eff toy lumi bkg stats JEC'],
                'quad_sum_result_nicks': ['eff','toy','total'],
                #'legend':'upper left',
                'filename': obs,
                'nicks_whitelist': ['total','lumi','bkg','eff','stats','toy','JEC','unf'],
                #'nicks_whitelist': ['stats'],#'toy','unf'],
                'labels': ['total','lumi','bkg','efficiency','unfolding','model','JEC','statistical'],
                'alphas': [0.5],
                'x_label': obs,
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'y_errors': False,
                'y_lims': [0,0.1],
                'y_label': "Relative Uncertainty",
                'www': 'comparison_uncertainties'+cut+dressed+puid+'_'+data+'_by_'+mc+match+'/uncertainties'+namestring,
                'x_log': True,
                'step': [True],
                'line_styles': ['-'],
                'markers': ['o','v','^','>','<','s','D','fill'],
                'colors': ['black','red','blue','green','purple','orange','magenta','cornflowerblue'],
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
            })
            if not mc == 'toy':
                d['nicks_whitelist'] = ['total','lumi','bkg','eff','stats','JEC','unf']
                d['labels'] = ['total','lumi','bkg','efficiency','unfolding','JEC','statistical']
                d['quad_sum_nicks'][-1] = 'eff lumi bkg stats JEC'
                d['markers'] = ['o','v','^','>','<','D','fill'],
                d['colors'] = ['black','red','blue','green','purple','magenta','cornflowerblue'],
            if not ybmin+ysmin>2:
                plots.append(d)
    return [PlottingJob(plots=plots, args=args)]


'''
def plot_compare_FSR_3D(args=None, obs='zpt', cut='_jet1pt20', match='',puid=''):
    noFSR_source1 = plots_folder+cut+puid+'/'+obs+'_amc'+match+'.root'
    inFSR_source1 = plots_folder+cut+'_FSR01'+puid+'/'+obs+'_amc'+match+'.root'
    noFSR_source2 = plots_folder+cut+puid+'/'+obs+'_mad'+match+'.root'
    inFSR_source2 = plots_folder+cut+'_FSR01'+puid+'/'+obs+'_mad'+match+'.root'
    noFSR_source3 = plots_folder+cut+puid+'/'+obs+'_hpp'+match+'.root'
    inFSR_source3 = plots_folder+cut+'_FSR01'+puid+'/'+obs+'_hpp'+match+'.root'
    filelist = [noFSR_source1,inFSR_source1,noFSR_source2,inFSR_source2,noFSR_source3,inFSR_source3]
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    plots = []
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
        for ysmin in [0.0,0.5,1.0,1.5,2.0]:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'files': filelist_binned,
                'folders': [''],
                'nicks': [   'genundressedamc', 'gendressedamc', 'genundressedmad', 'gendressedmad', 'genundressedhpp', 'gendressedhpp',
                            'recoundressedamc','recodressedamc','recoundressedmad','recodressedmad','recoundressedhpp','recodressedhpp'],
                'x_expressions': ['gen'+obs+namestring]*6+[obs+namestring]*6,
                'analysis_modules': ['NormalizeByBinWidth','Ratio'],
                'ratio_numerator_nicks': ['genundressedamc', 'gendressedamc', 'genundressedmad', 'gendressedmad', 'genundressedhpp', 'gendressedhpp'],
                'ratio_denominator_nicks': ['recoundressedamc','recodressedamc','recoundressedmad','recodressedmad','recoundressedhpp','recodressedhpp'],
                'ratio_denominator_no_errors': False,
                'y_subplot_label': 'Dressed/Bare',
                'filename': obs,
                'x_label': obs,
                'x_log': True,
                'x_errors': [1],
                #'subplot_legend': 'upper left',
                'y_log': True,
                'y_subplot_lims': [0.9,1.1],
                'labels': [ 'Bare Gen Muons amc','Dressed Gen Muons amc','Bare Reco Muons amc','Dressed Reco Muons amc',
                            'Bare Gen Muons mad','Dressed Gen Muons mad','Bare Reco Muons mad','Dressed Reco Muons mad',
                            'Bare Gen Muons hpp','Dressed Gen Muons hpp','Bare Reco Muons hpp','Dressed Reco Muons hpp',
                            ],
                'www': 'comparison_FSR'+cut+puid+'_'+match+'/FSR'+namestring,
                'markers': ['.'],
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'colors': ['darkblue','blue','darkred','red','darkgreen','green','darkorange','orange','darkmagenta','magenta','darkcyan','cyan','blue','red','green','orange','magenta','cyan'],
            })
            if not ybmin+ysmin>2:
                plots.append(d)
    return [PlottingJob(plots=plots, args=args)]
'''

def plot_compare_unfold_3D(args=None, obs='zpt', cut='_jet1pt20', data='amc', mc='mad', match='',dressed='',puid=''):
    unf_source  = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    data_source = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
    filelist = [unf_source,data_source]
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    plots = []
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
        for ysmin in [0.0,0.5,1.0,1.5,2.0]:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'files': filelist_binned,
                'folders': [''],
                'nicks': ['unf','gen','sig','reco'],
                'x_expressions': ['unfolded'+obs+namestring,'gen'+obs+namestring,'signal'+obs+namestring,obs+namestring],
                'analysis_modules': ['NormalizeByBinWidth','Ratio'],
                'ratio_numerator_nicks': ['unf','gen'],
                'ratio_denominator_nicks': ['sig','reco'],
                'ratio_denominator_no_errors': False,
                'y_subplot_label': 'Ratio',
                'subplot_fraction': 40,
                'filename': obs,
                'x_label': obs,
                'x_log': True,
                'x_errors': [1],
                'subplot_legend': 'upper left',
                'y_log': True,
                'y_subplot_lims': [0.9,1.1],
                'labels': ['Unfolded','Gen','Signal','Reco','Unfolded/Gen','Signal/Reco'],
                'www': 'comparison_unfold'+cut+match+puid+dressed+'_'+data+'_by_'+mc+'/unfold'+namestring,
                'markers': ['.'],
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'colors': ['black','blue','red','green','blue','red'],
            })
            if not ybmin+ysmin>2:
                plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def plot_3Dresponse(args=None,obs='phistareta',cut='_jet1pt20',mc='amc',match='',dressed='_FSR01',puid=''):
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    ybins = [0.0,0.5,1.0,1.5,2.0,2.5]
    ylist = [((xb,yb),(xs,ys))  for (xs,ys) in zip(ybins[:-1],ybins[1:]) for (xb,yb) in zip(ybins[:-1],ybins[1:]) if xb+xs<2.5]
    plots=[]
    d=({
        'files': [plots_folder+cut+dressed+puid+'/'+obs+'_'+mc+match+'.root'],
        'folders': [''],
        'x_label': 'reco'+obs,
        'x_expressions': 'response',
        'x_ticks': [],
        'y_label': 'gen'+obs,
        'y_ticks': [],
        'z_log':True,
        'z_lims':[1e-3,1e0],
        'z_label': 'Fraction of events',
        #'analysis_modules': ['NormalizeColumnsToUnity'],
        'analysis_modules': ['NormalizeRowsToUnity',],
        'colormap': 'summer_r',
        'www': 'response3D'+cut+'/'+mc+match,
        'filename': obs,
        'lines': l_obsbinedges,
        'texts': ['yb{}ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))],
               # +['yb{}ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))],
        'texts_x': [0.02,0.09,0.16,0.23,0.30, 0.37,0.44,0.51,0.58,0.65,0.72,0.78, 0.85, 0.91, 0.96],#+15*[1.02],
        'texts_y': 15*[1.02],#+[0.02,0.09,0.16,0.23,0.30, 0.37,0.44,0.51,0.58,0.65,0.72,0.78, 0.85, 0.91, 0.96],
        #'x_lims': [0,18],
        #'y_lims': [0,18],
        'texts_size': [5],
        'vertical_lines': l_obsbinedges,
        'lines_styles': 5*[':']+['--']+3*[':']+['--']+2*[':']+['--']+[':']+['--'],
        'vertical_lines_styles': 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--'],
    })
    #return d
    plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def plot_crossections(args=None,obs='zpt',cut='_jet1pt20',data='BCDEFGH',mc='NLO',match='',dressed='_FSR01',puid=''):
    unfold_3Dhist_by_inversion(args,obs,cut,data,'amc',match,dressed,puid)
    
    data_source = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_amc'+match+'.root'
    mc_source   = plots_folder+cut+dressed+puid+'/'+obs+'_'+mc+'.root'
    unc_source  = plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+'_total.root'

    filelist = [mc_source,data_source]#,unc_source]
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    ybins = [0.0,0.5,1.0,1.5,2.0,2.5]
    ylist = [((xb,yb),(xs,ys))  for (xs,ys) in zip(ybins[:-1],ybins[1:]) for (xb,yb) in zip(ybins[:-1],ybins[1:]) if xb+xs<2.5]
    scaling = [1e20,1e19,1e18,1e17,1e16,1e13,1e12,1e11,1e10,1e7,1e6,1e5,1e2,1e1,1e0]
    #scaling = [1e6,1e5,1e4,1e3,1e0,1e6,1e5,1e4,1e1,1e6,1e5,1e2,1e3,1e3,1e0]
    plots=[]
    #namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
    d = ({
        'files': [filelist_binned[0]]*len(ylist)+[filelist_binned[1]]*len(ylist),
        'folders': [''],
        'x_expressions':  ['gen'+obs+'_yb{}_ys{}'.format(int(2*yboost[0]),int(2*ystar[0])) for (yboost,ystar) in ylist]
                    +['unfolded'+obs+'_yb{}_ys{}'.format(int(2*yboost[0]),int(2*ystar[0])) for (yboost,ystar) in ylist],
        'nicks':    ['gen_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))]
                   +['unf_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))],
        'analysis_modules': ['NormalizeByBinWidth','ScaleHistograms'],
        'scale_nicks':  ['gen_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))]
                       +['unf_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))],
        'scales': 2*[1e0/35.9/1000*s for s in scaling],
        'x_log': True,
        'x_errors': [1]*len(ylist)+[0]*len(ylist),
        'y_log': True,
        'y_errors': [False]*len(ylist)+[True]*len(ylist),
        'markers': ['']*len(ylist)+['^','1','p','+','*','<','2','o','x','>','3','s','v','4','d'],
        'colors': ['grey']*len(ylist)+
                    [color for color in ['red','salmon','crimson','violet','brown','blue','cyan','royalblue','teal','orange','gold','yellow','green','lime','purple']],
        'y_lims':[1e-6,1e21] if obs == 'zpt' else [1e-4,1e23],
        'filename': obs,
        'x_label': obs,
        'www': 'unfolded3D_'+data+'_'+mc+cut+dressed+puid,
        'legend': None,
        'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
        'legend_cols': 2,
        })
    if mc in ['LO','NLO','NNLO']:
        d['scales']=[1e0*s for s in scaling]+[1e0/35.9/1000*s for s in scaling]
        d['histograms_to_normalize_by_binwidth'] = ['unf_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))]
    if obs == 'zpt':
        d['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\mathit{p}_T^Z d\\mathit{y_b} d\\mathit{y^*}}/(\\frac{p\\mathit{b}}{GeV})$'
    elif obs == 'phistareta':
        d['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\Phi^{*}_{\\eta} d\\mathit{y_b} d\\mathit{y^*}}/p\\mathit{b}$'
    plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def write_results_to_txt(args=None,obs='phistareta',cut='_jet1pt20',data='BCDEFGH',mc='mad',match='',dressed='_FSR01',puid=''):
    unfold_3Dhist_by_inversion(args,obs,cut,data,mc,match,dressed,puid)
    uncertainties_3Dhist(args,obs,cut,data,match,dressed,puid,varquantity='_total')
    data_source = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    unc_source  = plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+'_total.root'
    filelist = [data_source,unc_source]
    varlist = ['stat','lumi','bkg','eff','unf']
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    
    plots=[]
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
        for ysmin in [0.0,0.5,1.0,1.5,2.0]:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'files': [filelist_binned[0]]+len(varlist)*[filelist_binned[1]],
                'folders': [''],
                'nicks': ['data']+['unc_'+var for var in varlist],
                'x_expressions': ['unfolded'+obs+namestring]+['uncertainty_'+var+namestring for var in varlist],
                'x_label': obs,
                'x_log': True,
                'y_log': True,
                'analysis_modules': ['ScaleHistograms','NormalizeByBinWidth','PrintResults'],
                'scale_nicks':  ['data'],
                'scales':[1e0/35.9/1000],#/1.0/1000],
                'histograms_to_normalize_by_binwidth': ['data'],
                'filename': plots_folder+cut+dressed+puid+'/results/'+obs+namestring,
                #'output_dir': plots_folder+cut+dressed+puid+'/results',
                #'www': 'test/uncertainties'+namestring,
            })
            if not ybmin+ysmin>2:
                plots.append(d)
    return [PlottingJob(plots=plots, args=args)]


'''
def plot_3Dhist(args=None, obs='zpt', cut='_jet1pt20', data='BCDEFGH', mc='mad', match='',dressed='',puid='',varquantity='',variation=0,prefix='unfolded', ratio=False, txt=False):
    if not mc == 'toy':
        variation = 0
    if variation == 0:
        varquantity=''
    input_file_data = plots_folder+cut+dressed+puid+'/'+prefix+obs+'_'+data+'_by_'+mc+match+varquantity+variationstring[variation]+'_separated.root'
    #input_file_mc   = plots_folder+cut+dressed+puid+'/'+obs+'_'+mc+match+'_separated.root'
    #input_file_mc   = plots_folder+cut+dressed+puid+'/'+obs+'_NLO'+match+'_separated.root'
    input_file_mc   = plots_folder+cut+'/'+obs+'_amc'+match+dressed+puid+'_separated.root'
    ybins = [0.0,0.5,1.0,1.5,2.0,2.5]
    ylist = [((xb,yb),(xs,ys))  for (xs,ys) in zip(ybins[:-1],ybins[1:]) for (xb,yb) in zip(ybins[:-1],ybins[1:]) if xb+xs<2.5]
    #print ylist
    scaling = [1e6,1e5,1e4,1e3,1e0,1e6,1e5,1e4,1e1,1e6,1e5,1e2,1e3,1e3,1e0]
    d = ({
        'files': [input_file_mc]*len(ylist)
                +[input_file_data]*len(ylist),
        'folders': [''],
        'x_expressions': ['gen'+obs+'_yb{}_ys{}'.format(int(2*yboost[0]),int(2*ystar[0])) for (yboost,ystar) in ylist],
                   #+['unfolded'+obs+'_yb{}_ys{}'.format(int(2*yboost[0]),int(2*ystar[0])) for (yboost,ystar) in ylist],
        'nicks':    ['gen_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))]
                   +['unf_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))],
        'analysis_modules': ['NormalizeByBinWidth','ScaleHistograms'],
        'legend_cols': 2,
        'legend': None,
        'scale_nicks':  ['gen_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))]
                       +['unf_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))],
        'scales':[1e0/35.9/1.0/1000*s for s in scaling]+[1e0/35.9/1000*s for s in scaling],
        'x_log': True,
        'y_log': True,
        'labels':  ['(${}<y_b<{}$; ${}<y^*<{}$)'.format(
                    yboost[0],yboost[1],ystar[0],ystar[1]) for (yboost,ystar) in ylist],
        'x_errors': [1]*len(ylist)+[0]*len(ylist),
        #'y_errors': [False]*len(ylist)+[True]*len(ylist),
        #'x_lims': [30,1000] if obs == 'zpt' else [0.4,50],
        'www': 'unfolded3D'+cut+'/'+data+'_by_'+mc+varquantity+variationstring[variation],
        #'markers': ['']*len(ylist)+['^','<','>','v','d','1','2','3','4','d','o','s','+','x','*'],
         'markers': ['']*len(ylist)+['^','1','p','+','*','<','2','o','x','>','3','s','v','4','d'],
        #'colors': [color for color in ['red','orange','blue','green','purple','salmon','gold','cyan','lime','crimson','yellow','royalblue','violet','teal','brown']],
        'colors': [color for color in ['red','salmon','crimson','violet','brown','blue','cyan','royalblue','teal','orange','gold','yellow','green','lime','purple']],
        #['black', 'red', 'blue', 'green', 'purple', 'orange', 'cyan','magenta', 'gold', 'saddlebrown', 'olivedrab', 'lightsteelblue', 'burlywood', 'lightcoral']
        'y_lims':[1e-6,1e6] if obs == 'zpt' else [1e-3,1e10],
        'filename': obs,
        'x_label': obs,
        'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{6.2}}$",
    })
    if mc == 'NLO':
        d.update({
        'histograms_to_normalize_by_binwidth': ['unf_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))],
        'scales':[s for s in scaling]+[1e0/35.9/1000*s for s in scaling],
        #
        
        
        })
    if ratio:
        d['analysis_modules']+= ['Ratio']
        d['www']+='_ratio'
        d.update({  'ratio_numerator_nicks':   ['unf_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))],
                    'ratio_denominator_nicks': ['gen_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))],
                    'ratio_result_nicks':    ['ratio_yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))],
                    'ratio_denominator_no_errors': False,
                    #'scales': [1e0/35.9*4/1.0/1000]*len(ylist)+[1e0/35.9*4/1.0/1000/s for s in range(1,16)],
                    'nicks_whitelist': ['ratio'],#['_yb0'],#
                    #'x_ticks': [30,1000],
                    #'y_subplot_lims': [0.75,1.25],
                    #'subplot_fraction': 35,
                    'y_errors': [True],
                    'subplot_nicks': ['_dummy'],
                    'markers': ['.'],
                    'x_errors': [1],
                    'y_lims': [0.5,1.5],
                    'y_log': False,
                    'lines': [1],#1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4,3.6,3.8],
                    #'lumis' : [35.9],
        })
    if txt:
        d['analysis_modules']+= ['PrintResults']
        d.pop('www')
        d.update({  'filename': '/ceph/tberger/plots/3D'+cut+'/xsec_'+obs+'_'+data+'_by_'+mc+match+'_'+method,
                    'scales': [1]*len(ylist)+[1e0/35.9/1000]*len(ylist),
                    #'nicks_blacklist': ['gen'],
        })
    if obs == 'zpt':
        d['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\mathit{p}_T^Z d\\mathit{y_b} d\\mathit{y^*}}/(\\frac{p\\mathit{b}}{GeV})$'
    elif obs == 'phistareta':
        d['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\Phi^{*}_{\\eta} d\\mathit{y_b} d\\mathit{y^*}}/p\\mathit{b}$'
    return d
'''


def write_to_root(args=None,obs='zpt',order='NLO'):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args,obs)
    [l_obshists, h_reco, h_gen, h_recoresponse, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args, obs)
    ybins = [0.0,0.5,1.0,1.5,2.0,2.5]
    ylist = [((xb,yb),(xs,ys))  for (xs,ys) in zip(ybins[:-1],ybins[1:]) for (xb,yb) in zip(ybins[:-1],ybins[1:]) if xb+xs<2.5]
    
    #index_nlo  = lines.index('NLO')
    #index_nnlo = lines.index('NNLO')
    for ((xb,yb),(xs,ys)) in ylist:
        input_file = os.environ["EXCALIBURPATH"]+"/bettina_xsec/ZJ.NNLO.ZJtriple_yb{}_ystar{}_ptz.cross_section-NNPDF31_nnlo_as_0118.LO_NLO_NNLO.txt".format(int(2*xb),int(2*xs))
        with open(input_file) as f: lines = [line.rstrip('\n') for line in f]
        lines = [line.rstrip(']') for line in lines]
        index_start = lines.index(order)
        index_end   = lines.index('N'+order if order in ['LO','NLO'] else '####################################################################### ')
        y_index = l_ybinedges[int(2*xs)]+int(2*xb)
        print y_index
        list_lo =[]
        for i in xrange(index_start,index_end):
            line=lines[i+1].split('  ')
            line.pop(0)
            for x in line:
                list_lo.append(float(x))
        print list_lo
        for j in xrange(len(list_lo)):
            obs_index = l_obsbinedges[y_index]+j+1
            print obs_index
            h_gen.SetBinContent(obs_index,list_lo[j])
    output_file = ROOT.TFile("/ceph/tberger/plots/3D/"+obs+"_"+order+"_jet1pt20.root","RECREATE")
    h_gen.Write()
    h_reco.Write()
    return

def unfold_3Dhist(args=None,obs='zpt',cut='_jet1pt20',data='amc',mc='toy',match='',dressed='',puid='',method='dagostini', variation=0, varquantity=''):
    output_file = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'_'+method+'.root'
    input_file = plots_folder+cut+dressed+puid+'/'+obs+'_'+mc+match+'.root'
    if not mc == 'toy':
        variation = 0
    if not variation == 0:
        input_file = plots_folder+cut+dressed+puid+'/'+obs+'_toy'+match+varquantity+str(variation)+'.root'
    #if os.path.exists(output_file):
    #    print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
    #    return
    plots = []
    d=({
        'files': [  input_file,
                    plots_folder+cut+dressed+puid+'/'+obs+'_'+data+'.root',
                    input_file,
                    input_file,
                    #plots_folder+cut+'/'+obs+'_NLO'+match+dressed+puid+'.root',
                    ],
        'folders': [''],
        'x_expressions': ['response',obs,obs,'gen'+obs],
        'nicks': ['responsematrix','signal','reco','gen'],
        'analysis_modules': ['Unfolding'],
        'unfolding_variation': 0,
        'unfolding': 'signal',
        'unfolding_mc_reco': 'reco',#
        'unfolding_mc_gen': 'gen',#
        'unfolding_new_nicks': 'unfolded',
        'unfolding_method' : method,
        'unfolding_responsematrix': 'responsematrix',
        'unfolding_regularization': 1e-6,
        'unfolding_iterations': 4,
        'libRooUnfold': os.environ['EXCALIBURPATH']+'/../../../RooUnfold/libRooUnfold.so',
        'unfold_file' : [output_file],
        'write_matrix' : True,
    })
    if data=='BCDEFGH':
        backgroundlist = ['TTJets','TW','WW','WZ','ZZ']
        d['files']+= [plots_folder+cut+'/'+obs+'_'+x+match+dressed+puid+'.root' for x in backgroundlist]
        d['analysis_modules'] = ['SumOfHistograms']+d['analysis_modules']
        d['x_expressions'] += len(backgroundlist)*[obs]
        d.update({  'nicks': ['responsematrix','data','reco','gen']+backgroundlist,
                    'sum_nicks': ['data '+' '.join(backgroundlist)],
                    'sum_scale_factors' : ['1'+len(backgroundlist)*' -1'],
                    'sum_result_nicks': ['signal'],
        })
    plots.append(d)
    return [PlottingJob(plots=plots, args=args)]
    #return d(

        
        

