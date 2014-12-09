import ArtusConfigBase as base


def config():
    cfg = base.BaseConfig('mc', '2012', rundepMC=True, flavourCorrections=True, lhe=True)
    cfg["InputFiles"] = base.setInputFiles(
        ekppath="/storage/9/dhaitz/skims/2014_07_18_ee-mm-mcRD/*.root",
        nafpath="/nfs/dust/cms/user/dhaitz/skims/2014_07_18_ee-mm-mcRD/*.root"
    )
    cfg = base.expand(cfg, ['all', 'zcuts', 'incut'])
    cfg['PileupWeights'] = base.getPath() + "/data/pileup/weights_190456-208686_8TeV_22Jan2013ReReco_kappa5313_MC12_madgraph_rundep-2.root"
    cfg['RC'] = True
    cfg['EnableLumiReweighting'] = True
    cfg['EnableTriggerReweighting'] = True
    cfg['NEvents'] = 30459503
    cfg['XSection'] = 3503.71
    return cfg
