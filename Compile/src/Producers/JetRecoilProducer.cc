#include "Excalibur/Compile/interface/Producers/JetRecoilProducer.h"
/**
    \brief Produces quantities related to the total jet recoil.

    This producer implements the reconstruction of the total jet recoil.

    The jet recoil is defined as the vectorial sum of all
    jet pTs starting with the leading jet and down to a particular threshold.

    Configuration settings:
      - JetRecoilMinPtThreshold (float) :
            only jets above this pT threshold are included in the recoil.
*/

std::string JetRecoilProducer::GetProducerId() const { return "JetRecoilProducer"; }

void JetRecoilProducer::Init(ZJetSettings const& settings) {}

void JetRecoilProducer::Produce(ZJetEvent const& event,
                                ZJetProduct& product,
                                ZJetSettings const& settings) const
{
    // calculate total jet recoil (sum of jet pts)

    // -- uncorrected Jets
    KLV uncorrectedJetRecoil;
    bool foundJetsForRecoil = false;
    for (std::size_t i = 0; i < product.m_validJets.size(); ++i) {

        const KBasicJet* jet = product.m_validJets.at(i);
        if (jet->p4.Pt() >= settings.GetJetRecoilMinPtThreshold()) {
            uncorrectedJetRecoil.p4 += product.m_validJets.at(i)->p4;
            foundJetsForRecoil = true;
        }
        else {
            // assume pT won't increase again -> stop
            break;
        }
    }

    // if jets satisfying the criteria were found, write out recoil
    if (foundJetsForRecoil) {
        product.m_correctedJetRecoils["None"] = uncorrectedJetRecoil;
    }

    // -- corrected Jets

    // loop over all JEC correction levels
    for (auto const& corrLevelAndJets : product.m_correctedZJets) {
        // calculate total jet recoil (sum of jet pts)
        KLV jetRecoil;
        foundJetsForRecoil = false;
        for (std::size_t i = 0; i < corrLevelAndJets.second.size(); ++i) {

            const KJet* jet = corrLevelAndJets.second.at(i).get();
            if (jet->p4.Pt() >= settings.GetJetRecoilMinPtThreshold()) {
                jetRecoil.p4 += product.m_validJets.at(i)->p4;
                foundJetsForRecoil = true;
            }
            else {
                // assume pT won't increase again -> stop
                break;
            }
        }

        // if jets satisfying the criteria were found, write out recoil
        if (foundJetsForRecoil) {
            product.m_correctedJetRecoils[corrLevelAndJets.first] = jetRecoil;
        }
    }
}
