/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "Artus/KappaAnalysis/interface/KappaFactory.h"

#include "ZJetTypes.h"

class ZJetFactory : public KappaFactory
{ //<ZJetTypes> {
  public:
	ZJetFactory() : KappaFactory(){};
	virtual ~ZJetFactory(){};

	virtual ProducerBaseUntemplated* createProducer(std::string const& id)
	    ARTUS_CPP11_OVERRIDE;
	virtual FilterBaseUntemplated* createFilter(std::string const& id)
	    ARTUS_CPP11_OVERRIDE;
	virtual ConsumerBaseUntemplated* createConsumer(std::string const& id)
	    ARTUS_CPP11_OVERRIDE;
};
