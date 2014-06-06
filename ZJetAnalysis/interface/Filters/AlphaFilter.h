#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../ZJetTypes.h"

class AlphaFilter: public ZJetFilterBase {
public:

	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "alpha";
	}

	bool DoesEventPass(ZJetEvent const& event,
			ZJetProduct const& product, ZJetSettings const& settings) const
	{
		return DoesEventPass(event, product, settings.GetTaggedJets(), settings.GetAlphaMax());
	}

private:

	virtual bool DoesEventPass(ZJetEvent const& event,
		ZJetProduct const& product, std::string const& algoname, float const& alphamax) const
	{
		if (product.GetSecondJet(algoname)->p4.Pt() / product.Z.p4.Pt() > alphamax)
			return false;
		else
			return true;
	}
};


