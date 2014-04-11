/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/KappaAnalysis/interface/KappaPipelineSettings.h"

class ZJetPipelineSettings: public KappaPipelineSettings {
public:

};

class ZJetGlobalSettings: public KappaGlobalSettings {
public:

	IMPL_SETTING(bool, InputIsData)

};
