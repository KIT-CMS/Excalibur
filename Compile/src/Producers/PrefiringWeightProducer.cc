#include "Excalibur/Compile/interface/Producers/PrefiringWeightProducer.h"


#include <boost/algorithm/string.hpp>
#include "TH2.h"
#include <stdio.h>
#include "Kappa/DataFormats/interface/Kappa.h"

std::string PrefiringWeightProducer::GetProducerId() const { return "PrefiringWeightProducer"; }

void PrefiringWeightProducer::Init(ZJetSettings const& settings)
{
    const std::string prefiringJetWeightFilePath = settings.GetPrefiringJetWeightFilename();
    const std::string prefiringJetWeightHistName = settings.GetPrefiringJetWeightHistName();
    const std::string prefiringPhotonWeightFilePath = settings.GetPrefiringPhotonWeightFilename();
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
    if (!h_prefmap_photon)
    {
        LOG(ERROR) << "Histogram " << prefiringPhotonWeightHistName.c_str() << " not in file";
    }
    h_prefmap_photon->SetDirectory(0);
    prefiringPhotonWeightFile->Close();

}

double PrefiringWeightProducer::getPrefiringRate(double eta, double pt, TH2F* h_prefmap, fluctuations fluctuation) const
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
        for (unsigned int iph = 0; iph<product.m_pfPhotons.size(); ++iph)
        {
            KLV photon;
            photon.p4 = product.m_pfPhotons[iph]->p4;
            double pt_gam = photon.p4.Pt();
            double eta_gam = photon.p4.Eta();
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
        for (unsigned int iJet = 0; iJet < event.m_tjets->size();  ++iJet)
        {
            KLV jet;
            jet.p4 = event.m_tjets->at(iJet).p4;
            double pt_jet = jet.p4.Pt();
            double eta_jet = jet.p4.eta();
            if (pt_jet < 20.)
                continue;
            if (fabs(eta_jet) < 2.)
                continue;
            if (fabs(eta_jet) > 3.)
                continue;
            //Loop over photons to remove overlap
            double nonprefiringprobfromoverlappingphotons = 1.;
            for (unsigned int iph = 0; iph<product.m_pfPhotons.size(); ++iph)
            {
                KLV photon;
                photon.p4 = product.m_pfPhotons[iph]->p4;
                double pt_gam = photon.p4.Pt();
                double eta_gam = photon.p4.eta();
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
            double nonprefiringprobfromoverlappingjet = 1. - getPrefiringRate(eta_jet, pt_jet, h_prefmap_jet, fluct);
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
    product.m_optionalWeights["prefiringWeight"] =  1./nonPrefiringProba[0];
    product.m_optionalWeights["prefiringWeightUp"] =  1./nonPrefiringProba[1];
    product.m_optionalWeights["prefiringWeightDown"] =  1./nonPrefiringProba[2];
  
}

