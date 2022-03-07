#include "Excalibur/Compile/interface/Producers/LeptonSFProducer.h"

#include <boost/algorithm/string.hpp>
#include "TFile.h"

/*
This producer contains some un-intuitive programming constructs, which are
necessary to account for the different formats of the ROOT files containing
the scale factors (different axes, binning in absolute eta)

Config Keys:
- LeptonSFVariation             If Up/Down shifts should be stored. Choices True/False
- LeptonRecoSFRootfile          Path to ROOT file with efficiencies.
- LeptonRecoSFHistogramName     The name of the histogram inside the ROOT file.
- LeptonRecoSFYear              For Reco efficiencies high pt tables are available. Choices 2016/17/18/None
- LeptonIDSFRootfile
- LeptonIDSFHistogramName
- LeptonIsoSFRootfile
- LeptonIsoSFHistogramName
- LeptonTriggerSFRootfile

If the TrackingSFProducer is needed it has to be reimplemented. Look at the other SFs for guidance.

maybe also relevant:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariateElectronIdentification (SF files for MVA
ID)
https://twiki.cern.ch/twiki/bin/view/CMSPublic/DiLeptonAnalysis#Efficiencies_and_Scale_Factors
https://twiki.cern.ch/twiki/bin/viewauth/CMS/DileptonTriggerResults
http://lovedeep.web.cern.ch/lovedeep/WORK13/TnPRun2012ReReco_2013Oct28/effiPlots.html
https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2018 and other years
*/

//////////////
// LeptonSF //
//////////////

std::string LeptonSFProducer::GetProducerId() const { return "LeptonSFProducer"; }

void LeptonSFProducer::Init(ZJetSettings const& settings)
{
    // Get file
    LOG(INFO) << this->GetProducerId() << ": Loading file " << m_sffile << ", Histogram "
              << histoname;
    TFile file(m_sffile.c_str(), "READONLY");
    if (!file.Get(histoname.c_str())) {
        LOG(FATAL) << "Failed to open histogram " << histoname << " from file " << m_sffile;
    }
    sfhisto = (TH2F*)file.Get(histoname.c_str());
    sfhisto->SetDirectory(0);
    file.Close();

    // use this pointer, so we call child class methods if overwritten.
    // set correct bools for further processing
    this->SetEtaAxis2D(histoname);
    // Use highest pT bin as overflow bin
    this->SetOverflowPtBin();
}

void LeptonSFProducer::Produce(ZJetEvent const& event,
                               ZJetProduct& product,
                               ZJetSettings const& settings) const
{
    LOG(DEBUG) << "\n[" << this->GetProducerId() << "]";
    if (product.m_zValid) {
        const auto* lep1 = product.m_originalLeptons.at(product.m_zLeptons.first);
        const auto* lep2 = product.m_originalLeptons.at(product.m_zLeptons.second);
        float eff1, err1;
        float eff2, err2;
        std::tie(eff1, err1) = this->GetScaleFactorAndUnc(*lep1);
        std::tie(eff2, err2) = this->GetScaleFactorAndUnc(*lep2);
        float totEff = eff1 * eff2;
        product.m_optionalWeights["zl1" + weightName] = eff1;
        product.m_optionalWeights["zl2" + weightName] = eff2;
        product.m_weights["lepton" + weightName] = totEff;
        LOG(DEBUG) << "Lepton1 SF: " << eff1 << ", Lepton2 SF: " << eff2;
        LOG(DEBUG) << "Total SF: " << totEff;
        LOG(DEBUG) << "Apply Variation: " << settings.GetLeptonSFVariation();
        if (settings.GetLeptonSFVariation() == true) {
            product.m_optionalWeights["zl1" + weightName + "Up"] = eff1 + err1;
            product.m_optionalWeights["zl1" + weightName + "Down"] = eff1 - err1;
            product.m_optionalWeights["zl2" + weightName + "Up"] = eff2 + err2;
            product.m_optionalWeights["zl2" + weightName + "Down"] = eff2 - err2;
            // uncertainties should be assumed as fully correlated
            // https://cms-talk.web.cern.ch/t/questions-on-the-combination-of-muon-tnp-uncertainties/5968
            float totErr = eff1 * err2 + eff2 * err1;
            product.m_optionalWeights["lepton" + weightName + "Up"] = totEff + totErr;
            product.m_optionalWeights["lepton" + weightName + "Down"] = totEff - totErr;
            if (settings.GetDebugVerbosity() > 1) {
                LOG(DEBUG) << "Lepton1 SF up: " << eff1 + err1
                           << ", Lepton1 SF down: " << eff1 - err1;
                LOG(DEBUG) << "Lepton2 SF up: " << eff2 + err2
                           << ", Lepton2 SF down: " << eff2 - err2;
                LOG(DEBUG) << "Total SF up: " << totEff + totErr
                           << ", Total SF down: " << totEff - totErr;
            }
        }
    } else {
        LOG(DEBUG) << "No valid Z found. Only applying SFs to Z leptons.";
    }
}

