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

CMSLABEL = False
DATASETS = generate_datasets(args=None)
#YLIMS = generate_ylims(args=None)
VARIATIONSTRING = generate_variationstring(args=None)
#PLOTSFOLDER = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple_2019-06-18'
#PLOTSFOLDER = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple_2019-06-30'
#PLOTSFOLDER = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple_2019-08-02'
#PLOTSFOLDER = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple_2019-09-05'
PLOTSFOLDER = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple_2019-09-12'
MCLIST = ['amc','hpp','mad',]
LABELDICT = ({  'pow':"Powheg",'amc':"P8+aMC",'hpp':"HW+MG",'mad':"P8+MG",
                'toy':"Toy     ",
                #'toy0':"Toy from P8+MG",'toy1':"Toy from P8+aMC",'toy2':"Toy from HW+MG",'toy3':"Toy (10M events)"
                'toy0':"P8+MG",'toy1':"P8+aMC",'toy2':"HW+MG",'toy3':"10M events",
                'LO': 'LO', 'NLO': 'NLO', 'NNLO': 'NNLO',
                })
MARKERDICT = ({'pow':'p','amc':'s','hpp':'D','mad':'o','toy':'d','toy0':'^','toy1':'<','toy2':'>','toy3':'v','LO':'^','NLO':'s','NNLO':'o'})
COLORDICT = ({'pow':'orange','amc':'red','hpp':'blue','mad':'green','toy':'grey', 'toy0':'seagreen', 'toy1':'salmon', 'toy2': 'orchid','toy3':'gray','LO':'green','NLO':'blue','NNLO':'red'})

def prepare_3Dhist(args=None, obs='zpt'):
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

def invert_3Dhists(args=None, filename = ''):
#def invert_3Dhists(args=None, filename = '/portal/ekpbms2/home/tberger/Excalibur/CMSSW_7_4_7/src/Excalibur/ZJtriple/ZJtriple_2019-09-12_jet1pt20/theory/phistareta_LO_NNPDF31_nnlo_as_0118.root'):
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
                    ##################################################################################################################################################
                    # skip bin number 10 to compensate the missing bin in phistareta tables:
                    if (hist_index+1 not in [5,9,12,13,14,15] and obs=='phistareta'):
                        hist_bin = hist_bin.Rebin(17,"new",array('d',[0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0, 50.0]))
                        if 'uncertainty' in filename:
                            hist_bin.SetBinContent(11,hist_bin.GetBinContent(11)/2)
                        if 'theory' in filename:
                            hist_bin.SetBinError(11,hist_bin.GetBinError(11)*np.sqrt(8))
                        if 'subprocess' in filename:
                            hist_bin.SetBinContent(11,hist_bin.GetBinContent(11)/2)
                    ##################################################################################################################################################
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
    print "histograms written to",output_file


