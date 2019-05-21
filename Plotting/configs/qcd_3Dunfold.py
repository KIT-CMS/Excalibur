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
#def invert_3Dhists(args=None, filename = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple_jet1pt20/variations/zpt_toy_ADown.root'):
#def invert_3Dhists(args=None, filename = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple_jet1pt20/zpt_toy.root'):
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


def create_3Dhist(args=None, obs='zpt', cut='_jet1pt20', data='mad', match='', dressed='', puid='', varquantity='', variation=0):
    if data == 'toy':
        print "toy mc not created by this function."
        return
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, data, yboostbin=None, ystarbin=None)
    [l_obshists, h_reco, h_gen, h_recoresponse, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args, obs)
    # simulations are always scaled to match data comparison (weight, lumi)
    if data in ['BCDEFGH','BCD']:
        lumi = 1
        match = ''
    else:
        lumi = d['lumis'][0]
    h_genresponse = deepcopy(h_recoresponse)
    h_gen2  = deepcopy(h_gen)
    h_reco2 = deepcopy(h_reco)
    if varquantity == '_JEC':
        input_file = datasets[data].replace('.root',dressed+puid+varquantity+variationstring[variation]+'.root')
    elif varquantity == '_JER':
        input_file = datasets[data].replace('.root',dressed+puid+varquantity+'.root')
    else:
        input_file = datasets[data].replace('.root',dressed+puid+'.root')
    f_in = ROOT.TFile(input_file,"READ")
    print "Create histograms from file",input_file
    output_file = plots_folder+cut+dressed+puid+'/'+obs+"_"+data+match+".root"
    if not varquantity in ['_IDSF','_IsoSF','_TriggerSF','_JEC']:
        variation = 0
    if varquantity=='_JER' or not variation == 0:
        if not os.path.exists(plots_folder+cut+dressed+puid+'/variations'):
            print "WARNING: variations folder",plots_folder+cut+dressed+puid+'/variations',"does not exist!"
            return
        else:
            output_file = plots_folder+cut+dressed+puid+'/variations/'+obs+"_"+data+match+varquantity+variationstring[variation]+".root"
    print "Response will be written to", output_file
    if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        return
    ntuple_gen, ntuple_reco = f_in.Get("genzjetcuts_L1L2L3/ntuple"), f_in.Get("zjetcuts_L1L2L3/ntuple")
    if data in ['BCDEFGH','BCD']:
        ntuple_reco = f_in.Get("zjetcuts_L1L2L3Res/ntuple")
    f_out = ROOT.TFile(output_file,"RECREATE")
    print 'Fill 3D reco histogram'
    obsmin, obsmax = l_obshists[0].GetXaxis().GetXbins()[0],l_obshists[0].GetXaxis().GetXbins()[l_obshists[0].GetNbinsX()]
    for entry in ntuple_reco:
        zy,jet1y,event,weight = entry.zy,entry.jet1y,entry.event,entry.weight
        recocutweight = ( (entry.mupluspt >25) & (abs(entry.mupluseta) <2.4)
                        & (entry.muminuspt>25) & (abs(entry.muminuseta)<2.4)
                        & (abs(entry.zmass-91.1876)<20) )
        genzy,genjet1y = ( (entry.genzy, entry.genjet1y) if not data in ['BCD','BCDEFGH'] else (zy,jet1y))
        gencutweight = (  (entry.genmupluspt >25) & (abs(entry.genmupluseta) <2.4)
                        & (entry.genmuminuspt>25) & (abs(entry.genmuminuseta)<2.4)
                        & (abs(entry.genzmass-91.1876)<20) 
                        if not data in ['BCD','BCDEFGH'] else recocutweight)
        jet1pt = entry.jet1pt
        genjet1pt = (entry.genjet1pt if not data in ['BCD','BCDEFGH'] else jet1pt)
        yb,ys = 0.5*abs(zy+jet1y),0.5*abs(zy-jet1y)
        genyb,genys = 0.5*abs(genzy+genjet1y),0.5*abs(genzy-genjet1y)
        #yb,ys = entry.yboost,entry.ystar
        #genyb,genys = (entry.genyboost,entry.genystar) if not data in ['BCD','BCDEFGH'] else (entry.yboost,entry.ystar)
        if 'jet1pt20' in cut.split('_'):
            gencutweight  &= ((genjet1pt>20) if not data in ['BCD','BCDEFGH'] else 1)
            recocutweight &= (jet1pt>20)
        if 'jet1pt15' in cut.split('_'):
            gencutweight  &= ((genjet1pt>15) if not data in ['BCD','BCDEFGH'] else 1)
            recocutweight &= (jet1pt>15)
        if 'jet1pt10' in cut.split('_'):
            gencutweight  &= ((genjet1pt>10) if not data in ['BCD','BCDEFGH'] else 1)
            recocutweight &= (jet1pt>10)
        if not recocutweight:
            continue
        if data in ['BCDEFGH','BCD']:
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
        else:
            SFweight = 1
        if match == '_matched':
            gencutweight  &= (entry.matchedgenjet1pt==entry.genjet1pt)
            recocutweight &= (entry.matchedgenjet1pt==entry.genjet1pt)
        if obs =='zpt':
            recoobs,genobs = entry.zpt,(entry.genzpt if not data in ['BCD','BCDEFGH'] else entry.zpt)
        elif obs =='phistareta':
            recoobs,genobs = entry.phistareta,(entry.genphistareta if not data in ['BCD','BCDEFGH'] else entry.phistareta)
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
    if not data in ['BCD','BCDEFGH']:
      for entry in ntuple_gen:
        #yb,ys,event,weight = entry.yboost,entry.ystar,entry.event,entry.weight
        yb,ys,event,weight = 0.5*abs(entry.zy+entry.jet1y),0.5*abs(entry.zy-entry.jet1y),entry.event,entry.weight
        gencutweight = ((entry.genmupluspt>25) & (abs(entry.genmupluseta)<2.4)
                        & (entry.genmuminuspt>25) & (abs(entry.genmuminuseta)<2.4)
                        & (abs(entry.genzmass-91.1876)<20))
        #genyb,genys = entry.genyboost,entry.genystar
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
        if match == '_matched':
            gencutweight  &= (entry.matchedgenjet1pt==entry.genjet1pt)
            recocutweight &= (entry.matchedgenjet1pt==entry.genjet1pt)
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
    for cut in ['_jet1pt20']:
     for data in ['BCDEFGH','TTJets','TW','WW','WZ','ZZ','ptz','amc','mad','hpp','pow']:
        create_3Dhist(obs='zpt',       cut=cut,data=data)
        create_3Dhist(obs='phistareta',cut=cut,data=data)
     create_toy3Dhist(obs='zpt',       cut=cut,N_toys=N_toys)
     create_toy3Dhist(obs='phistareta',cut=cut,N_toys=N_toys)
     for varquantity in ['_Robs','_Ryj','_Ryz','_A','_F','_switch']:
      for variation in [-1,1]:
        create_toy3Dhist(obs='zpt',       cut=cut,varquantity=varquantity,variation=variation,N_toys=N_toys)
        create_toy3Dhist(obs='phistareta',cut=cut,varquantity=varquantity,variation=variation,N_toys=N_toys)
    return


