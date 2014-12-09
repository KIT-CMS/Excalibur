import ArtusConfigBase


def getBaseConfig(tagged, **kwargs):
    cfg = {
        'SkipEvents': 0,
        'EventCount': -1,
        'GlobalProducer': [],
        'L1Correction': 'L1FastJet',
        'EnableMetPhiCorrection': False,
        'MetPhiCorrectionParameters': [],
        'EnablePuReweighting': False,
        'Enable2ndJetReweighting': False,
        'EnableSampleReweighting': False,
        'EnableLumiReweighting': False,
        'HcalCorrection': 0.0,
        'Jec': "data or mc?",
        'JsonFile': "year?",
        'InputFiles': [],     # overridden by artus
        'OutputPath': "out",  # overridden by artus
        'Pipelines': {
            'default': {
                'Level': 1,
                'JetAlgorithm': "AK5PFJetsCHSL1L2L3",
                'Consumer': ["ntuple"],
                'Filter': [],
                'QuantitiesVector': [
                    "zpt", "zeta", "zy",
                    "zphi", "zmass", "npv", "rho",
                    "weight",
                    "jet1pt", "jet1eta", "jet1y", "jet1phi", "mpf", "rawmpf",
                    "METpt", "METphi", "rawMETpt", "rawMETphi", "sumEt", "jet1photonfraction",
                    "jet1chargedemfraction", "jet1chargedhadfraction", "jet1neutralhadfraction",
                    "jet1muonfraction", "jet1HFhadfraction", "jet1HFemfraction",
                    "jet2pt", "jet2eta", "jet2phi", "uept", "uephi", "ueeta",
                    "otherjetspt", "otherjetseta", "otherjetsphi",
                    "njets", "njetsinv", "njets30", "njets30barrel",
                    "jet1unc", "nputruth",
                ]
            }
        },
        'MinBiasXS': 68.5,
        'Tagged': tagged,
        'VetoPileupJets': False,
        'checkKappa': False,
        'RC': False,  # also provide random cone offset JEC, and use for type-I
        'FlavourCorrections': False,  # calculate additional MC flavour corrections

        # Wire kappa objects
        'electrons': 'electrons',
    }
    if tagged:
        cfg['Pipelines']['default']['QuantitiesVector'] += [
            "qglikelihood", "qgmlp",
            "combinedsecondaryvertexbjettag", "combinedsecondaryvertexmvabjettag",
            "jet1puJetIDFullLoose", "jet1puJetIDFullMedium", "jet1puJetIDFullTight",
            "jet1puJetIDCutbasedLoose", "jet1puJetIDCutbasedMedium", "jet1puJetIDCutbasedTight",
            "jet2puJetIDFullLoose", "jet2puJetIDFullMedium", "jet2puJetIDFullTight",
            "jet2puJetIDCutbasedLoose", "jet2puJetIDCutbasedMedium", "jet2puJetIDCutbasedTight",
        ]
    return cfg


##
##


def data(cfg, **kwargs):
    cfg['InputType'] = 'data'
    cfg['Pipelines']['default']['QuantitiesVector'] += ['run', 'eventnr', 'lumisec']
    cfg['Pipelines']['default']['Filter'].append('json')
    cfg['Pipelines']['default']['Filter'].append('hlt')
    cfg['GlobalProducer'] += ['hlt_selector', 'pileuptruth_producer']


