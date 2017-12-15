import configtools
import ROOT
import os
from copy import deepcopy
import argparse

parser = argparse.ArgumentParser(description='Load data & MC PU distributions')
parser.add_argument('-m', '--mc', type=str,  default="DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1",
                    help="MC type, possible choices:___________________"
                        "'DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1', "
                        "'DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16', "
                        "'DYJetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16' ")
parser.add_argument('-d', '--data', type=str, default="BCD",
                    help="data period, possible choices: ________________ 'BCD','EF','G','H'")
parser.add_argument('-p', '--path', type=str, default="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/",
                    help="path to MC files, possible choices:_________________ "
                        "'/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/', "
                        "'/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/' ")
parser.add_argument('-n', '--number_of_files', type=int, help="number of MC files to use for PU distribution")

args = parser.parse_args()
RUN=args.data
MC=args.mc
FOLDER=args.path
print RUN
print MC
print FOLDER

mc_path=FOLDER+'Zll_'+MC #
mc_filelist = os.listdir(mc_path) if args.number_of_files==None else os.listdir(mc_path)[1:args.number_of_files]
mc_file   = os.path.join(configtools.getPath() ,"data/pileup/PU_MC_"+MC+".root")
data_file = os.path.join(configtools.getPath() ,"data/pileup/PU_data_"+RUN+"_13TeV_23Sep2016ReReco.root")
pu_file   = os.path.join(configtools.getPath() ,"data/pileup/PUWeights_"+RUN+"_13TeV_23Sep2016ReReco_"+MC+".root")

if not os.path.exists(mc_file):
    mc_chain = ROOT.TChain("Events")
    npu_mc = ROOT.TH1D("pileup", "True Number of Pile-Up Interactions;nputruth;events", 80, 0, 80)
    for mc_filename in mc_filelist:
        print "get PU distribution from file "+mc_path+"/"+mc_filename
        mc_chain.Add(mc_path+'/'+mc_filename)
    print "write PU distribution from "+str(len(mc_filelist))+" files to file "+mc_file
    mc_chain.Draw("eventInfo.nPUMean >> pileup","","goff")
    mc_rootfile = ROOT.TFile(mc_file, "RECREATE")
    npu_mc.Write()
else:
    print "load MC PU distribution from "+mc_file
    mc_rootfile = ROOT.TFile(mc_file, "READ")
    npu_mc = deepcopy(mc_rootfile.Get("pileup"))

mc_rootfile.Close()
npu_mc.Scale(1.0/npu_mc.Integral())
#for entry in mc_chain:
#    npu_mc.Fill(entry.eventInfo.nPUMean)
print "load data PU distribution from "+data_file
data_rootfile = ROOT.TFile(data_file,"READ")
npu_data = data_rootfile.Get("pileup")
#npu_data.Rebin(10)
npu_data.Scale(1.0/npu_data.Integral())
npu_reweighting = deepcopy(npu_data)
data_rootfile.Close()

npu_reweighting.Divide(npu_mc)
#npu_reweighting.Rebin(10)
pu_rootfile = ROOT.TFile(pu_file, "RECREATE")
print "write PU reweighting information to file "+pu_file
npu_reweighting.Write()
pu_rootfile.Close()