def create_toy3Dhist(args=None, obs='zpt', cut='_jet1pt20', mc='mad', match='', dressed='', puid='', varquantity='', variation=0, N_toys=1000000):
    if mc == 'BCDEFGH':
        print "Can not create toy mc from data."
        return
    if varquantity in ['','_stats','_IDSF','_IsoSF','_TriggerSF']:
        variation = 0
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, '', mc, yboostbin=None, ystarbin=None)
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    h_genresponse = h_response.Clone("response_2")
    [h_rand,h_RMSobs,h_RMSyz,h_RMSyj,h_A,h_F,h_S] = [h_gen.Clone(name) for name in ['weight',obs+'res','zyres','jet1yres',obs+'A',obs+'F',obs+'switch']]
    l_RMSobs,l_RMSyz,l_RMSyj,l_switch,l_A,l_F= [],[],[],[],[],[]
    input_path  = plots_folder+cut+dressed+puid+'/resolution_985'
    output_file = plots_folder+cut+dressed+puid+'/'+obs+'_toy'+match+'.root'
    if not variation == 0:
        if not os.path.exists(plots_folder+cut+dressed+puid+'/variations'):
            print "WARNING: variations folder",plots_folder+cut+dressed+puid+'/variations',"does not exist!"
            return
        else:
            output_file = plots_folder+cut+dressed+puid+'/variations/'+obs+'_toy'+match+varquantity+variationstring[variation]+'.root'
    # check if gen distributions are existent
    if not (os.path.exists(plots_folder+cut+dressed+puid+'/gen'+obs+'_'+mc+'.root')
        and os.path.exists(plots_folder+cut+dressed+puid+'/genzy'+'_'+mc+'.root')
        and os.path.exists(plots_folder+cut+dressed+puid+'/genjet1y'+'_'+mc+'.root')):
        print "WARNING: gen distributions not created yet. Use merlin.py --py create_gendistributions"
        return
    f_genobs = ROOT.TFile(plots_folder+cut+dressed+puid+'/gen'+obs+'_'+mc+'.root','READ')
    f_genyz  = ROOT.TFile(plots_folder+cut+dressed+puid+'/genzy'+'_'+mc+'.root','READ')
    f_genyj  = ROOT.TFile(plots_folder+cut+dressed+puid+'/genjet1y'+'_'+mc+'.root','READ')
    h_rand_obs = f_genobs.Get('gen'+obs)
    h_rand_yz  = f_genyz.Get('genzy')
    h_rand_yj  = f_genyj.Get('genjet1y')
    # safety step to avoid overwriting of existing files
    if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        return
    print "toy MC will be written to "+output_file
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
            #f_in_yj = ROOT.TFile(input_path+"/jet1y_"+mc+namestring+"_bins_of_"+obs+".root","READ")
            f_in_yj_match = ROOT.TFile(input_path+"/matchedjet1y_"+mc+namestring+"_bins_of_"+obs+".root","READ")
            h_weight = f_in_obs.Get("gen"+obs)
            x_bins = [h_weight.GetBinLowEdge(i+1)+h_weight.GetBinWidth(i+1)/2 for i in xrange(h_weight.GetNbinsX())]
            h_rms_obs= f_in_obs.Get("sigma0")
            h_rms_yz = f_in_yz.Get("sigma0")
            #h_rms_yj = f_in_yj.Get("sigma0")
            h_rms_yj  = f_in_yj_match.Get("sigma0")
            h_switched = f_in_obs.Get("switched")
            h_fake =f_in_obs.Get("fakerate")
            h_acceptance = f_in_obs.Get("acceptance")
            if obs == 'zpt':
                fit1 = ROOT.TF1("fit1","[0]+[1]*sqrt(x)+[2]/sqrt(x)",obsmin,obsmax)
                fit2 = ROOT.TF1("fit2","[0]+[1]/sqrt(x)",obsmin,obsmax)
                fit3 = ROOT.TF1("fit3","[0]",obsmin,obsmax)
                fit4 = ROOT.TF1("fit4","[0]-[1]/x",obsmin,obsmax)
                fit6 = ROOT.TF1("fit6","[0]*exp(-[1]*x)",obsmin,obsmax)
            elif obs == 'phistareta':
                fit1 = ROOT.TF1("fit1","[0]+[1]*x+[2]/x",obsmin,obsmax)
                fit2 = ROOT.TF1("fit2","[0]+[1]/x",obsmin,obsmax)
                fit3 = ROOT.TF1("fit3","[0]+[1]*log(x)",obsmin,obsmax)
                fit4 = ROOT.TF1("fit4","[0]-[1]/x**2",obsmin,obsmax)
                fit6 = ROOT.TF1("fit6","[0]+[1]/x",obsmin,obsmax)
            fit5 = ROOT.TF1("fit5","[0]+[1]/x**3",obsmin,obsmax)
            fit2.SetParLimits(0,0,1)
            fit5.SetParLimits(0,0,1)
            fit6.SetParameters(0,10)
            fit6.SetParameters(1,0.001)
            
            fit_obs = h_rms_obs.Fit("fit1","S N")
            v_obs = [fit1(x_bins[i]) for i in xrange(h_rms_obs.GetNbinsX())]
            conf_obs = array('d',[0]*len(x_bins))
            fit_obs.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_obs,0.683)
            
            fit_yj = h_rms_yj.Fit("fit2","S N")
            v_yj = [fit2(x_bins[i]) for i in xrange(h_rms_yj.GetNbinsX())]
            conf_yj = array('d',[0]*len(x_bins))
            fit_yj.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_yj,0.683)
            
            fit_yz = h_rms_yz.Fit("fit3","S N")
            v_yz = [fit3(x_bins[i]) for i in xrange(h_rms_yz.GetNbinsX())]
            conf_yz = array('d',[0]*len(x_bins))
            fit_yz.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_yz,0.683)
            
            fit_A = h_acceptance.Fit("fit4","S N")
            v_A = [fit4(x_bins[i]) for i in xrange(h_acceptance.GetNbinsX())]
            conf_A = array('d',[0]*len(x_bins))
            fit_A.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_A,0.683)
            
            fit_F = h_fake.Fit("fit5","S N")
            v_F = [fit5(x_bins[i]) for i in xrange(h_fake.GetNbinsX())]
            conf_F = array('d',[0]*len(x_bins))
            fit_F.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_F,0.683)
            
            fit_S = h_switched.Fit("fit6","S N")
            v_S = [fit6(x_bins[i]) for i in xrange(h_switched.GetNbinsX())]
            conf_S = array('d',[0]*len(x_bins))
            fit_S.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_S,0.683)

            h_pu = f_in_obs.Get("PU")
        bin_index += 1
        
        h_RMSobs.SetBinContent(obsbin+1,v_obs[bin_index-1]), h_RMSobs.SetBinError(obsbin+1,conf_obs[bin_index-1])
        h_RMSyz.SetBinContent(obsbin+1,v_yz[bin_index-1])  , h_RMSyz.SetBinError(obsbin+1,conf_yz[bin_index-1])
        h_RMSyj.SetBinContent(obsbin+1,v_yj[bin_index-1])  , h_RMSyj.SetBinError(obsbin+1,conf_yj[bin_index-1])
        h_A.SetBinContent(obsbin+1,1-v_A[bin_index-1])     , h_A.SetBinError(obsbin+1,conf_A[bin_index-1])
        h_F.SetBinContent(obsbin+1,v_F[bin_index-1])       , h_F.SetBinError(obsbin+1,conf_F[bin_index-1])
        h_S.SetBinContent(obsbin+1,v_S[bin_index-1])       , h_S.SetBinError(obsbin+1,conf_S[bin_index-1])
        
        l_RMSobs.append(h_RMSobs[obsbin+1]+(variation*h_RMSobs.GetBinError(obsbin+1) if varquantity in ['_Robs']   else 0))
        l_RMSyz.append(  h_RMSyz[obsbin+1]+(variation* h_RMSyz.GetBinError(obsbin+1) if varquantity in ['_Ryz']    else 0))
        l_RMSyj.append(  h_RMSyj[obsbin+1]+(variation* h_RMSyj.GetBinError(obsbin+1) if varquantity in ['_Ryj']    else 0))
        l_A.append(          h_A[obsbin+1]-(variation*     h_A.GetBinError(obsbin+1) if varquantity in ['_A']      else 0))
        l_F.append(          h_F[obsbin+1]+(variation*     h_F.GetBinError(obsbin+1) if varquantity in ['_F']      else 0))
        l_switch.append(     h_S[obsbin+1]+(variation*     h_S.GetBinError(obsbin+1) if varquantity in ['_switch'] else 0))
        
    if match == '_matched':
        l_switch = [0]*h_gen.GetNbinsX()
    elif match == '_switched':
        l_switch = [1]*h_gen.GetNbinsX()
    #l_RMSobs = [0]*h_gen.GetNbinsX()
    #l_RMSyz  = [0]*h_gen.GetNbinsX()
    #l_RMSyj  = [0]*h_gen.GetNbinsX()
    #l_switch = [0]*h_gen.GetNbinsX()
    #l_switch = [1]*h_gen.GetNbinsX()
    #l_A  = [0]*h_gen.GetNbinsX()
    #l_F  = [0]*h_gen.GetNbinsX()
    if obs == 'zpt':
        print "zpt resolution in each bin:       ", [l_RMSobs[i] for i in range(5)]
    elif obs == 'phistareta':
        print "phistareta resolution in each bin:", [l_RMSobs[i] for i in range(5)]
    print "zy resolution in each bin:        ", [l_RMSyz[i]  for i in range(5)]
    print "jet1y resolution in each bin:     ", [l_RMSyj[i]  for i in range(5)]
    print "losses in each bin:               ", [l_A[i]      for i in range(5)]
    print "fakes in each bin:                ", [l_F[i]      for i in range(5)]
    print "switch prob in each bin:          ", [l_switch[i] for i in range(5)]
    print "3DtoyMC will be written to "+output_file
    print "create toys"
    for i in xrange(N_toys):
        if i%(N_toys/10) == 0:
            print "toy MC creation finished by "+str(100.*i/N_toys)+"%"
        genobs = h_rand_obs.GetRandom()
        genyz  = h_rand_yz.GetRandom()
        genyj  = h_rand_yj.GetRandom()
        #genobs = (1000-25)*np.random.random()+25
        #genyj = 4.8*np.random.random()-2.4
        #genyz = 4.8*np.random.random()-2.4
        genyb = abs(genyj+genyz)/2
        genys = abs(genyj-genyz)/2
        geny_index = l_ybinedges[int(genys/0.5)]+int(genyb/0.5)
        index = l_obsbinedges[geny_index]+l_obshists[geny_index].FindBin(genobs)-1
        if np.random.random() < l_switch[index]:
            genyj = h_rand_yj.GetRandom()
            #genyj = 4.8*np.random.random()-2.4
            genyb = abs(genyj+genyz)/2
            genys = abs(genyj-genyz)/2
        geny_index = l_ybinedges[int(genys/0.5)]+int(genyb/0.5)
        genobs_index = l_obsbinedges[geny_index]+l_obshists[geny_index].FindBin(genobs)-1
        while True:
            recoobs= genobs * (1+l_RMSobs[genobs_index]*np.random.randn())
            recoyz = genyz+l_RMSyz[genobs_index]*np.random.randn()
            recoyj = genyj+l_RMSyj[genobs_index]*np.random.randn()
            recoyb = abs(recoyj+recoyz)/2
            recoys = abs(recoyj-recoyz)/2
            if not (   (obs=='zpt'        and (recoyb+recoys > 2.4 or recoobs>1000 or recoobs<25 ))
                    or (obs=='phistareta' and (recoyb+recoys > 2.4 or recoobs>50   or recoobs<0.4))):
                        break
        recoy_index = l_ybinedges[int(recoys/0.5)]+int(recoyb/0.5)
        recoobs_index = l_obsbinedges[recoy_index]+l_obshists[recoy_index].FindBin(recoobs)-1
        randF,randA = np.random.random(),np.random.random()
        if randF > l_F[recoobs_index]:
            h_gen.Fill(index)
        if randA > l_A[index]:
            h_reco.Fill(recoobs_index)
        if randA > l_A[index] and randF > l_F[recoobs_index]:
            h_response.Fill(recoobs_index,index)
            h_genresponse.Fill(recoobs_index,genobs_index)
    f_out.cd()
    h_reco.Write()
    h_gen.Write()
    h_response.Write()
    h_genresponse.Write()
    h_RMSobs.Write()
    h_RMSyz.Write()
    h_RMSyj.Write()
    h_A.Write()
    h_F.Write()
    h_S.Write()
    print "3DtoyMC written to "+output_file
    return