def mc(cfg, addLHE, rundep, flavourCorrections, **kwargs):
    cfg['InputType'] = 'mc'
    cfg['Pipelines']['default']['QuantitiesVector'] += [
                    "npu", "eff",
                    "genjet1pt", "genjet1eta", "genjet1phi", "genjet2pt",
                    "matchedgenjet1pt", "matchedgenjet2pt", "genmpf",
                    "algoflavour", "physflavour",
                    "algopt", "physpt",
                    "jet1ptneutrinos", "genjet1ptneutrinos", "mpfneutrinos", "neutralpt3", "neutralpt5",
                    "genmupluspt", "genmupluseta", "genmuplusphi",
                    "genmuminuspt", "genmuminuseta", "genmuminusphi",
                    "ngenmuons", "ngenphotons", "ngenphotonsclose", "closestphotondr", "nzs", "ninternalmuons", "nintermediatemuons", "ptgenphotonsclose", "ptdiff13", "ptdiff12", "ptdiff23",
                    "genzpt", "genzy", "genzmass", "deltaRzgenz",
                    "deltaRgenjet1genjet2", "deltaRjet1jet2", "deltaRjet1genjet1", "deltaRjet2genjet2"
    ]
    cfg['GlobalProducer'] += ['jet_matcher', 'gen_balance_producer', 'gen_met_producer', 'weight_producer', 'flavour_producer']
    # put the gen_producer first since e.g. l5_producer depend on it
    cfg['GlobalProducer'].insert(0, 'gen_producer')
    cfg['AK5GenJets'] = 'AK5GenJetsNoNu'

    if addLHE:
        cfg['GlobalProducer'] += ['lhe_producer']
        cfg['LHE'] = 'LHE'
        cfg['Pipelines']['default']['QuantitiesVector'] += [
            'lhezpt', 'lhezeta', 'lhezy', 'lhezphi', 'lhezmass',
            'nlheelectrons', 'nlhemuons', 'nlhetaus',
        ]
    else:
        cfg['LHE'] = ''
    if rundep:
        cfg['Pipelines']['default']['QuantitiesVector'] += ['run', 'eventnr', 'lumisec']
    if flavourCorrections:
        cfg['FlavourCorrections'] = True
        cfg['Pipelines']['default']['QuantitiesVector'] += ["algol5pt", "physl5pt"]
        #insert l5_producer directly after jet corrector
        cfg['GlobalProducer'].insert(cfg['GlobalProducer'].index('jet_corrector') + 1, 'l5_producer')
        cfg['Pipelines']['default']['QuantitiesVector'] += ["mpfalgo", "mpfphys",
            "mpfneutrinosalgo", "mpfneutrinosphys", "jet1ptneutrinosalgo", "jet1ptneutrinosphys"]

##
##


def _2011(cfg, **kwargs):
    cfg['Run'] = 2011


def _2012(cfg, **kwargs):
    cfg['Run'] = '2012'


##
##


def ee(cfg, **kwargs):
    cfg['GlobalProducer'] = [
        'valid_electron_producer', 'electron_corrector', 'zee_producer',
         'valid_jet_ee_producer', 'jet_corrector', 'typeImet_producer',
         'jet_sorter', 'leading_jet_uncertainty_producer',
    ]
    cfg['Pipelines']['default']['QuantitiesVector'] += [
        "nelectrons",
        "emass", "ept", "eeta",
        "eminusmass", "eminuspt", "eminuseta", "eminusphi", "eminusiso", "eminusid", "eminustrigid",
        "eplusmass", "epluspt", "epluseta", "eplusphi", "eplusiso", "eplusid", "eplustrigid",
        "eplusecaliso03", "eminusecaliso03", "eplusecaliso04", "eminusecaliso04",
        "eplusidloose", "eplusidmedium", "eplusidtight", "eplusidveto",
        "eminusidloose", "eminusidmedium", "eminusidtight", "eminusidveto",
        "eidveto"
    ]
    cfg['ElectronID'] = 'loose'
    cfg['muons'] = ''
    cfg['electrons'] = 'electrons'
    cfg['Channel'] = 'ee'
    cfg['ExcludeECALGap'] = True

    cfg['Pipelines']['default'].update({
        'GenCuts': False,
        'Cuts': [
            'electron_eta',
            'electron_pt',
            'zmass_window',
            'zpt',

            'leadingjet_pt',
            'back_to_back',
        ],
        'CutElectronEta': 2.4,
        'CutElectronPt': 25.0,

        'CutZMassWindow': 10.0,
        'CutZPt': 30.0,

        'CutLeadingJetEta': 1.3,
        'CutLeadingJetPt': 12.0,

        'CutSecondLeadingToZPt': 0.2,
        'CutBack2Back': 0.34,
    })
    cfg['Pipelines']['default']['Filter'] += ['valid_z', 'valid_jet', 'metfilter', 'incut']


def em(cfg, **kwargs):
    # The order of these producers is important!
    cfg['GlobalProducer'] = [
        'valid_electron_producer', 'electron_corrector',
        'valid_muon_producer', 'muon_corrector',
        'zemu_producer',
    ]
    cfg['Pipelines']['default']['QuantitiesVector'] = [
        "zpt", "zmass"
    ]
    cfg['ElectronID'] = 'loose'
    cfg['muons'] = 'muons'
    cfg['electrons'] = 'correlectrons'
    cfg['Channel'] = 'emu'
    cfg['ExcludeECALGap'] = True

    cfg['Pipelines']['default'].update({
        'GenCuts': False,
        'Cuts': [
            #'muon_pt',
            #'muon_eta',
            'zemu_cuts',

            #'electron_eta',
            #'electron_pt',

            'zmass_window',
            'zpt',
        ],
        'CutMuonEta': 2.3,
        'CutMuonPt': 20.0,

        'CutElectronEta': 2.4,
        'CutElectronPt': 25.0,

        'CutZMassWindow': 10.0,
        'CutZPt': 30.0,
    })
    cfg['Pipelines']['default']['Filter'] += ['valid_z', 'incut']


