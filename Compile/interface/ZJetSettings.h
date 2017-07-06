#pragma once

#include "Artus/KappaAnalysis/interface/KappaSettings.h"

class ZJetSettings : public KappaSettings
{
  public:
    // ValidZllJetsProducer
    IMPL_SETTING(float, MinZllJetDeltaRVeto)

    // TypeIMETProducer
    IMPL_SETTING(float, TypeIJetPtMin)
    IMPL_SETTING_DEFAULT(bool, EnableMetPhiCorrection, false)
    IMPL_SETTING_DOUBLELIST(MetPhiCorrectionParameters)

    // ZJetCorrectionsProducer
    IMPL_SETTING_DEFAULT(std::string, CorrectionLevel, "None")
    IMPL_SETTING(std::string, Jec)
    IMPL_SETTING(std::string, L1Correction)
    IMPL_SETTING(bool, RC)
    IMPL_SETTING(bool, FlavourCorrections)
    IMPL_SETTING_DEFAULT(bool, ProvideL2ResidualCorrections, false)
    IMPL_SETTING_DEFAULT(bool, ProvideL2L3ResidualCorrections, false)

    // RecoJetGenJetMatchingProducer
    IMPL_SETTING_DEFAULT(double, DeltaRMatchingRecoJetGenJet, 0.25)

    // ZJetNumberGeneratedEventsWeightProducer (sample reweighting)
    IMPL_SETTING_DEFAULT(bool, SampleReweighting, false)
    IMPL_SETTING_DOUBLELIST(SampleReweightingCrossSections)
    IMPL_SETTING_INTLIST(SampleReweightingNEvents)

    // NPUProducer (insert npu from external file)
    IMPL_SETTING(std::string, NPUFile)  // pileup JSON reformatted as csv
    IMPL_SETTING(float, Minbxsec)       // MinBias Cross Section in mb

    // ZJetValidElectronsProducer
    IMPL_SETTING_DEFAULT(bool, ExcludeECALGap, false)

    // ZJetCutsFilter
    IMPL_SETTING(unsigned, CutNLeptonsMin)
    IMPL_SETTING(unsigned, CutNLeptonsMax)
    IMPL_SETTING(float, CutLeadingLeptonPtMin)   
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
	IMPL_SETTING(float, CutGenHTMax)
	IMPL_SETTING(std::string, CutEtaPhiCleaning)
	IMPL_SETTING(std::string, CutJetID)
	
       // LeptonSFProducer
    IMPL_SETTING(std::string, LeptonSFRootfile)
    IMPL_SETTING(std::string, LeptonTriggerSFRootfile)
    IMPL_SETTING_INTLIST(TriggerSFRuns)   
    IMPL_SETTING_DEFAULT(std::string, LeptonSFVariation, "None")
    IMPL_SETTING_DEFAULT(std::string, LeptonTriggerSFVariation, "None")
    IMPL_SETTING_DEFAULT(std::string, Channel, "mm")

    //GenZProducers
    IMPL_SETTING_DEFAULT(float, GenZMassRange, 20.0)
};
