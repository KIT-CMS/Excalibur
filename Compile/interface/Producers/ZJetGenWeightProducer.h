#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"

/**
   \brief GlobalProducer, for Gen weights (ISR/FSR/scales).
   
   This producer reads varied weights for an event based on the available weights in the MC skim 
   (m_genEventInfo->lheWeight).
   
   This producer needs the following config tags:
    - ZJetGenWeightNames
*/

class ZJetGenWeightProducer: public ZJetProducerBase
{

public:

	std::string GetProducerId() const override;

	void Init(ZJetSettings const& settings) override;

    void OnLumi(ZJetEvent const& event, ZJetSettings const& settings) override;

	void Produce(ZJetEvent const& event, ZJetProduct& product,
	                     ZJetSettings const& settings) const override;


private:
    std::vector<std::string> m_requestedNames;
    std::map<std::string, size_t> m_lheWeightNamesMap;

};