void LeptonSFProducer::SetEtaAxis2D(std::string histoname)
{
    // map with eta on x, pt on y is default!
    if (histoname.find("abseta") != std::string::npos) {
        m_absoluteEta = true;
        if (histoname.find("abseta_pt") != std::string::npos) {
            m_reversed_axes = false;
            LOG(INFO) << this->GetProducerId() << ": abs(eta)-pt map used for SF";
        } else if (histoname.find("pt_abseta") != std::string::npos) {
            LOG(INFO) << "pt-abs(eta) map (reversed axes) used for SF";
            m_reversed_axes = true;
        } else {
            LOG(FATAL) << this->GetProducerId()
                       << ": Neither pt-abs(eta) nor abs(eta)-pt map found for SF.";
        }
    }
    // Attention: abseta needs to be caught in advance!
    else if (histoname.find("eta") != std::string::npos) {
        m_absoluteEta = false;
        if (histoname.find("eta_pt") != std::string::npos) {
            m_reversed_axes = false;
            LOG(INFO) << this->GetProducerId() << ": eta-pt map used for SF";
        } else if (histoname.find("pt_eta") != std::string::npos) {
            m_reversed_axes = true;
            LOG(INFO) << this->GetProducerId() << ": pt-eta map (reversed axes) used for SF";
        } else {
            LOG(FATAL) << this->GetProducerId() << ": Neither pt-eta nor eta-pt map found for SF.";
        }
    } else
        LOG(FATAL) << this->GetProducerId() << ": No known abs(eta)- or eta-pt map found for SF.";
    return;
}

void LeptonSFProducer::SetOverflowPtBin()
{
    int nEta = m_reversed_axes ? sfhisto->GetNbinsY() : sfhisto->GetNbinsX();
    int nPt = m_reversed_axes ? sfhisto->GetNbinsX() : sfhisto->GetNbinsY();
    // start at bin 1, since 0 is underflow bin
    for (int i = 1; i <= nEta; ++i) {
        if (m_reversed_axes) {
            float eff = sfhisto->GetBinContent(nPt, i);
            float err = sfhisto->GetBinError(nPt, i);
            sfhisto->SetBinContent(nPt + 1, i, eff);
            sfhisto->SetBinError(nPt + 1, i, err);
        } else {
            float eff = sfhisto->GetBinContent(i, nPt);
            float err = sfhisto->GetBinError(i, nPt);
            sfhisto->SetBinContent(i, nPt + 1, eff);
            sfhisto->SetBinError(i, nPt + 1, err);
        }
    }
}

