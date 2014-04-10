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

	typedef typename ZJetTypes::global_setting_type global_setting_type;

	ZJetEventProvider(FileInterface2 & fi, InputTypeEnum inpType) : 
		KappaEventProvider<ZJetTypes>(fi,inpType) {}

	virtual void WireEvent(global_setting_type const& globalSettings) 
		ARTUS_CPP11_OVERRIDE
	{
		KappaEventProvider::WireEvent(globalSettings);
		m_event.m_vertexSummary = m_fi.Get<KVertexSummary>("goodOfflinePrimaryVerticesSummary");
		m_event.m_muons = m_fi.Get<KDataMuons>("muons");
	}
};
