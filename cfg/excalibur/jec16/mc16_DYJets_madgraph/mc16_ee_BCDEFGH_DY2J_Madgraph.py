import configtools
import os

RUN = 'BCDEFGH'
CH = 'ee'
JEC = 'Summer16_07Aug2017_V5'

_path_prefix = "srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only"

def config():
	cfg = configtools.getConfig('mc', 2016, CH, bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
            #ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DY2JetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16/*.root",
            ekppath=_path_prefix + "/store/user/dsavoiu/Skimming/ZJet_DY2JetsToLL_Summer16-madgraphMLM_asymptotic_2016_TrancheIV_v6-v1/*.root"
            #nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DY2JetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16/*.root",
	)
	cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_'+RUN+'_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
	cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_MC/'+JEC+'_MC')
	cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])

	cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/PUWeights_'+RUN+'_13TeV_23Sep2016ReReco_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
	cfg['NumberGeneratedEvents'] = 19970551
	cfg['GeneratorWeight'] = 1.0
	cfg['CrossSection'] = 332.8*1.23 # for: 2Jet_madgraphMLM
	return cfg
