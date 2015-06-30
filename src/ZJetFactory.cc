#include "ZJetFactory.h"

// producers
#include "Producers/ZProducer.h"
#include "Producers/TypeIMETProducer.h"
//#include "Producers/ZJetValidJetsProducer.h"
#include "Producers/ZJetCorrectionsProducer.h"
#include "Producers/JetSorter.h"
#include "Producers/RecoJetGenPartonMatchingProducer.h"
#include "Producers/RecoJetGenJetMatchingProducer.h"
#include "Producers/RadiationJetProducer.h"
#include "Producers/NPUProducer.h"

// filters
#include "Filters/ZFilter.h"
#include "Filters/ZJetCutsFilter.h"

// consumers
#include "Consumers/ZJetTreeConsumer.h"

ProducerBaseUntemplated* ZJetFactory::createProducer(std::string const& id)
{
	if (id == ZmmProducer().GetProducerId())
		return new ZmmProducer();
	else if (id == TypeIMETProducer().GetProducerId())
		return new TypeIMETProducer();
	//else if (id == ZJetValidTaggedJetsProducer().GetProducerId())
	//	return new ZJetValidTaggedJetsProducer();
	else if (id == ZJetCorrectionsProducer().GetProducerId())
		return new ZJetCorrectionsProducer();
	else if (id == JetSorter().GetProducerId())
		return new JetSorter();
	else if (id == RecoJetGenPartonMatchingProducer().GetProducerId())
		return new RecoJetGenPartonMatchingProducer();
	else if (id == RecoJetGenJetMatchingProducer().GetProducerId())
		return new RecoJetGenJetMatchingProducer();
	else if (id == RadiationJetProducer().GetProducerId())
		return new RadiationJetProducer();
	else if (id == NPUProducer().GetProducerId())
		return new NPUProducer();
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
	else if (id == ZPtCut().GetFilterId())
		return new ZPtCut();
	else if (id == BackToBackCut().GetFilterId())
		return new BackToBackCut();
	else if (id == ZFilter().GetFilterId())
		return new ZFilter();
	else if (id == MinNMuonsCut().GetFilterId())
		return new MinNMuonsCut();
	else if (id == MaxNMuonsCut().GetFilterId())
		return new MaxNMuonsCut();
	else if (id == AlphaCut().GetFilterId())
		return new AlphaCut();
	else if (id == BetaCut().GetFilterId())
		return new BetaCut();	
	else
		return KappaFactory::createFilter(id);
}

ConsumerBaseUntemplated* ZJetFactory::createConsumer(std::string const& id)
{
	if(id == ZJetTreeConsumer().GetConsumerId())
		return new ZJetTreeConsumer();
	else
	return KappaFactory::createConsumer(id);
}
