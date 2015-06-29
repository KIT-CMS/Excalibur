#pragma once

#include "Artus/KappaAnalysis/interface/KappaSettings.h"

class ZJetSettings : public KappaSettings
{
  public:
	// ZProducer
	IMPL_SETTING_DEFAULT(float, ZMass, 91.1876)
	IMPL_SETTING(float, ZMassRange)

	// TypeIMETProducer
	IMPL_SETTING_DEFAULT(float, JetPtMin, 10.)
	IMPL_SETTING(bool, EnableMetPhiCorrection)
	IMPL_SETTING_DOUBLELIST(MetPhiCorrectionParameters)
	
	// ZJetValidJetsProducer
	//IMPL_SETTING_DEFAULT(std::string, JetAlgorithm, "")
	//IMPL_SETTING_STRINGLIST_DEFAULT(GlobalAlgorithms, {});
	
	// ZJetCorrectionsProducer
	IMPL_SETTING_DEFAULT(std::string, CorrectionLevel, "None")
	IMPL_SETTING(std::string, Jec)
	IMPL_SETTING(std::string, L1Correction)
	IMPL_SETTING(bool, RC)
	IMPL_SETTING(bool, FlavourCorrections)
	
	// RecoJetGenJetMatchingProducer
	IMPL_SETTING_DEFAULT(double, DeltaRMatchingRecoJetGenJet, 0.25)

	// RadiationJetProducer
	IMPL_SETTING_DEFAULT(double, DeltaRRadiationJet, 1.0)
	
	// ZJetCutsFilter
	IMPL_SETTING_DEFAULT(int, CutNMuonsMin, 2)
	IMPL_SETTING_DEFAULT(int, CutNMuonsMax, 3)
	IMPL_SETTING(float, CutMuonPtMin)
	IMPL_SETTING(float, CutMuonEtaMax)
	IMPL_SETTING(float, CutLeadingJetPtMin)
	IMPL_SETTING(float, CutLeadingJetEtaMax)
	IMPL_SETTING(float, CutZPtMin)
	IMPL_SETTING(float, CutBackToBack)
	IMPL_SETTING(float, CutAlphaMax)
	IMPL_SETTING_DEFAULT(float, CutBetaMax, 1.0)

	IMPL_SETTING(std::string, NPUFile);
	IMPL_SETTING(double, Minbxsec);

};