def mm(cfg, **kwargs):
    # The order of these producers is important!
    cfg['GlobalProducer'] = [
        'valid_muon_producer', 'muon_corrector', 'z_producer',
        'valid_jet_producer', 'jet_corrector', 'typeImet_producer', 'jet_sorter',
        'unclustered_energy_producer', 'leading_jet_uncertainty_producer',
    ]
    cfg['Pipelines']['default']['QuantitiesVector'] += [
        "mupluspt", "mupluseta", "muplusphi",
        "muminuspt", "muminuseta", "muminusphi",
        "mu1pt", "mu1eta", "mu1phi",
        "mu2pt", "mu2eta", "mu2phi",
        "nmuons", "muplusiso", "muminusiso",
    ]
    cfg['muons'] = 'muons'
    cfg['electrons'] = ''
    cfg['Channel'] = 'mm'

    cfg['Pipelines']['default'].update({
            'GenCuts': False,
            'Cuts': [
                'zpt',
                'leadingjet_pt',
                'muon_eta',
                'muon_pt',
                'zmass_window',
                'back_to_back',
            ],
            'CutMuonEta': 2.3,
            'CutMuonPt': 20.0,
            'CutZMassWindow': 20.0,
            'CutLeadingJetEta': 1.3,

            'CutSecondLeadingToZPt': 0.2,
            'CutBack2Back': 0.34,

            'CutZPt': 30.0,
            'CutLeadingJetPt': 12.0,
    })
    cfg['Pipelines']['default']['Filter'] += ['valid_z', 'valid_jet', 'metfilter', 'incut']


###
###


def data_2011(cfg, **kwargs):
    cfg['Jec'] = ArtusConfigBase.getPath() + "/data/jec/GR_R_44_V13/GR_R_44_V13"
    cfg['JsonFile'] = ArtusConfigBase.getPath() + "/data/json/Cert_160404-180252_7TeV_ReRecoNov08_Collisions11_JSON_v2.txt"
    cfg['PileupTruth'] = ArtusConfigBase.getPath() + "/data/pileup/2011_pumean_pixelcorr.txt"


def data_2012(cfg, **kwargs):
    cfg['JsonFile'] = ArtusConfigBase.getPath() + "/data/json/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt"
    cfg['Jec'] = ArtusConfigBase.getPath() + "/data/jec/Winter14_V5/Winter14_V5_DATA"
    cfg['MetPhiCorrectionParameters'] = [0.2661, 0.3217, -0.2251, -0.1747]
    cfg['PileupTruth'] = ArtusConfigBase.getPath() + "/data/pileup/pumean_pixelcorr.txt"


def mc_2011(cfg, **kwargs):
    cfg['Jec'] = ArtusConfigBase.getPath() + "/data/jec/START44_V12/START44_V12"
    cfg["EnablePuReweighting"] = True
    cfg['PileupWeights'] = ArtusConfigBase.getPath() + "/data/pileup/weights_160404-180252_7TeV_ReRecoNov08_kappa539_MC11.root"


def mc_2012(cfg, **kwargs):
    cfg['Jec'] = ArtusConfigBase.getPath() + "/data/jec/Winter14_V5/Winter14_V5_MC"
    cfg['MetPhiCorrectionParameters'] = [0.1166, 0.0200, 0.2764, -0.1280]
    cfg["EnablePuReweighting"] = True


def mcee(cfg, **kwargs):
    cfg['Pipelines']['default']['QuantitiesVector'] += [
        "ngenelectrons", "ngeninternalelectrons", "ngenintermediateelectrons",
        "genepluspt", "genepluseta", "geneplusphi",
        "geneminuspt", "geneminuseta", "geneminusphi",
        "deltaReplusgeneplus", "deltaReminusgeneminus",
        'sf', 'sfplus', 'sfminus'
    ]
    cfg['GlobalProducer'] += ['electron_sf_producer']
    if cfg['ElectronID'] == 'mva':
        cfg['ScaleFactors'] = ArtusConfigBase.getPath() + '/data/Electron-NontrigMVAIdScaleFactors.root'
    elif cfg['ElectronID'] in ['loose', 'medium', 'tight', 'veto']:
        cfg['ScaleFactors'] = ArtusConfigBase.getPath() + '/data/Electron-CutBasedIdScaleFactors.root'


