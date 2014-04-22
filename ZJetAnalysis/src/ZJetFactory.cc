#include "ZJet/ZJetAnalysis/interface/ZJetFactory.h"

// producers
#include "ZJet/ZJetAnalysis/interface/Producers/ZProducer.h"
#include "ZJet/ZJetAnalysis/interface/Producers/ValidMuonProducer.h"
#include "ZJet/ZJetAnalysis/interface/Producers/ValidJetProducer.h"

// filters
#include "ZJet/ZJetAnalysis/interface/Filters/MuonFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/ValidZFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/ZPtFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/JetPtFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/JetEtaFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/AlphaFilter.h"

// consumers
#include "ZJet/ZJetAnalysis/interface/ZJetNtupleConsumer.h"



ZJetProducerBase * ZJetFactory::createProducer ( std::string const& id )
{
	if(id == ZProducer().GetProducerId())
		return new ZProducer();
	else if(id == ValidMuonProducer().GetProducerId())
		return new ValidMuonProducer();
	else if(id == ValidJetProducer().GetProducerId())
		return new ValidJetProducer();
	else
		return KappaFactory<ZJetTypes>::createProducer( id );	
}

ZJetFilterBase * ZJetFactory::createFilter ( std::string const& id )
{
	if(id == MuonFilter().GetFilterId())
		return new MuonFilter();
	else if(id == ValidZFilter().GetFilterId())
		return new ValidZFilter();
	else if(id == ZPtFilter().GetFilterId())
		return new ZPtFilter();
	else if(id == JetPtFilter().GetFilterId())
		return new JetPtFilter();
	else if(id == JetEtaFilter().GetFilterId())
		return new JetEtaFilter();
	else if(id == AlphaFilter().GetFilterId())
		return new AlphaFilter();
	else
		return KappaFactory<ZJetTypes>::createFilter( id );
}

ZJetConsumerBase * ZJetFactory::createConsumer ( std::string const& id )
{
	if(id == ZJetNtupleConsumer().GetConsumerId())
		return new ZJetNtupleConsumer();
	else
		return KappaFactory<ZJetTypes>::createConsumer( id );
}
