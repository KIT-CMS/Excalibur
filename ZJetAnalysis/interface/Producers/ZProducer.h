
#pragma once

#include "../ZJetTypes.h"


class ZProducer: public ZJetProducerBase {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE 
	{
		return "zproducer";
	}

	ZProducer() : ZJetProducerBase() {};

	virtual void Produce(ZJetEvent const& event, ZJetProduct& product,
		ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE;
};


