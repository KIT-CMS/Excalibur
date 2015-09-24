#pragma once

#include "ZJetTypes.h"

/** Producer class jet pt sorting.
 *
 *	Needs to run after the JEC producer.
 */

class JetSorter : public ZJetProducerBase
{
  public:
    virtual std::string GetProducerId() const override;

    JetSorter() : ZJetProducerBase() {}

    virtual void Produce(ZJetEvent const& event,
                         ZJetProduct& product,
                         ZJetSettings const& settings) const override;
};
