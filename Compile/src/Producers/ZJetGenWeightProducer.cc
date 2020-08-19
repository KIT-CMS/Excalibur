
#include "boost/algorithm/string/join.hpp"

#include "Artus/Utility/interface/DefaultValues.h"

#include "Excalibur/Compile/interface/Producers/ZJetGenWeightProducer.h"


std::string ZJetGenWeightProducer::GetProducerId() const {
	return "ZJetGenWeightProducer";
}


void ZJetGenWeightProducer::Init(ZJetSettings const& settings) {
	ZJetProducerBase::Init(settings);

	m_isDefaultWeight = false;

    if(settings.GetInputIsData())
	{
		LOG(FATAL) << "[ZJetGenWeightProducer] Input file is NOT MC, there are no generator weights for data! Get your life back together! ";
	}

	if(settings.GetZJetGenWeightNames().empty())
	{
		LOG(FATAL) << "[ZJetGenWeightProducer] There are no specific weights requested for read-out. Abort! ";
	}

	m_requestedNames = settings.GetZJetGenWeightNames();
}


void ZJetGenWeightProducer::OnRun(ZJetEvent const& event, ZJetSettings const& settings)
{
	assert(event.m_genEventInfoMetadata);

	// On first event, fill the lheWeightNamesMap
	if(m_lheWeightNamesMap.empty())
	{
		auto tmp_lheWeightNamesMap = event.m_genEventInfoMetadata->getLheWeightNamesMap(m_requestedNames);
		if(tmp_lheWeightNamesMap.empty())
		{
			LOG(WARNING) << "[ZJetGenWeightProducer] Running on a skim without weight variations! Setting weights to default value (1.0)!";
			m_isDefaultWeight =  true; 

			for (const auto& requestedName: m_requestedNames)
			{
				m_lheWeightNamesMap["genWeight_" + requestedName] = DefaultValues::UndefinedInt;
			}
			
			
		}
		else
		{
			for(const auto& lheWeightNamePair: tmp_lheWeightNamesMap)
			{
				m_lheWeightNamesMap["genWeight_" + lheWeightNamePair.first] = lheWeightNamePair.second;
			}
		}
		
		
		
	}
}


void ZJetGenWeightProducer::Produce(ZJetEvent const& event,
		ZJetProduct& product,
		ZJetSettings const& settings) const
{	
	assert(event.m_genEventInfo);

	for(const auto& lheWeightNamePair: m_lheWeightNamesMap)
	{ 
		if(!m_isDefaultWeight)
		{
			product.m_optionalWeights[lheWeightNamePair.first] = event.m_genEventInfo->getLheWeight(lheWeightNamePair.second, false);
		}
		else
		{
			product.m_optionalWeights[lheWeightNamePair.first] = 1.0;
		}
		
	}


	
}
