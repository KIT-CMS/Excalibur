/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Core/interface/Pipeline.h"
#include "Artus/Core/interface/PipelineRunner.h"

#include "Artus/KappaAnalysis/interface/KappaPipelineInitializer.h"

#include "ZJetEvent.h"
#include "ZJetProduct.h"
#include "ZJetPipelineSettings.h"

// all data types which are used for this analysis
struct ZJetTypes {
	typedef ZJetEvent event_type;
	typedef ZJetProduct product_type;
	typedef ZJetPipelineSettings setting_type;
	typedef ZJetGlobalSettings global_setting_type;
};

// Pass the template parameters for the Producers
typedef ProducerBase<ZJetTypes> ZJetProducerBase;

// Pass the template parameters for the Consumer
typedef ConsumerBase<ZJetTypes> ZJetConsumerBase;

// Pass the template parameters for the Filter
typedef FilterBase<ZJetTypes> ZJetFilterBase;

//Pass the template parameters for the Pipeline
typedef Pipeline<ZJetTypes> ZJetPipeline;

//Setup our custom pipeline runner
typedef PipelineRunner<ZJetPipeline, ZJetTypes> ZJetPipelineRunner;

typedef KappaPipelineInitializer<ZJetTypes> ZJetPipelineInitializer;