def unfold_by_inversion(args=None,obs='zpt',cut='_jet1pt20',data='mad',mc='mad',match='',dressed='', puid='',varquantity='',variation=0):
    if varquantity in ['','_IDSF','_IsoSF','_TriggerSF'] and not variation==0:
        print "WARNING: variations can not be computed for these variation quantities"
        variation = 0
    if not 'toy' in mc and not varquantity == '_stats':
        variation = 0
        print "WARNING: only statistical variations can be computed for this MC"
    input_file_data = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+'.root'
    input_file_mc   = plots_folder+cut+dressed+puid+'/'+obs+'_'+mc+match+'.root'
    output_file = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    if not variation == 0:
      if not varquantity == '_stats':
        input_file_mc = plots_folder+cut+dressed+puid+'/variations/'+obs+'_'+mc+match+varquantity+variationstring[variation]+'.root'
        output_file    = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+varquantity+variationstring[variation]+'.root'
      else:
        output_file    = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+varquantity+'.root'
    print "response will be written to", output_file
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
    h_prox = h_response.ProjectionX("projectionx",1,Nx,"e")
    h_proy = h_genresponse.ProjectionY("projectiony",1,Ny,"e")
    h_SF= h_genresponse.ProjectionX("SF",1,Nx,"e")
    h_SF.Divide(h_prox)
    
    h_fake = h_reco.Clone("fake")
    h_loss = h_gen.Clone("loss")
    h_fake.Add(h_prox,-1)
    h_loss.Add(h_proy,-1)
    for j in xrange(Ny):
        # sometimes negative values appear inside sqrt.
        h_fake.SetBinError(j+1,np.sqrt(abs(h_reco.GetBinError(j+1)**2-h_prox.GetBinError(j+1)**2)))
        h_loss.SetBinError(j+1,np.sqrt(abs( h_gen.GetBinError(j+1)**2-h_proy.GetBinError(j+1)**2)))
    print "data distribution:",[h_data[i+1] for i in xrange(6)]
    print "reco distribution:",[h_reco[i+1] for i in xrange(6)]
    print "gen  distribution:",[h_gen[i+1]  for i in xrange(6)]
    print "projection on X:",  [h_prox[i+1] for i in xrange(6)]
    print "projection on Y:",  [h_proy[i+1] for i in xrange(6)]
    print "scalefactors:",       [h_SF[i+1] for i in xrange(6)]
    print "fake distribution:",[h_fake[i+1] for i in xrange(6)]
    print "loss distribution:",[h_loss[i+1] for i in xrange(6)]
    if varquantity=='_stats' and not variation == 0:
        print "Statistical variation of response matrix"
        for j in xrange(Ny):
          for i in xrange(Nx):
            h_response.SetBinContent(i+1,j+1,h_response.GetBinContent(i+1,j+1)+h_response.GetBinError(i+1,j+1)*np.random.randn())
          h_loss.SetBinContent(j+1,h_loss[j+1]+h_loss.GetBinError(j+1)*np.random.randn())
          h_fake.SetBinContent(j+1,h_fake[j+1]+h_fake.GetBinError(j+1)*np.random.randn())
        h_gen = h_loss.Clone("gen"+obs)
        h_reco = h_loss.Clone(obs)
        h_gen.Add(h_prox)
        h_reco.Add(h_proy)
    if data == 'BCDEFGH':
        l_bkg = ['TTJets','TW','WW','WZ','ZZ']
        print "subtract backgrounds ",l_bkg
        for bkg in l_bkg:
            input_file_bkg = plots_folder+cut+dressed+puid+'/'+obs+'_'+bkg+'.root'
            f_bkg = ROOT.TFile(input_file_bkg,"READ")
            print input_file_bkg
            h_bkg = f_bkg.Get(obs)
            h_data.Add(h_bkg,-1)
            print "data distribution:",[h_data.GetBinContent(i+1) for i in xrange(6)]
    for i in xrange(Nx*Ny):
        # normalize matrix rows to correct for losses
        try:
            a_response[i]=h_response.GetBinContent(i/Nx+1,i%Ny+1)/h_gen[i%Ny+1]
        except ZeroDivisionError:
            a_response[i]=0
    for i in xrange(Nx):
        a_reco[i]        = h_reco.GetBinContent(i+1)
        a_gen[i]         = h_gen.GetBinContent(i+1)
        a_closure[i]     = h_closure.GetBinContent(i+1)
        a_data_e[i*Nx+i] = h_data.GetBinError(i+1)**2
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


