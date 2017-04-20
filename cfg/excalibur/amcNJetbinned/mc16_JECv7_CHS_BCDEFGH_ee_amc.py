import configtools
import os

def config():
	cfg = configtools.getConfig('mc', 2016, 'ee', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		#ekppath="/storage/jbod/tberger/SkimmingResults/Zll_DYJetsToLL_M-50_amcatnloFXFX-Summer16-pythia8_25ns/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root"
		#ekppath="srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/tberger/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root"
		#ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1/*.root"				
		#ekppath="/storage/jbod/tberger/SkimmingResults/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1/*.root"
		nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root"
		#nafpath0="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYJetsToLL_M-50_HT-70to100_madgraphMLM-pythia8_RunIISummer16/*.root",
		#nafpath1="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYJetsToLL_M-50_HT-100to200_madgraphMLM-pythia8_RunIISummer16/*.root",
		#nafpath2="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYJetsToLL_M-50_HT-200to400_madgraphMLM-pythia8_RunIISummer16/*.root",
		#nafpath3="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYJetsToLL_M-50_HT-400to600_madgraphMLM-pythia8_RunIISummer16/*.root",
		#nafpath4="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYJetsToLL_M-50_HT-800to1200_madgraphMLM-pythia8_RunIISummer16/*.root",
		#nafpath5="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYJetsToLL_M-50_HT-1200to2500_madgraphMLM-pythia8_RunIISummer16/*.root",
		#nafpath6="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYJetsToLL_M-50_HT-2500toInf_madgraphMLM-pythia8_RunIISummer16/*.root"
		
	)
	cfg['JsonFiles'] = [configtools.getPath() + 'data/json/Cert_BCDEFGH_13TeV_23Sep2016ReReco_Collisions16_JSON.txt']
	cfg['Jec'] = configtools.getPath() + '/data/JECDatabase/textFiles/Summer16_23Sep2016V7_MC/Summer16_23Sep2016V7_MC'
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
	cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/pileup_weights_BCDEFGH_13TeV_23Sep2016ReReco_Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
	cfg['NumberGeneratedEvents'] = 28968252 # for: amc@nlo
	cfg['GeneratorWeight'] =  0.669811834004
	cfg['CrossSection'] = 6025.2
	return cfg
