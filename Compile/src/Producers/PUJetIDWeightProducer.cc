#include "Excalibur/Compile/interface/Producers/PUJetIDWeightProducer.h"

std::string PUJetIDWeightProducer::GetProducerId() const { return "PUJetIDWeightProducer"; }

void PUJetIDWeightProducer::Init(ZJetSettings const& settings) {

    if (settings.GetInputIsData())
    {
        LOG(FATAL) << "PUJetID SFs can only be applied to MC!";
    }

    if (settings.GetPUJetID() != "none")
    {
        LOG(INFO) << "Loading PUJetID Efficiencies from file " << settings.GetPUJetIDEffFilename();
        TFile PUEffFile(settings.GetPUJetIDEffFilename().c_str(), "READONLY");
        if (PUEffFile.IsOpen() == false)
        {
            LOG(FATAL) << "File for PUJetID scalefactors not found. Please check PUEffFilename.";
        }

        std::string histName = settings.GetPUJetIDEffHistogramName();
        LOG(INFO) << "Loading histogram " << histName << " for PUJetID scalefactors";
        LOG(INFO) << "Using PUJetID " << settings.GetPUJetID() << ". Please verify the settings for the efficiency match the used PUJetID.";
        m_sfhisto = (TH2F*)PUEffFile.Get(histName.c_str());
        if (!m_sfhisto)
        {
            LOG(FATAL)<<"No histogram found with name " << histName;
        }
        m_sfhisto->SetDirectory(0);

        std::string errHistName = settings.GetPUJetIDEffErrHistogramName();
        LOG(INFO) << "Loading histogram " << errHistName << " for PUJetID scalefactors uncertainties.";
        m_errhisto = (TH2F*)PUEffFile.Get(errHistName.c_str());
        if (!m_errhisto)
        {
            LOG(FATAL)<<"no uncertainty histogram found with name" << errHistName;
        }
        m_errhisto->SetDirectory(0);

        PUEffFile.Close();
    }
}

void PUJetIDWeightProducer::Produce(ZJetEvent const& event,
                                    ZJetProduct& product,
                                    ZJetSettings const& settings) const {

    LOG(DEBUG) << "\n[" << this->GetProducerId() << "]";
    double sf = 1.0;
    double err = 0.0;

    const std::vector<std::shared_ptr<KJet>> theJets = product.m_correctedZJets["L1L2L3"];
    const std::vector<int> matchedGenJetIndices = product.m_matchedGenJets4["L1L2L3"];
    KLV* matchedGenJet = nullptr;

    LOG(DEBUG) << "Number of Jets " << theJets.size();
    LOG(DEBUG) << "Number of GenJets " << product.m_simpleGenJets.size();
    if (theJets.size() != matchedGenJetIndices.size()) {
        LOG(FATAL) << "Size of Jets and Matched GenJets differs!";
    }

    if (matchedGenJetIndices.size() < 1 || theJets.size() < 1) {
        LOG(DEBUG) << "No Jets and/or GenJets in event.";
    }
    for (uint i=0; i<theJets.size(); ++i) {
        LOG(DEBUG) << "Checking Jet with Pt" << theJets[i]->p4.Pt();
        int matched_idx = matchedGenJetIndices[i];
        if (matched_idx >= 0) {
            matchedGenJet = product.m_simpleGenJets[matched_idx];
            LOG(DEBUG) << "Matched GenJet Pt " << matchedGenJet->p4.Pt();
            const int histBinX = m_sfhisto->GetXaxis()->FindFixBin(theJets[i]->p4.Pt());
            const int histBinY = m_sfhisto->GetYaxis()->FindFixBin(theJets[i]->p4.Eta());
            // check for over-/underflows
            if ((histBinX > 0) && (histBinX <= m_sfhisto->GetNbinsX()) &&
                (histBinY > 0) && (histBinY <= m_sfhisto->GetNbinsY())) {
                LOG(DEBUG) << "PuJetID Efficiency found.";
                double new_sf = m_sfhisto->GetBinContent(histBinX, histBinY);
                double new_err = m_errhisto->GetBinContent(histBinX, histBinY);
                err = sf*new_err + new_sf*err;  // fully correlated
                sf *= new_sf;
            } else {
                LOG(DEBUG) << "No PuJetID Efficiency available.";
            }
        }
    }

    product.m_optionalWeights["puJetIDWeight"] = sf;
    product.m_optionalWeights["puJetIDWeightUp"] = sf + err;
    product.m_optionalWeights["puJetIDWeightDown"] = sf - err;

    LOG(DEBUG) << "puJetIDWeight: " << sf << " +/- " << err;
    return;
};
