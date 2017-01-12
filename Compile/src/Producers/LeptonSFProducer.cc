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
            m_sf[0][ix - 1][iy - 1] = static_cast<float>(
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
	if(product.m_zValid){
   	 	product.m_weights["leptonSFWeight"] =
        		GetScaleFactor(0, *product.m_zLeptons.first) * GetScaleFactor(0, *product.m_zLeptons.second);
	}
	else
		product.m_weights["leptonSFWeight"] = 0;
}

std::string LeptonTriggerSFProducer::GetProducerId() const { return "LeptonTriggerSFProducer"; }
void LeptonTriggerSFProducer::Init(ZJetSettings const& settings)
{
   m_sffile = settings.GetLeptonTriggerSFRootfile();
   TFile file(m_sffile.c_str(), "READONLY");
   double error_multiplier = 0.;
   if (settings.GetLeptonTriggerSFVariation() == "up") {
        LOG(WARNING) << "LeptonSFProducer: varying scale factor UP one sigma";
        error_multiplier = 1.;
    } 
   else if (settings.GetLeptonTriggerSFVariation() == "down") {
        LOG(WARNING) << "LeptonSFProducer: varying scale factor DOWN one sigma";
        error_multiplier = -1.;
   }
   m_etabins = &m_ybins;
   m_ptbins = &m_xbins;
   m_reversed_axes = true;
   m_absoluteeta = true;

    // Get file
    runs = settings.GetTriggerSFRuns();
    std::vector<TH2F*> sfhistos;
    int runcount = runs.size();
    if(runs.size()>0){
    	for (int i = 0; i < runcount; i++)
		sfhistos.push_back((TH2F*) file.Get(std::to_string(runs.at(i)).c_str()));
    }
    else{
	sfhistos.push_back((TH2F*) file.Get("histoSF"));
	runcount = 1;
    }
    // Get the pT and eta bin borders
    for (int iy = 0; iy <= sfhistos.at(0)->GetNbinsY(); ++iy)
        m_ybins.emplace_back(2 * sfhistos.at(0)->GetYaxis()->GetBinCenter(iy) -
                             sfhistos.at(0)->GetYaxis()->GetBinLowEdge(iy));
    for (int ix = 0; ix <= sfhistos.at(0)->GetNbinsX(); ++ix)
        m_xbins.emplace_back(2 * sfhistos.at(0)->GetXaxis()->GetBinCenter(ix) -
                             sfhistos.at(0)->GetXaxis()->GetBinLowEdge(ix));
    // Fill the m_sf array with the values from the root histo
    for (int i = 0; i < runcount; i++){
    	for (int iy = 1; iy <= sfhistos.at(0)->GetNbinsY(); iy++) {
        	for (int ix = 1; ix <= sfhistos.at(0)->GetNbinsX(); ix++) {
        	    m_sf[i][ix - 1][iy - 1] = static_cast<float>(
        	        sfhistos.at(i)->GetBinContent(ix, iy) - error_multiplier * sfhistos.at(i)->GetBinError(ix, iy));
		}
        }
    }
    file.Close();
}
void LeptonTriggerSFProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    bool foundrun = false;
    int run_index = 0;
    if (runs.empty())
	run_index = 0;
    else{
	for (unsigned int i = 0; i<runs.size(); ++i){
		if ((int) event.m_eventInfo->nRun < runs.at(i) && !foundrun){
			foundrun = true;
			run_index = i;
		}		
	}
	if (!foundrun){
		run_index = runs.size()-1;
		LOG(WARNING) << "No Trigger efficiencies for run " << event.m_eventInfo->nRun << " found, took efficiencies for up to run " << runs.back();
	}
    }
    if(product.m_zValid){
   	product.m_weights["leptonTriggerSFWeight"] =
        	1/(1-(1-GetScaleFactor(run_index, *product.m_zLeptons.first)) * (1-GetScaleFactor(run_index, *product.m_zLeptons.second)));
    }
    else
	product.m_weights["leptonTriggerSFWeight"] = 0;
}
