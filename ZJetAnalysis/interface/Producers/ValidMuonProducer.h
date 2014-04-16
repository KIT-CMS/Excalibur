
#pragma once

#include "../ZJetTypes.h"


class ValidMuonProducer: public ZJetProducerBase {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE 
	{
		return "validmuonproducer";
	}

	ValidMuonProducer() : ZJetProducerBase() {};

	virtual void ProduceGlobal(ZJetEvent const& event, ZJetProduct& product,
		ZJetGlobalSettings const& globalSettings) const ARTUS_CPP11_OVERRIDE;
};