std::tuple<float, float> LeptonSFProducer::GetScaleFactorAndUnc(KLV const& lepton) const
{
    float eta;
    eta = m_absoluteEta ? std::abs(lepton.p4.Eta()) : lepton.p4.Eta();
    int bin;
    bin = m_reversed_axes ? sfhisto->FindBin(lepton.p4.Pt(), eta)
                          : sfhisto->FindBin(eta, lepton.p4.Pt());
    float eff = sfhisto->GetBinContent(bin);
    float err = sfhisto->GetBinError(bin);
    // The followong might happen in nocut Pipelines.
    if (eff == 0.0) {
        LOG(DEBUG) << this->GetProducerId() << ": Found efficiency of zero! "
                   << "No under/overflow bin available? Weight set to 1+/-0";
        eff = 1.0;
    }
    return std::make_tuple(eff, err);
}

////////////////
// LeptonIDSF //
////////////////

std::string LeptonIDSFProducer::GetProducerId() const { return "LeptonIDSFProducer"; }

void LeptonIDSFProducer::Init(ZJetSettings const& settings)
{
    weightName = "IDSFWeight";
    m_sffile = settings.GetLeptonIDSFRootfile();
    if (settings.GetLeptonSFVariation() == true) {
        LOG(INFO) << this->GetProducerId() << ": SF variation up and down one sigma";
    }
    if (settings.GetChannel() == "mm") {
        histoname = settings.GetLeptonIDSFHistogramName();
    } else {
        LOG(ERROR) << "LeptonIDSFProducer not implemented for this channel";
    }

    LeptonSFProducer::Init(settings);
}

/////////////////
// LeptonIsoSF //
/////////////////

std::string LeptonIsoSFProducer::GetProducerId() const { return "LeptonIsoSFProducer"; }

void LeptonIsoSFProducer::Init(ZJetSettings const& settings)
{
    weightName = "IsoSFWeight";
    m_sffile = settings.GetLeptonIsoSFRootfile();
    if (settings.GetLeptonSFVariation() == true) {
        LOG(INFO) << this->GetProducerId() << ": SF variation up and down one sigma";
    }
    if (settings.GetChannel() == "mm") {
        histoname = settings.GetLeptonIsoSFHistogramName();
    } else {
        LOG(ERROR) << "LeptonIsoSFProducer not implemented for this channel";
    }

    LeptonSFProducer::Init(settings);
}

//////////////////////
// LeptonTrackingSF //
//////////////////////

std::string LeptonTrackingSFProducer::GetProducerId() const { return "LeptonTrackingSFProducer"; }

// Tracking SF Producer is not used at the moment, update is necessary if one wants to use it!

void LeptonTrackingSFProducer::Init(ZJetSettings const& settings)
{
    LOG(FATAL) << this->GetProducerId() << " is not implemented.";
}

/////////////////////
// LeptonTriggerSF //
/////////////////////

std::string LeptonTriggerSFProducer::GetProducerId() const { return "LeptonTriggerSFProducer"; }

void LeptonTriggerSFProducer::Init(ZJetSettings const& settings)
{
    weightName = "TriggerSFWeight";
    m_sffile = settings.GetLeptonTriggerSFRootfile();
    if (settings.GetLeptonSFVariation() == true) {
        LOG(INFO) << this->GetProducerId() << ": SF variation up and down one sigma";
    }
    if (settings.GetChannel() == "mm") {
        histoname = settings.GetLeptonTriggerSFHistogramName();
    } else {
        LOG(ERROR) << "LeptonTriggerSFProducer not implemented for this channel";
    }

    LeptonSFProducer::Init(settings);
}

