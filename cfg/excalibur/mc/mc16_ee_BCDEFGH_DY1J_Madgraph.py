import configtools
import os

RUN = 'BCDEFGH'
CH = 'ee'
JEC = 'Summer16_07Aug2017_V1'

def config():
    cfg = configtools.getConfig('mc', 2016, CH, bunchcrossing='25ns')
    cfg["InputFiles"].set_input(
        #ekppath="/storage/jbod/tberger/testfiles/skimming_output/MC/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16_testfile.root",
        ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DY1JetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16/*.root",
        nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DY1JetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16/*.root",
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_'+RUN+'_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_MC/'+JEC+'_MC')
    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])
    configtools.remove_quantities(cfg, ['jet1qgtag'])
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/pileup_weights_'+RUN+'_13TeV_23Sep2016ReReco_Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
    cfg['NumberGeneratedEvents'] = 62627174
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 1012.5*1.23 # for: 1Jet_madgraphMLM
    return cfg
