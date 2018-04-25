import configtools
import os

def config():
    cfg = configtools.getConfig('mc', 2016, 'mm', bunchcrossing='25ns')
    cfg["InputFiles"].set_input(
        #ekppath='/storage/gridka-nrg/tberger/Skimming/ZJet_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16_noJTB/*.root',
        #ekppath='/storage/c/tberger/testfiles/skimming_output/mc/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16_testfile_noJTB.root',
        ekppath="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-herwigpp_RunIISummer16_noJTB/*.root",
        nafpath="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-herwigpp_RunIISummer16_noJTB/*.root",
        #nafpath="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/testfiles/Zll_DYJetsToLL_M-50_madgraphMLM-herwigpp_RunIISummer16_testfile_noJTB.root",
        )
    cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'allzcuts', 'genzcuts'], ['None'])#,'L1L2L3''leptoncuts','genleptoncuts', 'allleptoncuts'
    configtools.remove_quantities(cfg, ['jet1flavor','jet1rc'])
    configtools.add_quantities(cfg, [   'mu1IDSFWeight', 'mu2IDSFWeight', 'leptonIDSFWeight',
                                        'mu1IsoSFWeight','mu2IsoSFWeight','leptonIsoSFWeight',
                                        'mu1TrackingSFWeight','mu2TrackingSFWeight','leptonTrackingSFWeight',
                                        'mu1TriggerSFWeight','mu2TriggerSFWeight','leptonTriggerSFWeight',
                                        #'leptonSFWeight','leptonTriggerSFWeight',
                                        #'jet1puidraw',
                                        ])
##### Add Producers: #####
    cfg['Processors'] = [  'producer:MuonTriggerMatchingProducer',
                            ] + cfg['Processors'] + [
                            'producer:LeptonIDSFProducer',
                            'producer:LeptonIsoSFProducer',
                            'producer:LeptonTrackingSFProducer',
                            'producer:LeptonTriggerSFProducer',
                            'producer:LeptonSFProducer',
                            ]
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
##### Specify input sources for Jets & Muons: #####
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
    cfg['ValidMuonsInput'] = "corrected"
    cfg['TaggedJets'] = 'ak4PFJets' # JTB switched off, non-CHS Jets
    cfg['GenJets'] = 'ak4GenJets'   # JTB switched off
##### Change selection: (see also http://cms.cern.ch/iCMS/analysisadmin/cadilines?line=SMP-17-002&tp=an&id=1891&ancode=SMP-17-002) #####
    cfg['MuonIso'] = 'loose'
    cfg['MuonID'] = 'tight'
    cfg['CutMuonPtMin'] = 25.0
    cfg['CutMuonEtaMax'] = 2.4
    cfg['ZMassRange'] = 15.0
    cfg['HltPaths'] = ['HLT_IsoMu24', 'HLT_IsoTkMu24']
    cfg["MuonTriggerFilterNames"] = ['HLT_IsoMu24_v2:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09','HLT_IsoTkMu24_v3:hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09']
##### LeptonSF files: #####
    cfg['LeptonIDSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/ID_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonIsoSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Iso_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Trigger_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonTrackingSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Tracking_EfficienciesAndSF_BCDEFGH.root")
##### MC specific properties: #####
    cfg['NumberGeneratedEvents'] = 122055388 # from geteventsscript
    cfg['GeneratorWeight'] =  1.0 #0.670123731536
    cfg['CrossSection'] = 1921.8*3
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/PUWeights_BCDEFGH_13TeV_23Sep2016ReReco_DYJetsToLL_M-50_madgraphMLM-herwigpp_RunIISummer16.root')
    return cfg
