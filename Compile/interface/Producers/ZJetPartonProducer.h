#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"

/*
 * ZJetDressedMuonsProducer
 * ==========================
 *
 * Extends the Artus/KappaAnalysis ValidMuonsProducer.
 *
 * Implements the following dressed muon definition:
 *    - dressed muons include the surrounding photons
 *      -> FSR can be estimated
 *
 */


class ZJetPartonProducer : public ZJetProducerBase
{
  public:
    ZJetPartonProducer() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    std::string GetProducerId() const override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;
};




