import configtools
import os

RUN = 'BCDEFGH'
CH = 'mm'
JEC = 'Summer16_07Aug2017_V5'

def config():
    cfg = configtools.getConfig('mc', 2016, CH, bunchcrossing='25ns')
    cfg["InputFiles"].set_input(
        #ekppath="srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/tberger/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root"
        #ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1/*.root"				
        ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DYJetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16/*.root",
        nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DYJetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16/*.root",
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_'+RUN+'_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_MC/'+JEC+'_MC')
    cfg = configtools.expand(cfg, ['nocuts','noalphanoetacuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])

    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/PUWeights_'+RUN+'_13TeV_23Sep2016ReReco_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
    cfg['NumberGeneratedEvents'] = 49144274 # for: HT-full_madgraphMLM
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 1921.8*3
    return cfg
