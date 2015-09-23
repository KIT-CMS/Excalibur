#pragma once

#include "ZJetTypes.h"

/** Producer class for Z boson reconstruction from muons/electrons.
 *
 *	Needs to run after the valid object producers.
 * 	Needs min 2 valid leptons and max 3 valid leptons!
 */

template <class TLepton1, class TLepton2>
class ZProducerBase : public ZJetProducerBase
{
  public:
    ZProducerBase(std::vector<TLepton1*> ZJetProduct::*validLeptons1,
                  std::vector<TLepton2*> ZJetProduct::*validLeptons2)
        : ZJetProducerBase(),
          m_validLeptonsMember1(validLeptons1),
          m_validLeptonsMember2(validLeptons2){};

    virtual void Produce(ZJetEvent const& event,
                         ZJetProduct& product,
                         ZJetSettings const& settings) const override

    {
        // Create all possible Z combinations
        // Note: If we have more than 3 muons in an event, this may produce double
        // counting
        std::vector<KLV> z_cand;
        std::vector<std::pair<KLepton*, KLepton*>> z_leptons;
        for (unsigned int i = 0; i < (product.*m_validLeptonsMember1).size(); ++i) {
            for (unsigned int j = i + 1; j < (product.*m_validLeptonsMember2).size(); ++j) {
                KLepton* const m1 = (product.*m_validLeptonsMember1).at(i);
                KLepton* const m2 = (product.*m_validLeptonsMember2).at(j);
                if (m1->charge() + m2->charge() == 0) {
                    KLV z;
                    z.p4 = m1->p4 + m2->p4;
                    if (z.p4.mass() > settings.GetZMass() - settings.GetZMassRange() &&
                        z.p4.mass() < settings.GetZMass() + settings.GetZMassRange()) {
                        z_cand.emplace_back(z);
                        if (m1->p4.Pt() > m2->p4.Pt())
                            z_leptons.emplace_back(m1, m2);
                        else
                            z_leptons.emplace_back(m2, m1);
                    }
                }
            }
        }
        // If there is more than one valid Z candidate we chose the one with its
        // mass closest to the Z mass.
        if (z_cand.size() > 0) {
            unsigned int best_z_cand = 9999;
            for (unsigned int i = 0; i < z_cand.size(); ++i) {
                if (best_z_cand == 9999 ||
                    fabs(z_cand[i].p4.mass() - settings.GetZMass()) <=
                        fabs(z_cand[best_z_cand].p4.mass() - settings.GetZMass())) {
                    best_z_cand = i;
                }
            }
            product.m_z = z_cand[best_z_cand];
            product.m_zLeptons = z_leptons.at(best_z_cand);
            product.m_validZ = true;
        } else {
            product.m_validZ = false;
            return;
        }
    }

    ;

  private:
    std::vector<TLepton1*> ZJetProduct::*m_validLeptonsMember1;
    std::vector<TLepton2*> ZJetProduct::*m_validLeptonsMember2;
};

class ZmmProducer : public ZProducerBase<KMuon, KMuon>
{
  public:
    virtual std::string GetProducerId() const override { return "ZmmProducer"; };
    ZmmProducer()
        : ZProducerBase<KMuon, KMuon>(&ZJetProduct::m_validMuons, &ZJetProduct::m_validMuons)
    {
    }
};

class ZeeProducer : public ZProducerBase<KElectron, KElectron>
{
  public:
    virtual std::string GetProducerId() const override { return "ZeeProducer"; };
    ZeeProducer()
        : ZProducerBase<KElectron, KElectron>(&ZJetProduct::m_validElectrons,
                                              &ZJetProduct::m_validElectrons)
    {
    }
};

class ZemProducer : public ZProducerBase<KElectron, KMuon>
{
  public:
    virtual std::string GetProducerId() const override { return "ZemProducer"; };
    ZemProducer()
        : ZProducerBase<KElectron, KMuon>(&ZJetProduct::m_validElectrons,
                                          &ZJetProduct::m_validMuons)
    {
    }
};