def unfold_by_tunfold(args=None,obs='zpt',cut='_jet1pt20',data='amc',mc='toy',match='',dressed='', puid='',varquantity='',variation=0):
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
    print "edge distribution:",[h_edge[i+1]/h_gen[i+1] for i in xrange(264)]
    print "fake distribution:",[h_fake[i+1]/h_reco[i+1] for i in xrange(264)]
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
    #unfold = ROOT.TUnfoldDensity(h_response,1,
    #                ROOT.TUnfold.ERegMode(2),
    #                ROOT.TUnfold.EConstraint(0),
    #                ROOT.TUnfoldDensity.EDensityMode(0),
    #                0,0,"0","*[B]")
    unfold = ROOT.TUnfold(
            h_response,
            ROOT.TUnfold.kHistMapOutputHoriz,   # gen-level on x axis
            ROOT.TUnfold.kRegModeNone,          # no regularization
            ROOT.TUnfold.kEConstraintNone,      # no constraints
            )
    print unfold
    unfold.SetInput(h_data)
    unfold.DoUnfold(0)#0,h_data)
    h_unfold = h_data.Clone("unfolded"+obs)
    h_covariance = h_response.Clone("covariance")
    h_correlation = h_response.Clone("correlation")
    unfold.GetOutput(h_unfold)
    unfold.GetEmatrix(h_covariance)
    for j in xrange(Ny):
        for i in xrange(Nx):
            h_correlation.SetBinContent(i+1,j+1,h_covariance.GetBinContent(i+1,j+1)
                                                /np.sqrt(h_covariance.GetBinContent(i+1,i+1)*h_covariance.GetBinContent(j+1,j+1)))
    #h_covariance = unfold.GetEmatrixTotal("covariance")print "fake distribution:",[h_fake[i+1] for i in xrange(6)]
    print "unfold distribution:",[h_unfold[i+1] for i in xrange(6)]
    print [h_correlation.GetBinContent(i+1,1) for i in xrange(7)]
    f_out.cd()
    h_unfold.Write()
    h_covariance.Write()
    h_correlation.Write()
    h_reco.Write()
    h_gen.Write()
    h_data.Write("signal"+obs)
    print "unfolding results written to",output_file
    return


def uncloop(args=None):
    for cut in ['_jet1pt20']:
     for dressed in ['']:
      for varquantity in [  '_stats_mad','_stats_amc','_stats_hpp','_stats_pow',#'_stats_ptz',
                            '_stats_toy',
                            '_Robs','_Ryj','_Ryz','_F','_A','_switch',
                            '_IDSF','_IsoSF','_TriggerSF',
                            '_bkg','_lumi',
                            '_JEC',#'_JER',
                            '_statistical',
                            ]:
        for data in [   #'amc',
                        #'hpp',
                        #'mad',
                        'BCDEFGH'
                        ]:
          create_uncertainties(obs='zpt',       cut=cut,data=data,dressed=dressed,varquantity=varquantity)
          create_uncertainties(obs='phistareta',cut=cut,data=data,dressed=dressed,varquantity=varquantity)
    return


def create_uncertainties(args=None, obs='zpt', cut='_jet1pt20', data='BCDEFGH',match='',dressed='',puid='',varquantity='_total',N_toys=1000):
    var=varquantity
    output_file = plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+varquantity+'.root'
    print "write uncertainty to file",output_file
    if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        return
    f_out = ROOT.TFile(output_file,"RECREATE")
    if varquantity in ['_stats_toy','_stats_amc','_stats_mad','_stats_hpp','_stats_pow','_stats_ptz']:
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
                unfold_by_inversion(args,obs,cut,data,mc,match,dressed,puid,varquantity='_stats',variation=i+1)
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
    elif varquantity in ['_Robs','_Ryz','_Ryj','_A','_F','_switch']:
            create_toy3Dhist(args,obs,cut,'mad',match,dressed,puid,varquantity='',variation=0)
            unfold_by_inversion(args,obs,cut,data,'toy',match,dressed,puid)
            input_file = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_toy'+match+'.root'
            f_in      = ROOT.TFile(input_file,"READ")
            h_central = f_in.Get('unfolded'+obs)
            h_uncertainty = h_central.Clone('uncertainty'+var)
            h_uncertainty.Reset()
            create_toy3Dhist(args,obs,cut,'mad',match,dressed,puid,varquantity=var,variation=1)
            create_toy3Dhist(args,obs,cut,'mad',match,dressed,puid,varquantity=var,variation=-1)
            unfold_by_inversion(args,obs,cut,data,'toy',match,dressed,puid,varquantity=var,variation=1)
            unfold_by_inversion(args,obs,cut,data,'toy',match,dressed,puid,varquantity=var,variation=-1)
            input_file_up   = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_toy'+match+var+'Up.root'
            input_file_down = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_toy'+match+var+'Down.root'
            f_in_up   = ROOT.TFile(input_file_up,  "READ")
            f_in_down = ROOT.TFile(input_file_down,"READ")
            h_up      = f_in_up.Get('unfolded'+obs)
            h_down    = f_in_down.Get('unfolded'+obs)
            for i in xrange(h_uncertainty.GetNbinsX()):
                h_uncertainty.SetBinContent(i+1,np.sqrt(((h_central[i+1]-h_up[i+1])**2+(h_central[i+1]-h_down[i+1])**2)/2)/h_central[i+1])
                h_uncertainty.SetBinError(i+1,0)
            f_out.cd()
            h_uncertainty.Write()
            h_central.Write('unfolded'+obs+var)
    elif varquantity in ['_IDSF','_IsoSF','_TriggerSF','_JEC']:
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
        unfold_by_inversion(args,obs,cut,data,'mad',match,dressed,puid)
        input_file = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_mad'+match+'.root'
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
                    'unf' : ['_stats_toy'],
                    'jec' : ['_JEC'],
                    'mod' : ['_Robs','_Ryz','_Ryj','_A','_F','_switch'],
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


def plot_datamc(args=None, obs='zpt', cut='_jet1pt20', data='BCDEFGH', mc='amc',match='',dressed='',puid=''):
    data_source = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
    mc_source   = plots_folder+cut+dressed+puid+'/'+obs+'_'+mc+match+'.root'
    bkg_list = ['TTJets','WZ','ZZ','TW','WW']
    bkg_source  =[plots_folder+cut+dressed+puid+'/'+obs+'_'+bkg+match+'.root' for bkg in bkg_list]
    filelist = [data_source,mc_source]+bkg_source
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    plots=[]
    d0 = ({
        'files': filelist,
        'x_expressions': [obs],
        'folders': [''],
        'nicks': ['Data','DY']+bkg_list,
        'sum_nicks' : ['DY '+' '.join(bkg_list)],
        'analysis_modules': ['SumOfHistograms','Ratio'],
        'sum_result_nicks' : ['sim'],
        'ratio_numerator_nicks': ['Data'],
        'ratio_denominator_nicks': ['sim'],
        'ratio_result_nicks':['ratio'],
        'ratio_denominator_no_errors': False,
        'stacks':['data','mc']+len(bkg_list)*['mc']+['ratio'],
        'www': 'comparison_datamc'+cut+dressed+puid+'_'+data+'_vs_'+mc+match,
        'filename': obs,
        'x_errors': [1],
        'x_label': 'Bin',
        'y_log': True,
        'y_lims': [1e-2,1e5] if obs =='zpt' else [1e0,1e7],
        'nicks_blacklist': ['sim'],
        'y_subplot_label': 'Data/Sim',
        'y_subplot_lims': [0.75,1.25],
        #'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{6.2}}$",
    })
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = deepcopy(d0)
            d.update({
                'files': filelist_binned,
                'x_expressions': [obs+namestring],
                'www': 'comparison_datamc'+cut+dressed+puid+'_'+data+'_vs_'+mc+match+'/datamc'+namestring,
                'analysis_modules': ['SumOfHistograms','NormalizeByBinWidth','Ratio'],
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'y_label': 'Events per binsize',
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'x_log': True,
                'x_label': obs,
            })
            plots.append(d)
    d0['figsize'] = [36,6]
    plots.append(d0)
    return [PlottingJob(plots=plots, args=args)]


