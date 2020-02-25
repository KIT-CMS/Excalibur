#include "Excalibur/Compile/interface/Producers/ValidZllJetsProducer.h"


// -- ValidZllJetsProducer

std::string ValidZllJetsProducer::GetProducerId() const { return "ValidZllJetsProducer"; }

void ValidZllJetsProducer::Init(ZJetSettings const& settings) {

    minZllJetDeltaRVeto = settings.GetMinZllJetDeltaRVeto();
    PUJetID = settings.GetPUJetID();
    minPUJetID = settings.GetMinPUJetID();
    PUJetIDModuleName = settings.GetPUJetIDModuleName();
    maxLeadingJetY = settings.GetCutLeadingJetYMax();
    objectJetY = settings.GetUseObjectJetYCut();
}

bool ValidZllJetsProducer::DoesJetPass(const KBasicJet* jet, ZJetEvent const& event, ZJetProduct const& product, ZJetSettings const& settings) const {

    // check if the leptons from the Z boson decay are too near the jet
    if (product.m_zValid) {
        if ((ROOT::Math::VectorUtil::DeltaR(jet->p4, product.m_zLeptons.first->p4) < minZllJetDeltaRVeto) ||
            (ROOT::Math::VectorUtil::DeltaR(jet->p4, product.m_zLeptons.second->p4) < minZllJetDeltaRVeto)) {
            return false;
        }
    }

    // check that PUJetID is above configured minimal value
    const KJet* kJet = dynamic_cast<const KJet*>(jet);  // need a KJet for PUJetID, not just a KBasicJet...
    if (kJet) {
        if (PUJetID == "none") {
            if (kJet->getTag(PUJetIDModuleName+"fullDiscriminant", event.m_jetMetadata) < minPUJetID) {
                return false;
            }
        }
        else if (PUJetID == "loose") {
            if (!bool(int(kJet->getTag(PUJetIDModuleName+"fullId", event.m_jetMetadata)) & (1 << 2))) {
                return false;
            }
        }
        else if (PUJetID == "medium") {
            if (!bool(int(kJet->getTag(PUJetIDModuleName+"fullId", event.m_jetMetadata)) & (1 << 1))) {
                return false;
            }
        }
        else if (PUJetID == "tight") {
            if (!bool(int(kJet->getTag(PUJetIDModuleName+"fullId", event.m_jetMetadata)) & (1 << 0))) {
                return false;
            }
        }
    }
    if (objectJetY) {
        if (std::abs(jet->p4.Rapidity()) > maxLeadingJetY) {
            return false;
        }
    }
    // all checks passed -> jet is valid
    return true;
}


// -- ValidZllGenJetsProducer

std::string ValidZllGenJetsProducer::GetProducerId() const { return "ValidZllGenJetsProducer"; }

void ValidZllGenJetsProducer::Init(ZJetSettings const& settings) {

    minZllJetDeltaRVeto = settings.GetMinZllJetDeltaRVeto();
    maxLeadingJetY = settings.GetCutLeadingJetYMax();
    objectJetY = settings.GetUseObjectJetYCut();
}

bool ValidZllGenJetsProducer::DoesJetPass(const KLV& genJet, ZJetEvent const& event, ZJetProduct const& product, ZJetSettings const& settings) const {

    // check if the leptons from the gen Z boson decay are too near the gen jet
    if (product.m_genBosonLVFound) {
        for (const auto& lep : product.m_genLeptonsFromBosonDecay) {
            if (ROOT::Math::VectorUtil::DeltaR(genJet.p4, lep->p4) < minZllJetDeltaRVeto)
                return false;
        }
    }
    if (objectJetY) {
        if (std::abs(genJet.p4.Rapidity()) > maxLeadingJetY) {
            return false;
        }
    }
    // all checks passed -> genjet is valid
    return true;
}
