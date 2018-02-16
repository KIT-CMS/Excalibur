import configtools
import os

RUN = 'BCDEFGH'
CH = 'ee'
JEC = 'Summer16_03Feb2017_V1'

def config():
	cfg = configtools.getConfig('mc', 2016, CH, bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		#ekppath="/storage/jbod/tberger/SkimmingResults/Zll_DYJetsToLL_M-50_amcatnloFXFX-Summer16-pythia8_25ns/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root"
		#ekppath="srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/tberger/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root"
		#ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1/*.root"				
		#ekppath="/storage/jbod/tberger/SkimmingResults/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1/*.root"
		ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root"
		)
	cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_'+RUN+'_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
	cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_MC/'+JEC+'_MC')
	cfg = configtools.expand(cfg, ['nocuts','noalphanoetacuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1qgtag'])
	cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/pileup_weights_'+RUN+'_13TeV_23Sep2016ReReco_Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
	cfg['NumberGeneratedEvents'] = 11043183 #28968252 # for: amc@nlo
	cfg['GeneratorWeight'] = 0.670123731536
	cfg['CrossSection'] = 1921.8*3
	return cfg
