#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"
/*
 * JetRecoilProducer
 * =================
 *
 * Implements the reconstruction of the total jet recoil.
 *
 * The jet recoil is defined as the vectorial sum of all jet pTs
 * starting with the pighest-pT jet and going down to a particular pT
 * threshold.
 *
 * When this producer is run, the valid jet collection in the product must
 * be sorted in order of descending pT.
 *
 * Settings used by this producer:
 *    - JetRecoilMinPtThreshold (float) :
 *          only jets above this pT threshold are included in the recoil.
 */


class JetRecoilProducer : public ZJetProducerBase
{
  public:
    JetRecoilProducer() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    std::string GetProducerId() const override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  private:
    // no private members
};
