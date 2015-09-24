#pragma once

#include "Artus/KappaAnalysis/interface/Consumers/KappaLambdaNtupleConsumer.h"

#include "ZJetTypes.h"

class ZJetTreeConsumer : public KappaLambdaNtupleConsumer<ZJetTypes>
{
  public:
    std::string GetConsumerId() const override;

    void Init(ZJetSettings const& settings) override;
};
