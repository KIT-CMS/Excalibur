/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "Artus/Consumer/interface/NtupleConsumerBase.h"

#include "ZJetTypes.h"


class ZJetNtupleConsumer: public NtupleConsumerBase<ZJetTypes> {

public:
	virtual std::string GetConsumerId() const
		ARTUS_CPP11_OVERRIDE
	{
		return "zjetntuple";
	}

private:

	float returnvalue(std::string string, ZJetEvent const& event,
			ZJetProduct const& product ) ARTUS_CPP11_OVERRIDE
	{
		if (string == "npv")
			return event.m_vertexSummary->nVertices;
		else if (string == "mu1pt")
			return event.m_muons->at(0).p4.Pt();
		else
			LOG(FATAL) << "The quantity " << string << " could not be added to the Ntuple!";
			return UNDEFINED_VALUE;
	}

};
