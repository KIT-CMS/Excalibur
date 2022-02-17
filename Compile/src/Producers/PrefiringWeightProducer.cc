/********************************************************************
 * Based on                                                         *
 * cmssw/PhysicsTools/PatUtils/plugins/L1PrefiringWeightProducer.cc *
 * with small modifications to match our setup                      *
 ********************************************************************/

#include "Excalibur/Compile/interface/Producers/PrefiringWeightProducer.h"

#include "Kappa/DataFormats/interface/Kappa.h"

#include "TFile.h"
#include "TF1.h"
#include "TH2.h"

std::string PrefiringWeightProducer::GetProducerId() const { return "PrefiringWeightProducer"; }

void PrefiringWeightProducer::Init(ZJetSettings const& settings)
{
    const std::string dataeraEcal_ = settings.GetDataEraECAL();
    const std::string dataeraMuon_ = settings.GetDataEraMuon();
    const bool useEMpt_ = settings.GetUseJetEMPt();
    const double prefiringRateSystUncEcal_ = settings.GetPrefiringRateSystematicUnctyECAL();
    const double prefiringRateSystUncMuon_ = settings.GetPrefiringRateSystematicUnctyMuon();
    const double jetMaxMuonFraction_ = settings.GetJetMaxMuonFraction();

    missingInputEcal_ = false;
    missingInputMuon_ = false;

    const std::string prefiringL1MapsPath = settings.GetPrefiringL1MapsPath();
    file_prefiringmaps_ = std::make_unique<TFile>(prefiringL1MapsPath.c_str(), "read");
    if (file_prefiringmaps_ == nullptr) {
        missingInputEcal_ = true;
        // The Error message in CMSSw says 0, but this is false.
        // Default declaration in the produce method is 1.
        LOG(ERROR) << this->GetProducerId() << ": "
            << "File with maps not found. All prefiring weights set to 1.";
    }
    TString mapphotonfullname = "L1prefiring_photonptvseta_" + dataeraEcal_;
    if (!file_prefiringmaps_->Get(mapphotonfullname)) {
        missingInputEcal_ = true;
        // The Error message in CMSSw says 0, but this is false.
        // Default declaration in the produce method is 1.
        LOG(ERROR) << this->GetProducerId() << ": "
            << "Photon map not found. All photons prefiring weights set to 1.";
    }
    h_prefmap_photon_ = (TH2F*) file_prefiringmaps_->Get(mapphotonfullname);
    h_prefmap_photon_->SetDirectory(0); // Necessary to avoid segfaults after closing the file
    TString mapjetfullname =
        (useEMpt_) ? "L1prefiring_jetemptvseta_" + dataeraEcal_ : "L1prefiring_jetptvseta_" + dataeraEcal_;
    if (!file_prefiringmaps_->Get(mapjetfullname)) {
        missingInputEcal_ = true;
        // The Error message in CMSSw says 0, but this is false.
        // Default declaration in the produce method is 1.
        LOG(ERROR) << this->GetProducerId() << ": " << "Jet map not found. All jets prefiring weights set to 1.";
    }
    h_prefmap_jet_ = (TH2F*) file_prefiringmaps_->Get(mapjetfullname);
    h_prefmap_jet_->SetDirectory(0); // Necessary to avoid segfaults after closing the file
    file_prefiringmaps_->Close();

    std::string fnameMuon = settings.GetL1MuonParametrizationsPath();
    file_prefiringparams_ = std::make_unique<TFile>(fnameMuon.c_str(), "read");
    if (file_prefiringparams_ == nullptr) {
        missingInputMuon_ = true;
        // The Error message in CMSSw says 0, but this is false.
        // Default declaration in the produce method is 1.
        LOG(ERROR) << this->GetProducerId() << ": "
            << "File with muon parametrizations not found. All prefiring weights set to 1.";
    }
    TString paramName = "L1prefiring_muonparam_0.0To0.2_" + dataeraMuon_;
    parametrization0p0To0p2_ = (TF1*) file_prefiringparams_->Get(paramName);
    paramName = "L1prefiring_muonparam_0.2To0.3_" + dataeraMuon_;
    parametrization0p2To0p3_ = (TF1*) file_prefiringparams_->Get(paramName);
    paramName = "L1prefiring_muonparam_0.3To0.55_" + dataeraMuon_;
    parametrization0p3To0p55_ = (TF1*) file_prefiringparams_->Get(paramName);
    paramName = "L1prefiring_muonparam_0.55To0.83_" + dataeraMuon_;
    parametrization0p55To0p83_ = (TF1*) file_prefiringparams_->Get(paramName);
    paramName = "L1prefiring_muonparam_0.83To1.24_" + dataeraMuon_;
    parametrization0p83To1p24_ = (TF1*) file_prefiringparams_->Get(paramName);
    paramName = "L1prefiring_muonparam_1.24To1.4_" + dataeraMuon_;
    parametrization1p24To1p4_ = (TF1*) file_prefiringparams_->Get(paramName);
    paramName = "L1prefiring_muonparam_1.4To1.6_" + dataeraMuon_;
    parametrization1p4To1p6_ = (TF1*) file_prefiringparams_->Get(paramName);
    paramName = "L1prefiring_muonparam_1.6To1.8_" + dataeraMuon_;
    parametrization1p6To1p8_ = (TF1*) file_prefiringparams_->Get(paramName);
    paramName = "L1prefiring_muonparam_1.8To2.1_" + dataeraMuon_;
    parametrization1p8To2p1_ = (TF1*) file_prefiringparams_->Get(paramName);
    paramName = "L1prefiring_muonparam_2.1To2.25_" + dataeraMuon_;
    parametrization2p1To2p25_ = (TF1*) file_prefiringparams_->Get(paramName);
    paramName = "L1prefiring_muonparam_2.25To2.4_" + dataeraMuon_;
    parametrization2p25To2p4_ = (TF1*) file_prefiringparams_->Get(paramName);

    if (parametrization0p0To0p2_ == nullptr || parametrization0p2To0p3_ == nullptr ||
        parametrization0p3To0p55_ == nullptr || parametrization0p55To0p83_ == nullptr ||
        parametrization0p83To1p24_ == nullptr || parametrization1p24To1p4_ == nullptr ||
        parametrization1p4To1p6_ == nullptr || parametrization1p6To1p8_ == nullptr ||
        parametrization1p8To2p1_ == nullptr || parametrization2p1To2p25_ == nullptr ||
        parametrization2p25To2p4_ == nullptr) {
        missingInputMuon_ = true;
        // The Error message in CMSSw says 0, but this is false.
        // Default declaration in the produce method is 1.
        LOG(ERROR) << this->GetProducerId() << ": "
            << "Muon parametrization not found for at least one bin. All prefiring weights set to 1.";
    }

    paramName = "L1prefiring_muonparam_HotSpot_" + dataeraMuon_;
    parametrizationHotSpot_ = (TF1*) file_prefiringparams_->Get(paramName);
    file_prefiringparams_->Close();
    if ((dataeraMuon_.find("2016") != std::string::npos) && parametrizationHotSpot_ == nullptr) {
        missingInputMuon_ = true;
        // The Error message in CMSSw says 0, but this is false.
        // Default declaration in the produce method is 1.
        LOG(ERROR) << this->GetProducerId() << ": "
            << "Year is 2016 and no Muon parametrization is found for hot spot. All prefiring weights set to 1.";
    }

}

void PrefiringWeightProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    //Photons
    const auto& thePhotons = product.m_pfPhotons;

    //Jets
    const auto& theJets = product.m_correctedZJets["L1L2L3Res"];

    //Muons
    const auto& theMuons = event.m_muons;

    //Probability for the event NOT to prefire, computed with the prefiring maps per object.
    //Up and down values correspond to the resulting value when shifting up/down all prefiring rates in prefiring maps.
    double nonPrefiringProba[3] = {1., 1., 1.};      //0: central, 1: up, 2: down
    double nonPrefiringProbaECAL[3] = {1., 1., 1.};  //0: central, 1: up, 2: down
    double nonPrefiringProbaMuon[7] = {
        1., 1., 1., 1., 1., 1., 1.};  //0: central, 1: up, 2: down, 3: up stat, 4: down stat, 5: up syst, 6: down syst

    for (const auto fluct : {fluctuations::central, fluctuations::up, fluctuations::down}) {
        if (!missingInputEcal_) {
            for (const auto& photon : thePhotons) {
                double pt_gam = photon->p4.Pt();
                double eta_gam = photon->p4.Eta();
                if (pt_gam < 20.)
                    continue;
                if (fabs(eta_gam) < 2.)
                    continue;
                if (fabs(eta_gam) > 3.)
                    continue;
                double prefiringprob_gam = getPrefiringRateEcal(eta_gam, pt_gam, h_prefmap_photon_, fluct);
                nonPrefiringProbaECAL[fluct] *= (1. - prefiringprob_gam);
            }

            //Now applying the prefiring maps to jets in the affected regions.
            for (const auto& jet : theJets) {
                double pt_jet = jet->p4.Pt();
                double eta_jet = jet->p4.Eta();
                double phi_jet = jet->p4.Phi();
                if (pt_jet < 20.)
                    continue;
                if (fabs(eta_jet) < 2.)
                    continue;
                if (fabs(eta_jet) > 3.)
                    continue;
                if (jetMaxMuonFraction_ > 0 && jet->muonFraction > jetMaxMuonFraction_)
                    continue;
                //Loop over photons to remove overlap
                double nonprefiringprobfromoverlappingphotons = 1.;
                bool foundOverlappingPhotons = false;
                for (const auto& photon : thePhotons) {
                    double pt_gam = photon->p4.Pt();
                    double eta_gam = photon->p4.Eta();
                    double phi_gam = photon->p4.Phi();
                    if (pt_gam < 20.)
                        continue;
                    if (fabs(eta_gam) < 2.)
                        continue;
                    if (fabs(eta_gam) > 3.)
                        continue;
                    double dR2 = ROOT::Math::VectorUtil::DeltaR2(jet->p4, photon->p4);
                    if (dR2 > 0.16)
                        continue;
                    double prefiringprob_gam = getPrefiringRateEcal(eta_gam, pt_gam, h_prefmap_photon_, fluct);
                    nonprefiringprobfromoverlappingphotons *= (1. - prefiringprob_gam);
                    foundOverlappingPhotons = true;
                }
                //useEMpt =true if one wants to use maps parametrized vs Jet EM pt instead of pt.
                if (useEMpt_)
                    pt_jet *= (jet->neutralHadronFraction + jet->chargedHadronFraction);
                double nonprefiringprobfromoverlappingjet = 1. - getPrefiringRateEcal(eta_jet, pt_jet, h_prefmap_jet_, fluct);

                if (!foundOverlappingPhotons) {
                    nonPrefiringProbaECAL[fluct] *= nonprefiringprobfromoverlappingjet;
                }
                //If overlapping photons have a non prefiring rate larger than the jet, then replace these weights by the jet one
                else if (nonprefiringprobfromoverlappingphotons > nonprefiringprobfromoverlappingjet) {
                    if (nonprefiringprobfromoverlappingphotons > 0.) {
                        nonPrefiringProbaECAL[fluct] *= nonprefiringprobfromoverlappingjet / nonprefiringprobfromoverlappingphotons;
                    } else {
                        nonPrefiringProbaECAL[fluct] = 0.;
                    }
                }
                //Last case: if overlapping photons have a non prefiring rate smaller than the jet, don't consider the jet in the event weight, and do nothing.
            }
        }
        //Now calculate prefiring weights for muons
        if (!missingInputMuon_) {
            for (KMuons::iterator muon = theMuons->begin(); muon != theMuons->end(); ++muon) {
                double pt = muon->p4.Pt();
                double phi = muon->p4.Phi();
                double eta = muon->p4.Eta();
                // Remove crappy tracker muons which would not have prefired the L1 trigger
                if (pt < 5 || !muon->idLoose())
                    continue;
                double prefiringprob_mu = getPrefiringRateMuon(eta, phi, pt, fluct);
                nonPrefiringProbaMuon[fluct] *= (1. - prefiringprob_mu);
            }
        }
    }
    // Calculate combined weight as product of the weight for individual objects
    for (const auto fluct : {fluctuations::central, fluctuations::up, fluctuations::down}) {
        nonPrefiringProba[fluct] = nonPrefiringProbaECAL[fluct] * nonPrefiringProbaMuon[fluct];
    }
    // Calculate statistical and systematic uncertainty separately in the muon case
    for (const auto fluct :
         {fluctuations::upSyst, fluctuations::downSyst, fluctuations::upStat, fluctuations::downStat}) {
        if (!missingInputMuon_) {
            for (KMuons::iterator muon = theMuons->begin(); muon != theMuons->end(); ++muon) {
                double pt = muon->p4.Pt();
                double phi = muon->p4.Phi();
                double eta = muon->p4.Eta();
                // Remove crappy tracker muons which would not have prefired the L1 trigger
                if (pt < 5 || !muon->idLoose())
                    continue;
                double prefiringprob_mu = getPrefiringRateMuon(eta, phi, pt, fluct);
                nonPrefiringProbaMuon[fluct] *= (1. - prefiringprob_mu);
            }
        }
    }
    //Move global prefire weights, as well as those for muons, photons, and jets, to the event
    //Up and Down are switched, since we use the inverse and apply it to data.
    product.m_optionalWeights["prefiringWeight"] =  1./nonPrefiringProba[0];
    product.m_optionalWeights["prefiringWeightUp"] =  1./nonPrefiringProba[2];
    product.m_optionalWeights["prefiringWeightDown"] =  1./nonPrefiringProba[1];

    product.m_optionalWeights["prefiringWeightECAL"] =  1./nonPrefiringProbaECAL[0];
    product.m_optionalWeights["prefiringWeightECALUp"] =  1./nonPrefiringProbaECAL[2];
    product.m_optionalWeights["prefiringWeightECALDown"] =  1./nonPrefiringProbaECAL[1];

    product.m_optionalWeights["prefiringWeightMuon"] =  1./nonPrefiringProbaMuon[0];
    product.m_optionalWeights["prefiringWeightMuonUp"] =  1./nonPrefiringProbaMuon[2];
    product.m_optionalWeights["prefiringWeightMuonDown"] =  1./nonPrefiringProbaMuon[1];
    product.m_optionalWeights["prefiringWeightMuonUpStat"] =  1./nonPrefiringProbaMuon[4];
    product.m_optionalWeights["prefiringWeightMuonDownStat"] =  1./nonPrefiringProbaMuon[3];
    product.m_optionalWeights["prefiringWeightMuonUpSyst"] =  1./nonPrefiringProbaMuon[6];
    product.m_optionalWeights["prefiringWeightMuonDownSyst"] =  1./nonPrefiringProbaMuon[5];
}

