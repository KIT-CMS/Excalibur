#include "Excalibur/Compile/interface/Producers/ValidZllJetsProducer.h"

#include "KappaTools/Toolbox/interface/StringTools.h"


// -- ValidZllJetsProducer

std::string ValidZllJetsProducer::GetProducerId() const { return "ValidZllJetsProducer"; }

void ValidZllJetsProducer::Init(ZJetSettings const& settings) {

    // get and validate pileup jet ID method
    std::string puJetIDSetting = KappaTools::tolower(settings.GetPUJetID());
    if (puJetIDSetting == "value") {
        m_puJetIDWorkingPoint = ValidZllJetsProducer::PUJetIDWorkingPoint::VALUE;
    }
    else if (puJetIDSetting == "none") {
        LOG(WARNING) << "ValidZllJetsProducer: Config variable 'PUJetID' is set to 'none', which " <<
                        "is deprecated and will be removed in the future. Use 'value' instead.";
        m_puJetIDWorkingPoint = ValidZllJetsProducer::PUJetIDWorkingPoint::VALUE;
    }
    else if (puJetIDSetting == "file") {
        m_puJetIDWorkingPoint = ValidZllJetsProducer::PUJetIDWorkingPoint::FILE;
    }
    else if (puJetIDSetting == "loose") {
        m_puJetIDWorkingPoint = ValidZllJetsProducer::PUJetIDWorkingPoint::LOOSE;
    }
    else if (puJetIDSetting == "medium") {
        m_puJetIDWorkingPoint = ValidZllJetsProducer::PUJetIDWorkingPoint::MEDIUM;
    }
    else if (puJetIDSetting == "tight") {
        m_puJetIDWorkingPoint = ValidZllJetsProducer::PUJetIDWorkingPoint::TIGHT;
    }
    else {
        // fell through -> invalid string supplied
        LOG(FATAL) << "ValidZllJetsProducer: Unknown value '" << puJetIDSetting << "' for setting 'puJetIDSetting'. "
                   << "Expected one of: file, loose, medium, tight, value";
    }

    minZllJetDeltaRVeto = settings.GetMinZllJetDeltaRVeto();
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
        if (m_puJetIDWorkingPoint == ValidZllJetsProducer::PUJetIDWorkingPoint::VALUE) {
            if (kJet->getTag(PUJetIDModuleName+"fullDiscriminant", event.m_jetMetadata) < minPUJetID) {
                return false;
            }
        }
        else if (m_puJetIDWorkingPoint == ValidZllJetsProducer::PUJetIDWorkingPoint::LOOSE) {
            if (!bool(int(kJet->getTag(PUJetIDModuleName+"fullId", event.m_jetMetadata)) & (1 << 2))) {
                return false;
            }
        }
        else if (m_puJetIDWorkingPoint == ValidZllJetsProducer::PUJetIDWorkingPoint::MEDIUM) {
            if (!bool(int(kJet->getTag(PUJetIDModuleName+"fullId", event.m_jetMetadata)) & (1 << 1))) {
                return false;
            }
        }
        else if (m_puJetIDWorkingPoint == ValidZllJetsProducer::PUJetIDWorkingPoint::TIGHT) {
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
