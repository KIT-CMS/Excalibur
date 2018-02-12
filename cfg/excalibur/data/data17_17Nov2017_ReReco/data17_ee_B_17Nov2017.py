import configtools
import os

RUN='B'
CH='ee'
JEC='Fall17_17Nov2017'+RUN+'_V4'

def config():
    cfg = configtools.getConfig('data', 2017, CH)
    cfg["InputFiles"].set_input(
        ekppathB="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/dsavoiu/Skimming/ZJet_DoubleEG_Run2017B-17Nov2017-v1/*.root",
        #ekppathB="/storage/gridka-nrg/dsavoiu/Skimming/ZJet_DoubleEG_Run2017B-17Nov2017-v1/*.root",
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt')]
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_DATA/'+JEC+'_DATA')
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ElectronID'] = 'user'  # old ID no longer written out in new skim
    cfg['ApplyElectronVID'] = True
    #cfg['ElectronVIDName'] = "Summer16-80X-V1"
    cfg['ElectronVIDName'] = "Fall17-94X-V1-Preliminary"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"

    cfg['ProvideL2ResidualCorrections'] = False
    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])
    return cfg
