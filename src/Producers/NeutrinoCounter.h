#pragma once

#include "ZJetTypes.h"

/* Producer class for counting neutrinos.  */

class NeutrinoCounter : public ZJetProducerBase
{
  public:
    std::string GetProducerId() const override { return "NeutrinoCounter"; };

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override
    {
        product.n_neutrinos = 0;

        for (KGenParticles::const_iterator part = event.m_genParticles->begin();
             part != event.m_genParticles->end(); ++part) {
            for (auto const& id : m_ids) {
                if ((std::abs(part->pdgId) == id) && (part->status() == m_status))
                    product.n_neutrinos += 1;
            }
        }
    }

  private:
    const std::vector<int> m_ids = {12, 14, 16};
    static const int m_status = 1;
};
