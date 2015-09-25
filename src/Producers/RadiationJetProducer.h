#pragma once

#include "ZJetTypes.h"

class RadiationJetProducer : public ZJetProducerBase
{
  public:
    std::string GetProducerId() const override;

    RadiationJetProducer() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  private:
    double m_deltaR = 0.0;

    void GetRadiationJets(std::string corrLevel,
                          ZJetEvent const& event,
                          ZJetProduct& product,
                          ZJetSettings const& settings) const;
};
