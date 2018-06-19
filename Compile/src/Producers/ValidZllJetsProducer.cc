#include "Excalibur/Compile/interface/Producers/ValidZllJetsProducer.h"

/**
    \brief Producer for valid jets given the constraints of Z->ll+Jet analyses

    This producer modifies the collection of valid jets to conform to the specific
    requirements of the Z->ll+Jets analyses.
    This producer should be run after any ValidJetsProducers, as it vetoes previously
    produced jets.

    Configuration settings:

    MinZllJetDeltaRVeto (type: float) required distance between jets and leptons from Z decay
*/

std::string ValidZllJetsProducer::GetProducerId() const { return "ValidZllJetsProducer"; }

void ValidZllJetsProducer::Init(ZJetSettings const& settings)
{
    minZllJetDeltaRVeto = settings.GetMinZllJetDeltaRVeto();
    minPUJetID = settings.GetMinPUJetID();
}

bool ValidZllJetsProducer::DoesntJetPass(const KBasicJet* jet, ZJetEvent const& event, ZJetProduct const& product, ZJetSettings const& settings) const {
    
    bool validjet = true;
    
    if (product.m_zValid) {
        validjet &= (ROOT::Math::VectorUtil::DeltaR(jet->p4,product.m_zLeptons.first->p4) > minZllJetDeltaRVeto)
                && (ROOT::Math::VectorUtil::DeltaR(jet->p4,product.m_zLeptons.second->p4) > minZllJetDeltaRVeto);
    }
    
    // unnecessary loop over jets to find the index
    for (unsigned int it = 0; it < product.m_validJets.size(); ++it) {
        if (jet == product.m_validJets[it]) {
            validjet &= static_cast<KJet*>(product.GetValidJet(settings, event, it))->getTag("pileupJetIdfullDiscriminant", event.m_jetMetadata) > minPUJetID;
        }
    }
    
    return validjet;
    
}

std::string ValidZllGenJetsProducer::GetProducerId() const { return "ValidZllGenJetsProducer"; }

void ValidZllGenJetsProducer::Init(ZJetSettings const& settings)
{
    minZllJetDeltaRVeto = settings.GetMinZllJetDeltaRVeto();
}

void ValidZllGenJetsProducer::Produce(ZJetEvent const& event,
                                   ZJetProduct& product,
                                   ZJetSettings const& settings) const
{
    assert(event.m_genJets);
    for (unsigned int jet=0; jet < ((KLVs*) event.m_genJets)->size(); ++jet) {
        bool validjet = true;
        for (unsigned int lep=0; lep<product.m_genLeptonsFromBosonDecay.size(); ++lep) {
            validjet = validjet && ROOT::Math::VectorUtil::DeltaR( ((KLVs*) event.m_genJets)->at(jet).p4, product.m_genLeptonsFromBosonDecay[lep]->p4) > minZllJetDeltaRVeto;
        }
        if (validjet) {
            product.m_simpleGenJets.push_back(&((KLVs*) event.m_genJets)->at(jet));
        }
    }
}

