#include "ZJet/ZJetAnalysis/interface/ZJetFactory.h"

// producers
//#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"
//#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauSpinnerProducer.h"
//#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EventWeightProducer.h"
//#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducer.h"

// filters
//#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/PreselectionFilter.h"

// consumers
#include "ZJet/ZJetAnalysis/interface/ZJetNtupleConsumer.h"
//#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttCutFlowHistogramConsumer.h"


ZJetProducerBase * ZJetFactory::createProducer ( std::string const& id )
{
	//if(id == DecayChannelProducer().GetProducerId())
	//	return new DecayChannelProducer();
	//else if(id == TauSpinnerProducer().GetProducerId())
	//	return new TauSpinnerProducer();
	//else
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
