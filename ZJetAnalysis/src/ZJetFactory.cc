#include "ZJet/ZJetAnalysis/interface/ZJetFactory.h"

// producers
#include "ZJet/ZJetAnalysis/interface/Producers/ZProducer.h"

// filters
//#include ""

// consumers
#include "ZJet/ZJetAnalysis/interface/ZJetNtupleConsumer.h"



ZJetProducerBase * ZJetFactory::createProducer ( std::string const& id )
{
	if(id == ZProducer().GetProducerId())
		return new ZProducer();
	else
		return KappaFactory<ZJetTypes>::createProducer( id );	
}

ZJetFilterBase * ZJetFactory::createFilter ( std::string const& id )
{
	//if(id == PreselectionFilter().GetFilterId())
	//	return new PreselectionFilter();
	//else
		return KappaFactory<ZJetTypes>::createFilter( id );
}

ZJetConsumerBase * ZJetFactory::createConsumer ( std::string const& id )
{
	if(id == ZJetNtupleConsumer().GetConsumerId())
		return new ZJetNtupleConsumer();
	else
		return KappaFactory<ZJetTypes>::createConsumer( id );
}
