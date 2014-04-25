/* Copyright (c) 2013 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/KappaAnalysis/interface/KappaProduct.h"
#include "Artus/Utility/interface/SafeMap.h"


class ZJetProduct : public KappaProduct
{
public:
	ZJetProduct() : KappaProduct() {};

	float m_product;
	KDataMuons m_validmuons;
	KDataMuons m_invalidmuons;
	const KDataMuon * m_decaymuons [2];

	bool has_valid_z;
	bool has_valid_genz;

	KDataLV Z;
	KDataLV GenZ;

	HLTTools* m_hltInfo = new HLTTools;
	
	std::map<std::string, KDataPFTaggedJets> m_validjets;
	std::map<std::string, KDataPFTaggedJets> m_invalidjets;

	KDataPFTaggedJet GetLeadingJet(std::string const& algoname) const
	{
		return SafeMap::Get(m_validjets, algoname).at(0);
	}

	KDataPFTaggedJet GetSecondJet(std::string const& algoname) const
	{
		if (m_validjets.at(algoname).size() < 2)
		{
			KDataPFTaggedJet jet;
			return jet;
		}
		return SafeMap::Get(m_validjets, algoname).at(1);
	}

	float GetMPF(const KDataPFMET* met) const //type1 !!!
	{
		return 1.0f + (Z.p4.Px() * met->p4.Px()
			+ Z.p4.Py() * met->p4.Py()) /
			 (Z.p4.Px() * Z.p4.Px()
			+ Z.p4.Py() * Z.p4.Py());
	}

};
