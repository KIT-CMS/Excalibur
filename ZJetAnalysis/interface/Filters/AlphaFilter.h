#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../ZJetTypes.h"

class AlphaFilter: public ZJetFilterBase {
public:

	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "alpha";
	}

	virtual bool DoesEventPassLocal(ZJetEvent const& event,
	ZJetProduct const& product,
	ZJetPipelineSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		return DoesEventPass(event, product, settings.GetJetAlgorithm() , settings.GetAlphaMax());
	}

	bool DoesEventPassGlobal(ZJetEvent const& event,
			ZJetProduct const& product, ZJetGlobalSettings const& global_settings) const
	{
		return DoesEventPass(event, product, global_settings.GetTaggedJets(), global_settings.GetAlphaMax());
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


