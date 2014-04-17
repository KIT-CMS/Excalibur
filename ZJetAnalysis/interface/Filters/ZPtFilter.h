#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../ZJetTypes.h"

class ZPtFilter: public ZJetFilterBase {
public:

	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "zpt";
	}

	virtual bool DoesEventPassLocal(ZJetEvent const& event,
	ZJetProduct const& product,
	ZJetPipelineSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		return DoesEventPass(event, product, settings.GetZPtMin());
	}

	bool DoesEventPassGlobal(ZJetEvent const& event,
			ZJetProduct const& product, ZJetGlobalSettings const& global_settings) const
	{
		return DoesEventPass(event, product, global_settings.GetZPtMin());
	}

private:

	virtual bool DoesEventPass(ZJetEvent const& event,
		ZJetProduct const& product, float const& zptmin) const
	{
		if (product.Z.p4.Pt() < zptmin)
			return false;
		else
			return true;
	}
};


