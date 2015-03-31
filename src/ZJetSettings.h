#pragma once

#include "Artus/KappaAnalysis/interface/KappaSettings.h"

class ZJetSettings : public KappaSettings
{
  public:
	IMPL_SETTING(bool, MuonID2011)
	IMPL_SETTING(float, MuonEtaMax)
	IMPL_SETTING(float, MuonPtMin)

	// ZProducer
	IMPL_SETTING_DEFAULT(float, ZMass, 91.1876)
	IMPL_SETTING(float, ZMassRange)

	//IMPL_SETTING(bool, VetoPileupJets)

	//IMPL_SETTING(float, ZPtMin)

	//IMPL_SETTING(float, JetEtaMax)
	//IMPL_SETTING(float, AlphaMax)
	//IMPL_SETTING(float, DeltaPhiMax)
	
	// TypeIMETProducer
	IMPL_SETTING(float, JetPtMin)
	IMPL_SETTING(bool, EnableMetPhiCorrection)
	
	// ZJetValidJetsProducer
	//IMPL_SETTING_DEFAULT(std::string, JetAlgorithm, "")
	//IMPL_SETTING_STRINGLIST_DEFAULT(GlobalAlgorithms, {});
	
	// ZJetCorrectionsProducer
	IMPL_SETTING_DEFAULT(std::string, CorrectionLevel, "None")
	//IMPL_SETTING(double, HcalCorrection)
	IMPL_SETTING(std::string, Jec)
	IMPL_SETTING(std::string, L1Correction)
	IMPL_SETTING(bool, RC)
	IMPL_SETTING(bool, FlavourCorrections)
};
