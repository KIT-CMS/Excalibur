import configtools
import os

RUN = 'BCDEFGH'
JEC = 'Summer16_07Aug2017_V1'

def config():
    cfg = configtools.getConfig('mc', 2016, 'mm', bunchcrossing='25ns')
    cfg["InputFiles"].set_input(
        ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/afriedel/Skimming/mcbkg_Moriond/ZZ/*.root",
        nafpath="/pnfs/desy.de/cms/tier2/store/user/afriedel/Skimming/mcbkg_Moriond/ZZ/*.root",
        )




    cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'leptoncuts', 'allzcuts', 'allleptoncuts','genleptoncuts','genzcuts'], ['None'])
    configtools.remove_quantities(cfg, ['jet1flavor','jet1rc'])
    # Add Muon Correction and SF Producers
    cfg['Processors'] += ['producer:MuonTriggerMatchingProducer','producer:LeptonSFProducer','producer:LeptonTriggerSFProducer',]
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
    cfg['ValidMuonsInput'] = "corrected"
    cfg['MuonIso'] = 'loose'
    cfg['CutMuonPtMin'] = 22.0
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_MC/'+JEC+'_MC')
    cfg['NumberGeneratedEvents'] = 998034
    
    cfg['CrossSection'] = 15.6  # http://arxiv.org/pdf/1512.05314v2.pdf
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/PUWeights_'+RUN+'_13TeV_23Sep2016ReReco_ZZ.root')
    cfg['LeptonSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016all/SFMC_BCDEF.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016all/SFTriggerMC_BCDEF.root")
    cfg['TriggerSFRuns'] = []
    return cfg
