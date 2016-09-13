#pragma once

#include "Artus/KappaAnalysis/interface/Consumers/KappaLambdaNtupleConsumer.h"

#include "Excalibur/Compile/interface/ZJetTypes.h"

class ZJetTreeConsumer : public KappaLambdaNtupleConsumer<ZJetTypes>
{
  public:
    std::string GetConsumerId() const override;

    void Init(ZJetSettings const& settings) override;
};
