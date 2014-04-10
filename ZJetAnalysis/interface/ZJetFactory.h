/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Core/interface/FactoryBase.h"


#include "ZJetTypes.h"

#include "ZJetPipelineSettings.h"
#include "ZJetEvent.h"
#include "ZJetProduct.h"

// producer
//#include "PtCorrectionProducer.h"
//#include "PtCorrectionProducerLocal.h"

// filter
//#include "Artus/Example/interface/PtFilter.h"

// consumer
#include "ZJetNtupleConsumer.h"
#include "ZJetCutFlowConsumer.h"

class ZJetFactory: public FactoryBase<ZJetTypes> {
public:

	ZJetFactory() : FactoryBase<ZJetTypes>() {
	}

	virtual ~ZJetFactory() {}

	virtual ZJetProducerBase * createProducer ( std::string const& id )
		ARTUS_CPP11_OVERRIDE
	{
		//if ( PtCorrectionProducer().GetProducerId() == id )
		//	return new PtCorrectionProducer();
		//else if ( PtCorrectionProducerLocal().GetProducerId() == id )
		//	return new PtCorrectionProducerLocal();
		//else
			return FactoryBase<ZJetTypes>::createProducer( id );
	}

	virtual ZJetConsumerBase * createConsumer ( std::string const& id )
		ARTUS_CPP11_OVERRIDE
	{
		if ( ZJetNtupleConsumer().GetConsumerId() == id )
			return new ZJetNtupleConsumer();
		else if ( ZJetCutFlowConsumer().GetConsumerId() == id )
			return new ZJetCutFlowConsumer();
		else
			return FactoryBase<ZJetTypes>::createConsumer( id );
	}

	virtual ZJetFilterBase * createFilter ( std::string const& id )
		ARTUS_CPP11_OVERRIDE
	{
		//if ( PtFilter().GetFilterId() == id )
		//	return new PtFilter();
		//else
			return FactoryBase<ZJetTypes>::createFilter( id );
	}


};
