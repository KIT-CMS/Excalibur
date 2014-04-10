/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Core/interface/CutFlow.h"

#include "Artus/Consumer/interface/CutFlowConsumerBase.h"

#include "ZJetTypes.h"


class ZJetCutFlowConsumer: public CutFlowConsumerBase< ZJetTypes > {

public:

	virtual void Finish() ARTUS_CPP11_OVERRIDE {
		LOG(INFO) << "Cut Flow for pipeline" << m_pipelineName << ":";
		LOG(INFO) << m_flow.ToString();
	}

};
