#include "Excalibur/Compile/interface/Producers/LeptonSFProducer.h"

#include <boost/algorithm/string.hpp>
#include "TH2.h"

/*
taken from https://twiki.cern.ch/twiki/bin/view/Main/EGammaScaleFactors2012

This producer contains some un-intuitive programming constructs, which are
necessary to account for the different formats of the ROOT files containing
the scale factors (different axes, binning in absolute eta)

needed tags:
- LeptonSFVariation      Vary SF by error. Choices: up, down, None


maybe also relevant:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariateElectronIdentification (SF files for MVA
ID)
https://twiki.cern.ch/twiki/bin/view/CMSPublic/DiLeptonAnalysis#Efficiencies_and_Scale_Factors
https://twiki.cern.ch/twiki/bin/viewauth/CMS/DileptonTriggerResults
http://lovedeep.web.cern.ch/lovedeep/WORK13/TnPRun2012ReReco_2013Oct28/effiPlots.html
*/

std::string LeptonSFProducer::GetProducerId() const { return "LeptonSFProducer"; }

void LeptonSFProducer::Init(ZJetSettings const& settings)
{
    // this is only the path, add filename according to ID
    //m_sffile = "$EXCALIBURPATH/data/SF.root";
   m_sffile = settings.GetLeptonSFRootfile();
   if(settings.GetChannel() == "mm"){
   	m_id = settings.GetMuonID();
    }
   else if(settings.GetChannel() == "ee"){
    	m_id = settings.GetElectronID();
    }
    else{
       LOG(FATAL) << "No scale factors implemented for this Channel!";
    }
    std::string histoname;  // histoname depending on id
    double error_multiplier = 0.;
    if (settings.GetLeptonSFVariation() == "up") {
        LOG(WARNING) << "LeptonSFProducer: varying scale factor UP one sigma";
        error_multiplier = 1.;
    } else if (settings.GetLeptonSFVariation() == "down") {
        LOG(WARNING) << "LeptonSFProducer: varying scale factor DOWN one sigma";
        error_multiplier = -1.;
    }
    // pt/eta axes are different for mva/cutbased
    // cutbased id has binning in absolute eta

        histoname = ("histoSF");
        m_etabins = &m_ybins;
        m_ptbins = &m_xbins;
        m_reversed_axes = true;
        m_absoluteeta = true;
    // Get file
    LOG(INFO) << "Loading lepton scale factors for ID " << m_id << ": File " << m_sffile
              << ", Histogram " << histoname;
    TFile file(m_sffile.c_str(), "READONLY");
    TH2F* sfhisto = (TH2F*)file.Get(histoname.c_str());

    // Get the pT and eta bin borders
    for (int iy = 0; iy <= sfhisto->GetNbinsY(); ++iy)
        m_ybins.emplace_back(2 * sfhisto->GetYaxis()->GetBinCenter(iy) -
                             sfhisto->GetYaxis()->GetBinLowEdge(iy));
    for (int ix = 0; ix <= sfhisto->GetNbinsX(); ++ix)
        m_xbins.emplace_back(2 * sfhisto->GetXaxis()->GetBinCenter(ix) -
                             sfhisto->GetXaxis()->GetBinLowEdge(ix));

    // Fill the m_sf array with the values from the root histo
    for (int iy = 1; iy <= sfhisto->GetNbinsY(); iy++) {
        for (int ix = 1; ix <= sfhisto->GetNbinsX(); ix++) {
            m_sf[ix - 1][iy - 1] = static_cast<float>(
                sfhisto->GetBinContent(ix, iy) + error_multiplier * sfhisto->GetBinError(ix, iy));
        }
    }
    delete sfhisto;
    file.Close();
}

void LeptonSFProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
   	 product.m_weights["leptonSFWeight"] =
        	GetScaleFactor(*product.m_zLeptons.first) * GetScaleFactor(*product.m_zLeptons.second);
}

std::string LeptonTriggerSFProducer::GetProducerId() const { return "LeptonTriggerSFProducer"; }
void LeptonTriggerSFProducer::Init(ZJetSettings const& settings)
{
    // this is only the path, add filename according to ID
    //m_sffile = "$EXCALIBURPATH/data/SF.root";
   m_sffile = settings.GetLeptonTriggerSFRootfile();
   double error_multiplier = 0.;
   if (settings.GetLeptonTriggerSFVariation() == "up") {
        LOG(WARNING) << "LeptonSFProducer: varying scale factor UP one sigma";
        error_multiplier = 1.;
    } 
   else if (settings.GetLeptonTriggerSFVariation() == "down") {
        LOG(WARNING) << "LeptonSFProducer: varying scale factor DOWN one sigma";
        error_multiplier = -1.;
   }
   std::string histoname = ("histoSF");
   m_etabins = &m_ybins;
   m_ptbins = &m_xbins;
   m_reversed_axes = true;
   m_absoluteeta = true;

    // Get file
    LOG(INFO) << "Loading lepton scale factors for Trigger " << m_id << ": File " << m_sffile
              << ", Histogram " << histoname;
    TFile file(m_sffile.c_str(), "READONLY");
    TH2F* sfhisto = (TH2F*)file.Get(histoname.c_str());

    // Get the pT and eta bin borders
    for (int iy = 0; iy <= sfhisto->GetNbinsY(); ++iy)
        m_ybins.emplace_back(2 * sfhisto->GetYaxis()->GetBinCenter(iy) -
                             sfhisto->GetYaxis()->GetBinLowEdge(iy));
    for (int ix = 0; ix <= sfhisto->GetNbinsX(); ++ix)
        m_xbins.emplace_back(2 * sfhisto->GetXaxis()->GetBinCenter(ix) -
                             sfhisto->GetXaxis()->GetBinLowEdge(ix));

    // Fill the m_sf array with the values from the root histo
    for (int iy = 1; iy <= sfhisto->GetNbinsY(); iy++) {
        for (int ix = 1; ix <= sfhisto->GetNbinsX(); ix++) {
            m_sf[ix - 1][iy - 1] = static_cast<float>(
                sfhisto->GetBinContent(ix, iy) - error_multiplier * sfhisto->GetBinError(ix, iy));
        }
    }
    delete sfhisto;
    file.Close();
}
void LeptonTriggerSFProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    bool firstlepton = false;
    bool seclepton = false;
    for (std::map<KMuon*, KLV*>::const_iterator muon = product.m_triggerMatchedMuons.begin();
                 muon != product.m_triggerMatchedMuons.end(); ++muon) {
                    if (std::abs(product.m_zLeptons.first->p4.Pt() - muon->first->p4.Pt()) <= 0.001f)
			firstlepton = true; 
		    else if (std::abs(product.m_zLeptons.second->p4.Pt() - muon->first->p4.Pt()) <= 0.001f)
			seclepton = true; 
            }
    if(firstlepton == true&&seclepton == true){
   	product.m_weights["leptonTriggerSFWeight"] =
        	1/(1-(1-GetScaleFactor(*product.m_zLeptons.first)) * (1-GetScaleFactor(*product.m_zLeptons.second)));
    }
    else if(firstlepton == true&&seclepton == false){
   	product.m_weights["leptonTriggerSFWeight"] =
        	1/GetScaleFactor(*product.m_zLeptons.first);
    }
    else if(firstlepton == false&&seclepton == true){
	product.m_weights["leptonTriggerSFWeight"] =
        	1/GetScaleFactor(*product.m_zLeptons.second);
    }
    else{
	product.m_weights["leptonTriggerSFWeight"] = 0;
    }
}
