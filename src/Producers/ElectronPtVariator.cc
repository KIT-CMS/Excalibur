#include "ElectronPtVariator.h"

#include <boost/algorithm/string.hpp>
#include "TH2.h"

/*
Vary electron pT up or down by factor given by weight file
*/

std::string ElectronPtVariator::GetProducerId() const { return "ElectronPtVariator"; }

void ElectronPtVariator::Init(ZJetSettings const& settings)
{
    std::string histoname;  // histoname depending on id

    double error_multiplier = 0.;
    if (settings.GetElectronPtVariation() == "up") {
        LOG(WARNING) << "ElectronPtVariator: varying pT UP one sigma";
        error_multiplier = 1.;
    } else if (settings.GetElectronPtVariation() == "down") {
        LOG(WARNING) << "ElectronPtVariator: varying pT DOWN one sigma";
        error_multiplier = -1.;
    }

    std::string sffile = settings.GetElectronPtVariationFile();

    // Get file
    LOG(INFO) << "Loading electron scale factors for ID "
              << ": File " << sffile << ", Histogram "
              << "mc";
    TFile file(sffile.c_str(), "READONLY");
    TH2D* sfhisto = dynamic_cast<TH2D*>(file.Get("mc"));

    // Get the pT and eta bin borders
    for (int iy = 0; iy <= sfhisto->GetNbinsY(); ++iy)
        m_etabins.emplace_back(2 * sfhisto->GetYaxis()->GetBinCenter(iy) -
                               sfhisto->GetYaxis()->GetBinLowEdge(iy));
    for (int ix = 0; ix <= sfhisto->GetNbinsX(); ++ix)
        m_ptbins.emplace_back(2 * sfhisto->GetXaxis()->GetBinCenter(ix) -
                              sfhisto->GetXaxis()->GetBinLowEdge(ix));

    // Fill the m_sf array with the values from the root histo
    for (int iy = 1; iy <= sfhisto->GetNbinsY(); iy++) {
        for (int ix = 1; ix <= sfhisto->GetNbinsX(); ix++) {
            m_sf[ix - 1][iy - 1] =
                static_cast<float>(1 + error_multiplier * sfhisto->GetBinContent(ix, iy));
        }
    }
    delete sfhisto;
    file.Close();
}

void ElectronPtVariator::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    for (auto electron : product.m_validElectrons) {
        electron->p4.SetPt(electron->p4.Pt() * GetScaleFactor(electron));
    }
}
