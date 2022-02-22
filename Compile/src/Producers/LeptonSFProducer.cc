#include "Excalibur/Compile/interface/Producers/LeptonSFProducer.h"

#include <boost/algorithm/string.hpp>
#include "TH2.h"
#include "TGraphAsymmErrors.h"
#include <stdio.h>

/*
taken from https://twiki.cern.ch/twiki/bin/view/Main/EGammaScaleFactors2012

This producer contains some un-intuitive programming constructs, which are
necessary to account for the different formats of the ROOT files containing
the scale factors (different axes, binning in absolute eta)

needed tags:
- LeptonIDSFVariation           Vary IDSF by error. Choices: up, down, None
- LeptonIsoSFVariation          Vary IsoSF by error. Choices: up, down, None
- LeptonTrackingSFVariation     Vary TrackingSF by error. Choices: up, down, None
- LeptonTriggerSFVariation      Vary TriggerSF by error. Choices: up, down, None
- LeptonRecoSFVariation         Vary RecoSF by error. Choices: up, down, None

maybe also relevant:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariateElectronIdentification (SF files for MVA
ID)
https://twiki.cern.ch/twiki/bin/view/CMSPublic/DiLeptonAnalysis#Efficiencies_and_Scale_Factors
https://twiki.cern.ch/twiki/bin/viewauth/CMS/DileptonTriggerResults
http://lovedeep.web.cern.ch/lovedeep/WORK13/TnPRun2012ReReco_2013Oct28/effiPlots.html
*/

//////////////
// LeptonSF //
//////////////

std::string LeptonSFProducer::GetProducerId() const { return "LeptonSFProducer"; }

void LeptonSFProducer::Init(ZJetSettings const& settings)
{
   
    
}

void LeptonSFProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    
}

////////////////
// LeptonIDSF //
////////////////

std::string LeptonIDSFProducer::GetProducerId() const { return "LeptonIDSFProducer"; }

void LeptonIDSFProducer::Init(ZJetSettings const& settings)
{
    m_sffile = settings.GetLeptonIDSFRootfile();
    if (settings.GetLeptonSFVariation() == true) {
        LOG(WARNING) << "LeptonIDSFProducer: varying scale factor UP and DOWN one sigma";
    }
    if(settings.GetChannel() == "mm"){
        histoname = settings.GetLeptonIDSFHistogramName();
    }
    else{
        LOG(ERROR) << "LeptonIsoSFProducer not implemented for this channel";
    }
    
    GetEtaAxis2D(m_etarev2D,histoname);
    m_absoluteeta   = m_etarev2D[0];
    m_reversed_axes = m_etarev2D[1];
    m_2D            = m_etarev2D[2];
    if (m_reversed_axes)
    {
        m_etabins = &m_ybins;
        m_ptbins = &m_xbins;
    }
    else
    {
        m_etabins = &m_xbins;
        m_ptbins = &m_ybins;
    }
    // Get file
    LOG(INFO) << "Loading lepton scale factors for ID " << m_id << ": File " << m_sffile
              << ", Histogram " << histoname;
    TFile file(m_sffile.c_str(), "READONLY");
    TH2F* sfhisto = (TH2F*)file.Get(histoname.c_str());
    if (!m_2D)
        // This step causes an unused variable warning. How can we get rid of it?
        TH1F* sfhisto = (TH1F*)file.Get(histoname.c_str());
    
    // Get the pT and eta bin borders
    for (int ix = 0; ix <= sfhisto->GetNbinsX(); ++ix){
        m_xbins.emplace_back(2 * sfhisto->GetXaxis()->GetBinCenter(ix) -
                             sfhisto->GetXaxis()->GetBinLowEdge(ix));
    }
    if (m_2D) {
        for (int iy = 0; iy <= sfhisto->GetNbinsY(); ++iy){
            m_ybins.emplace_back(2 * sfhisto->GetYaxis()->GetBinCenter(iy) -
                             sfhisto->GetYaxis()->GetBinLowEdge(iy));
        }
    }
    else {
        m_ybins.emplace_back(-1000);
        m_ybins.emplace_back( 1000);
    }
    // Fill the m_sf array with the values from the root histo
    for (int ix = 1; ix <= sfhisto->GetNbinsX(); ix++) {
        for (int iy = 1; iy <= sfhisto->GetNbinsY(); iy++) {
            m_sf[ix - 1][iy - 1] = static_cast<float>(sfhisto->GetBinContent(ix, iy));
            m_er[ix - 1][iy - 1] = static_cast<float>(sfhisto->GetBinError(ix, iy));
        }
    }
    delete sfhisto;
    file.Close();

}

void LeptonIDSFProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    if(product.m_zValid){
        const auto* lep1 = product.m_originalLeptons.at(product.m_zLeptons.first);
        const auto* lep2 = product.m_originalLeptons.at(product.m_zLeptons.second);
        product.m_weights["zl1IDSFWeight"] = 1/GetScaleFactor(0, *lep1);
        product.m_weights["zl2IDSFWeight"] = 1/GetScaleFactor(0, *lep2);
        product.m_weights["leptonIDSFWeight"] =
                //some old SF files already include the inverse, make sure you use them the right way!
                //GetScaleFactor(0, *product.m_zLeptons.first) * GetScaleFactor(0, *product.m_zLeptons.second);
                1/GetScaleFactor(0, *lep1) * 1/GetScaleFactor(0, *lep2);
        if (settings.GetLeptonSFVariation() == true) {
            product.m_weights["leptonIDSFWeightUp"] =
                1/GetScaleFactor(-1, *lep1) * 1/GetScaleFactor(-1, *lep2);
            product.m_weights["leptonIDSFWeightDown"] =
                1/GetScaleFactor( 1, *lep1) * 1/GetScaleFactor( 1, *lep2);
        }
    }
    else {
        product.m_weights["leptonIDSFWeight"] = 0;
        product.m_weights["leptonIDSFWeightUp"] = 0;
        product.m_weights["leptonIDSFWeightDown"] = 0;
    }
}

/////////////////
// LeptonIsoSF //
/////////////////

std::string LeptonIsoSFProducer::GetProducerId() const { return "LeptonIsoSFProducer"; }

void LeptonIsoSFProducer::Init(ZJetSettings const& settings)
{
    m_sffile = settings.GetLeptonIsoSFRootfile();
    if (settings.GetLeptonSFVariation() == true) {
        LOG(WARNING) << "LeptonIsoSFProducer: varying scale factor UP and DOWN one sigma";
    }
    
    if(settings.GetChannel() == "mm"){
        histoname = settings.GetLeptonIsoSFHistogramName();
    }
    else{
        LOG(ERROR) << "LeptonIsoSFProducer not implemented for this channel";
    }
    
    GetEtaAxis2D(m_etarev2D,histoname);
    m_absoluteeta   = m_etarev2D[0];
    m_reversed_axes = m_etarev2D[1];
    m_2D            = m_etarev2D[2];
    if (m_reversed_axes)
    {
        m_etabins = &m_ybins;
        m_ptbins = &m_xbins;
    }
    else
    {
        m_etabins = &m_xbins;
        m_ptbins = &m_ybins;
    }
    // Get file
    LOG(INFO) << "Loading lepton scale factors for Isolation " << m_id << ": File " << m_sffile
              << ", Histogram " << histoname;
    TFile file(m_sffile.c_str(), "READONLY");
    TH2F* sfhisto = (TH2F*)file.Get(histoname.c_str());
    if (!m_2D)
        // This step causes an unused variable warning. How can we get rid of it?
        TH1F* sfhisto = (TH1F*)file.Get(histoname.c_str());
    
    // Get the pT and eta bin borders
    for (int ix = 0; ix <= sfhisto->GetNbinsX(); ++ix){
        m_xbins.emplace_back(2 * sfhisto->GetXaxis()->GetBinCenter(ix) -
                             sfhisto->GetXaxis()->GetBinLowEdge(ix));
    }
    if (m_2D) {
        for (int iy = 0; iy <= sfhisto->GetNbinsY(); ++iy){
            m_ybins.emplace_back(2 * sfhisto->GetYaxis()->GetBinCenter(iy) -
                             sfhisto->GetYaxis()->GetBinLowEdge(iy));
        }
    }
    else {
        m_ybins.emplace_back(-1000);
        m_ybins.emplace_back( 1000);
    }
    // Fill the m_sf array with the values from the root histo
    for (int ix = 1; ix <= sfhisto->GetNbinsX(); ix++) {
        for (int iy = 1; iy <= sfhisto->GetNbinsY(); iy++) {
            m_sf[ix - 1][iy - 1] = static_cast<float>(sfhisto->GetBinContent(ix, iy));
            m_er[ix - 1][iy - 1] = static_cast<float>(sfhisto->GetBinError(ix, iy));
        }
    }
    delete sfhisto;
    file.Close();
}

void LeptonIsoSFProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    if(product.m_zValid){
        const auto* lep1 = product.m_originalLeptons.at(product.m_zLeptons.first);
        const auto* lep2 = product.m_originalLeptons.at(product.m_zLeptons.second);
        product.m_weights["zl1IsoSFWeight"] = 1/GetScaleFactor(0, *lep1);
        product.m_weights["zl2IsoSFWeight"] = 1/GetScaleFactor(0, *lep2);
        product.m_weights["leptonIsoSFWeight"] =
                //some old SF files already include the inverse, make sure you use them the right way!
                //GetScaleFactor(0, *product.m_zLeptons.first) * GetScaleFactor(0, *product.m_zLeptons.second);
                1/GetScaleFactor(0, *lep1) * 1/GetScaleFactor(0, *lep2);
        if (settings.GetLeptonSFVariation() == true) {
            product.m_weights["leptonIsoSFWeightUp"] =
                1/GetScaleFactor(-1, *lep1) * 1/GetScaleFactor(-1, *lep2);
            product.m_weights["leptonIsoSFWeightDown"] =
                1/GetScaleFactor( 1, *lep1) * 1/GetScaleFactor( 1, *lep2);
        }
    }
    else {
        product.m_weights["leptonIsoSFWeight"] = 0;
        if (settings.GetLeptonSFVariation() == true) {
            product.m_weights["leptonIsoSFWeightUp"] = 0;
            product.m_weights["leptonIsoSFWeightDown"] = 0;
        }
    }
}

//////////////////////
// LeptonTrackingSF //
//////////////////////

std::string LeptonTrackingSFProducer::GetProducerId() const { return "LeptonTrackingSFProducer"; }

// Tracking SF Producer is not used at the moment, update is necessary if one wants to use it!

void LeptonTrackingSFProducer::Init(ZJetSettings const& settings)
{
    /*m_sffile = settings.GetLeptonTrackingSFRootfile();
    if (settings.GetLeptonSFVariation() == true) {
        LOG(WARNING) << "LeptonTrackingSFProducer: varying scale factor UP and DOWN one sigma";
    } 
    
    if(settings.GetChannel() == "mm"){
        histoname = settings.GetLeptonTrackingSFHistogramName();
    }
    else{
        LOG(ERROR) << "LeptonTrackingSFProducer not implemented for this channel";
    }

    if (m_reversed_axes)
    {
        m_etabins = &m_ybins;
        m_ptbins = &m_xbins;
    }
    else
    {
        m_etabins = &m_xbins;
        m_ptbins = &m_ybins;
    }
    // Get file
    LOG(INFO) << "Loading lepton scale factors for Tracking: File " << m_sffile
              << ", Histogram " << histoname;
    TFile file(m_sffile.c_str(), "READONLY");
    TGraphAsymmErrors *sfhisto = (TGraphAsymmErrors*)file.Get(histoname.c_str());

    // Get the pT and eta bin borders
    m_xbins.emplace_back(sfhisto->GetX()[0] - sfhisto->GetErrorXlow(0));
    for (int ix = 0; ix < sfhisto->GetN(); ++ix){
        m_xbins.emplace_back(sfhisto->GetX()[ix] + sfhisto->GetErrorXhigh(ix));
    }
    m_ybins.emplace_back(0);
    m_ybins.emplace_back(10000);
    
    // Fill the m_sf array with the values from the root histos
    for (int ix = 1; ix <= sfhisto->GetN(); ix++) {
        m_sf[ix - 1][0] = static_cast<float>(sfhisto->GetY()[ix-1]);
        m_er[ix - 1][0] = static_cast<float>(sfhisto->GetErrorY(ix-1));
    }
    delete sfhisto;
    file.Close();*/
}

void LeptonTrackingSFProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    //some old SF files already include the inverse, make sure you use them the right way!
    /*if(product.m_zValid){
        product.m_weights["zl1TrackingSFWeight"] = 1/GetScaleFactor(0, 0, *product.m_zLeptons.first);
        product.m_weights["zl2TrackingSFWeight"] = 1/GetScaleFactor(0, 0, *product.m_zLeptons.second);
        product.m_weights["leptonTrackingSFWeight"] =
                1/GetScaleFactor(0, 0, *product.m_zLeptons.first) * 1/GetScaleFactor(0, 0, *product.m_zLeptons.second);
        if (settings.GetLeptonSFVariation() == true) {
            product.m_weights["leptonTrackingSFWeightUp"] =
                1/GetScaleFactor(0, -1, *product.m_zLeptons.first) * 1/GetScaleFactor(0, -1, *product.m_zLeptons.second);
            product.m_weights["leptonTrackingSFWeightDown"] =
                1/GetScaleFactor(0, 1, *product.m_zLeptons.first) * 1/GetScaleFactor(0, 1, *product.m_zLeptons.second);
        }
    }
    else {
        product.m_weights["leptonTrackingSFWeight"] = 0;
        if (settings.GetLeptonSFVariation() == true) {
            product.m_weights["leptonTrackingSFWeightUp"] = 0;
            product.m_weights["leptonTrackingSFWeightDown"] = 0;
        }
    }*/
}

/////////////////////
// LeptonTriggerSF //
/////////////////////

std::string LeptonTriggerSFProducer::GetProducerId() const { return "LeptonTriggerSFProducer"; }

void LeptonTriggerSFProducer::Init(ZJetSettings const& settings)
{
    m_sffile = settings.GetLeptonTriggerSFRootfile();
    if (settings.GetLeptonSFVariation() == true) {
        LOG(WARNING) << "LeptonTriggerSFProducer: varying scale factor UP and DOWN one sigma";
    }
    
    if(settings.GetChannel() == "mm"){
        histoname = settings.GetLeptonTriggerSFHistogramName();
    }
    else{
        LOG(ERROR) << "LeptonTriggerSFProducer not implemented for this channel";
    }
    /*
    // map with eta on x, pt on y is default!
    if (histoname.find("abseta") != std::string::npos) {
        m_absoluteeta = true;
        if (histoname.find("abseta_pt") != std::string::npos) {
            LOG(INFO) << "abs(eta)-pt map used for Lepton Trigger scale factor";
            m_reversed_axes = false;
            m_2D = true;
        }
        else if (histoname.find("pt_abseta") != std::string::npos) {
            LOG(INFO) << "pt-abs(eta) map (reversed axes) used for Lepton Trigger scale factor";
            m_reversed_axes = true;
            m_2D = true;
        }
        else {
            LOG(INFO) << "abs(eta) map used for Lepton Trigger scale factor";
            m_reversed_axes = false;
            m_2D = false;
            //LOG(ERROR) << "neither pt-abs(eta) nor abs(eta)-pt map found for Lepton Trigger scale factor";
        }
    }
    // Attention: abseta needs to be caught in advance!
    else if (histoname.find("eta") != std::string::npos) {
        m_absoluteeta = false;
        if ( histoname.find("eta_pt") != std::string::npos) {
            LOG(INFO) << "eta-pt map used for Lepton Trigger scale factor";
            m_reversed_axes = false;
            m_2D = true;
        }
        else if (histoname.find("pt_eta") != std::string::npos) {
            LOG(INFO) << "pt-eta map (reversed axes) used for Lepton Trigger scale factor";
            m_reversed_axes = true;
            m_2D = true;
        }
        else {
            LOG(INFO) << "eta map used for Lepton Trigger scale factor";
            m_reversed_axes = true;
            m_2D = false;
            //LOG(ERROR) << "neither pt-eta nor eta-pt map found for Lepton Trigger scale factor";
        }
    }
    else if (histoname.find("pt") != std::string::npos) {
            LOG(INFO) << "pt map used for Lepton Trigger scale factor";
            m_reversed_axes = true;
            m_2D = false;
        }
    else
        LOG(ERROR) << "neither abs(eta), eta nor pt map found for Lepton Trigger scale factor";
    */
    GetEtaAxis2D(m_etarev2D,histoname);
    m_absoluteeta   = m_etarev2D[0];
    m_reversed_axes = m_etarev2D[1];
    m_2D            = m_etarev2D[2];
    if (m_reversed_axes)
    {
        m_etabins = &m_ybins;
        m_ptbins = &m_xbins;
    }
    else
    {
        m_etabins = &m_xbins;
        m_ptbins = &m_ybins;
    }
    // Get file
    LOG(INFO) << "Loading lepton scale factors for Trigger " << m_id << ": File " << m_sffile
              << ", Histogram " << histoname;
    TFile file(m_sffile.c_str(), "READONLY");
    TH2F* sfhisto = (TH2F*)file.Get(histoname.c_str());
    if (!m_2D)
        // This step causes an unused variable warning. How can we get rid of it?
        TH1F* sfhisto = (TH1F*)file.Get(histoname.c_str());
    
    // Get the pT and eta bin borders
    for (int ix = 0; ix <= sfhisto->GetNbinsX(); ++ix){
        m_xbins.emplace_back(2 * sfhisto->GetXaxis()->GetBinCenter(ix) -
                             sfhisto->GetXaxis()->GetBinLowEdge(ix));
    }
    if (m_2D) {
        for (int iy = 0; iy <= sfhisto->GetNbinsY(); ++iy){
            m_ybins.emplace_back(2 * sfhisto->GetYaxis()->GetBinCenter(iy) -
                             sfhisto->GetYaxis()->GetBinLowEdge(iy));
        }
    }
    else {
        m_ybins.emplace_back(-1000);
        m_ybins.emplace_back( 1000);
    }
    // Fill the m_sf array with the values from the root histo
    for (int ix = 1; ix <= sfhisto->GetNbinsX(); ix++) {
        for (int iy = 1; iy <= sfhisto->GetNbinsY(); iy++) {
            m_sf[ix - 1][iy - 1] = static_cast<float>(sfhisto->GetBinContent(ix, iy));
            m_er[ix - 1][iy - 1] = static_cast<float>(sfhisto->GetBinError(ix, iy));
            //m_sfdata[ix - 1][iy - 1] = static_cast<float>(sfhisto->GetBinContent(ix, iy));
            //m_sfmc[ix - 1][iy - 1] = static_cast<float>(sfhistomc->GetBinContent(ix, iy));
            //m_erdata[ix - 1][iy - 1] = static_cast<float>(sfhistodata->GetBinError(ix, iy));
            //m_ermc[ix - 1][iy - 1] = static_cast<float>(sfhistomc->GetBinError(ix, iy));
        }
    }    
    file.Close();
}

void LeptonTriggerSFProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    if(product.m_zValid){
        const auto* lep1 = product.m_originalLeptons.at(product.m_zLeptons.first);
        const auto* lep2 = product.m_originalLeptons.at(product.m_zLeptons.second);
        product.m_weights["zl1TriggerSFWeight"] = 1/GetScaleFactor(0, *lep1);
        product.m_weights["zl2TriggerSFWeight"] = 1/GetScaleFactor(0, *lep2);
        product.m_weights["leptonTriggerSFWeight"] =
            1/(1-(1-GetScaleFactor(0, *lep1)) * (1-GetScaleFactor(0, *lep2)));
        if (settings.GetLeptonSFVariation() == true) {
            product.m_weights["leptonTriggerSFWeightUp"] =
                1/(1-
                  (1-GetScaleFactor(1, *lep1) + 0.005*GetScaleFactor(0, *lep1))
                * (1-GetScaleFactor(1, *lep2) + 0.005*GetScaleFactor(0, *lep2))
                );
            product.m_weights["leptonTriggerSFWeightDown"] =
                1/(1-
                  (1-GetScaleFactor(-1, *lep1) - 0.005*GetScaleFactor(0, *lep1))
                * (1-GetScaleFactor(-1, *lep2) - 0.005*GetScaleFactor(0, *lep2))
                );
        }
    }
    else {
        product.m_weights["leptonTriggerSFWeight"] = 0;
        if (settings.GetLeptonSFVariation() == true) {
            product.m_weights["leptonTriggerSFWeightUp"] = 0;
            product.m_weights["leptonTriggerSFWeightDown"] = 0;
        }
    }
}

/////////////////////
// LeptonRecoSF //
/////////////////////

std::string LeptonRecoSFProducer::GetProducerId() const { return "LeptonRecoSFProducer"; }

