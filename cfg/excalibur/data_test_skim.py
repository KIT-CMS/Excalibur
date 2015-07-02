import ZJetConfigBase as base


def config():
    cfg = base.getConfig('data', 2012, 'mm')
    cfg["InputFiles"] = base.setInputFiles(
        ekppath="/storage/a/mfischer/references/skims/skim_cmwssw_7_4_2.root",
        nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-05-18_DoubleMu_Run2012_22Jan2013_8TeV/*.root",
    )
    cfg = base.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['L1L2L3', 'L1L2L3Res'])

    return cfg
