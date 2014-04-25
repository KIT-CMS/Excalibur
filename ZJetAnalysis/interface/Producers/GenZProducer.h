
#pragma once

#include "../ZJetTypes.h"


class GenZProducer: public ZJetProducerBase {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE 
	{
		return "genzproducer";
	}

	GenZProducer() : ZJetProducerBase() {};

	virtual void ProduceGlobal(ZJetEvent const& event, ZJetProduct& product,
		ZJetGlobalSettings const& globalSettings) const ARTUS_CPP11_OVERRIDE;
};


