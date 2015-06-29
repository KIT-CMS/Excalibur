#pragma once

#include "ZJetTypes.h"

/*
	This producers calculates NPU ("mu", the expected pileup) in data per run and lumisection from a txt file in a specific format.
*/

class NPUProducer : public ZJetProducerBase
{
  public:
	std::string GetProducerId() const;

	NPUProducer() : ZJetProducerBase() {};

	void Init(ZJetSettings const& settings);

	void Produce(ZJetEvent const& event, ZJetProduct& product,
						 ZJetSettings const& settings) const;

  private:
	std::map<int, std::map<int, double> > m_pumean;
	mutable int lastrun;
	mutable int lastls;
};
