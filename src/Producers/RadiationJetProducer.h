#pragma once

#include "ZJetTypes.h"

class RadiationJetProducer : public ZJetProducerBase
{
  public:
    virtual std::string GetProducerId() const override;

    RadiationJetProducer() : ZJetProducerBase() {}

    virtual void Init(ZJetSettings const& settings) override;

    virtual void Produce(ZJetEvent const& event,
                         ZJetProduct& product,
                         ZJetSettings const& settings) const override;

  private:
    double m_deltaR;

    void GetRadiationJets(std::string corrLevel,
                          ZJetEvent const& event,
                          ZJetProduct& product,
                          ZJetSettings const& settings) const;
};
