import configtools
import os

RUN='BCD'
CH='mm'
JEC='Summer16_07Aug2017{}_V12'.format(RUN)

#_path_prefix = "/storage/gridka-nrg"
_path_prefix = "srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user"
#_path_prefix = "root://cmsxrootd-1.gridka.de:1094///store/user"

def config():
    cfg = configtools.getConfig('data', 2016, CH, JEC=JEC, IOV=RUN)
    cfg["InputFiles"].set_input(
        ekppathB1="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016B-Legacy-07Aug2017_ver1-v1/*.root".format(_path_prefix),
        ekppathB2="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016B-Legacy-07Aug2017_ver2-v1/*.root".format(_path_prefix),
        ekppathC="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016C-Legacy-07Aug2017-v1/*.root".format(_path_prefix),
        ekppathD="{}/tberger//Skimming/ZJet_DoubleMuon_Run2016D-Legacy-07Aug2017-v1/*.root".format(_path_prefix),
        )
    cfg['JsonFiles'] =  [os.path.join(configtools.getPath(),'data/json/Cert_{}_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'.format(RUN))]

    cfg['ProvideL2ResidualCorrections'] = True
    cfg = configtools.expand(cfg, ['nocuts', 'basiccuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res'])

    return cfg
