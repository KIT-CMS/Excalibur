#include "Excalibur/Compile/interface/Producers/JetCleaner.h"


// -- JetEtaPhiCleaner

std::string JetEtaPhiCleaner::GetProducerId() const { return "JetEtaPhiCleaner"; }

void JetEtaPhiCleaner::Init(ZJetSettings const& settings) {
    JetCleanerBase::Init(settings);

    // jets are rejected if the corresponding histogram bin value is greater than this
    m_cleaningHistogramsValueMaxValid = settings.GetJetEtaPhiCleanerHistogramValueMaxValid();

    // take the cleaning eta-phi histograms from the configured file
    TFile *cleaningFile = new TFile(settings.GetJetEtaPhiCleanerFile().c_str(), "READ");
    assert(cleaningFile && !cleaningFile->IsZombie());
    for (const auto& histoName : settings.GetJetEtaPhiCleanerHistogramNames()) {
        TH2D* cleaningHistogram = (TH2D*)cleaningFile->Get(histoName.c_str());
        assert(cleaningHistogram);
        m_cleaningHistograms.push_back(cleaningHistogram);
    }
}

bool JetEtaPhiCleaner::DoesJetPass(const KJet* jet, ZJetEvent const& event, ZJetProduct const& product, ZJetSettings const& settings) const {

    for (auto& hist : m_cleaningHistograms) {
        // if the bin value is above threshold, invalidate jet
        if (hist->GetBinContent(hist->FindBin(jet->p4.Eta(), jet->p4.Phi())) > m_cleaningHistogramsValueMaxValid) {
            return false;
        }
    }
    // no histogram with bin value above threshold found -> jet is valid
    return true;
}
