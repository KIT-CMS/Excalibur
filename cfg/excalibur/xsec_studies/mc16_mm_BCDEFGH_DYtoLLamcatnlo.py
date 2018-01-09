import configtools
import os

RUN = 'BCDEFGH'
JEC = 'Summer16_07Aug2017_V3'

def config():
    cfg = configtools.getConfig('mc', 2016, 'mm', bunchcrossing='25ns')
    cfg["InputFiles"].set_input(
        #ekppath='/storage/c/tberger/testfiles/skimming_output/mc/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16_testfile.root',
        ekppath="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16/*.root",
        #ekppath="srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/tberger/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root"
        #ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/MC-Summer16_metfix/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16/*.root",
        #ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1/*.root",
        nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25nsv2_v0-v1/*.root"
        )
    cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'leptoncuts', 'allzcuts', 'allleptoncuts','genleptoncuts','genzcuts'], ['None','L1L2L3'])
    configtools.remove_quantities(cfg, ['jet1flavor','jet1rc'])
    # Add Muon SF and Correction Producers
    cfg['Processors'] += ['producer:MuonTriggerMatchingProducer','producer:LeptonSFProducer','producer:LeptonTriggerSFProducer',]
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
    cfg['ValidMuonsInput'] = "corrected"
    cfg['MuonIso'] = 'loose'
    cfg['CutMuonPtMin'] = 22.0
    cfg['CutZPtMin'] = 40.0
    cfg['CutLeadingJetEtaMax'] = 2.5
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_MC/'+JEC+'_MC')
    cfg['NumberGeneratedEvents'] = 122055388 # from geteventsscript
    cfg['GeneratorWeight'] =  0.670123731536
    cfg['CrossSection'] = 1921.8*3
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/PUWeights_BCDEFGH_13TeV_23Sep2016ReReco_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
    cfg['LeptonSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016all/SFMC_BCDEF.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016all/SFTriggerMC_BCDEF.root")
    cfg['TriggerSFRuns'] = []
    return cfg
