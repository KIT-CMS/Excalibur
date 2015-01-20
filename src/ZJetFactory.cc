#include "ZJetFactory.h"

// producers
#include "Producers/ZProducer.h"

// filters
#include "Filters/ZMassFilter.h"

// consumers
//#include "Consumers/ZJetNtupleConsumer.h"

ProducerBaseUntemplated* ZJetFactory::createProducer(std::string const& id)
{
	if (id == ZProducer().GetProducerId())
		return new ZProducer();
	else
		return KappaFactory::createProducer(id);
}

FilterBaseUntemplated* ZJetFactory::createFilter(std::string const& id)
{
	if (id == ZMassFilter().GetFilterId())
		return new ZMassFilter();
	else
		return KappaFactory::createFilter(id);
}

ConsumerBaseUntemplated* ZJetFactory::createConsumer(std::string const& id)
{
	// if(id == ZJetLambdaNtupleConsumer().GetConsumerId())
	//	return new ZJetLambdaNtupleConsumer();
	// else
	return KappaFactory::createConsumer(id);
}
