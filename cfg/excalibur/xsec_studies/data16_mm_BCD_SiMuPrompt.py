import configtools
import os

def config():
	cfg = configtools.getConfig('data', 2016, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		#ekppath='/storage/jbod/tberger/testfiles/skimming_output/data/Zll_DoMuRun2016D-03Feb2017-v1_testfile.root',
		ekppathB='srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_SiMuRun2016B-PromptReco-v2/*.root',
	   	ekppathC='srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_SiMuRun2016C-PromptReco-v2/*.root',
		ekppathD='srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_SiMuRun2016D-PromptReco-v2/*.root',
		nafpathB='/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_SiMuRun2016B-PromptReco-v2/*.root',
		nafpathC='/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_SiMuRun2016C-PromptReco-v2/*.root',
		nafpathD='/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_SiMuRun2016D-PromptReco-v2/*.root',
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'leptoncuts'], ['None','L1L2L3','L1L2L3Res'])#, True)
	configtools.remove_quantities(cfg, [ 'jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])
	# Add Muon SF and Correction Producers
	cfg['Processors'] += ['producer:MuonTriggerMatchingProducer','producer:LeptonSFProducer','producer:LeptonTriggerSFProducer',]
	cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
	cfg['ValidMuonsInput'] = "corrected"
	# Change Trigger Requirements for SiMu Dataset
	cfg['HltPaths'] = ['HLT_IsoMu22', 'HLT_IsoTkMu22']
	cfg["MuonTriggerFilterNames"] = [
		"HLT_IsoMu22_v2:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09",
		"HLT_IsoTkMu22_v2:hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09",
		"HLT_IsoTkMu22_v3: hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09",
		"HLT_IsoMu22_v3:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09",
		"HLT_IsoTkMu22_v4:hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09"
		#'HLT_IsoMu24_v2:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09',
		#'HLT_IsoTkMu24_v3:hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09'
		]
	cfg['MuonIso'] = 'loose'
	cfg['CutMuonPtMin'] = 22.0
	cfg['CutZPtMin'] = 40.0
	cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt')]
	cfg['LeptonSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016/SFData_ICHEP.root")
	return cfg