def plot_resolution(args=None, obs='phistareta', cut='_jet1pt20', mc='mad',match='',dressed='',puid='',trunc = '_985'):
    plots=[]
    folder = plots_folder+cut+dressed+puid+'/resolution'+trunc+'/'
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
       for cut in ['_jet1pt20']:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'files': [folder+obs+'_'+mc+match+namestring+'.root'],
                'www': 'resolutions'+cut+dressed+puid+'_'+mc+match+'/resolution'+trunc+namestring,
                'folders': [''],
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'x_log': True,
                'x_label': 'gen'+obs,
                'x_errors': [1],
                'markers': [''],
                'texts_x': [0.03,0.1,0.4,0.7],
                'texts_y': [0.97,1.18,1.18,1.18],
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'function_display_result': True,
            })
            #if (ybmin,ysmin) == (0.0,2.0):
            #    d['function_ranges'] = ['25,250'] if obs =='zpt' else ['0.4,5']
            d1 = deepcopy(d)
            d1.update({
                'x_expressions': ['rms','sigma0','sigma'],
                'filename': obs+'_resolution',
                'nicks': ['rms','gauss','cryb'],
                'labels': ['RMS','Gaussian Width','Crystal Ball Width'],
                'analysis_modules': ['FunctionPlot'],
                'function_fit': ['rms','gauss','cryb'],
                'functions': ['[0]+[1]*sqrt(x)+[2]/sqrt(x)'] if obs == 'zpt' else ['[0]+[1]*x+[2]/x'],
                'function_parameters': ['1,1,1'],
                'function_nicknames': ['fit_rms','fit_gauss','fit_cryb'],
                'function_fit_parameter_names': ['p_0','p_1','p_2'],
                'alphas': [0.707],
                'nicks_whitelist': ['fit',''],
                'colors': ['green','orange','violet','darkgreen','darkorange','darkviolet'],
            })
            if obs == 'zpt':
                d1['y_lims'] = [0,0.1]
                d1['y_label'] = r'Relative $p_T^Z$ resolution'
                d1['texts']   = [r'$f(x)=p_0+p_1\\sqrt{x}+p_2\\frac{1}{\\sqrt{x}}$']+d1['texts']
            
            if obs == 'phistareta':
                d1['y_lims'] = [0,0.005]
                d1['y_label'] = r'Relative $\\Phi^*_\\eta$ resolution'
                d1['texts']   = [r'$f(x)=p_0+p_1x+p_2\\frac{1}{x}$']+d1['texts']
            d1['texts_x'] = [0.05]+d1['texts_x']
            d1['texts_y'] = [0.9]+d1['texts_y']
            d2 = deepcopy(d1)
            d2.update({
                'files': [folder+'matchedjet1y_'+mc+match+namestring+'_bins_of_'+obs+'.root'],
                'filename': 'jet1y_resolution_bins_of_'+obs,
                'functions': ['[0]+[1]/sqrt(x)'] if obs == 'zpt' else ['[0]+[1]/x'],
                'texts_y':[0.97,1.14,1.14,1.14],
                'y_lims': [0,0.05],
                'y_label': r'$y^{jet1}$ resolution',
            })
            d2['texts_y'] = [0.9]+d2['texts_y']
            d2['texts'][0] = ([r'$f(x)=p_0+p_1\\frac{1}{\\sqrt{x}}$'] if obs =='zpt' else [r'$f(x)=p_0+p_1\\frac{1}{x}$'])
            d3 = deepcopy(d1)
            d3.update({
                'files': [folder+'zy_'+mc+match+namestring+'_bins_of_'+obs+'.root'],
                'filename': 'zy_resolution_bins_of_'+obs,
                'functions': ['[0]' if obs == 'zpt' else ['[0]+[1]*log(x)']],
                'y_lims': [0,0.01] if obs=='zpt' else [0,0.02],
                'texts_y':[0.97,1.11,1.11,1.11] if obs=='zpt' else [0.97,1.14,1.14,1.14],
                'y_label': r'$y^{Z}$ resolution',
            })
            d3['texts_y'] = [0.9]+d3['texts_y']
            d3['texts'][0] = ([r'$f(x)=const'] if obs =='zpt' else [r'$f(x)=p_0+p_1\\log(x)$'])
            
            d4 = deepcopy(d)
            d4.update({
                'x_expressions': ['PU','matched','switched'],
                'nicks': ['PU','matched','switched'],
                'analysis_modules':['ScaleHistograms','FunctionPlot'],
                'scale_nicks': ['PU','matched','switched'],
                'scales': [100],
                'function_fit': ['switched'],
                'functions': ['[0]*exp(-[1]*x)'] if obs == 'zpt' else ['[0]+[1]/x'],
                'function_parameters': ['10,0.001'],
                'function_nicknames': ['fit_switched'],
                'function_fit_parameter_names': ['p_0','p_1'],
                'markers': ['fill'],
                'filename': obs+'_fractions',
                'y_lims': [0,125],
                'y_label': 'Fraction / %',
                'stacks': 3*['fraction']+['fit'],
                'labels': ['PU','Matched','Switched'],
                'colors': ['grey','steelblue','orange','gold'],
                'lines': [100],
                'texts_x':[0.03,0.05],
                'texts_y':[0.97,1.14],
                'y_ticks': [0,10,20,30,40,50,60,70,80,90,100],
            })
            d5 = deepcopy(d)
            d5.update({
                'x_expressions': ['acceptance','fakerate'],#,'purity','stability'],
                'nicks': ['acceptance','fakerate'],#'purity','stability'],
                'scale_nicks': ['acceptance','fakerate'],#'purity','stability'],
                'analysis_modules':['ScaleHistograms','FunctionPlot'],
                'scales': [100],
                'filename': obs+'_rates',
                'y_lims': [0,118],
                'y_label': 'Fraction / %',
                'y_ticks': [0,10,20,30,40,50,60,70,80,90,100],
                'alphas': [0.5],
                'lines': [100],
                'texts_x':[0.03,0.05,0.55],
                'texts_y':[0.97,1.15,1.15],
                'labels': ['Acceptance','Fakerate'],
                'function_fit': ['acceptance','fakerate'],
                'functions': [('[0]-[1]/x' if obs == 'zpt' else '[0]-[1]/x**2'),'[0]+[1]/x**3'],
                'function_parameters': ['100,1','100,1'],
                'function_nicknames': ['fit_acceptance','fit_fakerate'],
                'colors': ['coral','slategray','lightcoral','lightslategray']
            })
            d5['texts_x'] = [0.4,0.42]+d5['texts_x']
            d5['texts_y'] = [0.97,0.92]+d5['texts_y']
            d5['texts'][0] = [r'$f_{Acceptance}(x)=p_0-p_1\\frac{1}{x'+('' if obs=='zpt' else '^2')+'}$',r'$f_{Fakerate}(x)=p_0+p_1\\frac{1}{x^3}$']+d5['texts']
            plots.append(d1)
            plots.append(d2)
            plots.append(d3)
            plots.append(d4)
            plots.append(d5)
    return [PlottingJob(plots=plots, args=args)]


