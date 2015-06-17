#pragma once

#include "ZJetTypes.h"


class RadiationJetProducer : public ZJetProducerBase
{
  public:
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE;

	RadiationJetProducer() : ZJetProducerBase(){};
	
	virtual void Init(ZJetSettings const& settings);

	virtual void Produce(ZJetEvent const& event, ZJetProduct& product,
	                     ZJetSettings const& settings) const
	    ARTUS_CPP11_OVERRIDE;

  private:
	double deltaR;
  
	void GetRadiationJets(std::string corrLevel,
		ZJetEvent const& event, ZJetProduct& product, ZJetSettings const& settings) const;
};
