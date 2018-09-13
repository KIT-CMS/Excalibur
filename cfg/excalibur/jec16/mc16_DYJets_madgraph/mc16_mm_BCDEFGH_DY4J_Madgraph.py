import configtools
import os

RUN = 'BCDEFGH'
CH = 'mm'
JEC = 'Summer16_07Aug2017_V11'

def config():
	cfg = configtools.getConfig('mc', 2016, CH, JEC=JEC)
	cfg["InputFiles"].set_input(
		bmspath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DY4JetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DY4JetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16/*.root",
	)

	cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])

	cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/PUWeights_'+RUN+'_13TeV_23Sep2016ReReco_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
	cfg['NumberGeneratedEvents'] = 4197868
	cfg['GeneratorWeight'] = 1.0
	cfg['CrossSection'] = 54.8*1.23 # for: 4Jet_madgraphMLM

	return cfg
