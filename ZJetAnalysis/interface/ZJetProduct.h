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

	bool has_valid_z;

	KDataLV Z;

	HLTTools* m_hltInfo = new HLTTools;
	
	std::map<std::string, KDataPFTaggedJets> m_validjets;
	std::map<std::string, KDataPFTaggedJets> m_invalidjets;

	KDataPFTaggedJet GetLeadingJet(std::string const& algoname) const
	{
		return m_validjets.at(algoname).at(0);
	}

};
