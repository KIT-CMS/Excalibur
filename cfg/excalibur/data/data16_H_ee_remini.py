import configtools
import os

RUN='H'
CH='ee'
JEC='Summer16_03Feb2017'+RUN+'_V3'

def config():
	cfg = configtools.getConfig('data', 2016, CH, bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		#ekppath="/storage/jbod/tberger/SkimmingResults/Zll_DoElRun2016B-PromptReco-v2/*.root"
		ekppath0="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/reminiaod03Feb2017_metfix/Zll_DoElRun2016H-03Feb2017-ver2v1/*.root",
		ekppath1="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/reminiaod03Feb2017_metfix/Zll_DoElRun2016H-03Feb2017-ver3v1/*.root",
		nafpath0="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/reminiaod03Feb2017_metfix/Zll_DoElRun2016H-03Feb2017-ver2v1/*.root",
		nafpath1="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/reminiaod03Feb2017_metfix/Zll_DoElRun2016H-03Feb2017-ver3v1/*.root"
		)
	cfg['JsonFiles'] =  [os.path.join(configtools.getPath(),'data/json/Cert_'+RUN+'_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
	cfg['Jec'] = os.path.join(configtools.getPath(),'../JECDatabase/textFiles/'+JEC+'_DATA/'+JEC+'_DATA')
	cfg = configtools.expand(cfg, ['nocuts','noalphanoetacuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])
	configtools.remove_quantities(cfg, ['jet1qgtag'])
	return cfg
