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
/*
	#TODO update this code so it'll compile with Kappa2.0
	
	float m_product;
	KMuons m_validmuons;
	KMuons m_invalidmuons;
	const KMuon * m_decaymuons [2];

	bool has_valid_z;
	bool has_valid_genz;

	KLV Z;
	KGenParticle GenZ;
	KGenParticles m_genmuons;

	KJet * GetLeadingJet(std::string const& algoname) const
	{
		//if (std::string::npos == algoname.find("L1"))
			return static_cast<KJet*> (m_validJets.at(0));
		//else
		//	return SafeMap::Get(m_validjets, algoname).at(0);
	}

	KJet * GetSecondJet(std::string const& algoname) const
	{
		//if (std::string::npos == algoname.find("L1"))
		//{
			return static_cast<KJet*> (m_validJets.at(1));
			/*}
		else if (m_validjets.at(algoname).size() < 2)
		{
			KJet jet;
			return jet;
		}
		return SafeMap::Get(m_validjets, algoname).at(1);
			
	}

	float GetMPF(const KMET* met) const //type1 !!!
	{
		return 1.0f + (Z.p4.Px() * met->p4.Px()
			+ Z.p4.Py() * met->p4.Py()) /
			 (Z.p4.Px() * Z.p4.Px()
			+ Z.p4.Py() * Z.p4.Py());
	}
*/
};
