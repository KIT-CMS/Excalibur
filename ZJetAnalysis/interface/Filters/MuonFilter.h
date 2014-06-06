#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../ZJetTypes.h"

class MuonFilter: public ZJetFilterBase {
public:

	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "muons";
	}

	virtual bool DoesEventPass(ZJetEvent const& event,
	ZJetProduct const& product,
	ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		return DoesEventPass(event, product);
	}


private:

	virtual bool DoesEventPass(ZJetEvent const& event,
		ZJetProduct const& product) const
	{
		if (product.m_validmuons.size() < 2)
			return false;
		else
			return true;
	}
};


