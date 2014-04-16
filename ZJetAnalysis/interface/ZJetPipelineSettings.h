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
	
	IMPL_SETTING(bool, MuonID2011)
	IMPL_SETTING(float, MuonEtaMax)
	IMPL_SETTING(float, MuonPtMin)

	IMPL_SETTING(float, ZMassMax)
	IMPL_SETTING(float, ZMassMin)

};