void LeptonTriggerSFProducer::Produce(ZJetEvent const& event,
                                      ZJetProduct& product,
                                      ZJetSettings const& settings) const
{
    LOG(DEBUG) << "\n[" << this->GetProducerId() << "]";
    if (product.m_zValid) {
        const auto* lep1 = product.m_originalLeptons.at(product.m_zLeptons.first);
        const auto* lep2 = product.m_originalLeptons.at(product.m_zLeptons.second);
        float eff1, err1;
        float eff2, err2;
        std::tie(eff1, err1) = this->GetScaleFactorAndUnc(*lep1);
        std::tie(eff2, err2) = this->GetScaleFactorAndUnc(*lep2);
        float totEff = 1 - ((1 - eff1) * (1 - eff2));
        product.m_optionalWeights["zl1" + weightName] = eff1;
        product.m_optionalWeights["zl2" + weightName] = eff2;
        product.m_weights["lepton" + weightName] = totEff;
        LOG(DEBUG) << "Lepton1 SF: " << eff1 << ", Lepton2 SF: " << eff2;
        LOG(DEBUG) << "Total SF: " << totEff;
        LOG(DEBUG) << "Apply Variation: " << settings.GetLeptonSFVariation();
        if (settings.GetLeptonSFVariation() == true) {
            // assume errors as fully correlated, add simple instead of quadrature
            float totErr = err1 * (1 - eff2) + err2 * (1 - eff1);
            product.m_optionalWeights["zl1" + weightName + "Up"] = eff1 + err1;
            product.m_optionalWeights["zl1" + weightName + "Down"] = eff1 - err1;
            product.m_optionalWeights["zl2" + weightName + "Up"] = eff2 + err2;
            product.m_optionalWeights["zl2" + weightName + "Down"] = eff2 - err2;
            product.m_optionalWeights["lepton" + weightName + "Up"] = totEff + totErr;
            product.m_optionalWeights["lepton" + weightName + "Down"] = totEff - totErr;
            if (settings.GetDebugVerbosity() > 1) {
                LOG(DEBUG) << "Lepton1 SF up: " << eff1 + err1
                           << ", Lepton1 SF down: " << eff1 - err1;
                LOG(DEBUG) << "Lepton2 SF up: " << eff2 + err2
                           << ", Lepton2 SF down: " << eff2 - err2;
                LOG(DEBUG) << "Total SF up: " << totEff + totErr
                           << ", Total SF down: " << totEff - totErr;
            }
        }
    } else {
        LOG(DEBUG) << "No valid Z found. Only applying SFs to Z leptons.";
    }
}

/////////////////////
// LeptonRecoSF //
/////////////////////

std::string LeptonRecoSFProducer::GetProducerId() const { return "LeptonRecoSFProducer"; }

void LeptonRecoSFProducer::Init(ZJetSettings const& settings)
{
    weightName = "RecoSFWeight";
    m_sffile = settings.GetLeptonRecoSFRootfile();
    if (settings.GetLeptonSFVariation() == true) {
        LOG(INFO) << this->GetProducerId() << ": SF variation up and down one sigma";
    }
    if (settings.GetChannel() == "mm") {
        histoname = settings.GetLeptonRecoSFHistogramName();
    } else {
        LOG(ERROR) << "LeptonIsoSFProducer not implemented for this channel";
    }

    LeptonSFProducer::Init(settings);

    m_year = settings.GetLeptonRecoSFYear();
    LOG(INFO) << this->GetProducerId() << ": using year " << m_year << " for highPt SFs.";
}

std::tuple<float, float> LeptonRecoSFProducer::GetScaleFactorAndUnc(KLV const& lepton) const
{
    if ((lepton.p4.P() > 50.0 && std::abs(lepton.p4.Eta()) < 1.6) ||
        (lepton.p4.P() > 100.0 && std::abs(lepton.p4.Eta()) < 2.4)) {
        return GetHighPtEff(lepton);
    }
    // else fall back to given histo at medium/low pt
    return LeptonSFProducer::GetScaleFactorAndUnc(lepton);
}

