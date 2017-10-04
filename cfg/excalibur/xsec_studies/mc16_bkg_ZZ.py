import configtools
import os

RUN = 'BCDEFGH'
JEC = 'Summer16_03Feb2017_V1'

def config():
	cfg = configtools.getConfig('mc', 2016, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/afriedel/Skimming/mcbkg_Moriond/ZZ/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/afriedel/Skimming/mcbkg_Moriond/ZZ/*.root",
		)
	cfg['Pipelines']['default']['Processors'] += ['producer:MuonTriggerMatchingProducer','producer:LeptonSFProducer']#,'producer:LeptonTriggerSFProducer']
	cfg['Processors'] = ['producer:MuonCorrectionsProducer',]+cfg['Processors']#
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'leptoncuts', 'allzcuts', 'allleptoncuts','genleptoncuts','genzcuts'], ['None'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
	# Add Muon Correction and SF Producers
	cfg['ValidMuonsInput'] = "corrected"
	cfg['MuonIso'] = 'loose'
	cfg['CutMuonPtMin'] = 27.0
	cfg['CutZPtMin'] = 40.0
	cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_MC/'+JEC+'_MC')
	cfg['NumberGeneratedEvents'] = 998034
	cfg['CrossSection'] = 15.6  # http://arxiv.org/pdf/1512.05314v2.pdf
	cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/pileup_weights_'+RUN+'_13TeV_23Sep2016ReReco_Zll_DYJetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16.root')
	return cfg
