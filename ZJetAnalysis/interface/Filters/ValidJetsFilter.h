#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Utility/interface/SafeMap.h"

#include "../ZJetTypes.h"

class ValidJetsFilter: public ZJetFilterBase {
public:

	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "validjets";
	}

	virtual bool DoesEventPassLocal(ZJetEvent const& event,
	ZJetProduct const& product,
	ZJetPipelineSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		return DoesEventPass(event, product, settings.GetJetAlgorithm());
	}

	bool DoesEventPassGlobal(ZJetEvent const& event,
			ZJetProduct const& product, ZJetGlobalSettings const& global_settings) const
	{
		return DoesEventPass(event, product, global_settings.GetTaggedJets());
	}

private:

	virtual bool DoesEventPass(ZJetEvent const& event,
		ZJetProduct const& product, std::string const& algoname) const
	{
		if (product.m_validJets.size() < 1)
			return false;
		else
			return true;
	}
};


