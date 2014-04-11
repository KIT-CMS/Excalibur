/* Copyright (c) 2013 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/KappaAnalysis/interface/KappaEvent.h"

class ZJetEvent : public KappaEvent
{
public:
	ZJetEvent() : KappaEvent() {};
	KDataPFTaggedJets* m_tjets = 0;
};