void LeptonRecoSFProducer::SetOverflowPtBin()
{
    // For RECO SF, the mean at the plateu (pt>5) is recommended as overflow.
    // https://cms-talk.web.cern.ch/t/big-muon-reco-scale-factor-uncertainties-in-2018/7644
    int nEta = m_reversed_axes ? sfhisto->GetNbinsY() : sfhisto->GetNbinsX();
    int nPt = m_reversed_axes ? sfhisto->GetNbinsX() : sfhisto->GetNbinsY();
    // start at bin 1, since 0 is underflow bin
    for (int i = 1; i <= nEta; ++i) {
        float numerator = 0.0;
        float denominator = 0.0;
        if (m_reversed_axes) {
            for (int j = sfhisto->GetXaxis()->FindBin(5.0); j <= nPt; ++j) {
                float eff = sfhisto->GetBinContent(j, i);
                float err = sfhisto->GetBinError(j, i);
                if (err == 0) continue;
                denominator += 1 / (err * err);
                numerator += eff / (err * err);
            }
            sfhisto->SetBinContent(nPt + 1, i, numerator / denominator);
            sfhisto->SetBinError(nPt + 1, i, std::sqrt(1 / denominator));
        } else {
            for (int j = sfhisto->GetYaxis()->FindBin(5.0); j <= nPt; ++j) {
                float eff = sfhisto->GetBinContent(i, j);
                float err = sfhisto->GetBinError(i, j);
                if (err == 0) continue;
                denominator += 1 / (err * err);
                numerator += eff / (err * err);
            }
            sfhisto->SetBinContent(i, nPt + 1, numerator / denominator);
            sfhisto->SetBinError(i, nPt + 1, std::sqrt(1 / denominator));
        }
    }
}

