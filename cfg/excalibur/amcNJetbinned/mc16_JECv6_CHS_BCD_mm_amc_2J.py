import configtools
import os

def config():
	cfg = configtools.getConfig('mc', 2016, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root",
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYToLL_0J_amcatnloFXFX-pythia8_RunIISummer16_ext/*.root"
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYToLL_0J_amcatnloFXFX-pythia8_RunIISummer16_backup/*.root"
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYToLL_1J_amcatnloFXFX-pythia8_RunIISummer16_ext/*.root"
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYToLL_1J_amcatnloFXFX-pythia8_RunIISummer16_backup/*.root"
		nafpath0="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYToLL_2J_amcatnloFXFX-pythia8_RunIISummer16_ext/*.root"
		nafpath1="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYToLL_2J_amcatnloFXFX-pythia8_RunIISummer16_backup/*.root"
	)
	cfg['JsonFiles'] = [configtools.getPath() + 'data/json/Cert_BCD_13TeV_23Sep2016ReReco_Collisions16_JSON.txt']
	cfg['Jec'] = configtools.getPath() + '/data/JECDatabase/textFiles/Summer16_23Sep2016V6_MC/Summer16_23Sep2016V6_MC'
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
	cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/pileup_weights_BCD_13TeV_23Sep2016ReReco_Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
	cfg['NumberGeneratedEvents'] = 47974554+42324802 # for: 2J_amc@nlo_ext+backup
	cfg['GeneratorWeight'] = (0.291069970135+0.291054687037)/2
	cfg['CrossSection'] = 79.5 # for: 2J_amc@nlo
	return cfg
