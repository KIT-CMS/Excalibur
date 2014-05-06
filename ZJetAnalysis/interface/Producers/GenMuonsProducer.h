
#pragma once

#include "../ZJetTypes.h"


class GenMuonsProducer: public ZJetProducerBase {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE 
	{
		return "genmuonsproducer";
	}

	GenMuonsProducer() : ZJetProducerBase() {};

	virtual void ProduceGlobal(ZJetEvent const& event, ZJetProduct& product,
		ZJetGlobalSettings const& globalSettings) const ARTUS_CPP11_OVERRIDE
	{
		// Loop over gen particles
		for (KGenParticles::iterator it = event.m_genParticles->begin(); it != event.m_genParticles->end(); ++it)
		{
			if (std::abs(it->pdgId()) == 13)
				product.m_genmuons.push_back(*it);
		}
	}
};


