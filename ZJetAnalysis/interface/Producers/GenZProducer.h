
#pragma once

#include "../ZJetTypes.h"


class GenZProducer: public ZJetProducerBase {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE 
	{
		return "genzproducer";
	}

	GenZProducer() : ZJetProducerBase() {};

	virtual void Produce(ZJetEvent const& event, ZJetProduct& product,
		ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE;
};


