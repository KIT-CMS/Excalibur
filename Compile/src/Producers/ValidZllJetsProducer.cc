#include "Excalibur/Compile/interface/Producers/ValidZllJetsProducer.h"

#include "KappaTools/Toolbox/interface/StringTools.h"


// -- ValidZllJetsProducer

std::string ValidZllJetsProducer::GetProducerId() const { return "ValidZllJetsProducer"; }

void ValidZllJetsProducer::Init(ZJetSettings const& settings) {
    JetCleanerBase::Init(settings);

    // get and validate pileup jet ID method
    std::string puJetIDSetting = KappaTools::tolower(settings.GetPUJetID());
    if (puJetIDSetting == "value") {
        m_puJetIDWorkingPoint = ValidZllJetsProducer::PUJetIDWorkingPoint::VALUE;
        m_puJetIDMetadataTag = settings.GetPUJetIDModuleName() + "fullDiscriminant";
    }
    else if (puJetIDSetting == "none") {
        LOG(WARNING) << "[ValidZllJetsProducer] Config variable 'PUJetID' is set to 'none'. "
                     << "Skipping PUJetID veto.";
        m_puJetIDWorkingPoint = ValidZllJetsProducer::PUJetIDWorkingPoint::NONE;
        m_puJetIDMetadataTag = "";
    }
    else if (puJetIDSetting == "file") {
        m_puJetIDWorkingPoint = ValidZllJetsProducer::PUJetIDWorkingPoint::FILE;
        m_puJetIDMetadataTag = settings.GetPUJetIDModuleName() + "fullDiscriminant";
    }
    else if (puJetIDSetting == "loose") {
        m_puJetIDWorkingPoint = ValidZllJetsProducer::PUJetIDWorkingPoint::LOOSE;
        m_puJetIDMetadataTag = settings.GetPUJetIDModuleName() + "fullId";
    }
    else if (puJetIDSetting == "medium") {
        m_puJetIDWorkingPoint = ValidZllJetsProducer::PUJetIDWorkingPoint::MEDIUM;
        m_puJetIDMetadataTag = settings.GetPUJetIDModuleName() + "fullId";
    }
    else if (puJetIDSetting == "tight") {
        m_puJetIDWorkingPoint = ValidZllJetsProducer::PUJetIDWorkingPoint::TIGHT;
        m_puJetIDMetadataTag = settings.GetPUJetIDModuleName() + "fullId";
    }
    else {
        // fell through -> invalid string supplied
        LOG(FATAL) << "[ValidZllJetsProducer] Unknown value '" << puJetIDSetting << "' for setting 'PUJetID'. "
                   << "Expected one of: file, loose, medium, tight, value";
    }

    // load min PU jet ID histogram from file
    if (m_puJetIDWorkingPoint == ValidZllJetsProducer::PUJetIDWorkingPoint::FILE) {
        if (settings.GetMinPUJetIDFile().empty()) {
            LOG(FATAL) << "[ValidZllJetsProducer] Config variable 'PUJetID' is set to 'file', but "
                       << "'MinPUJetIDFile' was not provided (empty string)";
        }
        if (settings.GetMinPUJetIDHistogramName().empty()) {
            LOG(FATAL) << "[ValidZllJetsProducer] Config variable 'PUJetID' is set to 'file', but "
                       << "'MinPUJetIDHistogramName' was not provided (empty string)";
        }
        TFile minPUJetIDFile(settings.GetMinPUJetIDFile().c_str(), "READONLY");
        m_puJetIDMinValueHistogram = (TH2F*)minPUJetIDFile.Get(settings.GetMinPUJetIDHistogramName().c_str());
        if (!m_puJetIDMinValueHistogram) {
            LOG(FATAL) << "[ValidZllJetsProducer] Failed to get pileup jet ID histogram '" << settings.GetMinPUJetIDHistogramName()
                       << "' from file: " << settings.GetMinPUJetIDFile();
        }
        m_puJetIDMinValueHistogram->SetDirectory(0);
        minPUJetIDFile.Close();
    }

    minZllJetDeltaRVeto = settings.GetMinZllJetDeltaRVeto();
    maxLeadingJetY = settings.GetCutLeadingJetYMax();
    objectJetY = settings.GetUseObjectJetYCut();
    maxJetEta = settings.GetMaxJetEta();
    objectJetEta = settings.GetUseObjectJetEtaCut();
}

bool ValidZllJetsProducer::DoesJetPass(const KJet* jet, ZJetEvent const& event, ZJetProduct const& product, ZJetSettings const& settings) const {

    // check that PUJetID is above configured minimal value
    const KJet* kJet = dynamic_cast<const KJet*>(jet);  // need a KJet for PUJetID, not just a KBasicJet...
    if (kJet && (m_puJetIDWorkingPoint != ValidZllJetsProducer::PUJetIDWorkingPoint::NONE)) {
        const double puJetIDValue = kJet->getTag(m_puJetIDMetadataTag, event.m_jetMetadata);
        // LOG(DEBUG) << "PUJetIDValue: " <<  puJetIDValue;

        if (m_puJetIDWorkingPoint == ValidZllJetsProducer::PUJetIDWorkingPoint::FILE) {
            // lookup bin indices in PUJetID histogram corresponding to the jet pT/absEta
            const int histBinX = m_puJetIDMinValueHistogram->GetXaxis()->FindFixBin(kJet->p4.Pt());
            const int histBinY = m_puJetIDMinValueHistogram->GetYaxis()->FindFixBin(std::abs(kJet->p4.Eta()));

            // check for over-/underflows
            if ((histBinX > 0) && (histBinX <= m_puJetIDMinValueHistogram->GetNbinsX()) &&
                (histBinY > 0) && (histBinY <= m_puJetIDMinValueHistogram->GetNbinsY())) {

                // if bin is found, check puJetID and veto jet if it fails
                if (puJetIDValue < m_puJetIDMinValueHistogram->GetBinContent(histBinX, histBinY)) {
                    return false;
                }
            }
        }
        else if (m_puJetIDWorkingPoint == ValidZllJetsProducer::PUJetIDWorkingPoint::VALUE) {
            if (puJetIDValue < settings.GetMinPUJetID()) {
                return false;
            }
        }
        else if (m_puJetIDWorkingPoint == ValidZllJetsProducer::PUJetIDWorkingPoint::LOOSE) {
            if (!bool(int(puJetIDValue) & (1 << 2))) {
                return false;
            }
        }
        else if (m_puJetIDWorkingPoint == ValidZllJetsProducer::PUJetIDWorkingPoint::MEDIUM) {
            if (!bool(int(puJetIDValue) & (1 << 1))) {
                return false;
            }
        }
        else if (m_puJetIDWorkingPoint == ValidZllJetsProducer::PUJetIDWorkingPoint::TIGHT) {
            if (!bool(int(puJetIDValue) & (1 << 0))) {
                return false;
            }
        }
    }

    // invalidate all jets with absolute rapidity outside configured value
    if (objectJetY) {
        if (std::abs(jet->p4.Rapidity()) > maxLeadingJetY) {
            return false;
        }
    }
    // invalidate all jets with absolute eta outside configured value
    if (objectJetEta) {
        if (std::abs(jet->p4.Eta()) > maxJetEta) {
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
    maxJetEta = settings.GetMaxJetEta();
    objectJetEta = settings.GetUseObjectJetEtaCut();
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
    if (objectJetEta) {
        if (std::abs(genJet.p4.Eta()) > maxJetEta) {
            return false;
        }
    }
    // all checks passed -> genjet is valid
    return true;
}

