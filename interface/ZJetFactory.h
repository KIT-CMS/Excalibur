/* Copyright (c) 2014 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/KappaAnalysis/interface/KappaFactory.h"

#include "ZJetTypes.h"

class ZJetFactory : public KappaFactory
{
  public:
    ZJetFactory() : KappaFactory() {}
    virtual ~ZJetFactory() {}

    ProducerBaseUntemplated* createProducer(std::string const& id) override;
    FilterBaseUntemplated* createFilter(std::string const& id) override;
    ConsumerBaseUntemplated* createConsumer(std::string const& id) override;
};
