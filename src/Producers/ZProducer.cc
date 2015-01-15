
#include "ZJet/ZJetAnalysis/interface/Producers/ZProducer.h"


std::string ZProducer::GetProducerId() const {
	return "ZProducer";
}

void ZProducer::Produce(ZJetEvent const& event, ZJetProduct& product,
		ZJetSettings const& settings) const {
	//produce here
}
