#include "ValidZllJetsProducer.h"

/**
    \brief Producer for valid jets given the constraints of Z->ll+Jet analyses

    This producer modifies the collection of valid jets to conform to the specific
    requirements of the Z->ll+Jets analyses.
    This producer should be run after any ValidJetsProducers, as it vetoes previously
    produced jets.

    Configuration settings:

    MinZllJetDeltaRVeto (float) required distance between jets and leptons from Z decay
*/

std::string ValidZllJetsProducer::GetProducerId() const { return "ValidZllJetsProducer"; }

void ValidZllJetsProducer::Init(ZJetSettings const& settings)
{
    minZllJetDeltaRVeto = settings.GetMinZllJetDeltaRVeto();
}

void ValidZllJetsProducer::Produce(ZJetEvent const& event,
                                   ZJetProduct& product,
                                   ZJetSettings const& settings) const
{
    /*
    veto jets too close to leptons from Z decay to be considered actual jets

    Relies on the assumptation that the deltaR veto is tight enough to allow for
    only one jet vetoed by every lepton.
    */
    KLepton* zl1, *zl2;
    std::tie(zl1, zl2) = product.m_zLeptons;
    // nothing to do if there are no Zlls
    if (zl1 != nullptr) {
        std::size_t zl1_idx = product.m_validJets.size() + 1,
                    zl2_idx = product.m_validJets.size() + 1;
        for (std::size_t i = 0; i < product.m_validJets.size(); ++i) {
            if (ROOT::Math::VectorUtil::DeltaR(product.m_validJets.at(i)->p4, zl1->p4) >
                minZllJetDeltaRVeto) {
                zl1_idx = i;
                if (zl2_idx <= product.m_validJets.size())
                    break;
            } else if (ROOT::Math::VectorUtil::DeltaR(product.m_validJets.at(i)->p4, zl2->p4) >
                       minZllJetDeltaRVeto) {
                zl2_idx = i;
                if (zl1_idx <= product.m_validJets.size())
                    break;
            }
        }
        if (zl1_idx < zl2_idx)
            std::swap(zl1_idx, zl2_idx);
        if (zl1_idx <= product.m_validJets.size())
            product.m_validJets.erase(product.m_validJets.begin() + zl1_idx);
        if (zl2_idx <= product.m_validJets.size())
            product.m_validJets.erase(product.m_validJets.begin() + zl2_idx);
    }
}