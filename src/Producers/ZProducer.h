#pragma once

#include "ZJetTypes.h"

/** Producer class for Z boson reconstruction from muons/electrons.
 *
 *	Needs to run after the valid object producers.
 * 	Needs min 2 valid muons and max 3 valid muons!
 */

class ZProducer : public ZJetProducerBase
{
  public:
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE;

	ZProducer() : ZJetProducerBase(){};

	virtual void Produce(ZJetEvent const& event, ZJetProduct& product,
	                     ZJetSettings const& settings) const
	    ARTUS_CPP11_OVERRIDE;

  private:
};
