/* Copyright (c) 2013 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/KappaAnalysis/interface/KappaProduct.h"


class ZJetProduct : public KappaProduct
{
public:
	ZJetProduct() : KappaProduct() {};

	float m_product;
	KDataMuons m_validmuons;
	KDataMuons m_invalidmuons;
	const KDataMuon * m_decaymuons [2];

	bool has_valid_z;

	KDataLV Z;

	HLTTools* m_hltInfo = new HLTTools;
	
	std::map<std::string, KDataPFTaggedJets> m_validjets;
	std::map<std::string, KDataPFTaggedJets> m_invalidjets;

	KDataPFTaggedJet GetLeadingJet(std::string const& algoname) const
	{
		return m_validjets.at(algoname).at(0);
	}

	KDataPFTaggedJet GetSecondJet(std::string const& algoname) const
	{
		return m_validjets.at(algoname).at(1);
	}

	float GetMPF(const KDataPFMET* met) const //type1 !!!
	{
		return 1.0f + (Z.p4.Px() * met->p4.Px()
			+ Z.p4.Py() * met->p4.Py()) /
			 (Z.p4.Px() * Z.p4.Px()
			+ Z.p4.Py() * Z.p4.Py());
	}

};
