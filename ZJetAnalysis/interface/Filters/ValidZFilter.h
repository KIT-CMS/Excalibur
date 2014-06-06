#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../ZJetTypes.h"

class ValidZFilter: public ZJetFilterBase {
public:

	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "validz";
	}

	bool DoesEventPass(ZJetEvent const& event,
			ZJetProduct const& product, ZJetSettings const& settings) const
	{
		return DoesEventPass(event, product);
	}

private:

	virtual bool DoesEventPass(ZJetEvent const& event,
		ZJetProduct const& product) const
	{
		if (product.has_valid_z)
			return true;
		else
			return false;
	}
};


