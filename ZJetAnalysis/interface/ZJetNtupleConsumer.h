#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Core/interface/GlobalInclude.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumerBase.h"

#include "ZJetTypes.h"


class ZJetNtupleConsumer: public LambdaNtupleConsumerBase<ZJetTypes> {
public:

typedef std::function<float(ZJetEvent const&, ZJetProduct const&)> float_extractor_lambda;

ZJetNtupleConsumer() : LambdaNtupleConsumerBase<ZJetTypes>() { };

virtual void Init(Pipeline<ZJetTypes> * pset) ARTUS_CPP11_OVERRIDE;
virtual std::string GetConsumerId() const ARTUS_CPP11_OVERRIDE;

private:
	std::string algoname;

};
