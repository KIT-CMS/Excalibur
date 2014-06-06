
#pragma once

#include "../ZJetTypes.h"


class ValidMuonProducer: public ZJetProducerBase {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE 
	{
		return "validmuonproducer";
	}

	ValidMuonProducer() : ZJetProducerBase() {};

	virtual void Produce(ZJetEvent const& event, ZJetProduct& product,
		ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE;
};


