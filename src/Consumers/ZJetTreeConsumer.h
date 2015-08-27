#pragma once

#include "Artus/KappaAnalysis/interface/Consumers/KappaLambdaNtupleConsumer.h"

#include "ZJetTypes.h"

class ZJetTreeConsumer : public KappaLambdaNtupleConsumer<ZJetTypes>
{
  public:
    virtual std::string GetConsumerId() const override;

    virtual void Init(ZJetSettings const& settings) override;
};
