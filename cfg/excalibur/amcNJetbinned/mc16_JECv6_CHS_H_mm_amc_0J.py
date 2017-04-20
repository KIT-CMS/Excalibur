import configtools
import os

def config():
	cfg = configtools.getConfig('mc', 2016, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYToLL_0J_amcatnloFXFX-pythia8_RunIISummer16_ext/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYToLL_0J_amcatnloFXFX-pythia8_RunIISummer16_backup/*.root"
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYToLL_1J_amcatnloFXFX-pythia8_RunIISummer16_ext/*.root"
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYToLL_1J_amcatnloFXFX-pythia8_RunIISummer16_backup/*.root"
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYToLL_2J_amcatnloFXFX-pythia8_RunIISummer16_ext/*.root"
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC/Zll_DYToLL_2J_amcatnloFXFX-pythia8_RunIISummer16_backup/*.root"
	)
	cfg['JsonFiles'] = [configtools.getPath() + 'data/json/Cert_H_13TeV_23Sep2016ReReco_Collisions16_JSON.txt']
	cfg['Jec'] = configtools.getPath() + '/data/JECDatabase/textFiles/Summer16_23Sep2016V6_MC/Summer16_23Sep2016V6_MC'
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
	cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/pileup_weights_H_13TeV_23Sep2016ReReco_Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
	cfg['NumberGeneratedEvents'] = 49579613+44253240 # for: 0J_amc@nlo_backup
	cfg['GeneratorWeight'] = (0.81728086502*49579613+0.817330708441*44253240)/(49579613+44253240)
	cfg['CrossSection'] = 5678.7 # for: 0J_amc@nlo
	return cfg