def create_3Dhist(args=None, obs='zpt', cut='_jet1pt20', data='test', match='',  postfix='', varquantity='', variation=0):
    if data == 'toy':
        print "toy mc not created by this function."
        return
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args, obs, cut, data, data, yboostbin=None, ystarbin=None)
    [l_obshists, h_reco, h_gen, h_recoresponse, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args, obs)
    # simulations are always scaled to match data comparison (weight, lumi)
    if data in ['BCDEFGH','BCD','GH','17Jul2018']:
        lumi = 1
        match = ''
    else:
        lumi = d['lumis'][0]
    h_genresponse = deepcopy(h_recoresponse)
    h_gen2  = deepcopy(h_gen)
    h_reco2 = deepcopy(h_reco)
    if varquantity == '_JEC':
        input_file = DATASETS[data].replace('.root',postfix+varquantity+VARIATIONSTRING[variation]+'.root')
    elif varquantity in ['_JER','_MuScale']:
        input_file = DATASETS[data].replace('.root',postfix+varquantity+'.root')
    else:
        input_file = DATASETS[data].replace('.root',postfix+'.root')
    f_in = ROOT.TFile(input_file,"READ")
    print "Create histograms from file",input_file
    output_file = PLOTSFOLDER+cut+postfix+'/'+obs+"_"+data+match+".root"
    if not varquantity in ['_IDSF','_IsoSF','_TriggerSF','_JEC']:
        variation = 0
    if varquantity in ['_JER','_MuScale','_PUrho','_PUnpumean','_PUnpv'] or not variation == 0:
        if not os.path.exists(PLOTSFOLDER+cut+postfix+'/variations'):
            print "WARNING: variations folder",PLOTSFOLDER+cut+postfix+'/variations',"does not exist!"
            return
        else:
            output_file = PLOTSFOLDER+cut+postfix+'/variations/'+obs+"_"+data+match+varquantity+VARIATIONSTRING[variation]+".root"
    print "Response will be written to", output_file
    if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        return
    ntuple_gen, ntuple_reco = f_in.Get("genzjetcuts_L1L2L3/ntuple"), f_in.Get("zjetcuts_L1L2L3/ntuple")
    if data in ['BCDEFGH','BCD','GH','17Jul2018']:
        ntuple_reco = f_in.Get("zjetcuts_L1L2L3Res/ntuple")
    f_out = ROOT.TFile(output_file,"RECREATE")
    print 'Fill 3D reco histogram'
    obsmin, obsmax = l_obshists[0].GetXaxis().GetXbins()[0],l_obshists[0].GetXaxis().GetXbins()[l_obshists[0].GetNbinsX()]
    if '_PU' in varquantity:
        puobs = varquantity.split('PU')[-1]
        #pufile = PLOTSFOLDER+cut+postfix+'/gendistributions/pileupweight_'+puobs+'_'+data+'.root'
        pufile = PLOTSFOLDER+cut+postfix+'/gendistributions/pileupweight_'+puobs+'_mad.root'
        f_pu = ROOT.TFile(pufile,"READ")
        h_pu = f_pu.Get("pileupweight")
    for entry in ntuple_reco:
        weight = entry.weight
        if '_PU' in varquantity:
          puWeight = 1.0
          if puobs=='npumean':
            puWeight = h_pu.GetBinContent(h_pu.FindBin(entry.npumean))
            #print entry.npumean, puWeight
          elif puobs=='npv':
            puWeight = h_pu.GetBinContent(h_pu.FindBin(entry.npv))
          elif puobs=='rho':
            puWeight = h_pu.GetBinContent(h_pu.FindBin(entry.rho))
          if data in ['BCDEFGH','BCD','GH','17Jul2018']:
            weight = weight/(puWeight if not puWeight==0 else 1)
          else:
            weight = weight*puWeight/entry.puWeight
        zy,jet1y,event = entry.zy,entry.jet1y,entry.event
        recocutweight = ( (entry.mupluspt >25) & (abs(entry.mupluseta) <2.4)
                        & (entry.muminuspt>25) & (abs(entry.muminuseta)<2.4)
                        & (abs(entry.zmass-91.1876)<20) )
        genzy,genjet1y = ( (entry.genzy, entry.genjet1y) if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else (zy,jet1y))
        gencutweight = (  (entry.genmupluspt >25) & (abs(entry.genmupluseta) <2.4)
                        & (entry.genmuminuspt>25) & (abs(entry.genmuminuseta)<2.4)
                        & (abs(entry.genzmass-91.1876)<20) 
                        if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else recocutweight)
        jet1pt = entry.jet1pt
        genjet1pt = (entry.genjet1pt if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else jet1pt)
        yb,ys = 0.5*abs(zy+jet1y),0.5*abs(zy-jet1y)
        genyb,genys = 0.5*abs(genzy+genjet1y),0.5*abs(genzy-genjet1y)
        if 'jet1pt20' in cut.split('_'):
            gencutweight  &= ((genjet1pt>20) if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else 1)
            recocutweight &= (jet1pt>20)
        if 'jet1pt15' in cut.split('_'):
            gencutweight  &= ((genjet1pt>15) if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else 1)
            recocutweight &= (jet1pt>15)
        if 'jet1pt10' in cut.split('_'):
            gencutweight  &= ((genjet1pt>10) if not data in ['BCD','BCDEFGH','17Jul2018'] else 1)
            recocutweight &= (jet1pt>10)
        if not recocutweight:
            continue
        if data in ['BCDEFGH','GH','BCD','17Jul2018']:
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
            recoobs,genobs = entry.zpt,(entry.genzpt if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else entry.zpt)
        elif obs =='phistareta':
            recoobs,genobs = entry.phistareta,(entry.genphistareta if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else entry.phistareta)
        elif obs =='mupluspt':
            recoobs,genobs = entry.mupluspt,(entry.genmupluspt if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else entry.mupluspt)
        elif obs =='muminuspt':
            recoobs,genobs = entry.muminuspt,(entry.genmuminuspt if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else entry.muminuspt)
        elif obs =='mupluseta':
            recoobs,genobs = entry.mupluseta,(entry.genmupluseta if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else entry.mupluseta)
        elif obs =='muminuseta':
            recoobs,genobs = entry.muminuseta,(entry.genmuminuseta if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else entry.muminuseta)
        elif obs =='zy':
            recoobs,genobs = entry.zy,(entry.genzy if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else entry.zy)
        elif obs =='jet1y':
            recoobs,genobs = entry.jet1y,(entry.genjet1y if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else entry.jet1y)
        elif obs =='zmass':
            recoobs,genobs = entry.zmass,(entry.genzmass if not data in ['BCD','GH','BCDEFGH','17Jul2018'] else entry.zmass)
        else:
            print "WARNING: creation of 3D histogram for observable not implemented!"
            return
        if not (abs(yb+ys)>2.5 or recoobs<obsmin or recoobs>obsmax):
            #continue
            y_index = l_ybinedges[int(ys/0.5)]+int(yb/0.5)
            obs_index = l_obsbinedges[y_index]+l_obshists[y_index].FindBin(recoobs)-1
            h_reco.Fill(obs_index,recocutweight*weight*SFweight*lumi)
            if not (abs(genyb+genys)>2.5 or genobs<obsmin or genobs>obsmax):
                geny_index = l_ybinedges[int(genys/0.5)]+int(genyb/0.5)
                genobs_index = l_obsbinedges[geny_index]+l_obshists[geny_index].FindBin(genobs)-1
                h_recoresponse.Fill(obs_index,genobs_index,recocutweight*gencutweight*weight*SFweight*lumi)
    
    print 'Fill 3D gen histogram'
    if not data in ['BCD','GH','BCDEFGH','17Jul2018']:
      for entry in ntuple_gen:
        #yb,ys,event,weight = entry.yboost,entry.ystar,entry.event,entry.weight
        weight = entry.weight
        if '_PU' in varquantity:
          puWeight = 1.0
          if puobs=='npumean':
            puWeight = h_pu.GetBinContent(h_pu.FindBin(entry.npumean))
            #print entry.npumean, puWeight
          elif puobs=='npv':
            puWeight = h_pu.GetBinContent(h_pu.FindBin(entry.npv))
          elif puobs=='rho':
            puWeight = h_pu.GetBinContent(h_pu.FindBin(entry.rho))
          if data in ['BCDEFGH','BCD','GH','17Jul2018']:
            weight = weight/(puWeight if not puWeight==0 else 1)
          else:
            weight = weight*puWeight/entry.puWeight
        yb,ys,event = 0.5*abs(entry.zy+entry.jet1y),0.5*abs(entry.zy-entry.jet1y),entry.event
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
        elif obs =='mupluspt':
            recoobs,genobs = entry.mupluspt,entry.genmupluspt
        elif obs =='muminuspt':
            recoobs,genobs = entry.muminuspt,entry.genmuminuspt
        elif obs =='mupluseta':
            recoobs,genobs = entry.mupluseta,entry.genmupluseta
        elif obs =='muminuseta':
            recoobs,genobs = entry.muminuseta,entry.genmuminuseta
        elif obs =='zy':
            recoobs,genobs = entry.zy,entry.genzy
        elif obs =='jet1y':
            recoobs,genobs = entry.jet1y,entry.genjet1y
        elif obs =='zmass':
            recoobs,genobs = entry.zmass,entry.genzmass
        else:
            print "WARNING: creation of 3D histogram for observable not implemented!"
            return
        if not (abs(genyb+genys)>2.5  or genobs<obsmin or genobs>obsmax):
            #continue
            geny_index = l_ybinedges[int(genys/0.5)]+int(genyb/0.5)
            genobs_index = l_obsbinedges[geny_index]+l_obshists[geny_index].FindBin(genobs)-1
            h_gen.Fill(genobs_index,gencutweight*weight*lumi)
            if not (abs(yb+ys)>2.5 or recoobs<obsmin or recoobs>obsmax):
                y_index = l_ybinedges[int(ys/0.5)]+int(yb/0.5)
                obs_index = l_obsbinedges[y_index]+l_obshists[y_index].FindBin(recoobs)-1
                h_genresponse.Fill(obs_index,genobs_index,recocutweight*gencutweight*weight*lumi)
    print "response written to", output_file
    f_out.cd()
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
postfix=''
varquantity=''
variation=0
N_toys=1000000
'''

def create_toy3Dhist(args=None, obs='zpt', cut='_jet1pt20', mc='amc', match='', postfix='', varquantity='', variation=0, N_toys=1000000000, errors=0):
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
    l_rand_syj = []
    input_path  = PLOTSFOLDER+cut+postfix+'/resolution_985'
    #input_path  = PLOTSFOLDER+cut+postfix+'/resolution_95'
    #output_file = PLOTSFOLDER+cut+postfix+'/'+obs+'_toy_10M'+match+'.root'
    #output_file = PLOTSFOLDER+cut+postfix+'/'+obs+'_toy'+match+'.root'
    output_file = PLOTSFOLDER+cut+postfix+'/variations_'+mc+'/'+obs+'_toy'+match+varquantity+VARIATIONSTRING[variation]+'.root'
    #output_file = PLOTSFOLDER+cut+postfix+'/variations_'+mc+'/'+obs+'_toy_10000M.root'
    #output_file = PLOTSFOLDER+cut+postfix+'/'+obs+'_toy{}'.format(errors)+match+'.root'
    # toy0: parameters fitted +/- confidence interval
    # toy1: parameters from histogram +/- histogram errors
    # toy2: parameters from histogram +/- histogram errors scaled with sqrt(chi2/ndf)
    # toy3: parameters fitted +/- confidence interval; constant switching
    if not variation == 0:
        if not os.path.exists(PLOTSFOLDER+cut+postfix+'/variations_'+mc):
            print "WARNING: variations folder",PLOTSFOLDER+cut+postfix+'/variations_'+mc,"does not exist!"
            return
        else:
            output_file = PLOTSFOLDER+cut+postfix+'/variations_'+mc+'/'+obs+'_toy'+match+varquantity+VARIATIONSTRING[variation]+'.root'
            #output_file = PLOTSFOLDER+cut+postfix+'/variations/'+obs+'_toy{}'.format(errors)+match+varquantity+VARIATIONSTRING[variation]+'.root'
    # check if gen distributions are existent
    if not (os.path.exists(PLOTSFOLDER+cut+postfix+'/gendistributions/gen'+obs+'_'+mc+'.root')
        and os.path.exists(PLOTSFOLDER+cut+postfix+'/gendistributions/matchedgenjet1y'+'_'+mc+'.root')):
        print "WARNING: gen distributions not created yet. Use merlin.py --py create_gendistributions_3Dhist"
        return
    f_genobs = ROOT.TFile(PLOTSFOLDER+cut+postfix+'/gendistributions/gen'+obs+'_'+mc+'.root','READ')
    f_geny   = ROOT.TFile(PLOTSFOLDER+cut+postfix+'/gendistributions/matchedgenjet1y'+'_'+mc+'.root','READ')
    h_rand   = f_genobs.Get('gen'+obs)
    h_rand_y = f_geny.Get('matchedgenjet1y')
    while h_rand.GetBinContent(h_rand.GetMinimumBin()) < 0:
        h_rand.SetBinContent(h_rand.GetMinimumBin(),abs(h_rand.GetBinContent(h_rand.GetMinimumBin())))
    while h_rand_y.GetBinContent(h_rand_y.GetMinimumBin()) < 0:
        h_rand_y.SetBinContent(h_rand_y.GetMinimumBin(),abs(h_rand_y.GetBinContent(h_rand_y.GetMinimumBin())))
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
            f_in_yz = ROOT.TFile(input_path +"/zy_"+mc+namestring+"_bins_of_"+obs+".root","READ")
            f_in_yj = ROOT.TFile(input_path +"/matchedjet1y_"+mc+namestring+"_bins_of_"+obs+".root","READ")
            h_weight = f_in_obs.Get("gen"+obs)
            x_bins = [h_weight.GetBinLowEdge(i+1)+h_weight.GetBinWidth(i+1)/2 for i in xrange(h_weight.GetNbinsX())]
            #x_bins = [np.sqrt(h_weight.GetBinLowEdge(i+1)*(h_weight.GetBinLowEdge(i+1)+h_weight.GetBinWidth(i+1))) for i in xrange(h_weight.GetNbinsX())]
            h_rms_obs= f_in_obs.Get("rms")
            h_rms_yz = f_in_yz.Get("rms")
            h_rms_yj  = f_in_yj.Get("rms")
            h_switched = f_in_obs.Get("switched")
            h_fake =f_in_obs.Get("fakes")
            h_acceptance = f_in_obs.Get("losses")
                    
            #l_rand_syj.append(f_gensyj.Get("switchedgenjet1y"+namestring))
            if obs == 'zpt':
                fit1 = ROOT.TF1("fit1","[0]+[1]*sqrt(x)+[2]/sqrt(x)",obsmin,obsmax)
                fit2 = ROOT.TF1("fit2","[0]+[1]/sqrt(x)",obsmin,obsmax)
                fit3 = ROOT.TF1("fit3","[0]",obsmin,obsmax)
                fit5 = ROOT.TF1("fit5","[0]+[1]/x**3",obsmin,obsmax)
                fit4 = ROOT.TF1("fit4","[0]/2*(1+erf([1]*(x-[2])))+[3]",obsmin,obsmax)
                fit6 = ROOT.TF1("fit6","[0]*exp(-[1]*x)",obsmin,obsmax)
            elif obs == 'phistareta':
                fit1 = ROOT.TF1("fit1","[0]+[1]*x+[2]/x",obsmin,obsmax)
                fit2 = ROOT.TF1("fit2","[0]+[1]/x",obsmin,obsmax)
                fit3 = ROOT.TF1("fit3","[0]+[1]*log(x)",obsmin,obsmax)
                fit5 = ROOT.TF1("fit5","[0]+[1]/x**4",obsmin,obsmax)
                fit4 = ROOT.TF1("fit4","[0]/2*(1+erf([1]*(x-[2])))+[3]",obsmin,obsmax)
                fit6 = ROOT.TF1("fit6","[0]+[1]/x",obsmin,obsmax)
            fit2.SetParLimits(0,0,1)
            fit5.SetParLimits(0,0,1)
            fit4.SetParameters(1,0.01,0,0)
            #fit5.SetParameters(1,0.01,0,0)
            fit6.SetParameters(1,0.001)
            
            
            #fit_obs = h_rms_obs.Fit("fit1","S N")
            #norm_obs = max(fit_obs.Chi2()/fit_obs.Ndf(),1)
            #fit_yj = h_rms_yj.Fit("fit2","S N")
            #norm_yj = max(fit_yj.Chi2()/fit_yj.Ndf(),1)
            #fit_yz = h_rms_yz.Fit("fit3","S N")
            #norm_yz = max(fit_yz.Chi2()/fit_yz.Ndf(),1)
            #fit_A = h_acceptance.Fit("fit4","S N")
            #norm_A = max(fit_A.Chi2()/fit_A.Ndf(),1)
            #fit_F = h_fake.Fit("fit5","S N")
            #norm_F = max(fit_F.Chi2()/fit_F.Ndf(),1)
            #fit_S = h_switched.Fit("fit6","S N")
            #norm_S = max(fit_S.Chi2()/fit_S.Ndf(),1)
            #if not errors == 1:
            #  for i in xrange(h_rms_obs.GetNbinsX()):
            #    h_rms_obs.SetBinError(i+1,np.sqrt(norm_obs)*h_rms_obs.GetBinError(i+1))
            #    h_rms_yj.SetBinError(i+1,np.sqrt(norm_yj)*h_rms_yj.GetBinError(i+1))
            #    h_rms_yz.SetBinError(i+1,np.sqrt(norm_yz)*h_rms_yz.GetBinError(i+1))
            #    h_acceptance.SetBinError(i+1,np.sqrt(norm_A)*h_acceptance.GetBinError(i+1))
            #    h_fake.SetBinError(i+1,np.sqrt(norm_F)*h_fake.GetBinError(i+1))
            #    h_switched.SetBinError(i+1,np.sqrt(norm_S)*h_switched.GetBinError(i+1))
            
            fit_obs = h_rms_obs.Fit("fit1","S N")
            v_obs = [fit1(x_bins[i]) for i in xrange(h_rms_obs.GetNbinsX())]
            conf_obs = array('d',[0]*len(x_bins))
            fit_obs.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_obs,0.683)#,False)
            
            fit_yj = h_rms_yj.Fit("fit2","S N")
            v_yj = [fit2(x_bins[i]) for i in xrange(h_rms_yj.GetNbinsX())]
            conf_yj = array('d',[0]*len(x_bins))
            fit_yj.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_yj,0.683)#,False)
            
            fit_yz = h_rms_yz.Fit("fit3","S N")
            v_yz = [fit3(x_bins[i]) for i in xrange(h_rms_yz.GetNbinsX())]
            conf_yz = array('d',[0]*len(x_bins))
            fit_yz.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_yz,0.683)#,False)
            
            fit_A = h_acceptance.Fit("fit4","S N")
            v_A = [fit4(x_bins[i]) for i in xrange(h_acceptance.GetNbinsX())]
            conf_A = array('d',[0]*len(x_bins))
            fit_A.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_A,0.683)#,False)
            
            fit_F = h_fake.Fit("fit5","S N")
            v_F = [fit5(x_bins[i]) for i in xrange(h_fake.GetNbinsX())]
            conf_F = array('d',[0]*len(x_bins))
            fit_F.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_F,0.683)#,False)
            
            fit_S = h_switched.Fit("fit6","S N")
            v_S = [fit6(x_bins[i]) for i in xrange(h_switched.GetNbinsX())]
            conf_S = array('d',[0]*len(x_bins))
            fit_S.GetConfidenceIntervals(len(x_bins),1,1,array('d',x_bins),conf_S,0.683)#,False)

            h_pu = f_in_obs.Get("PU")
        bin_index += 1
        h_RMSobs.SetBinContent(obsbin+1,v_obs[bin_index-1]), h_RMSobs.SetBinError(obsbin+1,conf_obs[bin_index-1])
        h_RMSyz.SetBinContent(obsbin+1,v_yz[bin_index-1])  , h_RMSyz.SetBinError(obsbin+1,conf_yz[bin_index-1])
        h_RMSyj.SetBinContent(obsbin+1,v_yj[bin_index-1])  , h_RMSyj.SetBinError(obsbin+1,conf_yj[bin_index-1])
        if errors == 0 or errors == 3:
          h_A.SetBinContent(obsbin+1,v_A[bin_index-1])     , h_A.SetBinError(obsbin+1,conf_A[bin_index-1])
          h_F.SetBinContent(obsbin+1,v_F[bin_index-1])     , h_F.SetBinError(obsbin+1,conf_F[bin_index-1])
          h_S.SetBinContent(obsbin+1,v_S[bin_index-1])     , h_S.SetBinError(obsbin+1,conf_S[bin_index-1])
        else:
          #h_RMSobs.SetBinContent(obsbin+1,h_rms_obs[bin_index]) , h_RMSobs.SetBinError(obsbin+1,h_rms_obs.GetBinError(bin_index))
          #h_RMSyz.SetBinContent(obsbin+1,h_rms_yz[bin_index])   , h_RMSyz.SetBinError(obsbin+1,h_rms_yz.GetBinError(bin_index))
          #h_RMSyj.SetBinContent(obsbin+1,h_rms_yj[bin_index])   , h_RMSyj.SetBinError(obsbin+1,h_rms_yj.GetBinError(bin_index))
          h_A.SetBinContent(obsbin+1,h_acceptance[bin_index])   , h_A.SetBinError(obsbin+1,h_acceptance.GetBinError(bin_index))
          h_F.SetBinContent(obsbin+1,h_fake[bin_index])         , h_F.SetBinError(obsbin+1,h_fake.GetBinError(bin_index))
          h_S.SetBinContent(obsbin+1,h_switched[bin_index])     , h_S.SetBinError(obsbin+1,h_switched.GetBinError(bin_index))
        if errors == 3:
          h_S.SetBinContent(obsbin+1,0.06923384)               , h_S.SetBinError(obsbin+1,0.06923384)

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
    #l_A  = [0]*h_gen.GetNbinsX()
    #l_F  = [0]*h_gen.GetNbinsX()
    if obs == 'zpt':
        print "zpt resolution in each bin:       ", [l_RMSobs[i] for i in range(5)]
    elif obs == 'phistareta':
        print "phistareta resolution in each bin:", [l_RMSobs[i] for i in range(5)]
    print "zy resolution in each bin:        ", [l_RMSyz[i]  for i in range(5)]
    print "jet1y resolution in each bin:     ", [l_RMSyj[i]  for i in range(5)]
    print "losses in each bin:               ", [1-l_A[i]    for i in range(5)]
    print "fakes in each bin:                ", [1-l_F[i]    for i in range(5)]
    print "switch prob in each bin:          ", [l_switch[i] for i in range(5)]
    print "3DtoyMC will be written to "+output_file
    print "create toys"
    #ROOT.gRandom.SetSeed(1)
    #np.random.seed(1)
    genobs,genyz,genyj = ROOT.Double(0),ROOT.Double(0),ROOT.Double(0)
    xind,yind,zind = ROOT.Long(0),ROOT.Long(0),ROOT.Long(0)
    for i in xrange(N_toys):
        if i%(N_toys/10) == 0:
            print "toy MC creation finished by "+str(100.*i/N_toys)+"%"
        h_rand.GetRandom3(genobs,genyz,genyj)
        genyb = abs(genyj+genyz)/2
        genys = abs(genyj-genyz)/2
        geny_index = l_ybinedges[int(genys/0.5)]+int(genyb/0.5)
        index = l_obsbinedges[geny_index]+l_obshists[geny_index].FindBin(genobs)-1
        if np.random.random() < l_switch[index]:
            h_rand_y.GetBinXYZ(h_rand_y.FindBin(genyj,genyz),xind,yind,zind)
            h_rand_ym = h_rand_y.ProjectionX("genjet1y",yind-1,yind+1)
            genyj = ROOT.Double(h_rand_ym.GetRandom())
            genyb = abs(genyj+genyz)/2
            genys = abs(genyj-genyz)/2
        geny_index = l_ybinedges[int(genys/0.5)]+int(genyb/0.5)
        genobs_index = l_obsbinedges[geny_index]+l_obshists[geny_index].FindBin(genobs)-1
        recoobs= genobs * (1+l_RMSobs[genobs_index]*np.random.randn())
        recoyz = genyz+l_RMSyz[genobs_index]*np.random.randn()
        recoyj = genyj+l_RMSyj[genobs_index]*np.random.randn()
        recoyb = abs(recoyj+recoyz)/2
        recoys = abs(recoyj-recoyz)/2
        if (   (obs=='zpt'        and (recoyb+recoys > 2.4 or recoobs>1000 or recoobs<25 ))
                    or (obs=='phistareta' and (recoyb+recoys > 2.4 or recoobs>50   or recoobs<0.4))):
                        continue
        recoy_index = l_ybinedges[int(recoys/0.5)]+int(recoyb/0.5)
        recoobs_index = l_obsbinedges[recoy_index]+l_obshists[recoy_index].FindBin(recoobs)-1
        randF,randA = np.random.random(),np.random.random()
        if randF < l_F[recoobs_index]:
            h_gen.Fill(index)
        if randA < l_A[genobs_index]:
            h_reco.Fill(recoobs_index)
        if randA < l_A[genobs_index] and randF < l_F[recoobs_index]:
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


def unfold_by_inversion_3Dhist(args=None,obs='zpt',cut='_jet1pt20',data='mad',mc='amc',match='', postfix='',varquantity='',variation=0):
    if varquantity in ['','_IDSF','_IsoSF','_TriggerSF'] and not variation==0:
        print "WARNING: variations can not be computed for these variation quantities"
        variation = 0
    if not 'toy' in mc and not varquantity == '_stats':
        variation = 0
        print "WARNING: only statistical variations can be computed for this MC"
    input_file_data = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+'.root'
    input_file_mc   = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+mc+match+'.root'
    output_file = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    if not variation == 0:
      if not varquantity == '_stats':
        input_file_mc = PLOTSFOLDER+cut+postfix+'/variations/'+obs+'_'+mc+match+varquantity+VARIATIONSTRING[variation]+'.root'
        output_file    = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+varquantity+VARIATIONSTRING[variation]+'.root'
      else:
        output_file    = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+varquantity+'.root'
    print "response will be written to", output_file
    f_in_mc, f_in_data  = ROOT.TFile(input_file_mc,"READ"), ROOT.TFile(input_file_data,"READ")
    h_reco, h_gen, h_data, h_closure  = f_in_mc.Get(obs), f_in_mc.Get("gen"+obs), f_in_data.Get(obs), f_in_data.Get("gen"+obs)
    h_response, h_genresponse = f_in_mc.Get("response"),f_in_mc.Get("response_2")
    Nx,Ny = h_response.GetNbinsX(),h_response.GetNbinsY()
    [m_reco, m_gen, m_data, m_signal] = 4*[ROOT.TMatrixD(Nx,1)]
    [a_reco, a_gen, a_data, a_signal] = 4*[ROOT.TArrayD(Nx)]
    m_response = ROOT.TMatrixD(Nx,Ny)
    a_response = ROOT.TArrayD(Nx*Ny)
    m_unfold, m_data_e, m_unfold_e = ROOT.TMatrixD(1,Ny), ROOT.TMatrixD(Nx,Ny), ROOT.TMatrixD(Nx,Ny)
    a_edge, a_data_e = ROOT.TArrayD(Ny), ROOT.TArrayD(Nx*Ny)
    h_prox = h_response.ProjectionX("projectionx",1,Nx,"e")
    h_proy = h_response.ProjectionY("projectiony",1,Ny,"e")
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
    if varquantity=='_stats' and not variation == 0:
        print "Statistical variation of response matrix"
        for j in xrange(Ny):
          for i in xrange(Nx):
            h_response.SetBinContent(i+1,j+1,h_response.GetBinContent(i+1,j+1)+h_response.GetBinError(i+1,j+1)*np.random.randn())
          h_loss.SetBinContent(j+1,h_loss[j+1]+h_loss.GetBinError(j+1)*np.random.randn())
          h_fake.SetBinContent(j+1,h_fake[j+1]+h_fake.GetBinError(j+1)*np.random.randn())
        h_prox = h_response.ProjectionX("projectionx",1,Nx,"e")
        h_proy = h_response.ProjectionY("projectiony",1,Ny,"e")
        h_reco = h_fake.Clone(obs)
        h_gen = h_loss.Clone("gen"+obs)
        h_reco.Add(h_prox)
        h_gen.Add(h_proy)
    print "data distribution:",[h_data[i+1] for i in xrange(6)]#260,265)]
    print "reco distribution:",[h_reco[i+1] for i in xrange(6)]#260,265)]
    print "gen  distribution:",[h_gen[i+1]  for i in xrange(6)]#260,265)]
    print "fake distribution:",[h_fake[i+1] for i in xrange(6)]#260,265)]
    print "loss distribution:",[h_loss[i+1] for i in xrange(6)]#260,265)]
    #print "projection on X:",  [h_prox[i+1] for i in xrange(6)]
    #print "projection on Y:",  [h_proy[i+1] for i in xrange(6)]
    #print "scalefactors:",       [h_SF[i+1] for i in xrange(6)]
    if data == 'BCDEFGH':
        l_bkg = ['TT','TW','WW','WZ','ZZ']
        print "subtract backgrounds ",l_bkg
        for bkg in l_bkg:
            input_file_bkg = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+bkg+'.root'
            f_bkg = ROOT.TFile(input_file_bkg,"READ")
            print "background from",input_file_bkg
            h_bkg = f_bkg.Get(obs)
            h_data.Add(h_bkg,-1)
        print "data distribution after background subtraction:",[h_data.GetBinContent(i+1) for i in xrange(6)]#260,265)]
    for i in xrange(Nx*Ny):
        # normalize matrix rows to correct for losses
        try:
            a_response[i]=h_response.GetBinContent(i/Nx+1,i%Ny+1)/h_gen[i%Ny+1]
        except ZeroDivisionError:
            a_response[i]=0
    for i in xrange(Nx):
        a_reco[i]        = h_reco.GetBinContent(i+1)
        a_gen[i]         = h_gen.GetBinContent(i+1)
        a_data_e[i*Nx+i] = h_data.GetBinError(i+1)**2
        # correct for fakes
        try:
            a_data[i]    = h_data.GetBinContent(i+1)*(1-h_fake[i+1]/h_reco[i+1])
        except ZeroDivisionError:
            a_data[i]    = h_data.GetBinContent(i+1)
        
    print "data distribution after fake subtraction:",[a_data[i] for i in xrange(6)]#260,265)]
    m_response.SetMatrixArray(a_response.GetArray())
    m_reco.SetMatrixArray(a_reco.GetArray())
    m_gen.SetMatrixArray(a_gen.GetArray())
    m_data.SetMatrixArray(a_data.GetArray())
    m_data_e.SetMatrixArray(a_data_e.GetArray())
    m_inv    = deepcopy(m_response)
    m_dummy1 = deepcopy(m_response)
    m_dummy2 = deepcopy(m_response)
    m_inv.Invert()
    print "response matrix:",[h_response.GetBinContent(i+1,1) for i in xrange(6)]#260,265)]
    m_unfold.Mult(m_inv,m_data)
    m_dummy1.Transpose(m_inv)
    m_dummy2.Mult(m_data_e,m_dummy1)
    m_unfold_e.Mult(m_inv,m_dummy2)
    svd = ROOT.TDecompSVD(m_response)
    print "Response matrix Condition number is given as",svd.Condition()
    h_covariance  = h_response.Clone("covariance")
    h_correlation = h_response.Clone("correlation")
    h_unfold      = h_gen.Clone("unfolded"+obs)
    for j in xrange(Ny):
        for i in xrange(Nx):
            h_covariance.SetBinContent(i+1,j+1,m_unfold_e(i,j))
            h_response.SetBinContent(i+1,j+1,m_response(i,j))
            h_correlation.SetBinContent(i+1,j+1,m_unfold_e(i,j)/np.sqrt(m_unfold_e(i,i)*m_unfold_e(j,j)))
        h_unfold.SetBinContent(j+1,m_unfold(0,j))
        h_unfold.SetBinError(j+1,np.sqrt(m_unfold_e(j,j)))
    print "unfold distribution:",[h_unfold[i+1] for i in xrange(6)]#260,265)]
    print "correlation matrix:",[h_correlation.GetBinContent(i+1,1) for i in xrange(6)]#260,265)]
    #print "closure input/output:",[h_gen.GetBinContent(i+1)/h_reco.GetBinContent(i+1)
    #                                /(h_unfold.GetBinContent(i+1)/h_data.GetBinContent(i+1)) for i in xrange(260,265)]
    f_out = ROOT.TFile(output_file,"RECREATE")
    h_unfold.Write()
    h_reco.Write()
    h_gen.Write()
    h_data.Write("signal"+obs)
    h_response.Write()
    h_covariance.Write()
    h_correlation.Write()
    print "unfolding results written to",output_file
    return svd.Condition()


def unfold_by_tunfold_3Dhist(args=None,obs='zpt',cut='_jet1pt20',data='mad',mc='amc',match='', postfix='',varquantity='',variation=0):
    if varquantity in ['','_IDSF','_IsoSF','_TriggerSF'] and not variation==0:
        print "WARNING: variations can not be computed for these variation quantities"
        variation = 0
    if not 'toy' in mc and not varquantity == '_stats':
        variation = 0
        print "WARNING: only statistical variations can be computed for this MC"
    input_file_data = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+'.root'
    input_file_mc   = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+mc+match+'.root'
    output_file = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    if not variation == 0:
      if not varquantity == '_stats':
        input_file_mc = PLOTSFOLDER+cut+postfix+'/variations/'+obs+'_'+mc+match+varquantity+str(variation)+'.root'
      output_file    = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+varquantity+'.root'
    if '_PU' in varquantity:
      input_file_mc  = PLOTSFOLDER+cut+postfix+'/variations/'+obs+'_'+mc+match+varquantity+'.root'
      output_file    = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+varquantity+'.root'
    print "response will be written to", output_file
    f_in_mc, f_in_data  = ROOT.TFile(input_file_mc,"READ"), ROOT.TFile(input_file_data,"READ")
    h_reco, h_gen, h_data, h_closure  = f_in_mc.Get(obs), f_in_mc.Get("gen"+obs), f_in_data.Get(obs), f_in_data.Get("gen"+obs)
    h_response = f_in_mc.Get("response")
    Nx,Ny = h_response.GetNbinsX(),h_response.GetNbinsY()
    #h_response = ROOT.TH2D("response","",Nx,0,Nx,Ny,0,Ny)
    # fill new response matrix!
    #for j in xrange(Ny):
    #    for i in xrange(Nx):
    #        h_response.SetBinContent(i+1,j+1,h_response1.GetBinContent(i+1,j+1))
    #        h_response.SetBinError(i+1,j+1,h_response1.GetBinError(i+1,j+1))
    f_out = ROOT.TFile(output_file,"RECREATE")
    
    h_fake = h_reco.Clone("fake")
    h_loss = h_gen.Clone("loss")
    #h_prox = h_response.ProjectionX("projectionx",1,Nx,"e")
    #h_proy = h_genresponse.ProjectionY("projectiony",1,Ny,"e")
    h_prox = h_gen.Clone("projectionx")
    h_proy = h_reco.Clone("projectiony")
    for j in xrange(Ny):
        edge_gen =0
        edge_reco =0
        for i in xrange(Nx):
            edge_gen +=h_response.GetBinContent(i+1,j+1)
            edge_reco +=h_response.GetBinContent(j+1,i+1)
        h_fake.SetBinContent(j+1,h_reco[j+1]-edge_reco)
        h_loss.SetBinContent(j+1,h_gen[j+1] -edge_gen)
        # sometimes negative values appear inside sqrt.
        h_fake.SetBinError(j+1,np.sqrt(abs(h_reco.GetBinError(j+1)**2-h_prox.GetBinError(j+1)**2)))
        h_loss.SetBinError(j+1,np.sqrt(abs( h_gen.GetBinError(j+1)**2-h_proy.GetBinError(j+1)**2)))
    if varquantity=='_stats' and not variation == 0:
        print "Statistical variation of response matrix"
        for j in xrange(Ny):
          for i in xrange(Nx):
            h_response.SetBinContent(i+1,j+1,h_response.GetBinContent(i+1,j+1)+h_response.GetBinError(i+1,j+1)*np.random.randn())
          h_loss.SetBinContent(j+1,h_loss[j+1]+h_loss.GetBinError(j+1)*np.random.randn())
          h_fake.SetBinContent(j+1,h_fake[j+1]+h_fake.GetBinError(j+1)*np.random.randn())
        h_prox = h_response.ProjectionX("projectionx",1,Nx,"e")
        h_proy = h_response.ProjectionY("projectiony",1,Ny,"e")
        h_reco = h_fake.Clone(obs)
        h_gen = h_loss.Clone("gen"+obs)
        h_reco.Add(h_prox)
        h_gen.Add(h_proy)
    print "data distribution:",[h_data[i+1] for i in xrange(6)]#260,265)]
    print "reco distribution:",[h_reco[i+1] for i in xrange(6)]#260,265)]
    print "gen  distribution:",[h_gen[i+1]  for i in xrange(6)]#260,265)]
    print "fake distribution:",[h_fake[i+1] for i in xrange(6)]#260,265)]
    print "loss distribution:",[h_loss[i+1] for i in xrange(6)]#260,265)]
    if data == 'BCDEFGH':
        l_bkg = ['TT','TW','WW','WZ','ZZ']
        print "subtract backgrounds ",l_bkg
        for bkg in l_bkg:
            input_file_bkg = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+bkg+'.root'
            f_bkg = ROOT.TFile(input_file_bkg,"READ")
            print "background from",input_file_bkg
            h_bkg = f_bkg.Get(obs)
            h_data.Add(h_bkg,-1)
        print "data distribution after background subtraction:",[h_data.GetBinContent(i+1) for i in xrange(6)]#260,265)]
    h_covariance = h_response.Clone("covariance")
    h_correlation = h_response.Clone("correlation")
    h_signal = h_data.Clone()
    for i in xrange(Nx):
        # correct for fakes
        try:
            h_signal.SetBinContent(i+1,h_data.GetBinContent(i+1)-h_data[i+1]*h_fake[i+1]/h_reco[i+1])
        except ZeroDivisionError:
            print i
            #h_data.SetBinContent(i+1,h_data.GetBinContent(i+1))
        # set underflow bin to correct for losses
        #h_response.SetBinContent(i+1,0, h_loss[i+1])
        h_response.SetBinContent(0,i+1, h_loss[i+1])
    print "data distribution after fake subtraction:",[h_signal[i+1] for i in xrange(6)]#260,265)]
    print "response matrix:",[h_response.GetBinContent(1,i+1) for i in xrange(6)]#260,265)]
    unfold = ROOT.TUnfold(
            h_response,
            #ROOT.TUnfold.kHistMapOutputHoriz,   # gen-level on x axis
            ROOT.TUnfold.kHistMapOutputVert,    # gen-level on y axis
            ROOT.TUnfold.kRegModeNone,          # no regularization
            ROOT.TUnfold.kEConstraintNone,      # no constraints
            )
    unfold.SetInput(h_signal)
    unfold.DoUnfold(0)
    h_unfold = h_data.Clone("unfolded"+obs)
    unfold.GetOutput(h_unfold)
    unfold.GetEmatrix(h_covariance)
    for j in xrange(Ny):
        for i in xrange(Nx):
            h_correlation.SetBinContent(i+1,j+1,h_covariance.GetBinContent(i+1,j+1)
                                                /np.sqrt(h_covariance.GetBinContent(i+1,i+1)*h_covariance.GetBinContent(j+1,j+1)))
    print "unfold distribution:",[h_unfold[i+1] for i in xrange(6)]#260,265)]
    print "correlation matrix:",[h_correlation.GetBinContent(i+1,1) for i in xrange(6)]#260,265)]
    #print "closure input/output:",[h_gen.GetBinContent(i+1)/h_reco.GetBinContent(i+1)
    #                                /(h_unfold.GetBinContent(i+1)/h_data.GetBinContent(i+1)) for i in xrange(260,265)]
    f_out.cd()
    h_unfold.Write()
    h_reco.Write()
    h_gen.Write()
    h_data.Write("signal"+obs)
    h_response.Write()
    h_covariance.Write()
    h_correlation.Write()
    print "unfolding results written to",output_file
    return

def create_3Dunc(args=None, obs='phistareta', cut='_jet1pt20', data='BCDEFGH',match='', postfix='', varquantity='_total', N_toys=1000):
#def create_3Dunc(args=None, obs='zpt', cut='_jet1pt20', data='mad',match='', postfix='', varquantity='_PU', N_toys=1000):
    var=varquantity
    output_file = PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_'+data+match+varquantity+'.root'
    print "write uncertainty to file",output_file
    if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        return
    f_out = ROOT.TFile(output_file,"RECREATE")
    if '_stats' in varquantity:
    #if varquantity in ['_stats_toy','_stats_amc','_stats_mad','_stats_hpp','_stats_pow','_stats_ptz']:
        mc = varquantity.split('_')[-1]
        input_file = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+match+'.root'
        f_in      = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get(obs)
        h_uncertainty = h_central.Clone('uncertainty'+varquantity)
        h_uncertainty.Reset()
        h_sum = h_uncertainty.Clone('mean_'+mc)
        h_sqr = f_in.Get('response')
        h_sqr.Reset()
        h_cov = h_sqr.Clone("covariance_"+mc)
        for i in xrange(N_toys):
            unfold_by_inversion_3Dhist(args,obs,cut,data,mc,match,postfix,varquantity='_stats',variation=i+1)
            input_file_var   = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'_stats'+'.root'
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
    elif sum([(x in varquantity) for x in ['_Robs','_Ryz','_Ryj','_A','_F','_switch']]):
    #elif varquantity in ['_Robs','_Ryz','_Ryj','_A','_F','_switch']:
        mc = 'toy'#+varquantity[-1]
        var = varquantity#[:-1]
        #create_toy3Dhist(args,obs,cut,'mad',match,postfix,varquantity='',variation=0)
        unfold_by_inversion_3Dhist(args,obs,cut,data,mc,match,postfix)
        input_file = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
        f_in      = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get('unfolded'+obs)
        h_uncertainty = h_central.Clone('uncertainty'+varquantity)
        h_uncertainty.Reset()
        #create_toy3Dhist(args,obs,cut,'mad',match,postfix,varquantity=var,variation=1)
        #create_toy3Dhist(args,obs,cut,'mad',match,postfix,varquantity=var,variation=-1)
        unfold_by_inversion_3Dhist(args,obs,cut,data,mc,match,postfix,varquantity=var,variation=1)
        unfold_by_inversion_3Dhist(args,obs,cut,data,mc,match,postfix,varquantity=var,variation=-1)
        input_file_up   = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+var+'Up.root'
        input_file_down = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+var+'Down.root'
        f_in_up   = ROOT.TFile(input_file_up,  "READ")
        f_in_down = ROOT.TFile(input_file_down,"READ")
        h_up      = f_in_up.Get('unfolded'+obs)
        h_down    = f_in_down.Get('unfolded'+obs)
        for i in xrange(h_uncertainty.GetNbinsX()):
            #h_uncertainty.SetBinContent(i+1,np.sqrt(((h_central[i+1]-h_up[i+1])**2+(h_central[i+1]-h_down[i+1])**2)/2)/h_central[i+1])
            h_uncertainty.SetBinContent(i+1,max(abs(h_central[i+1]-h_up[i+1]),abs(h_central[i+1]-h_down[i+1]))/h_central[i+1])
            h_uncertainty.SetBinError(i+1,0)
        f_out.cd()
        h_uncertainty.Write()
        h_central.Write('unfolded'+obs+var)
    elif varquantity in ['_model_toy']:
        unfold_by_tunfold_3Dhist(args,obs,cut,data,'toy0',match,postfix)
        unfold_by_tunfold_3Dhist(args,obs,cut,data,'toy2',match,postfix)
        input_file_0 = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_toy0'+match+'.root'
        input_file_2 = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_toy2'+match+'.root'
        f_in_0 = ROOT.TFile(input_file_0,"READ")
        f_in_2 = ROOT.TFile(input_file_2,"READ")
        h_0 = f_in_0.Get('unfolded'+obs)
        h_2 = f_in_2.Get('unfolded'+obs)
        h_uncertainty = h_0.Clone('uncertainty'+varquantity)
        h_uncertainty.Reset()
        for i in xrange(h_uncertainty.GetNbinsX()):
            #h_uncertainty.SetBinContent(i+1,2*max(abs(h_0[i+1]-h_1[i+1])/(h_0[i+1]+h_1[i+1]),abs(h_0[i+1]-h_2[i+1])/(h_0[i+1]+h_2[i+1])))
            h_uncertainty.SetBinContent(i+1,2*abs(h_0[i+1]-h_2[i+1])/(h_0[i+1]+h_2[i+1]))
        f_out.cd()
        h_uncertainty.Write()
    elif varquantity in ['_IDSF','_IsoSF','_TriggerSF','_JEC']:
        input_file = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+match+'.root'
        create_3Dhist(args,obs,cut,data,match,postfix,varquantity=var,variation=1)
        create_3Dhist(args,obs,cut,data,match,postfix,varquantity=var,variation=-1)
        f_in      = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get(obs)
        h_uncertainty = h_central.Clone('uncertainty'+varquantity)
        h_uncertainty.Reset()
        input_file_up   = PLOTSFOLDER+cut+postfix+'/variations/'+obs+'_'+data+match+var+'Up.root'
        input_file_down = PLOTSFOLDER+cut+postfix+'/variations/'+obs+'_'+data+match+var+'Down.root'
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
    elif varquantity in ['_JER','_MuScale']:
        input_file = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+match+'.root'
        create_3Dhist(args,obs,cut,data,match,postfix,varquantity=var)
        f_in      = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get(obs)
        h_uncertainty = h_central.Clone('uncertainty'+varquantity)
        h_uncertainty.Reset()
        input_file_var   = PLOTSFOLDER+cut+postfix+'/variations/'+obs+'_'+data+match+var+'.root'
        f_in_var   = ROOT.TFile(input_file_var,"READ")
        h_var      = f_in_var.Get(obs)
        for i in xrange(h_uncertainty.GetNbinsX()):
            h_uncertainty.SetBinContent(i+1,abs(h_var[i+1]-h_central[i+1])/h_central[i+1])
            h_uncertainty.SetBinError(i+1,0)
        f_out.cd()
        h_uncertainty.Write()
        h_central.Write(obs)
    elif varquantity in ['_bkg']:
        if not data in ['BCDEFGH','17Jul2018']:
            print "WARNING: bkg uncertainty only defined for data"
            return
        input_file = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+match+'.root'
        f_in      = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get(obs)
        h_uncertainty = h_central.Clone('uncertainty'+varquantity)
        l_bkg = ['TT','TW','WW','WZ','ZZ']
        for bkg in l_bkg:
            f_bkg = ROOT.TFile(PLOTSFOLDER+cut+postfix+'/'+obs+'_'+bkg+match+'.root',"READ")
            h_bkg = f_bkg.Get(obs)
            h_bkg.Add(h_bkg)
        for i in xrange(h_uncertainty.GetNbinsX()):
            h_uncertainty.SetBinContent(i+1,h_bkg[i+1]/h_central[i+1]/2)
            h_uncertainty.SetBinError(i+1,0)
        f_out.cd()
        h_uncertainty.Write('uncertainty'+varquantity)
    elif varquantity in ['_lumi']:
        input_file = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+match+'.root'
        f_in      = ROOT.TFile(input_file,"READ")
        h_uncertainty = f_in.Get(obs)
        for i in xrange(h_uncertainty.GetNbinsX()):
            h_uncertainty.SetBinContent(i+1,0.025)
            h_uncertainty.SetBinError(i+1,0)
        f_out.cd()
        h_uncertainty.Write('uncertainty'+varquantity)
    elif varquantity in ['_statistical']:
        unfold_by_inversion_3Dhist(args,obs,cut,data,'mad',match,postfix)
        input_file = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_mad'+match+'.root'
        f_in       = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get('unfolded'+obs)
        h_uncertainty = h_central.Clone('uncertainty'+varquantity)
        for i in xrange(h_uncertainty.GetNbinsX()):
            h_uncertainty.SetBinContent(i+1,h_central.GetBinError(i+1)/h_central[i+1])
            h_uncertainty.SetBinError(i+1,0)
        f_out.cd()
        h_uncertainty.Write()
    elif '_PU' in varquantity:
        unfold_by_tunfold_3Dhist(args,obs,cut,data,'mad',match,postfix)
        input_file = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_mad'+match+'.root'
        f_in      = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get('unfolded'+obs)
        h_uncertainty = h_central.Clone('uncertainty'+varquantity)
        h_uncertainty.Reset()
        create_3Dhist(args,obs,cut,'mad',match,postfix,varquantity=var)
        unfold_by_tunfold_3Dhist(args,obs,cut,data,'mad',match,postfix,varquantity=var)
        input_file_var   = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_mad'+match+var+'.root'
        f_in_var   = ROOT.TFile(input_file_var,"READ")
        h_var      = f_in_var.Get('unfolded'+obs)
        for i in xrange(h_uncertainty.GetNbinsX()):
            h_uncertainty.SetBinContent(i+1,abs(h_var[i+1]-h_central[i+1])/h_central[i+1])
            h_uncertainty.SetBinError(i+1,0)
        f_out.cd()
        h_uncertainty.Write()
        h_central.Write(obs)
    elif '_total' in varquantity:
        input_file = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+match+'.root'
        f_in       = ROOT.TFile(input_file,"READ")
        h_uncertainty = f_in.Get(obs)
        h_uncertainty.Reset()
        varlist = ({'stat': ['_statistical'],
                    'lumi': ['_lumi'],
                    'bkg' : ['_bkg'],
                    'eff' : ['_IDSF','_IsoSF','_TriggerSF'],
                    'unf' : ['_stats_toy0','_model_toy','_Robs','_Ryz','_Ryj','_A','_F','_switch'],
                    #'unf' : ['_stats_toy'],
                    'jer' : ['_JER'],
                    'jec' : ['_JEC'],
                    'muon': ['_MuScale'],
                    })
        for vkey in varlist:
          h_unc = h_uncertainty.Clone("uncertainty_"+vkey)
          h_unc.Reset()
          print vkey,"uncertainty written"
          for v in varlist[vkey]:
            input_file_unc = PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_'+data+match+v+'.root'
            f_in_unc       = ROOT.TFile(input_file_unc,"READ")
            h_v            = f_in_unc.Get('uncertainty'+v)
            for i in xrange(h_uncertainty.GetNbinsX()):
                h_unc.SetBinContent(i+1,np.sqrt(h_unc[i+1]**2+h_v[i+1]**2))
                h_unc.SetBinError(i+1,0)
          if (not vkey == 'stat') or ('stat' in varquantity):
            for i in xrange(h_uncertainty.GetNbinsX()):
                h_uncertainty.SetBinContent(i+1,np.sqrt(h_uncertainty[i+1]**2+h_unc[i+1]**2))
                h_uncertainty.SetBinError(i+1,0)
          f_out.cd()
          h_unc.Write()
        h_uncertainty.Write('uncertainty'+varquantity)
    else:
        print "WARNING: uncertainty does not exist! Please remove",output_file
        return
    print "uncertainties written to",output_file
    return


def loop_3Dhist(args=None):
    N_toys = 1000000000
    cut = '_jet1pt20'
    postfix=''#'_puppi'
    for data in ['17Jul2018','hpp','amc','mad','WW','WZ','ZZ','TT','TW']:#,'pow','ptz',
        create_3Dhist(obs='zpt',cut=cut,data=data,postfix=postfix)
        create_3Dhist(obs='phistareta',cut=cut,data=data,postfix=postfix)
    for mc in ['hpp','mad']:
        create_toy3Dhist(obs='zpt',cut=cut,mc=mc,postfix=postfix,N_toys=N_toys)
        create_toy3Dhist(obs='phistareta',cut=cut,mc=mc,postfix=postfix,N_toys=N_toys)
        for varquantity in ['_F','_A','_switch','_Robs','_Ryj','_Ryz']:
          for variation in [-1,1]:
            create_toy3Dhist(obs='zpt',cut=cut,mc=mc,postfix=postfix,varquantity=varquantity,variation=variation,N_toys=N_toys)
            create_toy3Dhist(obs='phistareta',cut=cut,mc=mc,postfix=postfix,varquantity=varquantity,variation=variation,N_toys=N_toys)
    return

def loop_3Dunc(args=None):
    for cut in ['_jet1pt20']:
     for postfix in ['']:
      for varquantity in [  '_stats_mad','_stats_amc','_stats_hpp',#'_stats_pow','_stats_ptz',
                            '_stats_toy0','_stats_toy2',
                            #'_model_mad','_model_amc','_model_hpp',
                            '_PUnpumean','_PUnpv','_PUrho',
                            '_model_toy',
                            '_Robs', '_Ryj',  '_Ryz', '_F', '_A', '_switch',#'_stats_toy',
                            '_IDSF','_IsoSF','_TriggerSF',
                            '_bkg','_lumi',
                            '_JEC','_JER','_MuScale',
                            '_statistical',
                            '_total',
                            '_total_stat'
                            ]:
        for data in [   '17Jul2018',
                        #'amc',
                        #'hpp',
                        #'mad',
                        #'BCDEFGH'
                        ]:
          create_3Dunc(obs='zpt',       cut=cut,data=data,postfix=postfix,varquantity=varquantity)
          create_3Dunc(obs='phistareta',cut=cut,data=data,postfix=postfix,varquantity=varquantity)
    return

def calculate_closure_chi2(args=None, obs='zpt', cut='_jet1pt20', data='amc', mc='mad',match='', postfix='', ybindex=None, ysindex=None):
#def calculate_closure_chi2(args=None, obs='phistareta', cut='_jet1pt20', data='mad', mc='toy0',match='', postfix='', ybindex=0, ysindex=0):
  varlist = ['stats_'+mc]#,'model_'+mc]
  unfold_by_tunfold_3Dhist(args,obs,cut,data,mc,match,postfix)
  #f_chi2 = ROOT.TFile(PLOTSFOLDER+cut+postfix+'/chi2/'+obs+'_'+data+'_by_'+mc+match+'.root',"RECREATE")
  if 'toy' in mc:
      #varlist += ['Robs','Ryj','Ryz','switch','F','A']
      varlist = ['stats_'+mc,'model_toy','Robs','Ryj','Ryz','switch','F','A']
      #varlist = ['stats_toy','Robs','Ryj','Ryz','switch','F','A']
  f_data = ROOT.TFile(PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root',"READ")
  f_mc   = ROOT.TFile(PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+match+'.root',"READ")
  h_unf = f_data.Get("unfolded"+obs)
  h_gen = f_mc.Get("gen"+obs)
  h_unc = h_gen.Clone("uncertainty")
  h_unc.Reset()
  for var in varlist:
    f_var = ROOT.TFile(PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_17Jul2018'+match+'_'+var+'.root',"READ")
    h_var = f_var.Get("uncertainty_"+var)
    print var
    for i in xrange(h_unc.GetNbinsX()):
        h_unc.SetBinContent(i+1,np.sqrt(h_unc[i+1]**2+h_var[i+1]**2))
  chi2 = 0
  if not (ybindex==None or ysindex==None):
    [l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)[4:6]
    obsindexmin, obsindexmax = l_obsbinedges[l_ybinedges[ysindex]+int(ybindex)],l_obsbinedges[l_ybinedges[ysindex]+int(ybindex)+1]
  else:
      obsindexmin, obsindexmax = 0,h_unc.GetNbinsX()
  h_chi2 = h_unc.Clone("chi2")
  for i in xrange(obsindexmin, obsindexmax):
    chi2 += (h_unf[i+1]-h_gen[i+1])**2/((h_unc[i+1]*h_unf[i+1])**2+h_unf.GetBinError(i+1)**2)
    h_chi2.SetBinContent(i+1,(h_unf[i+1]-h_gen[i+1])/np.sqrt((h_unc[i+1]*h_unf[i+1])**2+h_unf.GetBinError(i+1)**2))
    h_chi2.SetBinError(i+1,0)
  #f_chi2.cd()
  #h_chi2.Write()
  #print PLOTSFOLDER+cut+postfix+'/chi2/'+obs+'_'+data+'_by_'+mc+match+'.root'
  print "chi2/ndf between gen",data,"and reco",data,"unfolded by",mc,"is",chi2/(obsindexmax-obsindexmin)
  return chi2/(obsindexmax-obsindexmin)


def write_closure_chi2(args=None, obs='zpt', cut='_jet1pt20', data='mad', mc='toy0',match='', postfix=''):
    output_path = PLOTSFOLDER+cut+postfix+'/chi2/'+obs+'_'+data+'_by_'+mc+match+'.root'
    f_out = ROOT.TFile(output_path,"RECREATE")
    [l_ybinedges,l_obsbinedges] = prepare_3Dhist(args,obs)[4:6]
    x    = range(len(l_obsbinedges)-1)
    xerr = range(len(l_obsbinedges)-1)
    y    = range(len(l_obsbinedges)-1)
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            #x[l_ybinedges[int(2*ysmin)]+int(2*ybmin)]    = (l_obsbinedges[l_ybinedges[int(2*ysmin)]+int(2*ybmin)]+l_obsbinedges[l_ybinedges[int(2*ysmin)]+int(2*ybmin)+1])/2.0
            #xerr[l_ybinedges[int(2*ysmin)]+int(2*ybmin)] = (l_obsbinedges[l_ybinedges[int(2*ysmin)]+int(2*ybmin)+1]-l_obsbinedges[l_ybinedges[int(2*ysmin)]+int(2*ybmin)])/2.0
            #y[l_ybinedges[int(2*ysmin)]+int(2*ybmin)]    = calculate_closure_chi2(args,obs,cut,data,mc,match,postfix,int(2*ybmin),int(2*ysmin))
            x[l_ybinedges[int(2*ysmin)]+int(2*ybmin)]    = l_ybinedges[int(2*ysmin)]+int(2*ybmin)+1
            xerr[l_ybinedges[int(2*ysmin)]+int(2*ybmin)] = 0.5
            y[l_ybinedges[int(2*ysmin)]+int(2*ybmin)]    = calculate_closure_chi2(args,obs,cut,data,mc,match,postfix,int(2*ybmin),int(2*ysmin))
    print l_obsbinedges
    print x
    print xerr
    h_out = ROOT.TGraphErrors(len(l_obsbinedges)-1,array('d',x),array('d',y),array('d',xerr))
    f_out.cd()
    h_out.Write("chi2_"+data+"_by_"+mc)
    print "chi2/ndf written to",output_path
    return


def plot_datamc_3Dhist(args=None, obs='phistareta', cut='_jet1pt20', data='17Jul2018', mc='mad', match='', postfix=''):
  plots=[]
  for obs in ['phistareta','zpt']:
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    data_source = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+match+'.root'
    mc_source   = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+mc+match+'.root'
    bkg_list = ['TT','WZ','ZZ','TW','WW']
    bkg_source  =[PLOTSFOLDER+cut+postfix+'/'+obs+'_'+bkg+match+'.root' for bkg in bkg_list]
    filelist = [data_source,mc_source]+bkg_source
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
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
        'www': 'datamc'+cut+postfix+'_'+data+'_vs_'+mc+match,
        'filename': obs,
        'x_errors': [1],
        'x_label': (r'$\\mathit{p}_T^Z$' if obs =='zpt' else r'$\\mathit{\\phi}^{*}_{\\eta}$')+' bin',
        'y_log': True,
        'y_lims': [1e-2,1e5] if obs =='zpt' else [1e0,1e7],
        'nicks_blacklist': ['sim'],
        'y_subplot_label': 'Data/Sim',
        'y_subplot_lims': [0.75,1.25],
        'texts_size': [20],
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
                'files': filelist_binned,
                'x_expressions': [obs+namestring],
                'www': 'datamc'+cut+postfix+'_'+data+'_vs_'+mc+match+'/datamc'+namestring,
                'analysis_modules': ['SumOfHistograms','NormalizeByBinWidth','Ratio'],
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'y_label': 'Events per binsize',
                'texts': [  r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$" if CMSLABEL else "",
                            r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'texts_y': [1.07,0.97],
                'x_log': True,
                'x_label': obs,
            })
            if ysmin>1.0:
                d['y_subplot_lims'] = [0.9,2.3]
            elif ysmin>0.5:
                d['y_subplot_lims'] = [0.8,1.8]
            elif ybmin>1.0:
                d['y_subplot_lims'] = [0.5,1.5]
            plots.append(d)
    d0['figsize'] = [36,6]
    d0['vertical_lines'] = l_obsbinedges
    d0['vertical_lines_styles'] = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    #plots.append(d0)
  return [PlottingJob(plots=plots, args=args)]


def plot_resolution_3Dhist(args=None, cut='_jet1pt20', mc='mad',match='', postfix='',trunc = '_985'):
  plots=[]
  folder = PLOTSFOLDER+cut+postfix+'/resolution'+trunc+'/'
  for obs in ['zpt','phistareta']:
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = ({
                'www': 'resolutions'+cut+postfix+'_'+mc+match+'/resolution'+trunc+namestring,
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
            l_bins = [float(x) for x in d0['x_bins'][0].split(' ')]
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
            for obsmin,obsmax in zip(l_bins[:-1],l_bins[1:]):
                d0['texts'][0] = [  #r"$\\bf{CMS} \\hspace{0.5} \\it{Simulation} \\hspace{0.2} \\it{Preliminary}$" if CMSLABEL else "",
                                    r"${}<p_T^Z/$GeV$<{}$".format(int(obsmin),int(obsmax)) if obs=='zpt' else r"${}<\\phi*_\\eta<{}$".format(obsmin,obsmax)]
                d0['x_expressions'] = ['resolution_{}_{}'.format(int(obsmin),int(obsmax)) if obs=='zpt' else 'resolution_{}_{}'.format(int(10*obsmin),int(10*obsmax))]
                d01 = deepcopy(d0)
                d01.update({
                    'files': [folder+obs+'_'+mc+match+namestring+'.root'],
                    'x_label': r"$R(p_T^{Z})$" if obs=='zpt' else r"$R(\\phi*_\\eta)$"
                })
                d01['www'] = d['www']+'/histograms_'+obs
                d02 = deepcopy(d0)
                d02.update({
                    'files': [folder+'zy_'+mc+match+namestring+'_bins_of_'+obs+'.root'],
                    'x_label': r"$R(y^{Z})$"
                })
                d02['www'] = d['www']+'/histograms_zy_bins_of_'+obs
                d03 = deepcopy(d0)
                d03.update({
                    'files': [folder+'matchedjet1y_'+mc+match+namestring+'_bins_of_'+obs+'.root'],
                    'x_label': r"$R(y^{jet1})$"
                })
                d03['www'] = d['www']+'/histograms_jet1y_bins_of_'+obs
                #plots.append(d01)
                #plots.append(d02)
                #plots.append(d03)
            d1 = deepcopy(d)
            d1.update({
                'files': [  folder+obs+'_'+mc+match+namestring+'.root',
                            folder+'matchedjet1y_'+mc+match+namestring+'_bins_of_'+obs+'.root',
                            folder+'zy_'+mc+match+namestring+'_bins_of_'+obs+'.root'],
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
                'files': [folder+obs+'_'+mc+match+namestring+'.root'],
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
                'files': [folder+obs+'_'+mc+match+namestring+'.root'],
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
                'files': [folder+obs+'_'+mc+match+namestring+'.root'],
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
            plots.append(d1)
            plots.append(d2)
            plots.append(d3)
            plots.append(d4)
  return [PlottingJob(plots=plots, args=args)]


#MCLIST = ['toy','toy0','toy1','toy2']
#MCLIST = ['mad','toy0']
#MCLIST = ['amc','toy1']
#MCLIST = ['toy0','toy1','toy2']
#PLOTSFOLDER = "ZJtriple/ZJtriple_2019-06-24"

def plot_closure_chi2(args=None, cut='_jet1pt20', data='17Jul2018', mc='toy0',match='', postfix=''):
  plots = []
  for obs in ['zpt','phistareta']:
    l_binedges = prepare_3Dhist(args,obs)[4]
    print l_binedges
    #l_binedges = prepare_3Dhist(args,obs)[5]
    filelist = []
    for sample in MCLIST:
        if mc=='toy':
            unfold_by_tunfold_3Dhist(args,obs,cut,sample,'toy0',match,postfix)
            unfold_by_tunfold_3Dhist(args,obs,cut,sample,'toy2',match,postfix)
            write_data(args,obs,cut,sample,match,postfix)
        #else:
         #   unfold_by_tunfold_3Dhist(args,obs,cut,sample,mc,match,postfix)
        write_closure_chi2(args,obs,cut,sample,mc,match,postfix)
        filelist.append(PLOTSFOLDER+cut+postfix+'/chi2/'+obs+'_'+sample+'_by_'+mc+match+'.root')
    d = ({
        'www': 'chi2'+cut+postfix+'_MC_by_'+mc+match,
        'files': filelist,
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
        'x_lims': [0.5,max(l_binedges)+1.5],
        'texts': [  r"$\\bf{CMS} \\hspace{0.5} \\it{Simulation} \\hspace{0.2} \\it{Preliminary}$" if CMSLABEL else "",
                    'unfolding in ',(r'($p_T^Z$,$y_b$,$y*$)' if obs=='zpt' else r'($\\phi*_\\eta$,$y_b$,$y*$)'),
                    'using',LABELDICT[mc],('Toy ' if 'toy' in mc else '')+'response'],
        'texts_size': 20,
        'texts_x': [0.05],
        'texts_y': [1.07,0.76,(0.71 if obs=='zpt' else 0.70),0.64,0.58,0.52],
        'labelsize': 25,
        'legend': 'upper left',
        'vertical_lines': [x+0.5 for x in l_binedges],
        'vertical_lines_styles': ['--'],
        #'vertical_lines_styles': 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--'],
    
    })
    plots.append(d)
  return [PlottingJob(plots=plots, args=args)]

#def plot_unfolding_closure_3Dhist(args=None, cut='_jet1pt20', data='BCDEFGH', mc='toy0',match='', postfix=''):
def plot_unfolding_closure_3Dhist(args=None, cut='_jet1pt20', data='17Jul2018', mc='mad',match='', postfix=''):
  varlist = 2*['stats_'+mc]
  plots=[]
  if 'toy' in mc:
      varlist = ['stats_'+mc,'model_toy','Robs','Ryj','Ryz','switch','F','A']#
  for obs in ['zpt','phistareta']:
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    filelist=[]
    for sample in MCLIST:
        #unfold_by_inversion_3Dhist(args,obs,cut,sample,mc,match,postfix)
        if mc=='toy':
            unfold_by_tunfold_3Dhist(args,obs,cut,sample,'toy0',match,postfix)
            unfold_by_tunfold_3Dhist(args,obs,cut,sample,'toy2',match,postfix)
            write_data(args,obs,cut,sample,match,postfix)
        else:
            unfold_by_tunfold_3Dhist(args,obs,cut,sample,mc,match,postfix)
        filelist.append(PLOTSFOLDER+cut+postfix+'/'+obs+'_'+sample+'.root')
        filelist.append(PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+sample+'_by_'+mc+match+'.root')
    filelist = filelist+[PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_'+data+'_'+var+'.root' for var in varlist]
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    d0 = ({
        'www': 'comparison_unfolding_samples'+cut+postfix+'_MC_by_'+mc+match,
        'files': filelist,
        'x_expressions': len(MCLIST)*['gen'+obs,'unfolded'+obs]+['uncertainty_'+x for x in varlist],
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
        'labels': [(LABELDICT[x]+' (chi2/ndf={:.3f})'.format(calculate_closure_chi2(args,obs,cut,x,mc,match,postfix)),
                    LABELDICT[x]+' (chi2/ndf={:.3f})'.format(calculate_closure_chi2(args,obs,cut,x,mc,match,postfix)),
                    "") for x in MCLIST]+["Toy Stat. Unc.","","Toy Syst. Unc.",""],
        'subplot_legend': 'upper left',
        'subplot_fraction': 45,
        'subplot_nicks': ['up','down','ratio'],
        'y_subplot_label': 'Unfolded/Gen',
        #'www': 'comparison_unfolding_samples'+cut+postfix+'_'+data+'_by_'+mc+match,
        'filename': obs,
        'x_label': (r'$\\mathit{p}_T^Z$' if obs =='zpt' else r'$\\mathit{\\phi}^{*}_{\\eta}$')+' Bin',
        'x_errors': len(MCLIST)*[1,0,0]+4*[0],
        'y_log': True,
        'y_lims': [1e0,1e10],
        'y_errors': len(MCLIST)*3*[True]+4*[False],
        'step': len(MCLIST)*3*[False]+2*[True]+2*[True],
        'line_styles': len(MCLIST)*3*['']+2*['-']+2*['-'],
        'markers': [('.',MARKERDICT[x],MARKERDICT[x]) for x in MCLIST]+['fill']*2+['']*2,
        'nicks_whitelist': MCLIST+['stats','model'],
        'nicks_blacklist': ['unity','unc'],
        #'marker_fill_styles': ['none'],
        #'edgecolors': ['pink'],
        'colors': [('dark'+COLORDICT[x],COLORDICT[x],COLORDICT[x]) for x in MCLIST]+['yellow','white','black','black'],
        #'y_subplot_lims': [0.95,1.05],
        #'y_subplot_lims': [0.75,1.25],
        'y_subplot_lims': [0.9,1.1],
        'texts': [''],
        'texts_x': [0], 
        'texts_y': [0], 
        'texts_size': [20],
        'labelsize': 25,
    })
    if not 'toy' in mc:
        d0['labels'][len(MCLIST)]   = LABELDICT[mc]+" Stat. Unc."
        #d0['labels'][len(MCLIST)+2] = LABELDICT[mc]+" Syst. Unc."
        d0['labels'][len(MCLIST)+1] = " "
        d0['nicks_blacklist']+=['model']
    i=0
    d1 = deepcopy(d0)
    d1['analysis_modules'] = ['NormalizeByBinWidth']+d0['analysis_modules']
    d1['histograms_to_normalize_by_binwidth'] = ['unc_'+x for x in varlist]
    d1['x_bins'] = [' '.join([str(x) for x in l_obsbinedges])]
    d1['x_errors'] = len(MCLIST)*[1,0,1]+4*[0]
    d1['filename'] = obs+'_ybins'
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = deepcopy(d0)
            d.update({
                'files': filelist_binned,
                'x_expressions': len(MCLIST)*['gen'+obs+namestring,'unfolded'+obs+namestring]+['uncertainty_'+x+namestring for x in varlist],
                #'www': 'comparison_unfolding_samples'+cut+postfix+'_'+data+'_by_'+mc+match+
                'x_label': obs,
                'y_label': 'Unfolded/Gen',
                'x_log': True,
                'y_lims': [0.9,1.1],
                'y_log': False,
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'texts': [  r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$" if CMSLABEL else "",
                            r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'nicks_whitelist': ['stats','model','ratio'],
                'x_errors': 4*[0]+len(MCLIST)*[1],
                'labels': ["Toy Stat. Unc.","","Toy Syst. Unc.",""
                            ]+[(LABELDICT[x]+' (chi2/ndf={:.3f})'.format(calculate_closure_chi2(args,obs,cut,x,mc,match,postfix,int(2*ybmin),int(2*ysmin)))) for x in MCLIST],
                'y_errors': 4*[False]+len(MCLIST)*[True],
                'step': 2*[True]+2*[True]+len(MCLIST)*[False],
                'line_styles': 2*['']+2*['-']+len(MCLIST)*[''],
                'markers': 2*['fill']+2*['']+[MARKERDICT[x] for x in MCLIST],
                'colors': ['yellow','white','black','black']+[COLORDICT[x] for x in MCLIST],
                'texts_size': [20],
                'texts_x': [0.03],
                'texts_y': [1.07,0.97],
                'subplot_nicks': ['dummy'],
                #'legend_cols': 2,
                'legend': 'lower left',
            })
            if not 'toy' in mc:
                d.update({
                'nicks_whitelist': ['stats','ratio'],
                'x_errors': 2*[0]+len(MCLIST)*[1],
                'labels': [LABELDICT[x]+" Stat. Unc.",""
                            ]+[(LABELDICT[x]+' (chi2/ndf={:.3f})'.format(calculate_closure_chi2(args,obs,cut,x,mc,match,postfix,int(2*ybmin),int(2*ysmin)))) for x in MCLIST],
                'y_errors': 2*[False]+len(MCLIST)*[True],
                'step': 2*[True]+len(MCLIST)*[False],
                'line_styles': 2*['']+len(MCLIST)*[''],
                'markers': 2*['fill']+[MARKERDICT[x] for x in MCLIST],
                'colors': ['yellow','white']+[COLORDICT[x] for x in MCLIST],
                })
            d['www'] = d['www']+'/unfolded'+namestring
            if ysmin==2.0:
                d['y_lims'] = [0.5,1.5]
            elif ybmin==2.0:
                d['y_lims'] = [0.75,1.25]
            elif ysmin+ybmin>1.0:
                d['y_lims'] = [0.65,1.35]
            #d0['texts']   += [x+' (chi2/ndf={:.3f})'.format(calculate_closure_chi2(args,obs,cut,x,mc,match,postfix,int(2*ybmin),int(2*ysmin))) for x in MCLIST]
            #d0['texts_y'] += [1-0.05*(x+1) for x in xrange(len(MCLIST))]
            plots.append(d)
    if obs == 'zpt':
        d0['texts_x'] += reduce(lambda x,y : x+y,[[0.001+x/265.0]*len(MCLIST) for x in [0, 19, 38, 57, 76, 93, 112, 131, 150, 167, 186, 205, 222, 239, 256]])
    elif obs == 'phistareta':
        d0['texts_x'] += reduce(lambda x,y : x+y,[[0.001+x/232.0]*len(MCLIST) for x in [0, 18, 36, 54, 72, 85, 103, 121, 139, 152, 170, 188, 201, 214, 227]])
    d0['figsize'] = [36,6]
    #d0['plot_modules'] = ['ExportRoot']
    d0['legend'] = None
    d0['vertical_lines'] = l_obsbinedges
    d0['vertical_lines_styles'] = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    #plots.append(d0)
    #plots.append(d1)
  return [PlottingJob(plots=plots, args=args)]

#def plot_uncertainty_3Dhist(args=None, cut='_jet1pt20', data='BCDEFGH', mc='toy', match='', postfix=''):
def plot_uncertainty_3Dhist(args=None, cut='_jet1pt20', data='17Jul2018', mc='toy', match='', postfix=''):
  plots = []
  varlist = ['stat','total','lumi','bkg','eff','unf','jec','jer']#,'muon']
  #varlist = ['stat','bkg','eff','unf','jec','jer']#,'muon']'lumi',
  for obs in ['zpt','phistareta']:
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    if not data in ['BCDEFGH','17Jul2018']:
        print "WARNING: uncertainties are meant for data only!"
        return
    filelist = [PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_'+data+match+'_total.root']
    #filelist = [PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_'+data+match+'_'+var+'.root' for var in varlist]
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    d0 = ({
        'files': filelist,
        'folders': [''],
        'nicks': varlist,
        'x_expressions': ['uncertainty_'+var for var in varlist],
        'filename': obs,
        #'analysis_modules': ['QuadraticSumOfHistograms'],
        #'quad_sum_nicks': [' '.join(varlist[1:])],
        #'quad_sum_result_nicks': ['total'],
        #'nicks_whitelist': ['stat','total']+varlist[1:],
        'labels': ['Statistical','Total systematic','Background','Efficiency','Unfolding','JEC','JER'],#'Muon Scale','Luminosity'
        'alphas': [0.5],
        'y_errors': False,
        'y_lims': [0.0,0.1],
        'y_label': "Relative Uncertainty",
        'www': 'comparison_uncertainties'+cut+postfix+'_'+data+'_by_'+mc+match,
        'step': [True],
        'legend': None,
        #'figsize': [36,6],
        #'legend_cols': 8,
        'line_styles': ['-'],
        'markers': ['fill','o','v','^','>','<','s','D'],#,'p'],
        'x_label': (r'$\\mathit{p}_T^Z$' if obs =='zpt' else r'$\\mathit{\\phi}^{*}_{\\eta}$')+' Bin',
        'texts_size': [20],
        'labelsize': 25,
    })
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = deepcopy(d0)
            d.update({
                'files': filelist_binned,
                'x_expressions': ['uncertainty_'+var+namestring for var in varlist],
                'x_log': True,
                'texts': [  r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$" if CMSLABEL else "",
                            r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'x_lims': [25,1000] if obs =='zpt' else [0.4,50],
                'x_label': obs,
                'texts_y': [1.05,0.97],
            })
            if ysmin>1.5:
                d['y_lims'] = [0,0.25]
                d['vertical_lines'] = [250 if obs =='zpt' else 5]
            elif ysmin>1.0:
                d['y_lims'] = [0,0.2]
            elif ysmin>0.5:
                d['y_lims'] = [0,0.15]
            elif ybmin+ysmin>1:
                d['y_lims'] = [0,0.16]
            d['www'] = d0['www']+'/uncertainties'+namestring
            plots.append(d)
    d0['figsize'] = [36,6]
    d0['vertical_lines'] = l_obsbinedges
    d0['vertical_lines_styles'] = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    d0['legend'] = 'upper left'
    #plots.append(d0)
  return [PlottingJob(plots=plots, args=args)]


def plot_unfolding_correction(args=None, obs='zpt', cut='_jet1pt20', data='17Jul2018', match='', postfix=''):
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    #unfold_by_inversion_3Dhist(args,obs,cut,data,mc,match,postfix)
    #unf_source  = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    #data_source = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+match+'.root'
    #filelist = [unf_source,data_source]
    #filelist = [PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+match+'.root']
    unfold_by_tunfold_3Dhist(args,obs,cut,data,'toy',match,postfix)
    #filelist = [PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_toy'+match+'.root']
    filelist = [PLOTSFOLDER+cut+postfix+'/crosssection_'+obs+'_'+data+match+'.root']
    samples = ['toy','toy0','toy2']#+MCLIST
    for mc in samples:
        #unfold_by_inversion_3Dhist(args,obs,cut,sample,mc,match,postfix)
        unfold_by_tunfold_3Dhist(args,obs,cut,data,mc,match,postfix)
        filelist.append(PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root')
    filelist.append(PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_'+data+'_model_toy'+match+'.root')
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    plots = []
    d0 = ({
        'files': filelist,
        'folders': [''],
        'nicks':         ['sig']+['unfby'+mc for mc in samples]+['unc_model'],
        #'x_expressions': ['signal'+obs]+len(samples)*['unfolded'+obs]+['uncertainty_model_toy'],
        'x_expressions': ['crossection_'+obs]+len(samples)*['unfolded'+obs]+['uncertainty_model_toy'],
        'analysis_modules': ['Ratio','SumOfHistograms'],
        #'ratio_denominator_no_errors': False,
        'ratio_numerator_nicks': ['sig']+['unfby'+mc for mc in samples],
        'ratio_denominator_nicks': ['sig'],
        'ratio_result_nicks': ['unity']+['ratio'+mc for mc in samples],
        'sum_nicks' : ['unity unc_model','unity unc_model'],
        'sum_scale_factors' : ['1 1', '1 -1'],
        'sum_result_nicks': ['model_up','model_down'],
        'subplot_nicks': ['model','ratio'],
        'y_subplot_label': 'Ratio',
        'subplot_fraction': 40,
        'filename': obs,
        'x_label': obs,
        'x_errors': [1],
        'y_errors': [1]*(1+len(samples))+2*[0]+[1]*len(samples),
        #'subplot_legend': 'lower left',
        'y_log': True,
        'y_subplot_lims': [0.98,1.02],
        'www': 'comparison_unfolding_'+data+cut+match+postfix,
        #'nicks_whitelist': ['sig']+samples+['model_up','model_down'],
        'nicks_blacklist': ['unity','unc_model'],
        #'labels': ['Unfolded','Signal','Unfolded/Signal'],
        #'alphas': [0.5],
        'markers': ['.']+[MARKERDICT[x] for x in samples]+2*['fill']+[MARKERDICT[x] for x in samples],
        'colors': ['black']+[COLORDICT[x] for x in samples]+['yellow','white']+['dark'+COLORDICT[x] for x in samples],
    })
    #if not data in ['BCD','BCDEFGH']:
    #    d0.update({
    #        'files': filelist,
    #        'nicks': ['unf','gen','sig','reco'],
    #        'x_expressions': ['unfolded'+obs,'gen'+obs,'signal'+obs,obs],
    #        'ratio_numerator_nicks': ['unf','gen'],
    #        'ratio_denominator_nicks': ['sig','reco'],
    #        'colors': ['black','blue','red','green','blue','red'],
    #        'labels': ['Unfolded','Gen','Signal','Reco','Unfolded/Signal','Gen/Reco'],
    #    })
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = deepcopy(d0)
            d.update({
                'files': filelist_binned,
                'x_expressions': ['unfolded'+obs+namestring,'signal'+obs+namestring],
                'x_log': True,
                'x_ticks': [30,50,100,200,400,1000],
                'y_label': 'Events per binsize',
                'analysis_modules': ['NormalizeByBinWidth','Ratio'],
                'www': 'comparison_unfold'+cut+match+postfix+'_'+data+'_by_'+mc+'/unfold'+namestring,
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
            })
            if not data in ['BCD','BCDEFGH']:
              d.update({
                'files': filelist_binned,
                'x_expressions': ['unfolded'+obs+namestring,'gen'+obs+namestring,'signal'+obs+namestring,obs+namestring],
              })
            #plots.append(d)
    d0['analysis_modules'] = ['NormalizeByBinWidth']+d0['analysis_modules']
    #d0['histograms_to_normalize_by_binwidth'] = ['unc_model']
    #d0['x_bins'] = [' '.join([str(x) for x in l_obsbinedges[:-1]+[l_obsbinedges[-1]-7+i for i in xrange(8)]])]
    #d0['x_bins'] = [' '.join([str(x) for x in l_obsbinedges])]
    d0['figsize'] = [36,6]
    #d0['figsize'] = [12,12]
    d0['vertical_lines'] = l_obsbinedges
    d0['vertical_lines_styles'] = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    plots.append(d0)
    return [PlottingJob(plots=plots, args=args)]

def plot_crosssections(args=None,cut='_jet1pt20',data='17Jul2018',mc='NNLO',match='',postfix='',pdf='NNPDF31_nnlo_as_0118'):
  plots=[]
  for obs in ['zpt','phistareta']:
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    unfold_by_tunfold_3Dhist(args,obs,cut,data,'toy0',match,postfix)
    #unfold_by_inversion_3Dhist(args,obs,cut,data,'amc',match,postfix)
    #write_data(args,obs,cut,data,match,postfix)
    data_source = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_toy0'+match+'.root'
    if mc in ['LO','NLO','NNLO']:
        write_theory(args,obs,cut,postfix,mc,pdf)
        mc_source   = PLOTSFOLDER+cut+postfix+'/theory/'+obs+'_'+mc+'_'+pdf+'.root'
    else:
        mc_source   = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+mc+match+'.root'
    unc_source  = PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_'+data+match+'_total_stat.root'
    filelist = [data_source,mc_source,unc_source]
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    ybins = [0.0,0.5,1.0,1.5,2.0,2.5]
    ylist = [((xb,yb),(xs,ys))  for (xs,ys) in zip(ybins[:-1],ybins[1:]) for (xb,yb) in zip(ybins[:-1],ybins[1:]) if xb+xs<2.5]
    markerlist = ['^','1','d','+','*','<','2','o','x','>','3','s','v','4','p']
    #markerlist = ['^','D','p','s','>','p','o','s','D','^','v','<','v','>','p']
    #markerlist = ['D','s','o','v','p','^','s','o','v','^','o','v','^','v','p']
    markerfilllist = 5*['top']+4*['left']+3*['right']+2*['bottom']+['full']
    colorlist = ['red','salmon','crimson','violet','brown','blue','cyan','royalblue','teal','orange','gold','yellow','green','lime','purple']
    scalelist = [1e20,1e19,1e18,1e17,1e16,1e13,1e12,1e11,1e10,1e7,1e6,1e5,1e2,1e1,1e0]
    #scalelist = [1e28,1e26,1e24,1e22,1e10,1e20,1e18,1e16,1e8,1e14,1e12,1e6,1e4,1e2,1e0]
    #scaling = [1e6,1e5,1e4,1e3,1e0,1e6,1e5,1e4,1e1,1e6,1e5,1e2,1e3,1e3,1e0]
    namelist = ['_yb{}_ys{}'.format(int(2*yboost[0]),int(2*ystar[0])) for (yboost,ystar) in ylist]
    d = ({
        'www': 'crosssections_'+data+'_'+mc+cut+postfix,
        'files': [filelist_binned],
        'folders': [''],
        'x_expressions': [('unfolded'+obs+name,'gen'+obs+name,'uncertainty_total_stat'+name) for name in namelist],
        'nicks':       [('unf'+name,'gen'+name,'unc'+name) for name in namelist],
        'analysis_modules': ['ScaleHistograms','NormalizeByBinWidth'],
        'scale_nicks':  [('unf'+name,'gen'+name) for name in namelist],
        #'scales': [1e0/35.9/1000],
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
        'marker_fill_styles': ['none'],#[(x,x) for x in markerfilllist],
        'markeredgewidth': 2.5,
        'markersize': 12,
        #'labelsize': 30,
        'labelsize': 40,
        'markers': [(x,'') for x in markerlist],
        'colors': [('black',x) for x in colorlist],
        'alphas': [0.707],
        'nicks_blacklist': ['unc'],
        'labels': [('bin'+x,'bin'+x) for x in namelist],
        'filename': obs,
        'x_label': obs,#(r'$\\mathit{p}_T^Z$' if obs =='zpt' else r'$\\mathit{\\phi}^{*}_{\\eta}$')+' Bin',
        'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
        'legend': None,
        #'legend_cols': 2,
        #'legend': 'upper left',
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
    d0 = deepcopy(d)
    n = 1
    d0.update({
        'filename': obs+'_ratio',
        'analysis_modules': ['Ratio','AddHistograms'],#,'Errorband'],
        'ratio_numerator_nicks':   [('unc'+name,  'gen'+name,  'unf'+name,  'unf'+name) for name in namelist],
        'ratio_denominator_nicks': [('unc'+name,  'gen'+name,  'unf'+name,  'gen'+name) for name in namelist],
        'ratio_result_nicks':    [('unity'+name,'scale'+name, 'stat'+name,'ratio'+name) for name in namelist],
        'add_nicks':             [('unity'+name+' ratio'+name,'unity'+name+' scale'+name,'unity'+name+' stat'+name,'unity'+name+' unc'+name,'unity'+name+' unc'+name) for name in namelist],
        'add_result_nicks': [('stacked1'+name,'stacked2'+name,'stacked3'+name,'up'+name,'down'+name) for name in namelist],
        #'errorband_histogram_nicks': [('stacked'+name+' unc'+name+' unc'+name) for name in namelist],
        #'errorband_result_nicks': ['errorband'+name for name in namelist],
        #'errorband_percentage_error': [True],
        #'markers': markerlist+2*len(namelist)*['fill'],
        'step':         2*len(namelist)*[0] +2*len(namelist)*[1],
        'line_styles':  2*len(namelist)*['']+2*len(namelist)*['-'],
        'line_widths': [1.5],
        'labels': 2*['bin'+x for x in namelist]+2*len(namelist)*['Unc'],
        'x_errors': [0],#2*len(namelist)*[0]+len(namelist)*[0]+2*len(namelist)*[0],
        'y_errors': [0],#2*len(namelist)*[0]+len(namelist)*[0]+2*len(namelist)*[0],
        'markers': markerlist[:len(namelist)]+len(namelist)*['errorband']+2*len(namelist)*[''],
        'colors':  len(namelist)*['black']+colorlist[:len(namelist)]+2*len(namelist)*['black'],
        'nicks_whitelist': ['stacked1','stacked2','up','down'],
        'subplot_nicks': ['dummy'],
        'y_log': False,
        'lines_styles': ['-',':',':'],
        'y_label': 'Ratio to theory',
        'y_lims': [0.5,15.5],
        #'add_scale_factors': [(str(len(ylist)-x-1)+' 1',str(len(ylist)-x-1)+' 1',str(len(ylist)-x-1)+' 1',str(len(ylist)-x) + ' 1',str(len(ylist)-x) + ' -1') for x in xrange(len(ylist))],
        'add_scale_factors': [((str(len(ylist)-x-1)+' 1',str(len(ylist)-x-1)+' 1',str(len(ylist)-x-1)+' 1',str(len(ylist)-x) + ' 1',str(len(ylist)-x) + ' -1') if not x==11 else ('0 0','0 0','0 0','0 0')) for x in xrange(len(ylist))],
        'lines': [(0.5+x,0.75+x,1.25+x) for x in xrange(len(namelist))],
        'y_ticks': [(0.75+x,1.0+x,1.25+x) for x in xrange(len(namelist))],
        #'add_scale_factors': [(str(n*(len(ylist)-x)-1)+' 1',str(n*(len(ylist)-x)-1)+' 1',str(n*(len(ylist)-x)-1)+' 1',str(n*(len(ylist)-x)) + ' 1',str(n*(len(ylist)-x)) + ' -1') for x in xrange(len(ylist))],
        #'lines': [(n*(0.5+x),n*(0.75+x),n*(1.25+x)) for x in xrange(len(namelist))],
        #'y_lims': [n*0.5,n*15.5],
        #'y_lims': [-30,30],
        'y_ticks': [(n*(0.75+x),n*(1.0+x),n*(1.25+x)) for x in xrange(len(namelist))],
        'texts_x':[0.03,(0.65 if obs =='zpt' else 0.66)],
    })
    #d0['figsize'] = [8,16]
    #d['figsize'] = [36,6]
    #d['vertical_lines'] = l_obsbinedges
    #d['vertical_lines_styles'] = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    plots.append(d)
    plots.append(d0)
  return [PlottingJob(plots=plots, args=args)]

#def plot_crosssections_3Dhist(args=None,cut='_jet1pt20',data='17Jul2018',match='',postfix='',pdf='NNPDF31_nnlo_as_0118',mclist=['LO','NLO','NNLO']):
def plot_crosssections_3Dhist(args=None,cut='_jet1pt20',data='17Jul2018',match='',postfix='',pdf='NNPDF31_nnlo_as_0118',mclist=['NLO','NNLO']):
#def plot_crosssections_3Dhist(args=None,cut='_jet1pt20',data='17Jul2018',match='',postfix='',pdf='',mclist=['mad','amc']):
  plots=[]
  for obs in ['zpt','phistareta']:
    for mc in mclist:
      if 'LO' in mc:
        write_theory(args,obs,cut,postfix,mc,pdf)
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    data_source = [PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_toy0'+match+'.root']
    mc_source   = [PLOTSFOLDER+cut+postfix+'/theory/'+obs+'_'+x+'_'+pdf+'.root' if 'LO' in x else
                   PLOTSFOLDER+cut+postfix+'/'+obs+'_'+x+match+'.root' for x in mclist]
    unc_source  = [PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_'+data+match+'_total.root']
    filelist =  data_source+mc_source+unc_source
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    d0 = ({
        'www': 'crosssections_'+data+'_'+'_'.join(mclist)+('_'+pdf if not pdf=='' else pdf)+cut+postfix,
        'files': filelist,
        'x_expressions': ['unfolded'+obs]+len(mclist)*['gen'+obs]+['uncertainty_total'],
        'x_label': (r'$\\mathit{p}_T^Z$' if obs =='zpt' else r'$\\mathit{\\phi}^{*}_{\\eta}$')+' Bin',
        'x_errors': [0],
        'folders': [''],
        'lumis': [35.9],
        'energies':[13],
        'nicks': ['data']+mclist+['uncertainty'],
        'analysis_modules': ['ScaleHistograms','NormalizeByBinWidth','Ratio','SumOfHistograms'],
        #'weights': ['1']+['{}'.format(6225.42/5941.0 if x=='amc' else 1) for x in mclist]+['1'],
        'scale_nicks':  ['data']+mclist,
        'scales': [1e0/35.9/1000*(5941.0/6225.42 if x=='amc' else 1) for x in ['data']+mclist],
        'histograms_to_normalize_by_binwidth': ['data']+mclist,
        'ratio_numerator_nicks':   ['uncertainty']+['data']+2*mclist,
        'ratio_denominator_nicks': ['uncertainty']+(1+2*len(mclist))*['data'],
        'ratio_result_nicks': ['unity']+['ratio'+x for x in ['data']+mclist]+['unc'+x for x in mclist],
        'sum_nicks': ['unity uncertainty','unity uncertainty'],
        'sum_scale_factors': ['1 1','1 -1'],
        'sum_result_nicks': ['unc_up','unc_down'],
        'nicks_blacklist': ['unity','uncertainty'],
        'filename': obs,
        'markers': ['.']+[MARKERDICT[x] for x in mclist]+['','','errorband']+[MARKERDICT[x] for x in mclist]+len(mclist)*['errorband'],
        #'markers': ['.']+['^','s','o']+['','','errorband']+['^','s','o']+3*['errorband'],
        'colors': ['black']+[COLORDICT[x] for x in mclist]+2*['black']+['steelblue']+2*[COLORDICT[x] for x in mclist],
        #'colors': ['black']+['green','blue','red']+2*['black']+['steelblue']+2*['green','blue','red'],
        'alphas': (3+len(mclist))*[1]+[0.707]+2*len(mclist)*[0.3],
        'step': True,
        'line_styles': ['-'],
        'y_log': True,
        'y_lims': [1e-6,1e1] if obs =='zpt' else [1e-5,1e3],
        'y_errors': False,
        'y_subplot_lims': [0.75,1.25],
        'y_label': 'Events per binwidth',
        'y_subplot_label': 'Ratio to Data',#'Sim/Data' if 'amc' in mclist else 'Theory/Data',
        'subplot_legend': 'lower left',
        'subplot_nicks': ['ratio','unc'],
        'labels': ['Data']+[LABELDICT[x] for x in mclist]+['Syst. Unc','','Stat. Unc']+2*len(mclist)*[''],
        #'labels': ['Data']+[mclist]+['Syst. Unc','','Stat. Unc']+2*len(mclist)*[''],
        'labelsize': 25,
    })
    if obs == 'zpt':
        d0['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\mathit{p}_T^Z dy_b dy^*}/(\\frac{pb}{GeV})$'
    elif obs == 'phistareta':
        d0['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\phi^{*}_{\\eta} dy_b dy^*}/pb$'
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = deepcopy(d0)
            d.update({
                'files': filelist_binned,
                'x_label': obs,
                'x_log': True,
                'x_ticks': [30,60,100,200,400,1000] if obs=='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'x_lims': [25,1000] if obs=='zpt' else [0.4,50],
                'texts_size': [20],
                'texts_x': [0.02],
                'subplot_fraction': 50,
                'texts': [r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary}$" if CMSLABEL else "",
                          r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'texts_y': [1.10,0.97],
            })
            d['x_expressions'] = [x+namestring for x in d0['x_expressions']]
            d['www'] = d0['www']+'/xsec'+namestring
            if ysmin>1.5: 
                d['y_subplot_lims'] = [0.0,2.0]
                d['vertical_lines'] = [250 if obs =='zpt' else 5]
            elif ysmin+ybmin>1.0:
                d['y_subplot_lims'] = [0.5,1.5]
            #if not (obs=='phistareta' and 'NLO' in mclist):
            plots.append(d)
    d0['figsize'] = [36,6]
    #d0['legend'] = None
    d0['vertical_lines'] = l_obsbinedges
    d0['vertical_lines_styles'] = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    #plots.append(d0)
  return [PlottingJob(plots=plots, args=args)]




def write_results_to_txt(args=None,obs='phistareta',cut='_jet1pt20',data='BCDEFGH',mc='mad',match='', postfix=''):
    unfold_by_inversion_3Dhist(args,obs,cut,data,mc,match,postfix)
    create_uncertainties(args,obs,cut,data,match,postfix,varquantity='_total')
    data_source = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    unc_source  = PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_'+data+match+'_total.root'
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
                'filename': PLOTSFOLDER+cut+postfix+'/results/'+obs+namestring,
                #'output_dir': PLOTSFOLDER+cut+postfix+'/results',
                #'www': 'test/uncertainties'+namestring,
            })
            if not ybmin+ysmin>2:
                plots.append(d)
    return [PlottingJob(plots=plots, args=args)]


#args,obs,cut,data,match,postfix = None,'zpt','_jet1pt20','BCDEFGH','',''
#PLOTSFOLDER = '/portal/ekpbms2/home/tberger/ZJtriple/ZJtriple_2019-06-30'


def write_data(args=None,obs='zpt',cut='_jet1pt20',data='BCDEFGH',match='',postfix=''):
    h_xsec = prepare_3Dhist(args, obs)[2]
    #toylist = ['toy0','toy2']
    toylist = ['toy0']
    #unclist = ['_statistical','_lumi','_bkg','_IDSF','_IsoSF','_TriggerSF','_stats_toy','_JEC','_Robs','_Ryz','_Ryj','_A','_F','_switch','_model_toy']
    unclist = ['stat','lumi','bkg','eff','unf','jec','mod']
    filelist = [PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+toy+match+'.root' for toy in toylist]
    #uncfilelist = [ PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_'+data+match+unc+'.root' for unc in unclist]
    output_file = PLOTSFOLDER+cut+postfix+'/'+obs+'_2016'+match+'.root'
    if data in ['mad','amc','hpp']:
        output_file = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_toy'+match+'.root'
    for f in filelist:
        f_in = ROOT.TFile(f,"READ")
        h_in = f_in.Get('unfolded'+obs)
        for i in xrange(h_xsec.GetNbinsX()):
            h_xsec.SetBinContent(i+1,h_xsec[i+1]+h_in[i+1]/len(filelist))
    f_unc = ROOT.TFile(PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_'+data+match+'_statistical.root','READ')
    h_unc = f_unc.Get("uncertainty_statistical")
    for i in xrange(h_xsec.GetNbinsX()):
            h_xsec.SetBinError(i+1,h_xsec[i+1]*h_unc[i+1])
    f_out = ROOT.TFile(output_file,"RECREATE")
    h_xsec.Write('unfolded'+obs if data in ['mad','amc','hpp'] else 'gen'+obs)
    print "crosssection written to",output_file
    return


def write_theory(args=None,obs='phistareta',cut='_jet1pt20',postfix='',order='LO',pdf='NNPDF31_nnlo_as_0118',unc='',subprocess=False):
#def write_theory(args=None,obs='zpt',cut='_jet1pt20',postfix='',order='LO',pdf='CT14nnlo',unc='',subprocess=False):
    [d, cutstring, gencutstring, weightstring, namestring] = basic_xsec(args,obs)
    [l_obshists, h_reco, h_gen, h_recoresponse, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args, obs)
    ybins = [0.0,0.5,1.0,1.5,2.0,2.5]
    ylist = [((xb,yb),(xs,ys))  for (xs,ys) in zip(ybins[:-1],ybins[1:]) for (xb,yb) in zip(ybins[:-1],ybins[1:]) if xb+xs<2.5]
    dpdf = ({  'CT14nlo': '0', 'MMHT2014nlo68cl': '1', 'NNPDF30_nlo_as_0118': '2', 'PDF4LHC15_nlo_mc': '3'})
    dorder = ({'LO': '1', 'NLO': '2', 'NNLO': '0'})
    obsexp = (obs if not obs=='zpt' else 'ptz')
    if not subprocess:
      for ((xb,yb),(xs,ys)) in ylist:
        if pdf in ['NNPDF31_nnlo_as_0118','MMHT2014nnlo68cl','ABMP16als118_5_nnlo','CT14nnlo','NNPDF31_nlo_as_0118']:
            input_file = ("/ceph/tberger/ZJtriple_tables/ZJtriple_"+obsexp+"/ZJ.NNLO.ZJtriple_yb{}_ystar{}_"+obsexp+"_"+pdf+"_L6.root").format(int(2*xb),int(2*xs))
            central_name    = "h"+dorder[order]+"100100"
            up_name_pdf     = "h"+dorder[order]+"100101"
            down_name_pdf   = "h"+dorder[order]+"100102"
            up_name_scale   = "h"+dorder[order]+"100108"
            down_name_scale = "h"+dorder[order]+"100109"
        else:
            input_file = ("/ceph/tberger/ZJtriple_tables/ZJtriple_"+obsexp+"/ZJ.NNLO.ZJtriple_yb{}_ystar{}_"+obsexp+".root").format(int(2*xb),int(2*xs))
            central_name    = "h"+dorder[order]+"1001"+dpdf[pdf]+"0"
            up_name_pdf     = "h"+dorder[order]+"1001"+dpdf[pdf]+"1"
            down_name_pdf   = "h"+dorder[order]+"1001"+dpdf[pdf]+"2"
            up_name_scale   = "h"+dorder[order]+"1001"+dpdf[pdf]+"8"
            down_name_scale = "h"+dorder[order]+"1001"+dpdf[pdf]+"9"
        f_in = ROOT.TFile(input_file,"READ")
        h_central = f_in.Get(central_name)
        h_up_pdf      = f_in.Get(up_name_pdf)
        h_down_pdf    = f_in.Get(down_name_pdf)
        h_up_scale      = f_in.Get(up_name_scale)
        h_down_scale    = f_in.Get(down_name_scale)
        y_index = l_ybinedges[int(2*xs)]+int(2*xb)
        #for j in xrange(h_central.GetNbinsX()):
        #    obs_index = l_obsbinedges[y_index]+j+1
        #    h_gen.SetBinContent(obs_index,h_central[j+1]*35.9*1000*h_central.GetBinWidth(j+1))
        #    if unc == 'pdf':
        #        h_gen.SetBinError(obs_index,h_gen[obs_index]*max(abs(h_up_pdf[j+1]),abs(h_down_pdf[j+1])))
        #    elif unc == 'scale':
        #        h_gen.SetBinError(obs_index,h_gen[obs_index]*max(abs(h_up_scale[j+1]),abs(h_down_scale[j+1])))
        #    else:
        #        h_gen.SetBinError(obs_index,h_gen[obs_index]*np.sqrt(max(abs(h_up_scale[j+1]),abs(h_down_scale[j+1]))**2+max(abs(h_up_pdf[j+1]),abs(h_down_pdf[j+1]))**2))
        for j in xrange(l_obshists[y_index].GetNbinsX()):
          obs_index = l_obsbinedges[y_index]+j+1
          ##################################################################################################################################################################
          # skip bin number 10 to compensate the missing bin in phistareta tables:
          if (y_index+1 not in [5,9,12,13,14,15] and obs=='phistareta'):
            j = j-1 if j>10 else j
            k = 1 if not j==10 else 0.5
            h_gen.SetBinContent(obs_index,k*h_central[j+1]*35.9*1000*h_central.GetBinWidth(j+1))
            if unc == 'pdf':
                h_gen.SetBinError(obs_index,k*h_gen[obs_index]*max(abs(h_up_pdf[j+1]),abs(h_down_pdf[j+1])))
            elif unc == 'scale':
                h_gen.SetBinError(obs_index,k*h_gen[obs_index]*max(abs(h_up_scale[j+1]),abs(h_down_scale[j+1])))
            else:
                h_gen.SetBinError(obs_index,k*h_gen[obs_index]*np.sqrt(max(abs(h_up_scale[j+1]),abs(h_down_scale[j+1]))**2+max(abs(h_up_pdf[j+1]),abs(h_down_pdf[j+1]))**2))

          else:
          ##################################################################################################################################################################
            h_gen.SetBinContent(obs_index,h_central[j+1]*35.9*1000*h_central.GetBinWidth(j+1))
            if unc == 'pdf':
                h_gen.SetBinError(obs_index,h_gen[obs_index]*max(abs(h_up_pdf[j+1]),abs(h_down_pdf[j+1])))
            elif unc == 'scale':
                h_gen.SetBinError(obs_index,h_gen[obs_index]*max(abs(h_up_scale[j+1]),abs(h_down_scale[j+1])))
            else:
                h_gen.SetBinError(obs_index,h_gen[obs_index]*np.sqrt(max(abs(h_up_scale[j+1]),abs(h_down_scale[j+1]))**2+max(abs(h_up_pdf[j+1]),abs(h_down_pdf[j+1]))**2))
      output_file = PLOTSFOLDER+cut+postfix+'/theory/'+obs+'_'+order+'_'+pdf+'.root'
      f_out = ROOT.TFile(output_file,"RECREATE")
      h_gen.Write()
      h_reco.Write()
      print "file written to",output_file
      return
    else:
      subproc_list = ['gg','qg','qq', 'aqaq','qaq','gaq']#,'q-q','q+q','q=q','q!q','aq=aq']
      output_file = PLOTSFOLDER+cut+postfix+'/theory/'+obs+'_'+order+'_'+pdf+'_subprocesses.root'
      f_out = ROOT.TFile(output_file,"RECREATE")
      for subproc in subproc_list:
        for ((xb,yb),(xs,ys)) in ylist:
          input_file = ("/ceph/tberger/ZJtriple_tables/ZJtriple_"+obsexp+"/ZJ."+order+".ZJtriple_yb{}_ystar{}_"+obsexp+"_"+pdf+"_subprocesses.root").format(int(2*xb),int(2*xs))
          f_in = ROOT.TFile(input_file,'READ')
          h_all = f_in.Get('all')
          h_subproc = f_in.Get(subproc)
          y_index = l_ybinedges[int(2*xs)]+int(2*xb)
          #for j in xrange(h_all.GetNbinsX()):
          #  obs_index = l_obsbinedges[y_index]+j+1
          #  h_gen.SetBinContent(obs_index,h_subproc[j+1]/h_all[j+1])
          #  h_gen.SetBinError(obs_index,0)
          for j in xrange(l_obshists[y_index].GetNbinsX()):
            obs_index = l_obsbinedges[y_index]+j+1
            # skip bin number 10 to compensate the missing bin in phistareta tables:
            if (y_index+1 not in [5,9,12,13,14,15] and obs=='phistareta'):
                j = j-1 if j>10 else j
            try:
                h_gen.SetBinContent(obs_index,h_subproc[j+1]/h_all[j+1])
            except ZeroDivisionError:
                h_gen.SetBinContent(obs_index,0)
            h_gen.SetBinError(obs_index,0)
            ########################################################################
        f_out.cd()
        h_gen.Write(obs+'_'+subproc)
      print "file written to",output_file
      return
      
def unfold_3Dhist(args=None,obs='zpt',cut='_jet1pt20',data='amc',mc='toy',match='',postfix='',method='dagostini', variation=0, varquantity=''):
    output_file = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'_'+method+'.root'
    input_file = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+mc+match+'.root'
    if not mc == 'toy':
        variation = 0
    if not variation == 0:
        input_file = PLOTSFOLDER+cut+postfix+'/'+obs+'_toy'+match+varquantity+str(variation)+'.root'
    #if os.path.exists(output_file):
    #    print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
    #    return
    plots = []
    d=({
        'files': [  input_file,
                    PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+'.root',
                    input_file,
                    input_file,
                    #PLOTSFOLDER+cut+'/'+obs+'_NLO'+match+postfix+'.root',
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
        backgroundlist = ['TT','TW','WW','WZ','ZZ']
        d['files']+= [PLOTSFOLDER+cut+'/'+obs+'_'+x+match+postfix+'.root' for x in backgroundlist]
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


def plot_Kfactors(args=None,cut='_jet1pt20',data='17Jul2018',match='',postfix='',pdf='NNPDF31_nnlo_as_0118'):
 plots=[]
 #for pdf in ['NNPDF30_nlo_as_0118','ABMP16als118_5_nnlo','CT14nnlo_as_0118','NNPDF31_nnlo_as_0118','MMHT2014nnlo68cl']:
 for obs in ['zpt','phistareta']:
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    #write_data(args,obs,cut,data,match,postfix)
    write_theory(args,obs,cut,postfix,'LO'  ,pdf,'scale')
    write_theory(args,obs,cut,postfix,'NLO' ,pdf,'scale')
    write_theory(args,obs,cut,postfix,'NNLO',pdf,'scale')
                #[PLOTSFOLDER+cut+postfix+'/'+obs+'_'+x+match+'.root' for x in ['2016']]
    filelist =  [PLOTSFOLDER+cut+postfix+'/theory/'+obs+'_'+x+'_'+pdf+'.root' for x in ['LO','NLO','NNLO']]
                #+[PLOTSFOLDER+cut+postfix+'/uncertainty/'+obs+'_BCDEFGH'+match+'_total.root'])
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    d0 = ({
        'www': 'comparison_Kfactors_NNLOJet'+cut+postfix+'_'+pdf,
        'files': filelist,
        'x_expressions': ['gen'+obs],
        'x_label': (r'$\\mathit{p}_T^Z$' if obs =='zpt' else r'$\\mathit{\\phi}^{*}_{\\eta}$')+' Bin',
        'x_errors': [0],
        'folders': [''],
        'title': pdf,
        'nicks': ['LO','NLO','NNLO'],
        'analysis_modules': ['ScaleHistograms','NormalizeByBinWidth','Ratio'],
        'scale_nicks': ['LO','NLO','NNLO'],
        'scales': [1e0/35.9/1000],
        'ratio_numerator_nicks': 2*['LO','NLO','NNLO'],
        'ratio_denominator_nicks': ['LO'],
        'ratio_result_nicks': ['ratioLO','ratioNLO','ratioNNLO','uncLO','uncNLO','uncNNLO'],
        'filename': obs,
        'markers': ['^','s','o','errorband','errorband','errorband'],
        'colors': ['green','blue','red'],
        'alphas': [0.3],
        'step': True,
        'line_styles': ['-'],
        'y_log': True,
        'y_lims': [1e-6,1e1] if obs =='zpt' else [1e-5,1e3],
        'y_errors': False,
        #'y_subplot_lims': [0.5,1.5],
        'y_subplot_label': 'Ratio to LO',
        'subplot_nicks': ['ratio','unc'],
        'labelsize': 25,
    })
    if obs == 'zpt':
        d0['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\mathit{p}_T^Z dy_b dy^*}/(\\frac{pb}{GeV})$'
    elif obs == 'phistareta':
        d0['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\phi^{*}_{\\eta} dy_b dy^*}/pb$'
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = deepcopy(d0)
            d.update({
                'files': filelist_binned,
                'x_label': obs,
                'x_log': True,
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'x_lims': [25,1000] if obs =='zpt' else [0.4,50],
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'texts_size': [20],
                'texts_x': [0.02],
                'texts_y': [0.97],
                'subplot_fraction': 40,
            })
            if ysmin>1.5: 
                d['vertical_lines'] = [250 if obs =='zpt' else 5]
            #d['analysis_modules'] = ['NormalizeByBinWidth']+d0['analysis_modules']
            d['x_expressions'] = [x+namestring for x in d0['x_expressions']]
            d['www'] = d0['www']+'/Kfactors'+namestring
            plots.append(d)
    d0['figsize'] = [36,6]
    #d0['legend'] = None
    d0['vertical_lines'] = l_obsbinedges
    d0['vertical_lines_styles'] = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    #plots.append(d0)
 return [PlottingJob(plots=plots, args=args)]


def plot_PDFs(args=None,cut='_jet1pt20',data='17Jul2018',match='',postfix='',order='NNLO'):
  plots=[]
  pdflist = ['CT14nnlo','MMHT2014nnlo68cl','NNPDF31_nnlo_as_0118','ABMP16als118_5_nnlo']
  #pdflist = ['CT14nnlo_as_0118','MMHT2014nnlo68cl','NNPDF31_nnlo_as_0118','ABMP16als118_5_nnlo']
  for obs in ['zpt','phistareta']:
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    #write_data(args,obs,cut,data,match,postfix)
    filelist =  []#PLOTSFOLDER+cut+postfix+'/'+obs+'_'+x+match+'.root' for x in ['2016']]
    for pdf in pdflist:
        write_theory(args,obs,cut,postfix,order,pdf,'pdf')
        filelist.append(PLOTSFOLDER+cut+postfix+'/theory/'+obs+'_'+order+'_'+pdf+'.root')
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    d0 = ({
        'www': 'comparison_PDFs_NNLOJet'+cut+postfix+'_'+order,
        'files': filelist,
        'x_expressions': ['gen'+obs],
        'x_label': (r'$\\mathit{p}_T^Z$' if obs =='zpt' else r'$\\mathit{\\phi}^{*}_{\\eta}$')+' Bin',
        'x_errors': [0],
        'folders': [''],
        'title': order,
        'nicks': pdflist,
        'analysis_modules': ['ScaleHistograms','NormalizeByBinWidth','Ratio'],
        'scale_nicks': pdflist,
        'scales': [1e0/35.9/1000],
        'ratio_numerator_nicks': 2*pdflist,
        'ratio_denominator_nicks': pdflist[0],
        'ratio_result_nicks': ['ratio'+pdf for pdf in pdflist]+['unc'+pdf for pdf in pdflist],
        'filename': obs,
        'alphas': [0.3],
        'markers': 2*['s','v','o','^']+len(pdflist)*['errorband'],
        'colors': ['orange','green','purple','blue'],
        'y_log': True,
        'step': True,
        'line_styles': ['-'],
        'y_errors': False,
        'y_lims': [1e-6,1e1] if obs =='zpt' else [1e-5,1e3],
        'y_label': 'Events per binsize',
        'y_subplot_label': 'Ratio to CT14',
        'y_subplot_lims': [0.95,1.05],
        'subplot_nicks': ['ratio','unc'],
        'labels': ['CT14','MMHT2014','NNPDF31','ABMP16'],
        'labelsize': 25,
    })
    if obs == 'zpt':
        d0['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\mathit{p}_T^Z dy_b dy^*}/(\\frac{pb}{GeV})$'
    elif obs == 'phistareta':
        d0['y_label'] = r'$ \\frac{d^3\\mathit{\\sigma}}{d\\phi^{*}_{\\eta} dy_b dy^*}/pb$'
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = deepcopy(d0)
            d.update({
                'files': filelist_binned,
                'x_label': obs,
                'x_log': True,
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'x_lims': [25,1000] if obs =='zpt' else [0.4,50],
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'texts_size': [20],
                'texts_x': [0.02],
                'texts_y': [0.97],
                'subplot_fraction': 40,
            })
            if ysmin>1.5: 
                d['vertical_lines'] = [250 if obs =='zpt' else 5]
            #d['analysis_modules'] = ['NormalizeByBinWidth']+d0['analysis_modules']
            d['x_expressions'] = [x+namestring for x in d0['x_expressions']]
            d['www'] = d0['www']+'/PDFs'+namestring
            plots.append(d)
    d0['figsize'] = [36,6]
    #d0['legend'] = None
    d0['vertical_lines'] = l_obsbinedges
    d0['vertical_lines_styles'] = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    #plots.append(d0)
  return [PlottingJob(plots=plots, args=args)]

def plot_subprocessfractions(args=None,cut='_jet1pt20',data='17Jul2018',match='',postfix='',order='NNLO',pdf='NNPDF31_nnlo_as_0118'):
  plots=[]
  subprocesslist = ['qaq','gaq','qg','gg','qq','aqaq']
  for obs in ['zpt','phistareta']:
   for order in ['LO','NLO','NNLO']:
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    write_theory(args,obs,cut,postfix,order,pdf,'',True)
    filelist = [PLOTSFOLDER+cut+postfix+'/theory/'+obs+'_'+order+'_'+pdf+'_subprocesses.root']
    filelist_binned = []
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    d0 = ({
        'www': 'comparison_subprocesses_NNLOJet'+cut+postfix+'_'+order+'_'+pdf,
        'files': filelist,
        'x_expressions': [obs+'_'+x for x in subprocesslist],
        'x_label': (r'$\\mathit{p}_T^Z$' if obs =='zpt' else r'$\\mathit{\\phi}^{*}_{\\eta}$')+' Bin',
        'folders': [''],
        'nicks': subprocesslist,
        'filename': obs,
        'markers': ['fill'],
        'stacks': ['pos','pos','pos','neg','pos','pos'],
        'colors': ['turquoise','gold','coral','springgreen','mediumvioletred','cornflowerblue'],
        'y_lims': [-0.3,1.8],
        'y_label': 'Subprocess decomposition',
        'title': order,
        'lines': [0,1],
        'lines_styles':[':'],
        'labels': ['quark-antiquark','gluon-antiquark','gluon-quark','gluon-gluon','quark-quark','antiquark-antiquark'],
        'labelsize': 25,
    })
    if order == 'LO':
        d0['nicks_blacklist'] = ['gg','qq', 'aqaq']
        d0['stacks'] = ['pos']
        d0['y_lims'] = [-0.1,1.3],
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d = deepcopy(d0)
            d.update({
                'files': filelist_binned,
                'x_label': obs,
                'x_log': True,
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'x_lims': [25,1000] if obs =='zpt' else [0.4,50],
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'texts_size': [20],
                'texts_x': [0.03],
                'texts_y': [0.97],
            })
            #if ysmin>1.5 and not order=='LO':
            #    d['stacks'] = ['pos']
            d['x_expressions'] = [x+namestring for x in d0['x_expressions']]
            d['www'] = d0['www']+'/fractions'+namestring
            plots.append(d)
    d0['figsize'] = [36,6]
    #d0['legend'] = None
    d0['vertical_lines'] = l_obsbinedges
    d0['vertical_lines_styles'] = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
    #plots.append(d0)
  return [PlottingJob(plots=plots, args=args)]


def plot_variations(args=None, obs='zpt', cut='_jet1pt20', data='amc', mc='toy', match='',postfix=''):
    #central_source = PLOTSFOLDER+cut+postfix+'/'+obs+'_'+data+match+'.root'
    central_source = PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'.root'
    varlist = ['Robs','Ryj','Ryz','F','A','switch']
    plots=[]
    for var in varlist:
        #filelist = [central_source]+[PLOTSFOLDER+cut+postfix+'/variations/'+obs+'_'+data+match+'_'+var+x+'.root' for x in ['Up','Down']]
        filelist = [central_source]+[PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_'+data+'_by_'+mc+match+'_'+var+x+'.root' for x in ['Up','Down']]
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
                'www': 'comparison_variations'+cut+'_'+data+'_by_'+mc+postfix+match+'/variations'+namestring,
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

def plot_detector_3Dhist(args=None,cut='_jet1pt20',data='',mc='toy0',match='',postfix=''):
#def plot_detector(args=None,cut='_jet1pt20',data='',mc='toy',match='_matched',postfix=''):
  plots=[]
  lines_list = 5*[':']+['--']+3*[':']+['--']+2*[':']+['--',':','--']
  samples = [mc]+MCLIST
  #samples = ['mad','amc','hpp']
  for obs in ['zpt','phistareta']:
    [l_obshists, h_reco, h_gen, h_response, l_ybinedges, l_obsbinedges] = prepare_3Dhist(args,obs)
    data_source = [PLOTSFOLDER+cut+postfix+'/'+obs+'_'+x+(match if x=='toy' else '')+'.root' for x in samples]
    d = ({
        'folders': [''],
        'www': 'detector'+cut+match,#+'_oldtoy',
        'figsize': [36,6],
        'vertical_lines': l_obsbinedges,
        'vertical_lines_styles': lines_list,
        'x_label': (r'$\\mathit{p}_T^Z$' if obs =='zpt' else r'$\\mathit{\\phi}^{*}_{\\eta}$')+' Bin',
        'texts_size': [20],
        'labelsize': 25,
    })
    d1 = deepcopy(d)
    d1.update({
        'files': data_source,
        'nicks': ['reco'+x for x in samples]+['gen'+x for x in samples],
        'x_expressions': len(samples)*[''+obs]+len(samples)*['gen'+obs],
        'y_log': True,
        'filename': obs,
        'analysis_modules': ['Ratio'],
        'ratio_numerator_nicks': ['reco'+x for x in samples],
        'ratio_denominator_nicks': ['gen'+x for x in samples],
        'ratio_result_nicks'
        #'ratio_denominator_no_errors': False,
        'x_errors': len(samples)*[0]+2*len(samples)*[1],
        'y_errors': len(samples)*[1]+len(samples)*[0]+len(samples)*[1],
        'colors': [COLORDICT[x] for x in samples],
        'markers': [MARKERDICT[x] for x in samples],
        'labels': [LABELDICT[x] for x in samples],
        #'colors': ['grey','orange','red','blue','green','darkgrey','darkorange','darkred','darkblue','darkgreen','black','orange','red','blue','green'],
        #'markers': ['x','1','2','3','4']+2*len(samples)*[''],
        'subplot_fraction': 40,
        #'y_subplot_lims': [0.0,2.0],
        #'y_subplot_lims': [0.8,1.0],
        'y_subplot_lims': [0.7,1.1],
        
    })
    #plots.append(d1)
    filelist_binned = []
    filelist = d1['files']
    for x in filelist:
        invert_3Dhists(args,x)
        filelist_binned.append(x.replace('.root','_binned.root'))
    for ybmin in [0.0,0.5,1.0,1.5,2.0]:
      for ysmin in [0.0,0.5,1.0,1.5,2.0]:
        if not ybmin+ysmin>2:
            namestring = '_yb{}_ys{}'.format(int(2*ybmin),int(2*ysmin))
            d0 = deepcopy(d1)
            d0.pop('figsize')
            d0.pop('vertical_lines')
            d0.update({
                'files': filelist_binned,
                'x_expressions': len(samples)*[obs+namestring]+len(samples)*['gen'+obs+namestring],
                'x_label': obs,
                'y_label': 'Reco/Gen',
                'x_log': True,
                'x_errors': [True],
                'x_ticks': [30,60,100,200,400,1000] if obs =='zpt' else [0.5,1.0,2.0,4.0,10,30],
                'y_lims': [0.8,1.1],
                'y_log': False,
                'nicks_whitelist': ['ratio'],
                'texts': [r"${}<y_b<{}$,${}<y*<{}$".format(ybmin,ybmin+0.5,ysmin,ysmin+0.5)],
                'texts_size': [15],
                'texts_x': [0.03],
                'texts_y': [0.97],
                'subplot_nicks': ['dummy'],
            })
            d0['www'] = d1['www']+'/detector'+namestring
            if ysmin==2.0:
                d0['y_lims'] = [0.5,1.5]
            elif ybmin==2.0:
                d0['y_lims'] = [0.6,1.2]
            #plots.append(d0)
    d2 = deepcopy(d)
    d2.update({
        'files': [data_source[0]],
        'nicks': ['R'+obs,'Ryz','Ryj'],
        'x_expressions': [obs+'res','zyres','jet1yres'],
        'y_lims':[0,0.1],
        'markers': ['1','2','3'],
        'colors': ['green','orange','purple'],
        'filename': obs+'_resolutions',
    })
    #plots.append(d2)
    d3 = deepcopy(d2)
    d3.update({
        'x_expressions': [obs+'F',obs+'A',obs+'switch'],
        'nicks': ['F','A','switch'],
        #'analysis_modules': ['Divide','SumOfHistograms','Ratio'],
        #'divide_numerator_nicks': ['F'],
        #'divide_denominator_nicks': ['F'],
        #'divide_result_nicks': ['unity'],
        #'sum_nicks': ['unity A','unity F'],
        #'sum_scalefactors': ['1 -1'],
        #'sum_result_nicks': ['loss','fake'],
        #'ratio_numerator_nicks': ['fake'],
        #'ratio_denominator_nicks': ['loss'],
        'y_lims':[0.6,1],
        #'y_subplot_lims': [0.8,1.0],
        #'subplot_fraction': 40,
        #'y_errors': [0],
        'markers': ['4','x','+'],
        'colors': ['black','red','blue'],
        'filename': obs+'_rates',
    })
    #plots.append(d3)
    for (i,mc_source) in enumerate(data_source):
      d4 = deepcopy(d)
      d4.update({
        'files': [mc_source],
        'x_expressions': ['response'],
        'x_label': (r'$\\mathit{p}_T^{Z,Gen}$' if obs =='zpt' else r'$\\mathit{\\phi}^{*,Gen}_{\\eta}$')+' Bin',
        'y_label': (r'$\\mathit{p}_T^{Z,Reco}$' if obs =='zpt' else r'$\\mathit{\\phi}^{*,Reco}_{\\eta}$')+' Bin',
        'z_log':True,
        'z_lims':[1e-4,1e0],
        'z_label': 'Fraction of events',
        'analysis_modules': ['NormalizeRowsToUnity'],
        'colormap': 'summer_r',
        'filename': obs+'_response_'+samples[i],
        'lines': l_obsbinedges,
        'lines_styles': lines_list,
        'figsize': [8,7],
        'texts': [(r"$\\bf{CMS} \\hspace{0.5} \\it{Simulation} \\hspace{0.2} \\it{Preliminary}$" if CMSLABEL else ""),
                   ""],#"Condition number = {:.3f}".format(unfold_by_inversion_3Dhist(args,obs,cut,samples[i],samples[i],match,postfix))],
        'texts_x': [0.03,0.20],
        'texts_y': [1.05,0.06],
      })
      plots.append(d4)
      d5 = deepcopy(d)
      unfold_by_tunfold_3Dhist(args,obs,cut,'17Jul2018',samples[i],match,postfix)
      d5.update({
        'files': [PLOTSFOLDER+cut+postfix+'/unfolded/'+obs+'_17Jul2018_by_'+samples[i]+match+'.root'],
        'x_expressions': ['correlation'],
        'x_label': (r'$\\mathit{p}_T^{Z,Gen}$' if obs =='zpt' else r'$\\mathit{\\phi}^{*,Gen}_{\\eta}$')+' Bin',
        'y_label': (r'$\\mathit{p}_T^{Z,Reco}$' if obs =='zpt' else r'$\\mathit{\\phi}^{*,Reco}_{\\eta}$')+' Bin',
        #'x_lims':[0,50],
        #'y_lims':[0,50],
        'z_lims':[-1,1],
        'z_log': True,
        'z_ticks':[-1e0,-1e-1,-1e-2,0.00,1e-2,1e-1,1e0],
        'z_label': 'Correlation coefficient',
        'colormap': 'bwr',#'coolwarm',
        'filename': obs+'_correlation_'+samples[i],
        'lines': l_obsbinedges,
        'lines_styles': lines_list,
        'figsize': [8,7],
        #'analysis_modules': ['GetCorrelationFactor'],
        'texts': [r"$\\bf{CMS} \\hspace{0.5} \\it{Simulation} \\hspace{0.2} \\it{Preliminary}$" if CMSLABEL else ""],
        'texts_x': [0.03],
        'texts_y': [1.05],
      })
      plots.append(d5)
  return [PlottingJob(plots=plots, args=args)]


#def create_gendistributions_3Dhist(args=None, cut='_jet1pt20', mc='mad',match='',postfix=''):
def create_gendistributions_3Dhist(args=None, cut='_jet1pt20', mc='hpp',match='',postfix=''):
    plots=[]
    for obs in ['genzpt','genphistareta','matchedgenjet1y']:
     output_file = PLOTSFOLDER+cut+postfix+'/gendistributions/'+obs+'_'+mc+'.root'
     if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        continue
     namestring = ''
     d = ({
            'files': [DATASETS[mc].replace('.root',postfix+'.root')],
            'folders': ['genzjetcuts_L1L2L3/ntuple'],
            'nicks':[obs+namestring],
            'x_expressions': [obs],
            'y_expressions': ['genzy'],
            'y_bins': ['24,-2.4,2.4'],
            'z_expressions': ['genjet1y'],
            'z_bins': ['24,-2.4,2.4'],
            'filename': output_file.replace('.root','')+namestring,
            'x_log': obs in ['genzpt','genphistareta'],
            'plot_modules': ['ExportRoot'],
            'output_dir': '/',
            'weights': ['(abs(genmupluseta)<2.4)&&(abs(genmuminuseta)<2.4)&&(genmupluspt>25)&&(genmuminuspt>25)&&(abs(genzmass-91.1876)<20)'],
     })
     if cut=='_jet1pt20':
         d['weights'][0] += '&&(genjet1pt>20)'
     else:
         print "cuts not known"
     if obs == 'genzpt':
         d['x_bins'] = ' '.join(['{}'.format(x) for x in np.logspace(1,np.log(1000)/np.log(25),30,True,25)])
         d['weights'][0] += '&&(genzpt>25)&&(genzpt<1000)'
     elif obs == 'genphistareta':
         d['x_bins'] = ' '.join(['{}'.format(x) for x in np.logspace(1,np.log(50)/np.log(0.4),30,True,0.4)])
         d['weights'][0] += '&&(genphistareta>0.4)&&(genphistareta<50)'
     elif obs in ['matchedgenjet1y']:
         # matched jets in case of switched event!
         d['x_bins'] = ['24,-2.4,2.4']
         d['weights'][0] += '&&(matchedgenjet1pt<genjet1pt)&&(matchedgenjet1pt>0)'
         d.pop('z_expressions')
     plots.append(d)
    if not plots==[]:
        return [PlottingJob(plots=plots, args=args)]

def create_pileupweightfiles(args=None, cut='_jet1pt20', data='17Jul2018', mc='hpp',match='',postfix=''):
    plots=[]
    for obs in ['npv','npumean','rho']:
     output_file = PLOTSFOLDER+cut+postfix+'/gendistributions/pileupweight_'+obs+'_'+mc+'.root'
     if os.path.exists(output_file):
        print "WARNING: file "+output_file+" already exists. Check if it can be removed!"
        continue
     d = ({
            'files': [DATASETS[data].replace('.root',postfix+'.root'),DATASETS[mc].replace('.root',postfix+'.root')],
            'folders': ['nocuts_L1L2L3Res/ntuple','nocuts_L1L2L3/ntuple'],
            'nicks':['data','mc'],
            'x_expressions': [obs],
            'x_bins': obs,
            'filename': output_file.replace('.root',''),
            'analysis_modules': ['NormalizeToFirstHisto','Ratio'],
            'ratio_numerator_nicks': ['data'],
            'ratio_denominator_nicks':['mc'],
            'ratio_result_nicks': ['pileupweight'],
            'plot_modules': ['ExportRoot'],
            'nicks_whitelist': ['pileupweight'],
            'output_dir': '/',
            #'weights': ['(abs(genmupluseta)<2.4)&&(abs(genmuminuseta)<2.4)&&(genmupluspt>25)&&(genmuminuspt>25)&&(abs(genzmass-91.1876)<20)'],
     })
     plots.append(d)
    if not plots==[]:
        return [PlottingJob(plots=plots, args=args)]




