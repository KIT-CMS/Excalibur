#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../ZJetTypes.h"

class DeltaPhiFilter: public ZJetFilterBase {
public:

	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "deltaphi";
	}


	bool DoesEventPass(ZJetEvent const& event,
			ZJetProduct const& product, ZJetSettings const& settings) const
	{
		return DoesEventPass(event, product, settings.GetTaggedJets(), settings.GetDeltaPhiMax());
	}

private:

	virtual bool DoesEventPass(ZJetEvent const& event,
		ZJetProduct const& product, std::string const& algoname, float const& deltaphimax) const
	{
		if ( (ROOT::Math::Pi() - ROOT::Math::VectorUtil::DeltaR(product.GetLeadingJet(algoname)->p4,
						product.Z.p4) ) > deltaphimax)
			return false;
		else
			return true;
	}
};


