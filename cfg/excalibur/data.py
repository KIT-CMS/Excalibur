import ZJetConfigBase as base


def config():
    cfg = base.getConfig('data', 2012, 'mm')
    cfg["InputFiles"] = base.setInputFiles(
        ekppath="/storage/a/dhaitz/skims/2015-04-13_DoubleMu_Run2012_22Jan2013_8TeV/*.root",
        nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-04-13_DoubleMu_Run2012_22Jan2013_8TeV/"
    )
    cfg = base.expand(cfg, ['finalcuts'])
    print cfg
    return cfg
