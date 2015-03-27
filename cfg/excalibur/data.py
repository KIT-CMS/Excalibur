import ZJetConfigBase as base


def config():
    cfg = base.getConfig('data', 2012, 'mm')
    cfg["InputFiles"] = base.setInputFiles(
        #ekppath="/storage/6/berger/kappatest/skim_kappa2_data.root",
        #ekppath="/storage/a/berger/kappatest/output/higgsTauTau_kSkimming_cfg.root",
        ekppath="/storage/6/berger/testfiles/kappa_DYJetsToLL_M_50_madgraph_8TeV_5147.root",
        nafpath=""
    )
    #algorithms = ["AK5PFTaggedJetsL1L2L3Res"]
    #base.addCHS(algorithms)
    #cfg = base.expand(cfg, ['nocuts', 'zcuts', 'finalcuts'], algorithms)
    cfg = base.expand(cfg, ['nocuts', 'zcuts', 'finalcuts'])
    print cfg
    return cfg
