#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../ZJetTypes.h"

class ZPtFilter: public ZJetFilterBase {
public:

	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "zpt";
	}

	bool DoesEventPass(ZJetEvent const& event,
			ZJetProduct const& product, ZJetSettings const& settings) const
	{
		return DoesEventPass(event, product, settings.GetZPtMin());
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


