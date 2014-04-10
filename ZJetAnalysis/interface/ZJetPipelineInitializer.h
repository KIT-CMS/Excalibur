/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Consumer/interface/ValueModifier.h"

#include "Artus/Consumer/interface/DrawHist1dConsumer.h"
#include "Artus/Consumer/interface/ProfileConsumerBase.h"

#include "ZJetTypes.h"

#include "ZJetPipelineSettings.h"
#include "ZJetEvent.h"
#include "ZJetProduct.h"

// filter
//#include "PtFilter.h"

// consumer
#include "ZJetNtupleConsumer.h"

class ZJetPipelineInitializer: public PipelineInitilizerBase<ZJetTypes > {
public:

	virtual void InitPipeline(ZJetPipeline * pLine,
			ZJetPipelineSettings const& pset) const ARTUS_CPP11_OVERRIDE
			{

		typedef std::function<
				std::vector<float>(event_type const&, product_type const& )> ValueExtractLambda;
		typedef std::pair<ValueExtractLambda, ValueModifiers> ValueDesc;

		// define how to extract Pt and the range

		//auto extractPtSim =
		//		[]( ZJetEvent const& ev, ZJetProduct const & prod )
		//		-> std::vector<float> {return { 1//return quantity
		//		};};

		BOOST_FOREACH(std::string id, pset.GetConsumers())
		{
			// the quantities_all serves as an alias which
			// will install custom producers to pipeline
			if (id == "quantities_all")
			{
				// add consumers here
			}
		}

	}
};
