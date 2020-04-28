#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"

/**
   \brief GlobalProducer, for PU weights splitted by run periods.
   
   This producer calculates a weight for an event based on the number of pileup truth
   interaction in a MC skim (m_genEventInfo->nPUMean) from an according set of PUWeightFiles.
   
   This producer needs the following config tags:
    - ZJetPUWeightFiles
    - ZJetPUWeightSuffixes
*/

class ZJetPUWeightProducer: public ZJetProducerBase
{

public:

	std::string GetProducerId() const override;

	void Init(ZJetSettings const& settings) override;

	void Produce(ZJetEvent const& event, ZJetProduct& product,
	                     ZJetSettings const& settings) const override;


private:
		std::vector<std::vector<double>> m_pileupWeights;
		std::vector<double> m_bins;
        std::vector<std::string> m_pileupWeightNames;

};