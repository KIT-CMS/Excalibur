#pragma once

#include "Artus/KappaAnalysis/interface/KappaSettings.h"

class ZJetSettings : public KappaSettings
{
  public:
	// ZProducer
	IMPL_SETTING_DEFAULT(float, ZMass, 91.1876)
	IMPL_SETTING(float, ZMassRange)

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
	
	// ZJetCutsFilter
	IMPL_SETTING(float, CutMuonPtMin)
	IMPL_SETTING(float, CutMuonEtaMax)
	IMPL_SETTING(float, CutLeadingJetPtMin)
	IMPL_SETTING(float, CutLeadingJetEtaMax)
};
