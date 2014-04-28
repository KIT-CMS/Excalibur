#include "ZJet/ZJetAnalysis/interface/ZJetFactory.h"

// producers
#include "ZJet/ZJetAnalysis/interface/Producers/ZProducer.h"
#include "ZJet/ZJetAnalysis/interface/Producers/GenZProducer.h"
#include "ZJet/ZJetAnalysis/interface/Producers/ValidMuonProducer.h"
#include "ZJet/ZJetAnalysis/interface/Producers/ZJetValidJetsProducer.h"

// filters
#include "ZJet/ZJetAnalysis/interface/Filters/MuonFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/ValidZFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/ValidGenZFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/ZPtFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/ValidJetsFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/JetPtFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/JetEtaFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/AlphaFilter.h"
#include "ZJet/ZJetAnalysis/interface/Filters/DeltaPhiFilter.h"

// consumers
#include "ZJet/ZJetAnalysis/interface/ZJetNtupleConsumer.h"



ZJetProducerBase * ZJetFactory::createProducer ( std::string const& id )
{
	if(id == ZProducer().GetProducerId())
		return new ZProducer();
	else if(id == GenZProducer().GetProducerId())
		return new GenZProducer();
	else if(id == ValidMuonProducer().GetProducerId())
		return new ValidMuonProducer();
	else if(id == ZJetValidJetsProducer().GetProducerId())
		return new ZJetValidJetsProducer();
	else
		return KappaFactory<ZJetTypes>::createProducer( id );	
}

ZJetFilterBase * ZJetFactory::createFilter ( std::string const& id )
{
	if(id == MuonFilter().GetFilterId())
		return new MuonFilter();
	else if(id == ValidZFilter().GetFilterId())
		return new ValidZFilter();
	else if(id == ValidGenZFilter().GetFilterId())
		return new ValidGenZFilter();
	else if(id == ZPtFilter().GetFilterId())
		return new ZPtFilter();
	else if(id == JetPtFilter().GetFilterId())
		return new JetPtFilter();
	else if(id == JetEtaFilter().GetFilterId())
		return new JetEtaFilter();
	else if(id == AlphaFilter().GetFilterId())
		return new AlphaFilter();
	else if(id == DeltaPhiFilter().GetFilterId())
		return new DeltaPhiFilter();
	else if(id == ValidJetsFilter().GetFilterId())
		return new ValidJetsFilter();
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