void LeptonRecoSFProducer::Init(ZJetSettings const& settings)
{
    m_year = settings.GetLeptonRecoSFYear();
    LOG(INFO) << this->GetProducerId() << ": using year " << m_year << " for highPt SFs.";
    m_sffile = settings.GetLeptonRecoSFRootfile();
    if (settings.GetLeptonSFVariation() == true) {
        LOG(INFO) << "LeptonRecoSFProducer: varying scale factor UP and DOWN one sigma";
    }

    if(settings.GetChannel() == "mm"){
        histoname = settings.GetLeptonRecoSFHistogramName();
    }
    else{
        LOG(ERROR) << "LeptonRecoSFProducer not implemented for this channel";
    }

    GetEtaAxis2D(m_etarev2D,histoname);
    m_absoluteeta   = m_etarev2D[0];
    m_reversed_axes = m_etarev2D[1];
    m_2D            = m_etarev2D[2];
    if (m_reversed_axes)
    {
        m_etabins = &m_ybins;
        m_ptbins = &m_xbins;
    }
    else
    {
        m_etabins = &m_xbins;
        m_ptbins = &m_ybins;
    }
    // Get file
    LOG(INFO) << "Loading lepton scale factors for Reco " << m_id << ": File " << m_sffile
              << ", Histogram " << histoname;
    TFile file(m_sffile.c_str(), "READONLY");
    TH2F* sfhisto = (TH2F*)file.Get(histoname.c_str());

    // Get the pT and eta bin borders
    for (int ix = 0; ix <= sfhisto->GetNbinsX(); ++ix){
        m_xbins.emplace_back(2 * sfhisto->GetXaxis()->GetBinCenter(ix) -
                             sfhisto->GetXaxis()->GetBinLowEdge(ix));
    }
    for (int iy = 0; iy <= sfhisto->GetNbinsY(); ++iy){
        m_ybins.emplace_back(2 * sfhisto->GetYaxis()->GetBinCenter(iy) -
                             sfhisto->GetYaxis()->GetBinLowEdge(iy));
    }
    // Fill the m_sf array with the values from the root histo
    for (int ix = 1; ix <= sfhisto->GetNbinsX(); ix++) {
        for (int iy = 1; iy <= sfhisto->GetNbinsY(); iy++) {
            m_sf[ix - 1][iy - 1] = static_cast<float>(sfhisto->GetBinContent(ix, iy));
            m_er[ix - 1][iy - 1] = static_cast<float>(sfhisto->GetBinError(ix, iy));
        }
    }
    file.Close();
}
void LeptonRecoSFProducer::Produce(ZJetEvent const& event,
                                    ZJetProduct& product,
                                    ZJetSettings const& settings) const
{
    LOG(DEBUG) << "\n[" << this->GetProducerId() << "]";
    if(product.m_zValid){
        const auto* lep1 = product.m_originalLeptons.at(product.m_zLeptons.first);
        const auto* lep2 = product.m_originalLeptons.at(product.m_zLeptons.second);
        LOG(DEBUG) << "Apply LeptonRecoSFVariation: " << settings.GetLeptonSFVariation();
        float sf1 = 1/GetScaleFactor(0, *lep1);
        float sf2 = 1/GetScaleFactor(0, *lep2);
        product.m_weights["zl1RecoSFWeight"] = sf1;
        product.m_weights["zl2RecoSFWeight"] = sf2;
        product.m_weights["leptonRecoSFWeight"] = sf1*sf2;
        LOG(DEBUG) << "sf1: " << sf1 << ", sf2: " << sf2;
        if (settings.GetLeptonSFVariation() == true) {
            // up has -1 since it's inside the denominator, down +1
            float sf1u = 1/GetScaleFactor(-1, *lep1);
            float sf1d = 1/GetScaleFactor(+1, *lep1);
            float sf2u = 1/GetScaleFactor(-1, *lep2);
            float sf2d = 1/GetScaleFactor(+1, *lep2);
            product.m_weights["zl1RecoSFWeightUp"] = sf1u;
            product.m_weights["zl1RecoSFWeightDown"] = sf1d;
            product.m_weights["zl2RecoSFWeightUp"] = sf2u;
            product.m_weights["zl2RecoSFWeightDown"] = sf2d;
            // proper error propagation needed
            product.m_weights["leptonRecoSFWeightUp"] = sf1u*sf2u;
            product.m_weights["leptonRecoSFWeightDown"] = sf1d*sf2d;
            if(settings.GetDebugVerbosity() > 1) {
                LOG(DEBUG) << "zl1RecoSFWeightUp: " << sf1u << ", zl1RecoSFWeightDown: " << sf1d;
                LOG(DEBUG) << "zl2RecoSFWeightUp: " << sf2u << ", zl2RecoSFWeightDown: " << sf2d;
                LOG(DEBUG) << "leptonRecoSFWeightUp: " << sf1u*sf2u << ", leptonRecoSFWeightDown: " << sf1d*sf2d;
            }
        }
    } else {
        LOG(DEBUG) << "No valid Z found. Only applying SFs to Z leptons.";
    }
}

