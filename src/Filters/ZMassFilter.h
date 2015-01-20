#pragma once

#include "ZJetTypes.h"

#include "Artus/Core/interface/FilterBase.h"

/** Producer class for Z boson reconstruction from muons/electrons.
 *
 *	Needs to run after the valid object producers.
 */

class ZMassFilter : public ZJetFilterBase
{
  public:
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE;

	// ZMassFilter() : ZJetFilterBase() {};

	virtual bool DoesEventPass(
	    ZJetEvent const& event, ZJetProduct const& product,
	    ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE;
};