def plot_unfolding_closure(args=None, obs='zpt', cut='_jet1pt20', data='BCDEFGH', mc='toy',match='',dressed='',puid=''):
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    unfold_by_inversion(args,obs,cut,'pow',mc,match,dressed,puid)
    unfold_by_inversion(args,obs,cut,'amc',mc,match,dressed,puid)
    unfold_by_inversion(args,obs,cut,'hpp',mc,match,dressed,puid)
    unfold_by_inversion(args,obs,cut,'mad',mc,match,dressed,puid)
    #unfold_by_tunfold(args,obs,cut,'pow',mc,match,dressed,puid)
    #unfold_by_tunfold(args,obs,cut,'amc',mc,match,dressed,puid)
    #unfold_by_tunfold(args,obs,cut,'hpp',mc,match,dressed,puid)
    #unfold_by_tunfold(args,obs,cut,'mad',mc,match,dressed,puid)
    
    signal_source1 = plots_folder+cut+dressed+puid+'/'+obs+'_pow'+match+'.root'
    signal_source2 = plots_folder+cut+dressed+puid+'/'+obs+'_amc'+match+'.root'
    signal_source3 = plots_folder+cut+dressed+puid+'/'+obs+'_hpp'+match+'.root'
    signal_source4 = plots_folder+cut+dressed+puid+'/'+obs+'_mad'+match+'.root'
    unfold_source1 = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_pow_by_'+mc+match+'.root'
    unfold_source2 = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_amc_by_'+mc+match+'.root'
    unfold_source3 = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_hpp_by_'+mc+match+'.root'
    unfold_source4 = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_mad_by_'+mc+match+'.root'
    unc_source     = plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+'_stats_'+mc+'.root'
    varlist = ['Robs','Ryj','Ryz','F','A','switch']
    #varlist = ['Ryj']#,'switch'
    filelist = [signal_source1,unfold_source1,
                signal_source2,unfold_source2,
                signal_source3,unfold_source3,
                signal_source4,unfold_source4,
                unc_source]+[
                plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+'_'+var+'.root' for var in varlist]
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    plots=[]
    d0 = ({
        'files': filelist,
        'x_expressions': 4*['gen'+obs,'unfolded'+obs]+['uncertainty_stats_'+mc]+['uncertainty_'+x for x in varlist],
        'folders': [''],
        'nicks': ['powgen','powunf','amcgen','amcunf','hppgen','hppunf','madgen','madunf','unc_mc']+['unc_'+x for x in varlist],
        'analysis_modules': ['QuadraticSumOfHistograms','Ratio','SumOfHistograms'],#,'MultiplyHistograms'
        'quad_sum_nicks': ['unc_'+' unc_'.join(varlist)],
        'quad_sum_result_nicks': ['unc_toy'],
        'ratio_numerator_nicks': ['unc_mc','powunf','amcunf','hppunf','madunf'],
        'ratio_denominator_nicks': ['unc_mc','powgen','amcgen','hppgen','madgen'],
        'ratio_result_nicks': ['unity','ratio_pow','ratio_amc','ratio_hpp','ratio_mad'],
        'sum_nicks' : ['unity unc_mc','unity unc_mc','unity unc_toy','unity unc_toy'],
        'sum_scale_factors' : ['1 1', '1 -1','1 1', '1 -1'],
        'sum_result_nicks': ['mc_up','mc_down','toy_up','toy_down'],
        'labels': ["Powheg","Powheg","","aMC@NLO","aMC@NLO","","Herwig++","Herwig++","","Madgraph","Madgraph","","Toy Syst. Unc.","","Toy Stat. Unc.",""],
        'subplot_legend': 'lower left',
        'subplot_fraction': 45,
        'subplot_nicks': ['up','down','ratio'], 
        'y_subplot_label': 'Unfolded/Gen',
        'www': 'comparison_unfolding_samples'+cut+dressed+puid+'_'+data+'_by_'+mc+match,
        'filename': obs,
        'x_label': 'Bin',
        'x_errors': 4*[1,0,0]+4*[0],
        'y_log': True,
        'y_errors': 12*[True]+4*[False],
        'step': 12*[False]+2*[True]+2*[False],
        'line_styles': 12*['']+2*['-']+2*[''],
        'markers': ['.','p','p','.','s','s','.','D','D','.','o','o']+['']*2+['fill']*2,
        'nicks_whitelist': ['pow','amc','hpp','mad','toy','mc'],
        'nicks_blacklist': ['unity','unc'],
        'colors': ['darkorange','orange','orange','darkred','red','red','darkblue','blue','blue','darkgreen','green','green','black','black','yellow','white'],
        'y_subplot_lims': [0.8,1.2],
    })
    if mc=='amc':
        d0['labels'].insert(9,"aMC@NLO Stat. Unc.")
    elif mc=='hpp':
        d0['labels'].insert(9,"Herwig++ Stat. Unc.")
    elif mc=='mad':
        d0['labels'].insert(9,"Madgraph Stat. Unc.")
    elif mc=='pow':
        d0['labels'].insert(9,"Powheg Stat. Unc.")
    if not mc=='toy':
        d0['nicks_blacklist']+=['toy']
        d0['labels'].pop(10)
        d0['labels'].insert(10," ")
        d0.update({
            'colors': ['darkred','red','red','darkblue','blue','blue','darkgreen','green','green','yellow','white'],
            'step': [False],
            'line_styles': [''],
            'markers': ['.','s','s','.','D','D','.','o','o']+['fill']*2,
            'subplot_legend': 'upper left',
        })
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = deepcopy(d0)
            d.update({
                'files': filelist_binned,
                'x_expressions': 4*['gen'+obs+namestring,'unfolded'+obs+namestring]+['uncertainty_stats_'+mc+namestring]+['uncertainty_'+x+namestring for x in varlist],
                'www': 'comparison_unfolding_samples'+cut+dressed+puid+'_'+data+'_by_'+mc+match+'/unfolded'+namestring,
                'x_label': obs,
                'x_log': True,
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
            })
            plots.append(d)
    d0['figsize'] = [36,6]
    d0['vertical_lines'] = l_obsbinedges
    d0['vertical_lines_styles'] = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    plots.append(d0)
    return [PlottingJob(plots=plots, args=args)]


def plot_uncertainty(args=None, obs='zpt', cut='_jet1pt20', data='BCDEFGH', mc='toy', match='',dressed='',puid=''):
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    if not data == 'BCDEFGH':
        print "WARNING: uncertainties are meant for data only!"
        return
    varlist = ['statistical','stats_'+mc,'lumi','bkg','IDSF','IsoSF','TriggerSF','JEC','Robs','Ryj','Ryz','F','A','switch']#
    filelist = [plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+data+match+'_'+var+'.root' for var in varlist]
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    plots = []
    d0 = ({
        'files': filelist,
        'folders': [''],
        'nicks': varlist,
        'x_expressions': ['uncertainty_'+var for var in varlist],
        'analysis_modules': ['QuadraticSumOfHistograms'],
        'quad_sum_nicks': ['IDSF IsoSF TriggerSF','Robs Ryz Ryj F A switch','eff toy lumi bkg JEC stats_'+mc],#
        'quad_sum_result_nicks': ['eff','toy','total'],
        'filename': obs,
        'nicks_whitelist': ['statistical','total','lumi','bkg','eff','stats_'+mc,'JEC','toy'],
        'labels': ['Statistical','Total systematic','Lumi','Background','ID/Trigger','Unfolding statistical','JEC','Unfolding modelling'],
        'alphas': [0.5],
        'y_errors': False,
        'y_lims': [0,0.2],
        'y_label': "Relative Uncertainty",
        'www': 'comparison_uncertainties'+cut+dressed+puid+'_'+data+'_by_'+mc+match,
        'step': [True],
        'line_styles': ['-'],
        'markers': ['fill','o','v','^','>','<','s','D'],
        'x_label': 'Bin',
    })
    if not mc == 'toy':
        d0['nicks_whitelist'] = ['statistical','total','lumi','bkg','eff','JEC'],#'stats_'+mc,
        d0['labels'] = ['Statistical','Total systematic','Lumi','Background','ID/Trigger','Unfolding statistical','JEC'],
        d0['quad_sum_nicks'][-1] = 'eff lumi bkg stats_'+mc+' JEC'
        d0['markers'] = ['fill','o','v','^','>','<','s'],
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = deepcopy(d0)
            d.update({
                'files': filelist_binned,
                'x_expressions': ['uncertainty_'+var+namestring for var in varlist],
                'x_log': True,
                'www': 'comparison_uncertainties'+cut+dressed+puid+'_'+data+'_by_'+mc+match+'/uncertainties'+namestring,
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'x_label': obs,
            })
            plots.append(d)
    d0['figsize'] = [36,6]
    d0['vertical_lines'] = l_obsbinedges
    d0['vertical_lines_styles'] = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    d0['legend'] = 'upper left'
    plots.append(d0)
    return [PlottingJob(plots=plots, args=args)]


def plot_unfolding_correction(args=None, obs='zpt', cut='_jet1pt20', data='mad', mc='toy', match='',dressed='',puid=''):
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    unfold_by_inversion(args,obs,cut,data,mc,match,dressed,puid)
    unf_source  = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    data_source = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
    filelist = [unf_source,data_source]
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    plots = []
    d0 = ({
        'files': filelist[0],
        'folders': [''],
        'nicks': ['unf','sig'],
        'x_expressions': ['unfolded'+obs,'signal'+obs],
        'analysis_modules': ['Ratio'],
        'ratio_denominator_no_errors': False,
        'y_subplot_label': 'Ratio',
        'subplot_fraction': 40,
        'filename': obs,
        'x_label': obs,
        'x_errors': [1],
        'subplot_legend': 'lower left',
        'y_log': True,
        'y_subplot_lims': [0.5,1.5],
        'www': 'comparison_unfold'+cut+match+puid+dressed+'_'+data+'_by_'+mc,
        'labels': ['Unfolded','Signal','Unfolded/Signal'],
        'markers': ['.'],
    })
    if not data in ['BCD','BCDEFGH']:
        d0.update({
            'files': filelist,
            'nicks': ['unf','gen','sig','reco'],
            'x_expressions': ['unfolded'+obs,'gen'+obs,'signal'+obs,obs],
            'ratio_numerator_nicks': ['unf','gen'],
            'ratio_denominator_nicks': ['sig','reco'],
            'colors': ['black','blue','red','green','blue','red'],
            'labels': ['Unfolded','Gen','Signal','Reco','Unfolded/Signal','Gen/Reco'],
        })
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = deepcopy(d0)
            d.update({
                'files': filelist_binned[0],
                'x_expressions': ['unfolded'+obs+namestring,'signal'+obs+namestring],
                'x_log': True,
                'x_ticks': [30,50,100,200,400,1000],
                'y_label': 'Events per binsize',
                'analysis_modules': ['NormalizeByBinWidth','Ratio'],
                'www': 'comparison_unfold'+cut+match+puid+dressed+'_'+data+'_by_'+mc+'/unfold'+namestring,
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
            })
            if not data in ['BCD','BCDEFGH']:
              d.update({
                'files': filelist_binned,
                'x_expressions': ['unfolded'+obs+namestring,'gen'+obs+namestring,'signal'+obs+namestring,obs+namestring],
              })
            plots.append(d)
    d0['figsize'] = [36,6]
    d0['vertical_lines'] = l_obsbinedges
    d0['vertical_lines_styles'] = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    plots.append(d0)
    return [PlottingJob(plots=plots, args=args)]

