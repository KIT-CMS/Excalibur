#pragma once

#include "Artus/KappaAnalysis/interface/KappaSettings.h"

class ZJetSettings : public KappaSettings
{
  public:
    // ZProducer
    IMPL_SETTING_DEFAULT(float, ZMass, 91.1876f)
    IMPL_SETTING(float, ZMassRange)

    // ValidZllJetsProducer
    IMPL_SETTING(float, MinZllJetDeltaRVeto)

    // TypeIMETProducer
    IMPL_SETTING_DEFAULT(float, JetPtMin, 10.0f)
    IMPL_SETTING_DEFAULT(bool, EnableMetPhiCorrection, false)
    IMPL_SETTING_DOUBLELIST(MetPhiCorrectionParameters)
    IMPL_SETTING_DEFAULT(bool, MetAddMuons, false)

    // ZJetCorrectionsProducer
    IMPL_SETTING_DEFAULT(std::string, CorrectionLevel, "None")
    IMPL_SETTING(std::string, Jec)
    IMPL_SETTING(std::string, L1Correction)
    IMPL_SETTING(bool, RC)
    IMPL_SETTING(bool, FlavourCorrections)
    IMPL_SETTING(bool, ProvideResidualCorrections)

    // RecoJetGenJetMatchingProducer
    IMPL_SETTING_DEFAULT(double, DeltaRMatchingRecoJetGenJet, 0.25)

    // RadiationJetProducer
    IMPL_SETTING_DEFAULT(double, DeltaRRadiationJet, 1.0)

    // ZJetNumberGeneratedEventsWeightProducer (sample reweighting)
    IMPL_SETTING_DEFAULT(bool, SampleReweighting, false)
    IMPL_SETTING_DOUBLELIST(SampleReweightingCrossSections)
    IMPL_SETTING_INTLIST(SampleReweightingNEvents)

    // NPUProducer (insert npu from external file)
    IMPL_SETTING(std::string, NPUFile)  // pileup JSON reformatted as csv
    IMPL_SETTING(float, Minbxsec)       // MinBias Cross Section in mb

    // ElectronSFProducer
    IMPL_SETTING(std::string, ElectronSFRootfilePath)
    IMPL_SETTING_DEFAULT(std::string, ElectronSFVariation, "None")

    // ElectronPtVariationProducer
    IMPL_SETTING(std::string, ElectronPtVariationFile)
    IMPL_SETTING_DEFAULT(std::string, ElectronPtVariation, "None")

    // MuonCorrector
    IMPL_SETTING(std::string, MuonCorrectionParameters)
    IMPL_SETTING_DEFAULT(std::string, MuonCorrectionParametersRunD, "None")
    IMPL_SETTING_DEFAULT(bool, MuonRadiationCorrection, false)
    IMPL_SETTING_DEFAULT(bool, MuonSmearing, false)

    // ZJetCutsFilter
    IMPL_SETTING(unsigned, CutNMuonsMin)
    IMPL_SETTING(unsigned, CutNMuonsMax)
    IMPL_SETTING(float, CutMuonPtMin)
    IMPL_SETTING(float, CutMuonEtaMax)
    IMPL_SETTING(float, CutElectronPtMin)
    IMPL_SETTING(float, CutElectronEtaMax)
    IMPL_SETTING(float, CutLeadingJetPtMin)
    IMPL_SETTING(float, CutLeadingJetEtaMax)
    IMPL_SETTING(float, CutZPtMin)
    IMPL_SETTING(float, CutBackToBack)
    IMPL_SETTING(float, CutAlphaMax)
    IMPL_SETTING_DEFAULT(float, CutBetaMax, 1.0f)
};
