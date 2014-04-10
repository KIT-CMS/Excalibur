/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/KappaAnalysis/interface/KappaPipelineSettings.h"

class ZJetPipelineSettings: public KappaPipelineSettings {
public:


	VarCache<stringvector> quantities;
	stringvector GetQuantities() const
	{
		RETURN_CACHED(quantities, PropertyTreeSupport::GetAsStringList(GetPropTree(), "Pipelines." + GetName() + ".Quantities"))
	}

};

class ZJetGlobalSettings: public KappaGlobalSettings {
public:

	IMPL_SETTING(bool, InputIsData)

};
