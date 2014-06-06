#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../ZJetTypes.h"

class JetPtFilter: public ZJetFilterBase {
public:

	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "jetpt";
	}

	bool DoesEventPass(ZJetEvent const& event,
			ZJetProduct const& product, ZJetSettings const& settings) const
	{
		return DoesEventPass(event, product, settings.GetTaggedJets(), settings.GetJetPtMin());
	}

private:

	virtual bool DoesEventPass(ZJetEvent const& event,
		ZJetProduct const& product, std::string const& algoname, float const& jetptmin) const
	{
		if (product.GetLeadingJet(algoname)->p4.Pt() < jetptmin)
			return false;
		else
			return true;
	}
};


