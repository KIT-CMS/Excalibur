import configtools
import os

RUN = 'BCDEFGH'
CH = 'mm'
JEC = 'Summer16_03Feb2017_V1'

def config():
	cfg = configtools.getConfig('mc', 2016, CH, bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root",
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DYToLL_0J_amcatnloFXFX-pythia8_RunIISummer16_ext/*.root"
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DYToLL_0J_amcatnloFXFX-pythia8_RunIISummer16_backup/*.root"
		nafpath0="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DYToLL_1J_amcatnloFXFX-pythia8_RunIISummer16_ext/*.root",
		nafpath1="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DYToLL_1J_amcatnloFXFX-pythia8_RunIISummer16_backup/*.root"
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DYToLL_2J_amcatnloFXFX-pythia8_RunIISummer16_ext/*.root"
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DYToLL_2J_amcatnloFXFX-pythia8_RunIISummer16_backup/*.root"
	)
	cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_'+RUN+'_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
	cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_MC/'+JEC+'_MC')
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
	cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/pileup_weights_'+RUN+'_13TeV_23Sep2016ReReco_Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
	cfg['NumberGeneratedEvents'] = 89014732 #49852571+41597712 # for: 1J_amc@nlo_ext+backup
	cfg['GeneratorWeight'] = 0.454344141597 #(0.454289167955*49852571+0.454404319161*41597712)/(49852571+41597712)
	cfg['CrossSection'] = 266.7 # for: 1J_amc@nlo
	return cfg
