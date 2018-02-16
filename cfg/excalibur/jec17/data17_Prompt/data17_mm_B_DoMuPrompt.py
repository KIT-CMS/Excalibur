import configtools
import os

RUN='B'
CH='mm'
JEC='Summer16_03Feb2017BCD_V3'

def config():
	cfg = configtools.getConfig('data', 2016, CH, bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppathB1="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/dsavoiu/Skimming/ZJet_DoubleMuon_Run2017B-PromptReco-v1/*.root",
		ekppathB2="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/dsavoiu/Skimming/ZJet_DoubleMuon_Run2017B-PromptReco-v2/*.root",
	
		)
	cfg['JsonFiles'] =  [os.path.join(configtools.getPath(),'data/json/Cert_'+RUN+'_13TeV_PromptReco_Collisions17_JSON.txt')]
	cfg['Jec'] = os.path.join(configtools.getPath(),'../JECDatabase/textFiles/'+JEC+'_DATA/'+JEC+'_DATA')
	cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
	cfg = configtools.expand(cfg, ['nocuts','noalphanoetacuts','noetaphicleaning','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])
	configtools.remove_quantities(cfg, ['jet1qgtag'])
	return cfg