float LeptonRecoSFProducer::GetScaleFactor(float err_shift, KLV const& lepton) const {
    float eff, eff_err;
    if ((lepton.p4.P() > 50.0 && std::abs(lepton.p4.Eta()) < 1.6) ||
        (lepton.p4.P() > 100.0 && std::abs(lepton.p4.Eta()) < 2.4)) {
        std::tie(eff, eff_err) = GetHighPtEff(lepton);
        return eff + err_shift*eff_err;
    }
    // else fall back to given histo at medium/low pt
    return LeptonSFProducer::GetScaleFactor(err_shift, lepton);
}

std::tuple<float, float> LeptonRecoSFProducer::GetHighPtEff(KLV const& lepton) const {
    float eta = std::abs(lepton.p4.Eta());
    if (m_year=="2018") {
        // https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2018#High_pT_above_120_GeV
        if (eta < 1.6) {
            if (50.0 < lepton.p4.P() && lepton.p4.P() < 100.0)
                return std::make_tuple(0.9943, 0.0007);
            if (100.0 < lepton.p4.P() && lepton.p4.P() < 150.0)
                return std::make_tuple(0.9948, 0.0007);
            else if (150.0 < lepton.p4.P() && lepton.p4.P() < 200.0)
                return std::make_tuple(0.9950, 0.0009);
            else if (200.0 < lepton.p4.P() && lepton.p4.P() < 300.0)
                return std::make_tuple(0.994, 0.001);
            else if (300.0 < lepton.p4.P() && lepton.p4.P() < 400.0)
                return std::make_tuple(0.9914, 0.0009);
            else if (400.0 < lepton.p4.P() && lepton.p4.P() < 600.0)
                return std::make_tuple(0.993, 0.002);
            else if (600.0 < lepton.p4.P() && lepton.p4.P() < 1500.0)
                return std::make_tuple(0.991, 0.004);
            else if (1500.0 < lepton.p4.P() && lepton.p4.P() < 3500.0)
                return std::make_tuple(1.0, 0.1);
        }
        else if (1.6 < eta && eta < 2.4) {
            if (100.0 < lepton.p4.P() && lepton.p4.P() < 150.0)
                return std::make_tuple(0.993, 0.001);
            else if (150.0 < lepton.p4.P() && lepton.p4.P() < 200.0)
                return std::make_tuple(0.990, 0.001);
            else if (200.0 < lepton.p4.P() && lepton.p4.P() < 300.0)
                return std::make_tuple(0.988, 0.001);
            else if (300.0 < lepton.p4.P() && lepton.p4.P() < 400.0)
                return std::make_tuple(0.981, 0.002);
            else if (400.0 < lepton.p4.P() && lepton.p4.P() < 600.0)
                return std::make_tuple(0.983, 0.003);
            else if (600.0 < lepton.p4.P() && lepton.p4.P() < 1500.0)
                return std::make_tuple(0.978, 0.006);
            else if (1500.0 < lepton.p4.P() && lepton.p4.P() < 3500.0)
                return std::make_tuple(0.98, 0.03);
        } else {
            LOG(ERROR) << "No RecoSF available for this p and eta region. Using 1+/-0";
            return std::make_tuple(1.0, 0.0);
        }
    } else if (m_year=="2017") {
        // https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2017#High_pT_above_120_GeV
        if (eta < 1.6) {
            if (50.0 < lepton.p4.P() && lepton.p4.P() < 100.0)
                return std::make_tuple(0.9938, 0.0006);
            if (100.0 < lepton.p4.P() && lepton.p4.P() < 150.0)
                return std::make_tuple(0.9950, 0.0007);
            else if (150.0 < lepton.p4.P() && lepton.p4.P() < 200.0)
                return std::make_tuple(0.996, 0.001);
            else if (200.0 < lepton.p4.P() && lepton.p4.P() < 300.0)
                return std::make_tuple(0.996, 0.001);
            else if (300.0 < lepton.p4.P() && lepton.p4.P() < 400.0)
                return std::make_tuple(0.994, 0.001);
            else if (400.0 < lepton.p4.P() && lepton.p4.P() < 600.0)
                return std::make_tuple(1.003, 0.006);
            else if (600.0 < lepton.p4.P() && lepton.p4.P() < 1500.0)
                return std::make_tuple(0.987, 0.003);
            else if (1500.0 < lepton.p4.P() && lepton.p4.P() < 3500.0)
                return std::make_tuple(0.9, 0.1);
        }
        else if (1.6 < eta && eta < 2.4) {
            if (100.0 < lepton.p4.P() && lepton.p4.P() < 150.0)
                return std::make_tuple(0.993, 0.001);
            else if (150.0 < lepton.p4.P() && lepton.p4.P() < 200.0)
                return std::make_tuple(0.989, 0.001);
            else if (200.0 < lepton.p4.P() && lepton.p4.P() < 300.0)
                return std::make_tuple(0.986, 0.001);
            else if (300.0 < lepton.p4.P() && lepton.p4.P() < 400.0)
                return std::make_tuple(0.989, 0.001);
            else if (400.0 < lepton.p4.P() && lepton.p4.P() < 600.0)
                return std::make_tuple(0.983, 0.003);
            else if (600.0 < lepton.p4.P() && lepton.p4.P() < 1500.0)
                return std::make_tuple(0.986, 0.006);
            else if (1500.0 < lepton.p4.P() && lepton.p4.P() < 3500.0)
                return std::make_tuple(1.01, 0.01);
        } else {
            LOG(ERROR) << "No RecoSF available for this p and eta region. Using 1+/-0";
            return std::make_tuple(1.0, 0.0);
        }
    } else if (m_year=="2016") {
        // https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2016#High_pT_above_120_GeV
        if (eta < 1.6) {
            if (50.0 < lepton.p4.P() && lepton.p4.P() < 100.0)
                return std::make_tuple(0.9914, 0.0008);
            if (100.0 < lepton.p4.P() && lepton.p4.P() < 150.0)
                return std::make_tuple(0.9936, 0.0009);
            else if (150.0 < lepton.p4.P() && lepton.p4.P() < 200.0)
                return std::make_tuple(0.993, 0.001);
            else if (200.0 < lepton.p4.P() && lepton.p4.P() < 300.0)
                return std::make_tuple(0.993, 0.002);
            else if (300.0 < lepton.p4.P() && lepton.p4.P() < 400.0)
                return std::make_tuple(0.990, 0.004);
            else if (400.0 < lepton.p4.P() && lepton.p4.P() < 600.0)
                return std::make_tuple(0.990, 0.003);
            else if (600.0 < lepton.p4.P() && lepton.p4.P() < 1500.0)
                return std::make_tuple(0.989, 0.004);
            else if (1500.0 < lepton.p4.P() && lepton.p4.P() < 3500.0)
                return std::make_tuple(0.8, 0.3);
        }
        else if (1.6 < eta && eta < 2.4) {
            if (100.0 < lepton.p4.P() && lepton.p4.P() < 150.0)
                return std::make_tuple(0.993, 0.001);
            else if (150.0 < lepton.p4.P() && lepton.p4.P() < 200.0)
                return std::make_tuple(0.991, 0.001);
            else if (200.0 < lepton.p4.P() && lepton.p4.P() < 300.0)
                return std::make_tuple(0.985, 0.001);
            else if (300.0 < lepton.p4.P() && lepton.p4.P() < 400.0)
                return std::make_tuple(0.981, 0.002);
            else if (400.0 < lepton.p4.P() && lepton.p4.P() < 600.0)
                return std::make_tuple(0.979, 0.004);
            else if (600.0 < lepton.p4.P() && lepton.p4.P() < 1500.0)
                return std::make_tuple(0.978, 0.005);
            else if (1500.0 < lepton.p4.P() && lepton.p4.P() < 3500.0)
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
