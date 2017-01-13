import configtools


def config():
	cfg = configtools.getConfig('data', 2016, 'ee', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/jbod/tberger/SkimmingResults/Zll_DoElRun2016B-PromptReco-v2/*.root"
		#ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoElRun2016B-ReReco-v3/*.root"
	)
	#cfg['JsonFiles'] = configtools.getPath() + '/data/json/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'
	#cfg['JsonFiles'] = configtools.RunJSON('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-280385_13TeV_PromptReco_Collisions16_JSON_NoL1T_v2.txt')#27.22/fb
	#cfg['JsonFiles'] = configtools.RunJSON('/home/tberger/Excalibur/CMSSW_8_0_24/src/Excalibur/data/json/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt')#27.22/fb
	#cfg['JsonFiles'] = configtools.RunJSON('/home/tberger/Excalibur/CMSSW_8_0_21/src/Excalibur/data/json/Cert_BCD_13TeV_23Sep2016ReReco_Collisions16_JSON.txt') #12.89/fb
	#cfg['Jec'] = configtools.getPath() + '/data/JECDatabase/textFiles/Summer16_23Sep2016BCDV1_DATA/Summer16_23Sep2016BCDV1_DATA'
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])
	configtools.remove_quantities(cfg, ['jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])
	return cfg