def plot_crossections(args=None,obs='zpt',cut='_jet1pt20',data='BCDEFGH',mc='NNLO',match='',dressed='',puid=''):
    unfold_by_inversion(args,obs,cut,data,'amc',match,dressed,puid)
    
    data_source = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_mad'+match+'.root'
    mc_source   = plots_folder+cut+dressed+puid+'/'+obs+'_'+mc+'.root'
    unc_source  = plots_folder+cut+dressed+puid+'/uncertainty/'+obs+'_'+'BCDEFGH'+match+'_total.root'

    filelist = [mc_source,data_source,unc_source]
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    ybins = [0.0,0.5,1.0,1.5,2.0,2.5]
    ylist = [((xb,yb),(xs,ys))  for (xs,ys) in zip(ybins[:-1],ybins[1:]) for (xb,yb) in zip(ybins[:-1],ybins[1:]) if xb+xs<2.5]
    scaling = [1e20,1e19,1e18,1e17,1e16,1e13,1e12,1e11,1e10,1e7,1e6,1e5,1e2,1e1,1e0]
    #scaling = [1e6,1e5,1e4,1e3,1e0,1e6,1e5,1e4,1e1,1e6,1e5,1e2,1e3,1e3,1e0]
    plots=[]
    namelist = ['_yb{}_ys{}'.format(int(2*yboost[0]),int(2*ystar[0])) for (yboost,ystar) in ylist]
    #namelist = [' _yb{}_ys{}'.format(int(2*ylist[i][0][0]),int(2*ylist[i][1][0])) for i in xrange(len(ylist))]
    d1 = ({
        'files': [filelist_binned[0]]*len(ylist)+[filelist_binned[1]]*len(ylist),
        'folders': [''],
        'x_expressions':  ['gen'+obs+x for x in namelist]
                    +['unfolded'+obs+x for x in namelist],
        'nicks':       ['gen'+x for x in namelist]+['unf'+x for x in namelist],
        'scale_nicks': ['gen'+x for x in namelist]+['unf'+x for x in namelist],
        'scales': [1e0/35.9/1000*s for s in scaling],
        'analysis_modules': ['NormalizeByBinWidth','ScaleHistograms'],
        'x_log': True,
        'x_errors': [1]*len(ylist)+[0]*len(ylist),
        'y_log': True,
        'y_errors': [False]*len(ylist)+[True]*len(ylist),
        'markers': ['']*len(ylist)+['^','1','p','+','*','<','2','o','x','>','3','s','v','4','d'],
        'colors': ['dimgrey']*len(ylist)+
                    [color for color in ['red','salmon','crimson','violet','brown','blue','cyan','royalblue','teal','orange','gold','yellow','green','lime','purple']],
        'y_lims':[1e-6,1e21] if obs == 'zpt' else [1e-4,1e23],
        'filename': obs,
        'x_label': obs,
        'labels': ['Theory ('+mc+')']*len(ylist)+['Unfolded data']*len(ylist),
        'www': 'crossections_'+data+'_'+mc+cut+dressed+puid,
        #'marker_fill_styles':['none'],
        #'hatch': ['+'],
        'legend': None,
        #'legen_cols': 2,
        'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
    })
    if obs == 'zpt':
        d1['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\mathit{p}_T^Z d\\mathit{y_b} d\\mathit{y^*}}/(\\frac{p\\mathit{b}}{GeV})$'
    elif obs == 'phistareta':
        d1['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\Phi^{*}_{\\eta} d\\mathit{y_b} d\\mathit{y^*}}/p\\mathit{b}$'
    plots.append(d1)
    
    d2 = deepcopy(d1)
    d2['analysis_modules'] = ['Ratio','AddHistograms']
    d2['files'] += [filelist_binned[2]]*len(ylist)
    d2['x_expressions'] += ['uncertainty_total'+x for x in namelist]
    d2['nicks']         += ['unc'+x for x in namelist]
    d2.update({
        'ratio_numerator_nicks':  ['unf'+x for x in namelist]+['unc'+x for x in namelist],
        'ratio_denominator_nicks':['gen'+x for x in namelist]+['unc'+x for x in namelist],
        'ratio_result_nicks':     ['ratio'+x for x in namelist]+['unity'+x for x in namelist],
        'add_nicks':             ['unity'+x+' ratio'+x for x in namelist]
                                +['unity'+x+' unc'+x for x in namelist]
                                +['unity'+x+' unc'+x for x in namelist],
        'add_scale_factors': [str(len(ylist)-x-1)+' 1' for x in xrange(len(ylist))]
                            +[str(len(ylist)-x)+' 1' for x in xrange(len(ylist))]
                            +[str(len(ylist)-x)+' -1' for x in xrange(len(ylist))],
        'add_result_nicks': ['stacked'+x for x in namelist]+['up'+x for x in namelist]+['down'+x for x in namelist],
        'nicks_whitelist': [('stacked'+x,'up'+x,'down'+x) for x in namelist],
        'subplot_nicks': ['_dummy'],
        'markers': [(x,'fill','fill') for x in ['^','1','p','+','*','<','2','o','x','>','3','s','v','4','d']],
        'colors': [(color,'silver','white') for color in ['red','salmon','crimson','violet','brown','blue','cyan','royalblue','teal','orange','gold','yellow','green','lime','purple']],
        'y_lims': [0.5,15.5],
        'x_errors': [0],
        'y_ticks': [0],
        'y_log': False,
        'y_errors': True,
        'figsize': [6,12],
        'lines': [(0.5+x,0.75+x,1.25+x) for x in xrange(3*len(ylist))],
        'lines_styles': ['-',':',':'],
        'filename': obs+'_ratio',
        'y_label': 'Unfolded data / Theory ('+mc+')',
        'legend': None,
    })
    plots.append(d2)
    return [PlottingJob(plots=plots, args=args)]

def write_results_to_txt(args=None,obs='phistareta',cut='_jet1pt20',data='BCDEFGH',mc='mad',match='',dressed='_FSR01',puid=''):
    unfold_by_inversion(args,obs,cut,data,mc,match,dressed,puid)
    create_uncertainties(args,obs,cut,data,match,dressed,puid,varquantity='_total')
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


def write_to_root(args=None,obs='zpt',cut='_jet1pt20',match='',dressed='',puid='',order='NNLO',pdf=''):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args,obs)
    [l_obshists, h_reco, h_gen, h_recoresponse, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args, obs)
    ybins = [0.0,0.5,1.0,1.5,2.0,2.5]
    ylist = [((xb,yb),(xs,ys))  for (xs,ys) in zip(ybins[:-1],ybins[1:]) for (xb,yb) in zip(ybins[:-1],ybins[1:]) if xb+xs<2.5]
    dpdf = ({  '_CT14nlo': '0', '_MMHT2014nlo68cl': '1', '_NNPDF30_nlo_as_0118': '2', '_PDF4LHC15_nlo_mc': '3'})
    dorder = ({'LO': '1', 'NLO': '2', 'NNLO': '0'})
    for ((xb,yb),(xs,ys)) in ylist:
        #input_file = "/portal/ekpbms1/home/tberger/PDFfits/xfitter-2.0.0/datafiles/lhc/cms/zjet/ZJtriple/theory_files/ZJ.NNLO.ZJtriple_yb{}_ystar{}_ptz.root".format(int(2*xb),int(2*xs))
        input_file = "/portal/ekpbms1/home/tberger/PDFfits/xfitter-2.0.0/datafiles/lhc/cms/zjet/ZJtriple/theory_files/ZJ.NNLO.ZJtriple_yb{}_ystar{}_ptz_NNPDF31_nnlo_as_0118.root".format(int(2*xb),int(2*xs))
        f_in = ROOT.TFile(input_file,"READ")
        #central_name = "h"+dorder[order]+"1001"+dpdf[pdf]+"0"
        #up_name      = "h"+dorder[order]+"1001"+dpdf[pdf]+"8"
        #down_name    = "h"+dorder[order]+"1001"+dpdf[pdf]+"9"
        central_name = "h3100100"
        up_name      = "h3100108"
        down_name    = "h3100109"
        h_central = f_in.Get(central_name)
        h_up      = f_in.Get(up_name)
        h_down    = f_in.Get(down_name)
        y_index = l_ybinedges[int(2*xs)]+int(2*xb)
        for j in xrange(h_central.GetNbinsX()):
            obs_index = l_obsbinedges[y_index]+j+1
            print obs_index
            h_gen.SetBinContent(obs_index,h_central[j+1]*35.9*1000*h_central.GetBinWidth(j+1))
            h_gen.SetBinError(obs_index,h_gen[obs_index]*max(abs(h_up[j+1]),abs(h_down[j+1])))
    output_file = plots_folder+cut+dressed+puid+'/'+obs+'_'+order+match+pdf+'.root'
    print "file written to",output_file
    f_out = ROOT.TFile(output_file,"RECREATE")
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


def plot_variations(args=None, obs='zpt', cut='_jet1pt20', data='amc', mc='toy', match='',dressed='',puid=''):
    #central_source = plots_folder+cut+dressed+puid+'/'+obs+'_'+data+match+'.root'
    central_source = plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    varlist = ['Robs','Ryj','Ryz','F','A','switch']
    plots=[]
    for var in varlist:
        #filelist = [central_source]+[plots_folder+cut+dressed+puid+'/variations/'+obs+'_'+data+match+'_'+var+x+'.root' for x in ['Up','Down']]
        filelist = [central_source]+[plots_folder+cut+dressed+puid+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'_'+var+x+'.root' for x in ['Up','Down']]
        filelist_binned = []
        for x in filelist:
            invert_3Dhists(args,x)
            filelist_binned.append(x.replace('.root','_binned.root'))
        for ybmin in [0.0,0.5,1.0,1.5,2.0]:
          for ysmin in [0.0,0.5,1.0,1.5,2.0]:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'files': [filelist_binned],
                'nicks': ['central','up','down'],
                'folders': [''],
                'x_expressions': ['unfolded'+obs+namestring],
                #'x_expressions': [obs+namestring] if not var=='F' else ['gen'+obs+namestring],
                'www': 'comparison_variations'+cut+'_'+data+'_by_'+mc+dressed+puid+match+'/variations'+namestring,
                'y_log': True,
                'x_log': True,
                'x_label': obs,
                'x_errors': [1],
                'x_ticks': [30,50,100,1000],
                'filename': obs+'_'+var,
                'analysis_modules': ['Ratio'],
                'ratio_numerator_nicks': ['up','down'],
                'ratio_denominator_nicks': ['central'],
                'ratio_denominator_no_errors': False,
                'markers': ['o','^','v','^','v'],
                'colors': ['black','darkorange','darkgreen','darkorange','darkgreen'],
                'y_subplot_lims': [0.985,1.015],
                'y_subplot_label': 'Ratio to central',
            })
            if not ybmin+ysmin>2:
                plots.append(d)
    return [PlottingJob(plots=plots, args=args)]