double PrefiringWeightProducer::getPrefiringRateEcal(double eta,
                                                     double pt,
                                                     TH2F* h_prefmap,
                                                     fluctuations fluctuation) const {
    //Check pt is not above map overflow
    int nbinsy = h_prefmap->GetNbinsY();
    double maxy = h_prefmap->GetYaxis()->GetBinLowEdge(nbinsy + 1);
    if (pt >= maxy)
        pt = maxy - 0.01;
    int thebin = h_prefmap->FindBin(eta, pt);

    double prefrate = h_prefmap->GetBinContent(thebin);

    double statuncty = h_prefmap->GetBinError(thebin);
    double systuncty = prefiringRateSystUncEcal_ * prefrate;

    if (fluctuation == up)
        prefrate = std::min(1., prefrate + sqrt(pow(statuncty, 2) + pow(systuncty, 2)));
    else if (fluctuation == down)
        prefrate = std::max(0., prefrate - sqrt(pow(statuncty, 2) + pow(systuncty, 2)));
    if (prefrate > 1.) {
        LOG(WARNING) << this->GetProducerId() << ": " << "Found a prefiring probability > 1. Setting to 1.";
        return 1.;
    }
    return prefrate;
}

double PrefiringWeightProducer::getPrefiringRateMuon(double eta,
                                                     double phi,
                                                     double pt,
                                                     fluctuations fluctuation) const {
    double prefrate;
    double statuncty;
    if ((dataeraMuon_.find("2016") != std::string::npos) && (eta > 1.24 && eta < 1.6) &&
        (phi > 2.44346 && phi < 2.79253)) {
        prefrate = parametrizationHotSpot_->Eval(pt);
        statuncty = parametrizationHotSpot_->GetParError(2);
    } else if (std::abs(eta) < 0.2) {
        prefrate = parametrization0p0To0p2_->Eval(pt);
        statuncty = parametrization0p0To0p2_->GetParError(2);
    } else if (std::abs(eta) < 0.3) {
        prefrate = parametrization0p2To0p3_->Eval(pt);
        statuncty = parametrization0p2To0p3_->GetParError(2);
    } else if (std::abs(eta) < 0.55) {
        prefrate = parametrization0p3To0p55_->Eval(pt);
        statuncty = parametrization0p3To0p55_->GetParError(2);
    } else if (std::abs(eta) < 0.83) {
        prefrate = parametrization0p55To0p83_->Eval(pt);
        statuncty = parametrization0p55To0p83_->GetParError(2);
    } else if (std::abs(eta) < 1.24) {
        prefrate = parametrization0p83To1p24_->Eval(pt);
        statuncty = parametrization0p83To1p24_->GetParError(2);
    } else if (std::abs(eta) < 1.4) {
        prefrate = parametrization1p24To1p4_->Eval(pt);
        statuncty = parametrization1p24To1p4_->GetParError(2);
    } else if (std::abs(eta) < 1.6) {
        prefrate = parametrization1p4To1p6_->Eval(pt);
        statuncty = parametrization1p4To1p6_->GetParError(2);
    } else if (std::abs(eta) < 1.8) {
        prefrate = parametrization1p6To1p8_->Eval(pt);
        statuncty = parametrization1p6To1p8_->GetParError(2);
    } else if (std::abs(eta) < 2.1) {
        prefrate = parametrization1p8To2p1_->Eval(pt);
        statuncty = parametrization1p8To2p1_->GetParError(2);
    } else if (std::abs(eta) < 2.25) {
        prefrate = parametrization2p1To2p25_->Eval(pt);
        statuncty = parametrization2p1To2p25_->GetParError(2);
    } else if (std::abs(eta) < 2.4) {
        prefrate = parametrization2p25To2p4_->Eval(pt);
        statuncty = parametrization2p25To2p4_->GetParError(2);
    } else {
        LOG(DEBUG) << this->GetProducerId() << ": " << "Muon outside of |eta| <= 2.4. Prefiring probability set to 0.";
        return 0.;
    }
    double systuncty = prefiringRateSystUncMuon_ * prefrate;

    if (fluctuation == up)
        prefrate = std::min(1., prefrate + sqrt(pow(statuncty, 2) + pow(systuncty, 2)));
    else if (fluctuation == down)
        prefrate = std::max(0., prefrate - sqrt(pow(statuncty, 2) + pow(systuncty, 2)));
    else if (fluctuation == upSyst)
        prefrate = std::min(1., prefrate + systuncty);
    else if (fluctuation == downSyst)
        prefrate = std::max(0., prefrate - systuncty);
    else if (fluctuation == upStat)
        prefrate = std::min(1., prefrate + statuncty);
    else if (fluctuation == downStat)
        prefrate = std::max(0., prefrate - statuncty);

    if (prefrate > 1.) {
        LOG(WARNING) << this->GetProducerId() << ": " << "Found a prefiring probability > 1. Setting to 1.";
        return 1.;
    }
    return prefrate;
}
