
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/GenParticleMatchingProducers.h"

#include "ZJetTypes.h"

/** Producer for reco jet gen parton matches
 *
 *  Possible config tags:
 *  - DeltaRMatchingRecoJetGenParticle (default provided)
 *  - JetMatchingAlgorithm (default provided)
 */

class RecoJetGenPartonMatchingProducer : public RecoJetGenParticleMatchingProducer
{
  public:
    std::string GetProducerId() const override;

    void Produce(KappaEvent const& event,
                 KappaProduct& product,
                 KappaSettings const& settings) const override;
};
