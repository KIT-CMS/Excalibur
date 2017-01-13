import configtools


def config():
	cfg = configtools.getConfig('mc', 2016, 'ee', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/jbod/tberger/SkimmingResults/Zll_DYJetsToLL_M-50_amcatnloFXFX-Summer16-pythia8_25ns/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root"
		#ekppath="srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/tberger/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root"
		#ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1/*.root"				
		#ekppath="/storage/jbod/tberger/SkimmingResults/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1/*.root"
		#nafpath="//pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1/*.root"
	)
	#cfg['JsonFiles'] = configtools.RunJSON('/home/tberger/Excalibur/CMSSW_8_0_21/src/Excalibur/data/json/Cert_BCD_13TeV_23Sep2016ReReco_Collisions16_JSON.txt') #12.89/fb
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	#cfg['Jec'] = configtools.getPath() + '/data/JECDatabase/textFiles/Summer16_23Sep2016V1_MC/Summer16_23Sep2016V1_MC'
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
	cfg['NumberGeneratedEvents'] = 28611654 # for full Set: 28696958   
	cfg['GeneratorWeight'] =  0.670201351233 #for: Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1
	cfg['CrossSection'] = 6025.2
	return cfg
