#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "Artus/KappaAnalysis/interface/Consumers/KappaLambdaNtupleConsumer.h"

#include "ZJetTypes.h"


class ZJetLambdaNtupleConsumer: public KappaLambdaNtupleConsumer<ZJetTypes> {
public:

	typedef typename ZJetTypes::event_type event_type;
	typedef typename ZJetTypes::product_type product_type;
	typedef typename ZJetTypes::setting_type setting_type;

	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;
};
