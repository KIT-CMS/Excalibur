#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../ZJetTypes.h"

class JetEtaFilter: public ZJetFilterBase {
public:

	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "jeteta";
	}

	virtual bool DoesEventPass(ZJetEvent const& event,
	ZJetProduct const& product,
	ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		return DoesEventPass(event, product, settings.GetJetAlgorithm() , settings.GetJetEtaMax());
	}

private:

	virtual bool DoesEventPass(ZJetEvent const& event,
		ZJetProduct const& product, std::string const& algoname, float const& jetetamax) const
	{
		if (std::abs(product.GetLeadingJet(algoname)->p4.Eta()) > jetetamax)
			return false;
		else
			return true;
	}
};


