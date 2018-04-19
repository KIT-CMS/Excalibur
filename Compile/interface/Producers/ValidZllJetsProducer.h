#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"

class ValidZllJetsProducer : public ZJetProducerBase
{
  public:
    ValidZllJetsProducer() : ZJetProducerBase(), minZllJetDeltaRVeto(0) {}

    void Init(ZJetSettings const& settings) override;

    std::string GetProducerId() const override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  private:
    float minZllJetDeltaRVeto;
};

class ValidZllGenJetsProducer : public ZJetProducerBase
{
  public:
    ValidZllGenJetsProducer() : ZJetProducerBase(), minZllJetDeltaRVeto(0) {}

    void Init(ZJetSettings const& settings) override;

    std::string GetProducerId() const override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  private:
    float minZllJetDeltaRVeto;
};