std::tuple<float, float> LeptonRecoSFProducer::GetHighPtEff(KLV const& lepton) const
{
    float eta = std::abs(lepton.p4.Eta());
    if (m_year == "2018") {
        // https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2018#High_pT_above_120_GeV
        if (eta < 1.6) {
            if (lepton.p4.P() < 50.0)
                LOG(FATAL) << "Low/Medium Pt Reco SF should be used.";
            else if (lepton.p4.P() < 100.0)
                return std::make_tuple(0.9943, 0.0007);
            else if (lepton.p4.P() < 150.0)
                return std::make_tuple(0.9948, 0.0007);
            else if (lepton.p4.P() < 200.0)
                return std::make_tuple(0.9950, 0.0009);
            else if (lepton.p4.P() < 300.0)
                return std::make_tuple(0.994, 0.001);
            else if (lepton.p4.P() < 400.0)
                return std::make_tuple(0.9914, 0.0009);
            else if (lepton.p4.P() < 600.0)
                return std::make_tuple(0.993, 0.002);
            else if (lepton.p4.P() < 1500.0)
                return std::make_tuple(0.991, 0.004);
            else if (lepton.p4.P() < 3500.0)
                return std::make_tuple(1.0, 0.1);
        } else if (eta < 2.4) {
            if (lepton.p4.P() < 100.0)
                LOG(FATAL) << "Low/Medium Pt Reco SF should be used.";
            else if (lepton.p4.P() < 150.0)
                return std::make_tuple(0.993, 0.001);
            else if (lepton.p4.P() < 200.0)
                return std::make_tuple(0.990, 0.001);
            else if (lepton.p4.P() < 300.0)
                return std::make_tuple(0.988, 0.001);
            else if (lepton.p4.P() < 400.0)
                return std::make_tuple(0.981, 0.002);
            else if (lepton.p4.P() < 600.0)
                return std::make_tuple(0.983, 0.003);
            else if (lepton.p4.P() < 1500.0)
                return std::make_tuple(0.978, 0.006);
            else if (lepton.p4.P() < 3500.0)
                return std::make_tuple(0.98, 0.03);
        } else {
            LOG(ERROR) << "No RecoSF available for this p and eta region. Using 1+/-0";
            return std::make_tuple(1.0, 0.0);
        }
    } else if (m_year == "2017") {
        // https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2017#High_pT_above_120_GeV
        if (eta < 1.6) {
            if (lepton.p4.P() < 50.0)
                LOG(FATAL) << "Low/Medium Pt Reco SF should be used.";
            else if (lepton.p4.P() < 100.0)
                return std::make_tuple(0.9938, 0.0006);
            else if (lepton.p4.P() < 150.0)
                return std::make_tuple(0.9950, 0.0007);
            else if (lepton.p4.P() < 200.0)
                return std::make_tuple(0.996, 0.001);
            else if (lepton.p4.P() < 300.0)
                return std::make_tuple(0.996, 0.001);
            else if (lepton.p4.P() < 400.0)
                return std::make_tuple(0.994, 0.001);
            else if (lepton.p4.P() < 600.0)
                return std::make_tuple(1.003, 0.006);
            else if (lepton.p4.P() < 1500.0)
                return std::make_tuple(0.987, 0.003);
            else if (lepton.p4.P() < 3500.0)
                return std::make_tuple(0.9, 0.1);
        } else if (eta < 2.4) {
            if (lepton.p4.P() < 100.0)
                LOG(FATAL) << "Low/Medium Pt Reco SF should be used.";
            else if (lepton.p4.P() < 150.0)
                return std::make_tuple(0.993, 0.001);
            else if (lepton.p4.P() < 200.0)
                return std::make_tuple(0.989, 0.001);
            else if (lepton.p4.P() < 300.0)
                return std::make_tuple(0.986, 0.001);
            else if (lepton.p4.P() < 400.0)
                return std::make_tuple(0.989, 0.001);
            else if (lepton.p4.P() < 600.0)
                return std::make_tuple(0.983, 0.003);
            else if (lepton.p4.P() < 1500.0)
                return std::make_tuple(0.986, 0.006);
            else if (lepton.p4.P() < 3500.0)
                return std::make_tuple(1.01, 0.01);
        } else {
            LOG(ERROR) << "No RecoSF available for this p and eta region. Using 1+/-0";
            return std::make_tuple(1.0, 0.0);
        }
    } else if (m_year == "2016") {
        // https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2016#High_pT_above_120_GeV
        if (eta < 1.6) {
            if (lepton.p4.P() < 50.0)
                LOG(FATAL) << "Low/Medium Pt Reco SF should be used.";
            else if (lepton.p4.P() < 100.0)
                return std::make_tuple(0.9914, 0.0008);
            else if (lepton.p4.P() < 150.0)
                return std::make_tuple(0.9936, 0.0009);
            else if (lepton.p4.P() < 200.0)
                return std::make_tuple(0.993, 0.001);
            else if (lepton.p4.P() < 300.0)
                return std::make_tuple(0.993, 0.002);
            else if (lepton.p4.P() < 400.0)
                return std::make_tuple(0.990, 0.004);
            else if (lepton.p4.P() < 600.0)
                return std::make_tuple(0.990, 0.003);
            else if (lepton.p4.P() < 1500.0)
                return std::make_tuple(0.989, 0.004);
            else if (lepton.p4.P() < 3500.0)
                return std::make_tuple(0.8, 0.3);
        } else if (eta < 2.4) {
            if (lepton.p4.P() < 100.0)
                LOG(FATAL) << "Low/Medium Pt Reco SF should be used.";
            else if (lepton.p4.P() < 150.0)
                return std::make_tuple(0.993, 0.001);
            else if (lepton.p4.P() < 200.0)
                return std::make_tuple(0.991, 0.001);
            else if (lepton.p4.P() < 300.0)
                return std::make_tuple(0.985, 0.001);
            else if (lepton.p4.P() < 400.0)
                return std::make_tuple(0.981, 0.002);
            else if (lepton.p4.P() < 600.0)
                return std::make_tuple(0.979, 0.004);
            else if (lepton.p4.P() < 1500.0)
                return std::make_tuple(0.978, 0.005);
            else if (lepton.p4.P() < 3500.0)
                return std::make_tuple(0.9, 0.2);
        } else {
            LOG(ERROR) << "No RecoSF available for this p and eta region. Using 1+/-0";
            return std::make_tuple(1.0, 0.0);
        }
    } else if (m_year != "none") {
        LOG(FATAL) << "No high pt RecoSF available for year " << m_year;
    }
    LOG(ERROR) << "No RecoSF available for this year. Using 1+/-0";
    return std::make_tuple(1.0, 0.0);
}