def plot_3Dresponse(args=None,obs='zpt',cut='_jet1pt20',data='',mc='toy',match='',dressed='',puid=''):
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    mc_source   = plots_folder+cut+dressed+puid+'/'+obs+'_'+mc+match+'.root'
    plots=[]
    lines_list = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    samples = ['toy','pow','amc']#,'hpp','mad']
    data_source = ([plots_folder+cut+dressed+puid+'/'+obs+'_'+x+match+'.root' for x in ['toy']]
        +[  plots_folder+cut+dressed+puid+'/variations/'+obs+'_toy'+match+'_switchDown.root',
            plots_folder+cut+dressed+puid+'/variations/'+obs+'_toy'+match+'_switchUp.root'])
    d1 = ({
        'files': data_source,
        'nicks': ['reco'+x for x in samples]+['gen'+x for x in samples],
        'folders': [''],
        'x_expressions': len(samples)*[''+obs]+len(samples)*['gen'+obs],
        'www': 'response3D'+cut,
        'y_log': True,
        'x_label': 'Bin',
        'filename': obs,
        'labels': ['Toy','Powheg','aMC@NLO','Herwig++','Madgraph'],
        'analysis_modules': ['Ratio'],
        'ratio_numerator_nicks': ['reco'+x for x in samples],
        'ratio_denominator_nicks': ['gen'+x for x in samples],
        #'ratio_denominator_no_errors': False,
        'x_errors': len(samples)*[0]+2*len(samples)*[1],
        'y_errors': len(samples)*[1]+len(samples)*[0]+len(samples)*[1],
        'markers': ['x','1','2','3','4']+2*len(samples)*[''],
        'figsize': [36,6],
        'vertical_lines': l_obsbinedges,
        'vertical_lines_styles': lines_list,
        'colors': ['grey','orange','red','blue','green','darkgrey','darkorange','darkred','darkblue','darkgreen','black','orange','red','blue','green'],
        'subplot_fraction': 40,
        'y_subplot_lims': [0.5,1.5],
        #'y_subplot_lims': [0.8,1.0],
        #'y_subplot_label': 'Ratio to central',
    })
    plots.append(d1)
    d2 = ({
        'files': [mc_source],
        'folders': [''],
        'x_expressions': ['response'],
        'x_ticks': [],
        'y_label': 'gen'+obs,
        'x_label': obs,
        'y_ticks': [],
        'z_log':True,
        'z_lims':[1e-3,1e0],
        'z_label': 'Fraction of events',
        #'analysis_modules': ['NormalizeColumnsToUnity'],
        'analysis_modules': ['NormalizeRowsToUnity',],
        'colormap': 'summer_r',
        'www': 'response3D'+cut,
        'filename': obs+'_response',
        'lines': l_obsbinedges,
        'vertical_lines': l_obsbinedges,
        'lines_styles': lines_list,
        'vertical_lines_styles': lines_list,
    })
    plots.append(d2)
    d3 = ({
        'files': [mc_source],
        'nicks': ['R'+obs,'Ryz','Ryj'],
        'folders': [''],
        'x_expressions': [obs+'res','zyres','jet1yres'],
        'www': 'response3D'+cut,
        'x_label': 'Bin',
        'y_lims':[0,0.1],# if obs=='zpt' else [0,0.03],
        #'y_log': True,
        'markers': ['1','2','3'],
        'colors': ['green','orange','purple'],
        'filename': obs+'_resolutions',
        'figsize': [36,6],
        'vertical_lines': l_obsbinedges,
        'vertical_lines_styles': lines_list,
    })
    plots.append(d3)
    d4 = deepcopy(d3)
    d4.update({
        'nicks': ['F','A','switch'],
        'x_expressions': [obs+'F',obs+'A',obs+'switch'],
        #'y_lims':[0.6,1.0],# if obs=='zpt' else [0.8,1.0],
        'y_lims':[0,0.5],
        'markers': ['4','x',''],
        'colors': ['black','red','blue'],
        'filename': obs+'_rates',
    })
    plots.append(d4)
    return [PlottingJob(plots=plots, args=args)]


def create_gendistributions(args=None, obs='jet1y', cut='_jet1pt20', mc='mad',match='',dressed='',puid=''):
    plots=[]
    output_file = plots_folder+cut+dressed+puid+'/gen'+obs+'_'+mc+'.root'
    if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        return
    d = ({
        'files': [datasets[mc]],
        'folders': ['genzjetcuts_L1L2L3/ntuple'],
        'nicks':['gen'+obs],
        'x_expressions': [obs],
        'filename': output_file.replace('.root',''),
        'x_log': True,
        'plot_modules': ['ExportRoot'],
        'output_dir': '/',
        'weights': ['(abs(genmupluseta)<2.4)&&(abs(genmuminuseta)<2.4)&&(genmupluspt>25)&&(genmuminuspt>25)&&(abs(genzmass-91.1876)<20)'],
    })
    if cut=='_jet1pt20':
        d['weights'] = ['(genjet1pt>20)&&'+x for x in d['weights']]
    else:
        print "cuts not known"
    if obs == 'zpt':
        d['x_bins'] = ' '.join(['{}'.format(x) for x in np.logspace(1,np.log(1000)/np.log(25),100,True,25)])
    elif obs == 'phistareta':
        d['x_bins'] = ' '.join(['{}'.format(x) for x in np.logspace(1,np.log(50)/np.log(0.4),100,True,0.4)])
    elif obs in ['zy','jet1y']:
        d['x_bins'] = ['96,-2.4,2.4']
    else:
        d['x_bins'] = obs
    plots.append(d)
    return [PlottingJob(plots=plots, args=args)]


