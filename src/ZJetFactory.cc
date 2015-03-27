#include "ZJetFactory.h"

// producers
#include "Producers/ZProducer.h"
//#include "Producers/TypeIMETProducer.h"
//#include "Producers/ZJetValidJetsProducer.h"
#include "Producers/ZJetCorrectionsProducer.h"

// filters
#include "Filters/ZFilter.h"
//#include "Filters/ZJetValidJetsFilter.h"

// consumers
//#include "Consumers/ZJetNtupleConsumer.h"

ProducerBaseUntemplated* ZJetFactory::createProducer(std::string const& id)
{
	if (id == ZProducer().GetProducerId())
		return new ZProducer();
	//else if (id == TypeIMETProducer().GetProducerId())
	//	return new TypeIMETProducer();
	//else if (id == ZJetValidTaggedJetsProducer().GetProducerId())
	//	return new ZJetValidTaggedJetsProducer();
	else if (id == ZJetCorrectionsProducer().GetProducerId())
		return new ZJetCorrectionsProducer();
	else
		return KappaFactory::createProducer(id);
}

FilterBaseUntemplated* ZJetFactory::createFilter(std::string const& id)
{
	if (id == ZFilter().GetFilterId())
		return new ZFilter();
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
