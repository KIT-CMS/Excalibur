import ZJetConfigBase as base


def config():
    cfg = base.getConfig('mc', 2012, 'mm')
    cfg["InputFiles"] = base.setInputFiles(
        #ekppath="/storage/a/berger/kappatest/output/higgsTauTau_kSkimming_cfg.root", # MC, 100 events
        ekppath="/storage/6/berger/testfiles/kappa_DYJetsToLL_M_50_madgraph_8TeV_5147.root", # MC, 20000 events
        #ekppath="/storage/a/dhaitz/skims/test/DYJetsToLL_M_50_madgraph_8TeV_kappa2.root", # MC, 1000 events
        #ekppath="/home/berger/runtests/newmaster/2015-03-27_skim_kappa2_7_2_2/CMSSW_7_2_2/src/kappatuple.root", # MC, new skimmed file with different met name
        nafpath=""
    )
    cfg = base.expand(cfg, ['nocuts', 'zcuts', 'finalcuts'])
    print cfg
    return cfg
