#pragma once

#include "ZJetTypes.h"

/** Producer class for Z boson reconstruction from muons/electrons.
 *
 *	Needs to run after the valid object producers.
 * 	Needs at least 2 valid leptons to construct a Z.
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
        /*
        Try all lepton combinations to find a valid Z

        Exactly one Z must be reconstructed. Events with any more or less are
        deemed ambigious, not having *a* valid Z.
        */
        int found_zs = 0;
        KLV z_cand;
        std::pair<KLepton*, KLepton*> z_leptons;
        // do not double count when matching leptons from the same collection
        // NOTE: this check could probably be done more elegantly...
        bool same_ll_collection = ((static_cast<void*>(&(product.*m_validLeptonsMember1))) ==
                                   (static_cast<void*>(&(product.*m_validLeptonsMember2))));
        for (unsigned int i = 0; i < (product.*m_validLeptonsMember1).size(); ++i) {
            for (unsigned int j = (same_ll_collection ? i + 1 : 0);
                 j < (product.*m_validLeptonsMember2).size();
                 ++j) {
                KLepton* const m1 = (product.*m_validLeptonsMember1).at(i);
                KLepton* const m2 = (product.*m_validLeptonsMember2).at(j);
                // valid Z is neutral and close to Z mass
                if (m1->charge() + m2->charge() == 0) {
                    KLV z;
                    z.p4 = m1->p4 + m2->p4;
                    if (z.p4.mass() > settings.GetZMass() - settings.GetZMassRange() &&
                        z.p4.mass() < settings.GetZMass() + settings.GetZMassRange()) {
                        // allow only 1 Z per event
                        if (++found_zs > 1)
                            break;
                        z_cand = z;
                        if (m1->p4.Pt() > m2->p4.Pt())
                            z_leptons = std::make_pair(m1, m2);
                        else
                            z_leptons = std::make_pair(m2, m1);
                    }
                }
            }
            if (found_zs > 1)
                break;
        }
        if (found_zs == 1) {
            product.m_z = z_cand;
            product.m_zLeptons = z_leptons;
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
