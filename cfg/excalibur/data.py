import ZJetConfigBase as base


def config():
    cfg = base.getConfig('data', 2012, 'mm')
    cfg["InputFiles"] = base.setInputFiles(
        ekppath="/storage/6/berger/kappatest/skim_kappa2_data.root", # DATA, AK5PFTaggedJets missing
        nafpath=""
    )
    cfg = base.expand(cfg, ['nocuts', 'zcuts', 'finalcuts'])
    print cfg
    return cfg
