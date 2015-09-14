#pragma once

#include "ZJetTypes.h"

/*
    This producers calculates NPU ("mu", the expected pileup) in data per run and lumisection from a
   txt file in a specific format.
*/

class NPUProducer : public ZJetProducerBase
{
  public:
    std::string GetProducerId() const;

    NPUProducer() : ZJetProducerBase(), lastrun(0), lastls(0){};

    void Init(ZJetSettings const& settings);

    void Produce(ZJetEvent const& event, ZJetProduct& product, ZJetSettings const& settings) const;

  private:
    std::map<unsigned long, std::map<unsigned long, float>> m_pumean;
    mutable unsigned long lastrun;
    mutable unsigned long lastls;
};
