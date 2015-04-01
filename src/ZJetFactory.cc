#include "ZJetFactory.h"

// producers
#include "Producers/ZProducer.h"
//#include "Producers/TypeIMETProducer.h"
//#include "Producers/ZJetValidJetsProducer.h"
#include "Producers/ZJetCorrectionsProducer.h"
#include "Producers/JetSorter.h"

// filters
#include "Filters/ZFilter.h"
#include "Filters/ZJetCutsFilter.h"

// consumers
#include "Consumers/ZJetLambdaNtupleConsumer.h"

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
	else if (id == JetSorter().GetProducerId())
		return new JetSorter();
	else
		return KappaFactory::createProducer(id);
}

FilterBaseUntemplated* ZJetFactory::createFilter(std::string const& id)
{
	if (id == MuonPtCut().GetFilterId())
		return new MuonPtCut();
	else if (id == MuonEtaCut().GetFilterId())
		return new MuonEtaCut();
	else if (id == LeadingJetPtCut().GetFilterId())
		return new LeadingJetPtCut();
	else if (id == LeadingJetEtaCut().GetFilterId())
		return new LeadingJetEtaCut();
	else if (id == ZFilter().GetFilterId())
		return new ZFilter();
	else
		return KappaFactory::createFilter(id);
}

ConsumerBaseUntemplated* ZJetFactory::createConsumer(std::string const& id)
{
	if(id == ZJetLambdaNtupleConsumer().GetConsumerId())
		return new ZJetLambdaNtupleConsumer();
	else
	return KappaFactory::createConsumer(id);
}
