#pragma once

#include "Artus/KappaAnalysis/interface/Consumers/KappaLambdaNtupleConsumer.h"

#include "ZJetTypes.h"


class ZJetLambdaNtupleConsumer: public KappaLambdaNtupleConsumer<ZJetTypes> {
public:

	virtual std::string GetConsumerId() const ARTUS_CPP11_OVERRIDE;

	virtual void Init(ZJetSettings const& settings) ARTUS_CPP11_OVERRIDE;
};
