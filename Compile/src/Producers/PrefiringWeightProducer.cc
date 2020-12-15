#include "Excalibur/Compile/interface/Producers/PrefiringWeightProducer.h"


#include <boost/algorithm/string.hpp>
#include "TH2.h"
#include "TGraphAsymmErrors.h"
#include <stdio.h>


std::string PrefiringWeightProducer::GetProducerId() const { return "PrefiringWeightProducer"; }

void PrefiringWeightProducer::Init(ZJetSettings const& settings)
{
    const std::string prefiringJetWeightFilePath = settings.GetPrefiringJetWeightFile();
    const std::string prefiringJetWeightHistName = settings.GetPrefiringJetWeightHistName();
    const std::string prefiringPhotonWeightFilePath = settings.GetPrefiringPhotonWeightFile();
    const std::string prefiringPhotonWeightHistName = settings.GetPrefiringPhotonWeightHistName();

    // open file containing prefireing jet weight map
    TFile* prefiringJetWeightFile = new TFile(prefiringJetWeightFilePath.c_str(), "READ");
    LOG(INFO) << "Prefiring jet weight file: " << prefiringJetWeightFilePath;
    if(prefiringJetWeightFile->IsOpen())
    {
        LOG(DEBUG) << "Opened prefiring jet weight file successful";
    }
    else
    {
        LOG(ERROR) << "Could not open prefiring jet weight file!";    
    }
    // read in the weight maps
    h_prefmap_jet = (TH2F*) prefiringJetWeightFile->Get(prefiringJetWeightHistName.c_str());
    // detach ownership of object and close file
    h_prefmap_jet->SetDirectory(0);
    prefiringJetWeightFile->Close();


     // open file containing prefireing photon weight map
    TFile* prefiringPhotonWeightFile = new TFile(prefiringPhotonWeightFilePath.c_str(), "READ");
    LOG(INFO) << "Prefiring photo weight file: " << prefiringPhotonWeightFilePath;
    if(prefiringPhotonWeightFile->IsOpen())
    {
        LOG(DEBUG) << "Opened prefiring photon weight file successful";
    }
    else
    {
        LOG(ERROR) << "Could not open prefiring photon weight file!";    
    }
    // read in the weight maps
    h_prefmap_photon = (TH2F*) prefiringPhotonWeightFile->Get(prefiringPhotonWeightHistName.c_str());
    // detach ownership of object and close file
    h_prefmap_photon->SetDirectory(0);
    prefiringPhotonWeightFile->Close();
   

}

double PrefiringWeightProducer::getPrefiringRate(double eta,
                                                 double pt,
                                                 TH2F* h_prefmap,
                                                 fluctuations fluctuation) const
{
    if (h_prefmap == nullptr)
        LOG(ERROR) << "Prefiring map histogram not found";
    int nbinsy = h_prefmap->GetNbinsY();
    double maxy = h_prefmap->GetYaxis()->GetBinLowEdge(nbinsy + 1);
    if (pt >= maxy)
        pt = maxy - 0.01;
    int thebin = h_prefmap->FindBin(eta, pt);

    double prefrate = h_prefmap->GetBinContent(thebin);

    double statuncty = h_prefmap->GetBinError(thebin);
    double systuncty = prefiringRateSystUnc_ * prefrate;

    if (fluctuation == up)
        prefrate = std::min(1., prefrate + sqrt(pow(statuncty, 2) + pow(systuncty, 2)));
    if (fluctuation == down)
        prefrate = std::max(0., prefrate - sqrt(pow(statuncty, 2) + pow(systuncty, 2)));
    return prefrate;
}


void PrefiringWeightProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    double nonPrefiringProba[3] = {1., 1., 1.};  //0: central, 1: up, 2: down
    for (const auto fluct : {fluctuations::central, fluctuations::up, fluctuations::down}) {
        // applying the prefiring maps to photons in the affected regions.
        for (std::vector<KPhoton>::iterator photon = event.m_pfPhotons->begin(); photon != event.m_pfPhoton->end();
                 ++photon)
        {
            double pt_gam = photon.pt();
            double eta_gam = photon.eta();
            if (pt_gam < 20.)
                continue;
            if (fabs(eta_gam) < 2.)
                continue;
            if (fabs(eta_gam) > 3.)
                continue;
            double prefiringprob_gam = getPrefiringRate(eta_gam, pt_gam, h_prefmap_photon, fluct);
            nonPrefiringProba[fluct] *= (1. - prefiringprob_gam);
        }
        // applying the prefiring maps to jets in the affected regions.
        for (std::vector<TJet>::iterator jet = event.m_basicJets->begin();  jet != event.m_basicJets->end(); ++jet)
        {
            double pt_jet = jet.pt();
            double eta_jet = jet.eta();
            double phi_jet = jet.phi();
            if (pt_jet < 20.)
                continue;
            if (fabs(eta_jet) < 2.)
                continue;
            if (fabs(eta_jet) > 3.)
                continue;
            //Loop over photons to remove overlap
            double nonprefiringprobfromoverlappingphotons = 1.;
            for (const auto& photon : *thePhotons)
            {
                double pt_gam = photon.pt();
                double eta_gam = photon.eta();
                double phi_gam = photon.phi();
                if (pt_gam < 20.)
                    continue;
                if (fabs(eta_gam) < 2.)
                    continue;
                if (fabs(eta_gam) > 3.)
                    continue;
                double dR = ROOT::Math::VectorUtil::DeltaR(photon.p4, jet.p4);
                if (dR > 0.4)
                    continue;
                double prefiringprob_gam = getPrefiringRate(eta_gam, pt_gam, h_prefmap_photon, fluct);
                nonprefiringprobfromoverlappingphotons *= (1. - prefiringprob_gam);

            }
            if (nonprefiringprobfromoverlappingphotons == 1.)
            {
                nonPrefiringProba[fluct] *= nonprefiringprobfromoverlappingjet;
            }
            //If overlapping photons have a non prefiring rate larger than the jet, then replace these weights by the jet one
            else if (nonprefiringprobfromoverlappingphotons > nonprefiringprobfromoverlappingjet)
            {
                if (nonprefiringprobfromoverlappingphotons != 0.)
                {
                    nonPrefiringProba[fluct] *= nonprefiringprobfromoverlappingjet / nonprefiringprobfromoverlappingphotons;
                } else
                {
                    nonPrefiringProba[fluct] = 0.;
                }
            }
            //Last case: if overlapping photons have a non prefiring rate smaller than the jet, don't consider the jet in the event weight, and do nothing.
        }
    }
    product.m_weights["prefiringWeight"] =  1./nonPrefiringProba[0];
    product.m_weights["prefiringWeightUp"] =  1./nonPrefiringProba[1];
    product.m_weights["prefiringWeightDown"] =  1./nonPrefiringProba[2];
  
}