def _2011mm(cfg, **kwargs):
    cfg['MuonID2011'] = True


def _2012mm(cfg, **kwargs):
    cfg['MuonID2011'] = False


##
##

def mc_2011mm(cfg, **kwargs):
    cfg["MuonSmearing"] = True
    cfg["MuonRadiationCorrection"] = False
    cfg["MuonCorrectionParameters"] = ArtusConfigBase.getPath() + "/data/muoncorrection/MuScleFit_2011_MC_44X.txt"


def mc_2012ee(cfg, **kwargs):
    cfg['PileupWeights'] = ArtusConfigBase.getPath() + "/data/pileup/weights_190456-208686_8TeV_22Jan2013ReReco_2014_01_31_zee_mc.root"
    cfg['HltPaths'] = ["HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v%d" % v for v in range(15, 20)]
    cfg['GlobalProducer'] += ['hlt_selector']
    cfg['Pipelines']['default']['Filter'].append('hlt')
    cfg['Pipelines']['default']['QuantitiesVector'].append('hlt')


def mc_2012mm(cfg, **kwargs):
    cfg['PileupWeights'] = ArtusConfigBase.getPath() + "/data/pileup/weights_190456-208686_8TeV_22Jan2013ReReco_68_5mb_kappa539_MC12_madgraph_tags.root"
    cfg["MuonSmearing"] = True
    cfg["MuonRadiationCorrection"] = False
    cfg["MuonCorrectionParameters"] = ArtusConfigBase.getPath() + "/data/muoncorrection/MuScleFit_2012_MC_53X_smearReReco.txt"


def data_2011mm(cfg, **kwargs):
    cfg['HltPaths'] = [
        # Mu7 Trigger
        "HLT_DoubleMu7_v1", "HLT_DoubleMu7_v2", "HLT_DoubleMu7_v3", "HLT_DoubleMu7_v4", "HLT_DoubleMu7_v5",
        # Mu8 Trigger
        "HLT_Mu8_v16",
        # Mu13_Mu8 Trigger
        "HLT_Mu13_Mu8_v1", "HLT_Mu13_Mu8_v2", "HLT_Mu13_Mu8_v3", "HLT_Mu13_Mu8_v4", "HLT_Mu13_Mu8_v5",
        "HLT_Mu13_Mu8_v6", "HLT_Mu13_Mu8_v7", "HLT_Mu13_Mu8_v8", "HLT_Mu13_Mu8_v9", "HLT_Mu13_Mu8_v10",
        "HLT_Mu13_Mu8_v11", "HLT_Mu13_Mu8_v12", "HLT_Mu13_Mu8_v13", "HLT_Mu13_Mu8_v14",
        "HLT_Mu13_Mu8_v15", "HLT_Mu13_Mu8_v16", "HLT_Mu13_Mu8_v17", "HLT_Mu13_Mu8_v18",
        # Mu17_Mu8 Trigger
        "HLT_Mu17_Mu8_v10", "HLT_Mu17_Mu8_v11"
        ]
    cfg["MuonSmearing"] = False
    cfg["MuonRadiationCorrection"] = False
    cfg["MuonCorrectionParameters"] = ArtusConfigBase.getPath() + "/data/muoncorrection/MuScleFit_2011_DATA_44X.txt"


def data_2012mm(cfg, **kwargs):
    cfg['HltPaths'] = ["HLT_Mu17_Mu8_v%d" % v for v in range(1, 30)]
    cfg["MuonRadiationCorrection"] = False
    cfg["MuonSmearing"] = False
    cfg["MuonCorrectionParameters"] = ArtusConfigBase.getPath() + "/data/muoncorrection/MuScleFit_2012ABC_DATA_ReReco_53X.txt"
    cfg["MuonCorrectionParametersRunD"] = ArtusConfigBase.getPath() + "/data/muoncorrection/MuScleFit_2012D_DATA_ReReco_53X.txt"


def data_2012ee(cfg, **kwargs):
    cfg['HltPaths'] = ["HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v%d" % v for v in range(15, 20)]


def data_2012em(cfg, **kwargs):
    cfg['HltPaths'] = ["HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v%d" % v for v in range(3, 10)] + ["HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v%d" % v for v in range(3, 10)]


