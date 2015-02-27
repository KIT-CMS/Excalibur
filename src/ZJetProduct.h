#pragma once

#include "Artus/KappaAnalysis/interface/KappaProduct.h"
#include "Artus/Utility/interface/SafeMap.h"

class ZJetProduct : public KappaProduct
{
  public:
	ZJetProduct() : KappaProduct(){};

	IMPL_PROPERTY(bool, ValidZ)
	IMPL_PROPERTY(KLV, Z)

	KJet* GetLeadingJet(std::string const& algoname) const
	{
		// if (std::string::npos == algoname.find("L1"))
		return static_cast<KJet*>(m_validJets.at(0));
		// else
		//	return SafeMap::Get(m_validjets, algoname).at(0);
	}

	KJet* GetSecondJet(std::string const& algoname) const
	{
		// if (std::string::npos == algoname.find("L1"))
		//{
		return static_cast<KJet*>(m_validJets.at(1));
		//}
		// else if (m_validjets.at(algoname).size() < 2)
		//{
		// return SafeMap::Get(m_validjets, algoname).at(1);
	}

	double GetMPF(const KLV* met) const
	{
		double scalPtEt =
		    GetRefZ().p4.Px() * met->p4.Px() + GetRefZ().p4.Py() * met->p4.Py();

		double scalPtSq = GetRefZ().p4.Px() * GetRefZ().p4.Px() +
		                  GetRefZ().p4.Py() * GetRefZ().p4.Py();

		return 1.0f + scalPtEt / scalPtSq;
	}
};
