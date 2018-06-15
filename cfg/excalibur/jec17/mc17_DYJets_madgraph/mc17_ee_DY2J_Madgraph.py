import configtools
import os

RUN = 'BCDEFGH'
CH = 'ee'
JEC = 'Fall17_17Nov2017_V10'

def config():
    cfg = configtools.getConfig('mc', 2017, CH)
    cfg["InputFiles"].set_input(
        ekppathB="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/dsavoiu/Skimming/ZJet_DY2JetsToLL_Fall17-madgraphMLM_realistic_v10-v1/*.root",
        #ekppathB="/storage/gridka-nrg/dsavoiu/Skimming/ZJet_DY2JetsToLL_Fall17-madgraphMLM_realistic_v10-v1/*.root",
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt')]
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_MC/'+JEC+'_MC')
    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc17_DYJets_madgraph/PUWeights_BCDEF_17Nov2017_DY2JetsToLL_Fall17-madgraphMLM_realistic_v10-v1.root')
    cfg['NumberGeneratedEvents'] = 11623646
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 332.8*1.23  # from mc16 config

    cfg['ElectronID'] = 'user'  # old ID no longer written out in new skim
    cfg['ApplyElectronVID'] = True
    #cfg['ElectronVIDName'] = "Summer16-80X-V1"
    cfg['ElectronVIDName'] = "Fall17-94X-V1-Preliminary"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"

    return cfg


