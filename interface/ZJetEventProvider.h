/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/KappaAnalysis/interface/KappaEventProvider.h"

#include "ZJetTypes.h"

/**
\brief class to connect the analysis specific event content to the pipelines.
*/

class ZJetEventProvider: public KappaEventProvider<ZJetTypes> {
public:

	typedef typename ZJetTypes::setting_type setting_type;

	ZJetEventProvider(FileInterface2 & fi, InputTypeEnum inpType);

	virtual void WireEvent(setting_type const& settings) ARTUS_CPP11_OVERRIDE;
};
