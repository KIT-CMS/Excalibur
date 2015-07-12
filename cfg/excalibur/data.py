import ZJetConfigBase as base


def config():
    cfg = base.getConfig('data', 2012, 'mm')
    base.changeNamingScheme(cfg)
    cfg["InputFiles"] = base.setInputFiles(
        ekppath="/storage/a/mfischer/skims/2015-07-10_MF_AnyMu_2015_746/MIN_MU_COUNT_2-MIN_MU_PT_8.0/DoubleMu_Run2015B_Jul2015_13TeV/*.root",
        #nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-05-18_DoubleMu_Run2012_22Jan2013_8TeV/*.root",
    )
    cfg = base.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['L1L2L3', 'L1L2L3Res'])

    for pipeline in cfg['Pipelines']:
        for tag in ['jet1btag','jet1qgtag']:
            if tag in cfg['Pipelines'][pipeline]['Quantities']:
                cfg['Pipelines'][pipeline]['Quantities'].remove(tag)

    cfg['Jec'] = '/portal/ekpcms6/home/gfleig/new/Excalibur/data/jec/Winter14_V6/Winter14_V5_DATA'
    cfg['TaggedJets'] = 'ak5PFJetsCHS'
    cfg['PileupDensity'] = 'pileupDensity'

    for tag in ['filter:JsonFilter', 'filter:HltFilter']:
        if tag in cfg['Processors']:
            cfg['Processors'].remove(tag)

    return cfg
