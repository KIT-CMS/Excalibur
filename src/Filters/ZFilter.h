#pragma once

#include "ZJetTypes.h"

#include "Artus/Core/interface/FilterBase.h"

/** Filter class for Z boson.
 *
 *	Needs to run after the Z producer.
 */

class ZFilter : public ZJetFilterBase
{
  public:
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE;

	ZFilter() : ZJetFilterBase(){};

	virtual bool DoesEventPass(
	    ZJetEvent const& event, ZJetProduct const& product,
	    ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE;
};
