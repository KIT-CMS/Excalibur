import configtools
import os

RUN='D'
CH='mm'
JEC='Fall17_17Nov2017'+RUN+'_V4'

def config():
    cfg = configtools.getConfig('data', 2017, CH)
    cfg["InputFiles"].set_input(
        ekppathD="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/dsavoiu/Skimming/ZJet_DoubleMuon_Run2017D-17Nov2017-v1-r2/*.root",
        #ekppathD="/storage/gridka-nrg/dsavoiu/Skimming/ZJet_DoubleMuon_Run2017D-17Nov2017-v1-r2/*.root",
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt')]
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_DATA/'+JEC+'_DATA')
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ProvideL2ResidualCorrections'] = False
    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])
    return cfg
