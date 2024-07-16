#include "Excalibur/Compile/interface/Consumers/ZJetTreeConsumer.h"
#include "Artus/KappaAnalysis/interface/Producers/ValidElectronsProducer.h"
#include "Artus/KappaAnalysis/interface/Producers/ValidJetsProducer.h"

std::string ZJetTreeConsumer::GetConsumerId() const { return "ZJetTreeConsumer"; }

inline int kleptonflavour_to_pdgid(const int& kappa_lepton_flavour)
{
    // translates KLeptonFlavour::Type enum to PDG IDs
    switch (kappa_lepton_flavour) {
        case 1:
            return DefaultValues::pdgIdElectron;
        case 2:
            return DefaultValues::pdgIdMuon;
        case 3:
            return DefaultValues::pdgIdTau;
        default:
            return DefaultValues::UndefinedInt;
    }
}

void ZJetTreeConsumer::Init(ZJetSettings const& settings)
{
    // Add possible quantities for the lambda ntuples consumers

    ////////////////////////
    // General quantities //
    ////////////////////////
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "npu", [](ZJetEvent const& event, ZJetProduct const& product) {
            return event.m_genEventInfo->nPU;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "npumean", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            if (settings.GetInputIsData()) {
                return product.npumean_data;
            } else {
                return event.m_genEventInfo->nPUMean;
            }
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "hlt", [](ZJetEvent const& event, ZJetProduct const& product) {
            return (!product.m_selectedHltNames.empty());  // check whether any HLT has fired
        });

    ///////
    // Z //
    ///////

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zpt",
        [](ZJetEvent const& event, ZJetProduct const& product) { return (product.m_zValid ? product.m_z.p4.Pt(): DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zeta",
        [](ZJetEvent const& event, ZJetProduct const& product) { return (product.m_zValid ? product.m_z.p4.Eta(): DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zphi",
        [](ZJetEvent const& event, ZJetProduct const& product) { return (product.m_zValid ? product.m_z.p4.Phi(): DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zeta",
        [](ZJetEvent const& event, ZJetProduct const& product) { return (product.m_zValid ? product.m_z.p4.Eta(): DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zy", [](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_zValid ? product.m_z.p4.Rapidity(): DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zmass",
        [](ZJetEvent const& event, ZJetProduct const& product) { return (product.m_zValid ? product.m_z.p4.mass(): DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "ystar", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_zValid && (product.GetValidJetCount(settings, event) > 0) 
                ? std::abs(product.m_z.p4.Rapidity() - product.GetValidPrimaryJet(settings, event)->p4.Rapidity())/2
                : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "yboost", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_zValid && (product.GetValidJetCount(settings, event) > 0) 
                ? std::abs(product.m_z.p4.Rapidity() + product.GetValidPrimaryJet(settings, event)->p4.Rapidity())/2
                : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "backtoback", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_zValid && (product.GetValidJetCount(settings, event) > 0)
                ? std::abs(std::abs(product.m_z.p4.Phi() - product.GetValidPrimaryJet(settings, event)->p4.Phi()))// - std::atan(1)*4)
                : DefaultValues::UndefinedFloat);
        });

    // True Z: from hard process
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truezpt",
        [](ZJetEvent const& event, ZJetProduct const& product) {
            return(product.GetTrueZ(event)!=nullptr ? product.GetTrueZ(event)->p4.Pt() : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truezeta",
        [](ZJetEvent const& event, ZJetProduct const& product) {
            return(product.GetTrueZ(event)!=nullptr ? product.GetTrueZ(event)->p4.Eta() : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truezphi",
        [](ZJetEvent const& event, ZJetProduct const& product) {
            return(product.GetTrueZ(event)!=nullptr ? product.GetTrueZ(event)->p4.Phi() : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truezy", [](ZJetEvent const& event, ZJetProduct const& product) {
            return(product.GetTrueZ(event)!=nullptr ? product.GetTrueZ(event)->p4.Rapidity() : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truezmass", [](ZJetEvent const& event, ZJetProduct const& product) {
            return(product.GetTrueZ(event)!=nullptr ? product.GetTrueZ(event)->p4.mass() : DefaultValues::UndefinedFloat);
        });
    // Gen Z
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genzpt",
        [](ZJetEvent const& event, ZJetProduct const& product) { 
            return(product.m_genBosonLVFound ? product.m_genBosonLV.Pt() : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genzeta",
        [](ZJetEvent const& event, ZJetProduct const& product) { 
            return(product.m_genBosonLVFound ? product.m_genBosonLV.Eta() : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genzphi",
        [](ZJetEvent const& event, ZJetProduct const& product) { 
            return(product.m_genBosonLVFound ? product.m_genBosonLV.Phi() : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genzy", [](ZJetEvent const& event, ZJetProduct const& product) {
            return(product.m_genBosonLVFound ? product.m_genBosonLV.Rapidity() : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genzmass",
        [](ZJetEvent const& event, ZJetProduct const& product) {
        return(product.m_genBosonLVFound ? product.m_genBosonLV.mass() : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genystar", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genBosonLVFound && (product.m_simpleGenJets.size() > 0)
                ? std::abs(product.m_genBosonLV.Rapidity() - product.m_simpleGenJets.at(0)->p4.Rapidity())/2
                : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genyboost", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genBosonLVFound && (product.m_simpleGenJets.size() > 0)
                ? std::abs(product.m_genBosonLV.Rapidity() + product.m_simpleGenJets.at(0)->p4.Rapidity())/2
                : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "deltarzgenz", [](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genBosonLVFound ? ROOT::Math::VectorUtil::DeltaR(product.m_genBosonLV, product.m_z.p4)
                                        : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genbacktoback", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genBosonLVFound && (product.m_simpleGenJets.size() > 0)
                ? std::abs(std::abs(product.m_genBosonLV.Phi() + product.m_simpleGenJets.at(0)->p4.Phi()))// - std::atan(1)*4)
                : DefaultValues::UndefinedFloat);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenystar", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KLV* genJet = product.GetMatchedGenJet(event, settings, 0);
            return (product.m_genBosonLVFound && genJet != nullptr)
                ? std::abs(product.m_genBosonLV.Rapidity() - genJet->p4.Rapidity())/2
                : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenyboost", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KLV* genJet = product.GetMatchedGenJet(event, settings, 0);
            return (product.m_genBosonLVFound && genJet != nullptr)
                ? std::abs(product.m_genBosonLV.Rapidity() + genJet->p4.Rapidity())/2
                : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenbacktoback", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KLV* genJet = product.GetMatchedGenJet(event, settings, 0);
            return (product.m_genBosonLVFound && genJet != nullptr)
                ? std::abs(std::abs(product.m_genBosonLV.Phi() - genJet->p4.Phi()))// - std::atan(1)*4)
                : DefaultValues::UndefinedFloat;
        });
    ////////////////
    // Phistareta //
    ////////////////

    LambdaNtupleConsumer<ZJetTypes>::AddDoubleQuantity(
       "genphistareta", [](ZJetEvent const& event, ZJetProduct const& product) {
            if (!product.m_genBosonLVFound)
                return DefaultValues::UndefinedDouble;
            return product.GetGenPhiStarEta(event);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddDoubleQuantity(
       "truephistareta", [](ZJetEvent const& event, ZJetProduct const& product) {
            if (product.GetTrueZ(event)!=nullptr)
                return product.GetTruePhiStarEta(event);
            return DefaultValues::UndefinedDouble;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddDoubleQuantity(
        "phistareta", [](ZJetEvent const& event, ZJetProduct const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedDouble;
            return product.GetPhiStarEta(event);
        });

    //////////
    // Jets //
    //////////

    // Leading jet
    // basic quantities
    
    
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jetHT", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetHT(settings, event);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? product.GetValidPrimaryJet(settings, event)->p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1eta", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? product.GetValidPrimaryJet(settings, event)->p4.Eta()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? product.GetValidPrimaryJet(settings, event)->p4.Rapidity()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? product.GetValidPrimaryJet(settings, event)->p4.Phi()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1area", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->area
                       : DefaultValues::UndefinedFloat;
        });

    // leading jet flavor (only filled in MC)
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1flavor", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->flavour
                       : DefaultValues::UndefinedFloat;
        });

    // Jet IDs
    KappaEnumTypes::JetIDVersion jetIDVersionEnumType = KappaEnumTypes::ToJetIDVersion(settings.GetJetIDVersion());
    for (const std::string& idName : {"loose", "tight", "tightlepveto"}) {
        KappaEnumTypes::JetID jetIDEnumType = KappaEnumTypes::ToJetID(idName);
        for (unsigned int iJet = 0; iJet < 3; ++iJet) {
            const std::string branchName = "jet" + std::to_string(iJet + 1) + "id" + idName;
            LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
                branchName, [iJet, jetIDVersionEnumType, jetIDEnumType, settings](event_type const& event, product_type const& product) {
                    return (product.GetValidJetCount(settings, event) > iJet)
                               ? ValidJetsProducer::passesJetID(dynamic_cast<KBasicJet*>(product.GetValidJet(settings, event, iJet)),
                                                                jetIDVersionEnumType,
                                                                jetIDEnumType,
                                                                settings)
                               : DefaultValues::UndefinedFloat;
               });
        }
    }

    // PF fractions
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1pf", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->photonFraction
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1ef", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->electronFraction
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1chf", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->chargedHadronFraction
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1nhf", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->neutralHadronFraction
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1mf", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->muonFraction
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1hfhf", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->hfHadronFraction
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1hfemf", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->hfEMFraction
                       : DefaultValues::UndefinedFloat;
        });
    // taggers
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1btag", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->getTag("CombinedSecondaryVertexBJetTags", event.m_jetMetadata)
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1qgtag", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->getTag("QGlikelihood", event.m_jetMetadata)
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1puidraw", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->getTag(settings.GetPUJetIDModuleName()+"fullDiscriminant", event.m_jetMetadata)
                       : DefaultValues::UndefinedFloat;
        });
    
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1puidtight", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? bool(int(static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->getTag(settings.GetPUJetIDModuleName()+"fullId", event.m_jetMetadata)) & (1 << 0))
                             //->getId("puJetIDFullTight", event.m_jetMetadata)
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1puidmedium", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? bool(int(static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->getTag(settings.GetPUJetIDModuleName()+"fullId", event.m_jetMetadata)) & (1 << 1))
                             //->getId("puJetIDFullMedium", event.m_jetMetadata)
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1puidloose", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? bool(int(static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->getTag(settings.GetPUJetIDModuleName()+"fullId", event.m_jetMetadata)) & (1 << 2))
                             //->getId("puJetIDFullLoose", event.m_jetMetadata)
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1btag", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))
                             ->getTag("pfCombinedInclusiveSecondaryVertexV2BJetTags", event.m_jetMetadata)
                       : DefaultValues::UndefinedFloat;
        });
    // correction factors
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1l1", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? (product.jetpt_l1 /
                          product.GetValidJet(settings, event, 0, "None")->p4.Pt())
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1rc", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? (product.jetpt_rc /
                          product.GetValidJet(settings, event, 0, "None")->p4.Pt())
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1l2", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? (product.jetpt_l1l2l3 / product.jetpt_l1)
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1res", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? (product.jetpt_l1l2l3res / product.jetpt_l1l2l3)
                       : DefaultValues::UndefinedFloat;
        });

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1ptraw", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0)
                       ? product.GetValidJet(settings, event, 0, "None")->p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1ptl1", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0) ? product.jetpt_l1
                                                                   : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet1ptl1l2l3", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 0) ? product.jetpt_l1l2l3res
                                                                   : DefaultValues::UndefinedFloat;
        });

    // Second leading jet
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet2pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 1)
                       ? product.GetValidJet(settings, event, 1)->p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet2phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 1)
                       ? product.GetValidJet(settings, event, 1)->p4.Phi()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet2eta", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 1)
                       ? product.GetValidJet(settings, event, 1)->p4.Eta()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet2y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 1)
                       ? product.GetValidJet(settings, event, 1)->p4.Rapidity()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet2puidraw", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 1)
                       ? static_cast<KJet*>(product.GetValidJet(settings, event, 1))
                             ->getTag(settings.GetPUJetIDModuleName()+"fullDiscriminant", event.m_jetMetadata)
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet2puidtight", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 1)
                       ? bool(int(static_cast<KJet*>(product.GetValidJet(settings, event, 1))
                             ->getTag(settings.GetPUJetIDModuleName()+"fullId", event.m_jetMetadata)) & (1 << 0))
                             //->getId("puJetIDFullTight", event.m_jetMetadata)
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet2puidmedium", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 1)
                       ? bool(int(static_cast<KJet*>(product.GetValidJet(settings, event, 1))
                             ->getTag(settings.GetPUJetIDModuleName()+"fullId", event.m_jetMetadata)) & (1 << 1))
                             //->getId("puJetIDFullMedium", event.m_jetMetadata)
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jet2puidloose", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetValidJetCount(settings, event) > 1)
                       ? bool(int(static_cast<KJet*>(product.GetValidJet(settings, event, 1))
                             ->getTag(settings.GetPUJetIDModuleName()+"fullId", event.m_jetMetadata)) & (1 << 2))
                             //->getId("puJetIDFullLoose", event.m_jetMetadata)
                       : DefaultValues::UndefinedFloat;
        });
    // add additional Jets: (default: jet3)
    for (unsigned i = 2; i < 3; ++i) {
        LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
            "jet"+ std::to_string(i+1) +"pt", [i, settings](ZJetEvent const& event, ZJetProduct const& product) {
                return (product.GetValidJetCount(settings, event) > i)
                        ? product.GetValidJet(settings, event, i)->p4.Pt()
                        : DefaultValues::UndefinedFloat;
            });
        LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
             "jet"+ std::to_string(i+1) +"phi", [i, settings](ZJetEvent const& event, ZJetProduct const& product) {
                return (product.GetValidJetCount(settings, event) > i)
                       ? product.GetValidJet(settings, event, i)->p4.Phi()
                       : DefaultValues::UndefinedFloat;
            });
        LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
            "jet"+ std::to_string(i+1) + "eta", [i, settings](ZJetEvent const& event, ZJetProduct const& product) {
                return (product.GetValidJetCount(settings, event) > i)
                       ? product.GetValidJet(settings, event, i)->p4.Eta()
                       : DefaultValues::UndefinedFloat;
            });
        LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
            "jet"+ std::to_string(i+1) + "y", [i, settings](ZJetEvent const& event, ZJetProduct const& product) {
                return (product.GetValidJetCount(settings, event) > i)
                       ? product.GetValidJet(settings, event, i)->p4.Rapidity()
                       : DefaultValues::UndefinedFloat;
            });
        }
    // General jet stuff
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "njets", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetValidJetCount(settings, event);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "njetsinv", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetInvalidJetCount(settings, event);
        });

    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "njets10", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.CountValidJetsAbovePt(settings, event, 10.0);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "njets20", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.CountValidJetsAbovePt(settings, event, 20.0);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "njets30", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.CountValidJetsAbovePt(settings, event, 30.0);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "lheNOutPartons", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return event.m_genEventInfo->lheNOutPartons;
        });

    // Jet recoil
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jetrecoilpt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            const KLV* jetRecoil = product.GetJetRecoil(settings, event);
            return jetRecoil ? product.GetJetRecoil(settings, event)->p4.Pt()
                             : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jetrecoilphi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            const KLV* jetRecoil = product.GetJetRecoil(settings, event);
            return jetRecoil ? product.GetJetRecoil(settings, event)->p4.Phi()
                             : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jetrecoileta", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            const KLV* jetRecoil = product.GetJetRecoil(settings, event);
            return jetRecoil ? product.GetJetRecoil(settings, event)->p4.Eta()
                             : DefaultValues::UndefinedFloat;
        });

    // Gen jets
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genHT", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetGenHT(event);
        });

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "uncleanedgenjet1pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (((KLVs*) event.m_genJets) != nullptr && ((KLVs*) event.m_genJets)->size() > 0)
                       ? ((KLVs*) event.m_genJets)->at(0).p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "uncleanedgenjet1eta", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (((KLVs*) event.m_genJets) != nullptr && ((KLVs*) event.m_genJets)->size() > 0)
                       ? ((KLVs*) event.m_genJets)->at(0).p4.Eta()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "uncleanedgenjet2pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (((KLVs*) event.m_genJets) != nullptr && ((KLVs*) event.m_genJets)->size() > 1)
                       ? ((KLVs*) event.m_genJets)->at(1).p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "uncleanedgenjet2eta", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (((KLVs*) event.m_genJets) != nullptr && ((KLVs*) event.m_genJets)->size() > 1)
                       ? ((KLVs*) event.m_genJets)->at(1).p4.Eta()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genjet1pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_simpleGenJets.size() > 0)
                       ? product.m_simpleGenJets.at(0)->p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genparton1pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genPartons.size() > 0 && product.m_genPartons.at(0) != nullptr)
                       ? product.m_genPartons.at(0)->p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genparton1y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genPartons.size() > 0 && product.m_genPartons.at(0) != nullptr)
                       ? product.m_genPartons.at(0)->p4.Rapidity()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genparton1phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genPartons.size() > 0 && product.m_genPartons.at(0) != nullptr)
                       ? product.m_genPartons.at(0)->p4.Phi()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genparton1mass", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genPartons.size() > 0 && product.m_genPartons.at(0) != nullptr)
                       ? product.m_genPartons.at(0)->p4.mass()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genparton1flavour", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genPartons.size() > 0 && product.m_genPartons.at(0) != nullptr)
                       ? product.m_genPartons.at(0)->pdgId
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genjet1eta", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_simpleGenJets.size() > 0)
                       ? product.m_simpleGenJets.at(0)->p4.Eta()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genjet1phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_simpleGenJets.size() > 0)
                       ? product.m_simpleGenJets.at(0)->p4.Phi()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genjet1y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_simpleGenJets.size() > 0)
                       ? product.m_simpleGenJets.at(0)->p4.Rapidity()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genjet2pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_simpleGenJets.size() > 1)
                       ? product.m_simpleGenJets.at(1)->p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genjet2eta", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_simpleGenJets.size() > 1)
                       ? product.m_simpleGenJets.at(1)->p4.Eta()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genjet2phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_simpleGenJets.size() > 1)
                       ? product.m_simpleGenJets.at(1)->p4.Phi()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genjet2y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_simpleGenJets.size() > 1)
                       ? product.m_simpleGenJets.at(1)->p4.Rapidity()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genjet3pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_simpleGenJets.size() > 2)
                       ? product.m_simpleGenJets.at(2)->p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genjet3eta", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_simpleGenJets.size() > 2)
                       ? product.m_simpleGenJets.at(2)->p4.Eta()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genjet3phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_simpleGenJets.size() > 2)
                       ? product.m_simpleGenJets.at(2)->p4.Phi()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genjet3y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_simpleGenJets.size() > 2)
                       ? product.m_simpleGenJets.at(2)->p4.Rapidity()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "ngenjets", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetValidJetCount(settings, event, "Gen");
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "ngenjets10", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.CountValidJetsAbovePt(settings, event, 10.0, "Gen");
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "ngenjets30", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.CountValidJetsAbovePt(settings, event, 30.0, "Gen");
        });

    // Reco jet - gen parton matches
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenparton1pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 0);
            return (genParton != nullptr) ? genParton->p4.Pt() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenparton1y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 0);
            return (genParton != nullptr) ? genParton->p4.Rapidity() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenparton1phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 0);
            return (genParton != nullptr) ? genParton->p4.Phi() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenparton1mass", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 0);
            return (genParton != nullptr) ? genParton->p4.mass() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "matchedgenparton1flavour", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 0);
            return (genParton != nullptr) ? static_cast<float>(genParton->pdgId)
                                          : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenparton2pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 1);
            return (genParton != nullptr) ? genParton->p4.Pt() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenparton2y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 1);
            return (genParton != nullptr) ? genParton->p4.Rapidity() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenparton2phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 1);
            return (genParton != nullptr) ? genParton->p4.Phi() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenparton2mass", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 1);
            return (genParton != nullptr) ? genParton->p4.mass() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "matchedgenparton2flavour", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 1);
            return (genParton != nullptr) ? static_cast<float>(genParton->pdgId)
                                          : DefaultValues::UndefinedFloat;
        });

    // Reco jet - gen jet matches
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenjet1pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KLV* genJet = product.GetMatchedGenJet(event, settings, 0);
            return (genJet != nullptr) ? genJet->p4.Pt() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenjet1eta", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KLV* genJet = product.GetMatchedGenJet(event, settings, 0);
            return (genJet != nullptr) ? genJet->p4.Eta() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenjet1y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KLV* genJet = product.GetMatchedGenJet(event, settings, 0);
            return (genJet != nullptr) ? genJet->p4.Rapidity() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenjet1phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KLV* genJet = product.GetMatchedGenJet(event, settings, 0);
            return (genJet != nullptr) ? genJet->p4.Phi() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenjet2pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KLV* genJet = product.GetMatchedGenJet(event, settings, 1);
            return (genJet != nullptr) ? genJet->p4.Pt() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenjet2eta", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KLV* genJet = product.GetMatchedGenJet(event, settings, 1);
            return (genJet != nullptr) ? genJet->p4.Eta() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenjet2y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KLV* genJet = product.GetMatchedGenJet(event, settings, 1);
            return (genJet != nullptr) ? genJet->p4.Rapidity() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenjet2phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KLV* genJet = product.GetMatchedGenJet(event, settings, 1);
            return (genJet != nullptr) ? genJet->p4.Phi() : DefaultValues::UndefinedFloat;
        });
    
    // deltaR for jets
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "deltarjet1genjet1", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (((KLVs*) event.m_genJets) != nullptr 
                                    && ((KLVs*) event.m_genJets)->size() > 0
                                    && product.GetValidJetCount(settings, event) > 0
                        ? ROOT::Math::VectorUtil::DeltaR(((KLVs*) event.m_genJets)->at(0).p4, product.GetValidJet(settings, event, 0)->p4)
                        : DefaultValues::UndefinedFloat);
    });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "deltarjet2genjet2", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (((KLVs*) event.m_genJets) != nullptr 
                                    && ((KLVs*) event.m_genJets)->size() > 1
                                    && product.GetValidJetCount(settings, event) > 1
                        ? ROOT::Math::VectorUtil::DeltaR(((KLVs*) event.m_genJets)->at(1).p4, product.GetValidJet(settings, event, 1)->p4)
                        : DefaultValues::UndefinedFloat);
    });

    // Skim jet - jets found in skim, without checks for validity etc
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "skimjet1pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (event.m_tjets->size() > 0) ? event.m_tjets->front().p4.Pt()
                                               : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "skimjet1phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (event.m_tjets->size() > 0) ? event.m_tjets->front().p4.Phi()
                                               : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "skimjet1eta", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (event.m_tjets->size() > 0) ? event.m_tjets->front().p4.Eta()
                                               : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "skimjet1validity", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return ((event.m_tjets->size() > 0) &&
                    (product.GetValidJetCount(settings, event, "None") > 0))
                       ? (event.m_tjets->front().p4 ==
                          product.GetValidJet(settings, event, 0, "None")->p4)
                       : DefaultValues::UndefinedFloat;
        });

    /////////
    // MET //
    /////////

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "met", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMet(settings, event)->p4.Pt();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "metphi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMet(settings, event)->p4.Phi();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "sumet", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMet(settings, event)->sumEt;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "rawmet", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMet(settings, event, "None")->p4.Pt();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "rawmetphi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMet(settings, event, "None")->p4.Phi();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mpf", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMPF(product.GetMet(settings, event));
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mpflead", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMPFlead(settings, event);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mpfjets", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMPFjets(settings, event);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mpfunclustered", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMPFunclustered(settings, event);
        });
    
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "rawmpf", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMPF(product.GetMet(settings, event, "None"));
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "rawmpflead", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMPFlead(settings, event, "None");
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "rawmpfjets", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMPFjets(settings, event, "None");
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "rawmpfunclustered", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetMPFunclustered(settings, event, "None");
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mettype1pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return std::abs(product.GetMet(settings, event)->p4.Pt() -
                            product.GetMet(settings, event, "None")->p4.Pt());
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mettype1vecpt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return std::abs((product.GetMet(settings, event)->p4 -
                             product.GetMet(settings, event, "None")->p4).Pt());
        });

    //////////
    // JNPF //
    //////////

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "jnpf", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetJNPF(settings, event);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "rawjnpf", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.GetJNPF(settings, event, "None");
        });

    ///////////////
    // Z LEPTONS //
    ///////////////

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "validz", [](event_type const& event, product_type const& product) {
            if (product.m_zValid)
                return 1;
            else
                return 0;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genzfound", [](event_type const& event, product_type const& product) {
            if (product.m_genzfound)
                return 1;
            else
                return 0;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "validgenzfound", [](event_type const& event, product_type const& product) {
            if (product.m_validgenzfound)
                return 1;
            else
                return 0;
        });
    // leading Z decay lepton
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zl1pt", [](event_type const& event, product_type const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedFloat;
            return product.m_zLeptons.first->p4.Pt();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zl1phi", [](event_type const& event, product_type const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedFloat;
            return product.m_zLeptons.first->p4.Phi();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zl1eta", [](event_type const& event, product_type const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedFloat;
            return product.m_zLeptons.first->p4.Eta();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "zl1pdgid", [](event_type const& event, product_type const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedInt;
            return kleptonflavour_to_pdgid(product.m_zLeptons.first->flavour());
        });
    // second leading Z decay lepton
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zl2pt", [](event_type const& event, product_type const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedFloat;
            return product.m_zLeptons.second->p4.Pt();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zl2phi", [](event_type const& event, product_type const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedFloat;
            return product.m_zLeptons.second->p4.Phi();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zl2eta", [](event_type const& event, product_type const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedFloat;
            return product.m_zLeptons.second->p4.Eta();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "zl2pdgid", [](event_type const& event, product_type const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedInt;
            return kleptonflavour_to_pdgid(product.m_zLeptons.second->flavour());
        });
    // positive charge Z decay lepton
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zlpluspt", [](ZJetEvent const& event, ZJetProduct const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedFloat;
            return product.m_zLeptons.first->charge() > 0 ? product.m_zLeptons.first->p4.Pt()
                                                          : product.m_zLeptons.second->p4.Pt();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zlplusphi", [](ZJetEvent const& event, ZJetProduct const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedFloat;
            return product.m_zLeptons.first->charge() > 0 ? product.m_zLeptons.first->p4.Phi()
                                                          : product.m_zLeptons.second->p4.Phi();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zlpluseta", [](ZJetEvent const& event, ZJetProduct const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedFloat;
            return product.m_zLeptons.first->charge() > 0 ? product.m_zLeptons.first->p4.Eta()
                                                          : product.m_zLeptons.second->p4.Eta();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "zlpluspdgid", [](ZJetEvent const& event, ZJetProduct const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedInt;
            return product.m_zLeptons.first->charge() > 0
                       ? kleptonflavour_to_pdgid(product.m_zLeptons.first->flavour())
                       : kleptonflavour_to_pdgid(product.m_zLeptons.second->flavour());
        });
    // negative charge Z decay lepton
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zlminuspt", [](ZJetEvent const& event, ZJetProduct const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedFloat;
            return product.m_zLeptons.first->charge() < 0 ? product.m_zLeptons.first->p4.Pt()
                                                          : product.m_zLeptons.second->p4.Pt();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zlminusphi", [](ZJetEvent const& event, ZJetProduct const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedFloat;
            return product.m_zLeptons.first->charge() < 0 ? product.m_zLeptons.first->p4.Phi()
                                                          : product.m_zLeptons.second->p4.Phi();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "zlminuseta", [](ZJetEvent const& event, ZJetProduct const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedFloat;
            return product.m_zLeptons.first->charge() < 0 ? product.m_zLeptons.first->p4.Eta()
                                                          : product.m_zLeptons.second->p4.Eta();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "zlminuspdgid", [](ZJetEvent const& event, ZJetProduct const& product) {
            if (!product.m_zValid)
                return DefaultValues::UndefinedInt;
            return product.m_zLeptons.first->charge() < 0
                       ? kleptonflavour_to_pdgid(product.m_zLeptons.first->flavour())
                       : kleptonflavour_to_pdgid(product.m_zLeptons.second->flavour());
        });

    ///////////
    // MUONS //
    ///////////

    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "nmuons", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.m_validMuons.size();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mupluspt", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin();
                 muon != product.m_validMuons.end(); ++muon) {
                if ((*muon)->charge() > 0)
                    return (*muon)->p4.Pt();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mupluseta", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin();
                 muon != product.m_validMuons.end(); ++muon) {
                if ((*muon)->charge() > 0)
                    return (*muon)->p4.Eta();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muplusphi", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin();
                 muon != product.m_validMuons.end(); ++muon) {
                if ((*muon)->charge() > 0)
                    return (*muon)->p4.Phi();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muplusmass", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin();
                 muon != product.m_validMuons.end(); ++muon) {
                if ((*muon)->charge() > 0)
                    return (*muon)->p4.mass();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muplusiso", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin();
                 muon != product.m_validMuons.end(); ++muon) {
                if ((*muon)->charge() > 0)
                    return (*muon)->pfIso();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muminuspt", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin();
                 muon != product.m_validMuons.end(); ++muon) {
                if ((*muon)->charge() < 0)
                    return (*muon)->p4.Pt();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muminuseta", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin();
                 muon != product.m_validMuons.end(); ++muon) {
                if ((*muon)->charge() < 0)
                    return (*muon)->p4.Eta();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muminusphi", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin();
                 muon != product.m_validMuons.end(); ++muon) {
                if ((*muon)->charge() < 0)
                    return (*muon)->p4.Phi();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muminusmass", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin();
                 muon != product.m_validMuons.end(); ++muon) {
                if ((*muon)->charge() < 0)
                    return (*muon)->p4.mass();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muminusiso", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin();
                 muon != product.m_validMuons.end(); ++muon) {
                if ((*muon)->charge() < 0)
                    return (*muon)->pfIso();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu1pt", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->p4.Pt()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu1phi", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->p4.Phi()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu1eta", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->p4.Eta()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu1mass", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->p4.mass()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu1iso", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->pfIso()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu1sumchpt", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->sumChargedHadronPt
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu1sumnhet", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->sumNeutralHadronEt
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu1sumpet", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->sumPhotonEt
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu1sumpupt", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->sumPUPt
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu1idloose", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->idLoose()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu1idmedium", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->idMedium()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu1idtight", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->idTight()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu2pt", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->p4.Pt()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu2phi", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->p4.Phi()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu2eta", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->p4.Eta()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu2mass", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->p4.mass()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu2iso", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->pfIso()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu2sumchpt", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->sumChargedHadronPt
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu2sumnhet", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->sumNeutralHadronEt
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu2sumpet", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->sumPhotonEt
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu2sumpupt", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->sumPUPt
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu2idloose", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() > 1 ? product.m_validMuons[1]->idLoose()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu2idmedium", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() > 1 ? product.m_validMuons[1]->idMedium()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu2idtight", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() > 1 ? product.m_validMuons[1]->idTight()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu3pt", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 3 ? product.m_validMuons[2]->p4.Pt()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu3phi", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 3 ? product.m_validMuons[2]->p4.Phi()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu3eta", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 3 ? product.m_validMuons[2]->p4.Eta()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "mu3mass", [](event_type const& event, product_type const& product) {
            return product.m_validMuons.size() >= 3 ? product.m_validMuons[2]->p4.mass()
                                                    : DefaultValues::UndefinedFloat;
        });

    // Gen muons
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "ngenmuons", [](ZJetEvent const& event, ZJetProduct const& product) {
            return product.m_genMuons.size();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "nvalidgenmuons", [](ZJetEvent const& event, ZJetProduct const& product) {
            return product.m_validGenMuons.size();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genzl1pt", [](event_type const& event, product_type const& product) {
            return product.m_genLeptonsFromBosonDecay.size() >= 1 ? product.m_genLeptonsFromBosonDecay[0]->p4.Pt()
                                                    : DefaultValues::UndefinedFloat;
        });
     LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genzl2pt", [](event_type const& event, product_type const& product) {
            return product.m_genLeptonsFromBosonDecay.size() >= 2 ? product.m_genLeptonsFromBosonDecay[1]->p4.Pt()
                                                    : DefaultValues::UndefinedFloat;
        });
     LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genzl1eta", [](event_type const& event, product_type const& product) {
            return product.m_genLeptonsFromBosonDecay.size() >= 1 ? product.m_genLeptonsFromBosonDecay[0]->p4.Eta()
                                                    : DefaultValues::UndefinedFloat;
        });
     LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genzl2eta", [](event_type const& event, product_type const& product) {
            return product.m_genLeptonsFromBosonDecay.size() >= 2 ? product.m_genLeptonsFromBosonDecay[1]->p4.Eta()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genzl1phi", [](event_type const& event, product_type const& product) {
            return product.m_genLeptonsFromBosonDecay.size() >= 1 ? product.m_genLeptonsFromBosonDecay[0]->p4.Phi()
                                                    : DefaultValues::UndefinedFloat;
        });
     LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genzl2phi", [](event_type const& event, product_type const& product) {
            return product.m_genLeptonsFromBosonDecay.size() >= 2 ? product.m_genLeptonsFromBosonDecay[1]->p4.Phi()
                                                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genph1pt", [](event_type const& event, product_type const& product) {
            return (product.m_genPhotons.size() > 0) ? product.m_genPhotons[0]->p4.Pt()
                                                        : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genph1eta", [](event_type const& event, product_type const& product) {
            return (product.m_genPhotons.size() > 0) ? product.m_genPhotons[0]->p4.Eta()
                                                        : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genph1phi", [](event_type const& event, product_type const& product) {
            return (product.m_genPhotons.size() > 0) ? product.m_genPhotons[0]->p4.Phi()
                                                        : DefaultValues::UndefinedFloat;
        });

    //////////////
    // Gen Taus //
    //////////////

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truetaupluspt", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genTau = product.m_genTaus.begin();
                 genTau != product.m_genTaus.end(); ++genTau) {
                if ((*genTau)->charge() > 0)
                    return (*genTau)->p4.Pt();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truetauplusy", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genTau = product.m_genTaus.begin();
                 genTau != product.m_genTaus.end(); ++genTau) {
                if ((*genTau)->charge() > 0)
                    return (*genTau)->p4.Rapidity();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truetaupluseta", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genTau = product.m_genTaus.begin();
                 genTau != product.m_genTaus.end(); ++genTau) {
                if ((*genTau)->charge() > 0)
                    return (*genTau)->p4.Eta();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truetauplusphi", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genTau = product.m_genTaus.begin();
                 genTau != product.m_genTaus.end(); ++genTau) {
                if ((*genTau)->charge() > 0)
                    return (*genTau)->p4.Phi();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truetauplusmass", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genTau = product.m_genTaus.begin();
                 genTau != product.m_genTaus.end(); ++genTau) {
                if ((*genTau)->charge() > 0)
                    return (*genTau)->p4.mass();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truetauminuspt", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genTau = product.m_genTaus.begin();
                 genTau != product.m_genTaus.end(); ++genTau) {
                if ((*genTau)->charge() < 0)
                    return (*genTau)->p4.Pt();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truetauminusy", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genTau = product.m_genTaus.begin();
                 genTau != product.m_genTaus.end(); ++genTau) {
                if ((*genTau)->charge() < 0)
                    return (*genTau)->p4.Rapidity();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truetauminuseta", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genTau = product.m_genTaus.begin();
                 genTau != product.m_genTaus.end(); ++genTau) {
                if ((*genTau)->charge() < 0)
                    return (*genTau)->p4.Eta();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truetauminusphi", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genTau = product.m_genTaus.begin();
                 genTau != product.m_genTaus.end(); ++genTau) {
                if ((*genTau)->charge() < 0)
                    return (*genTau)->p4.Phi();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truetauminusmass", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genTau = product.m_genTaus.begin();
                 genTau != product.m_genTaus.end(); ++genTau) {
                if ((*genTau)->charge() < 0)
                    return (*genTau)->p4.mass();
            }
            return DefaultValues::UndefinedFloat;
        });

    /////////////////
    // Gen Leptons //
    /////////////////

    // first N leptons in order of pT
    for (unsigned int iLep = 0; iLep < 2; ++iLep) {
        // gen muon pt, eta, phi
        LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
            "genmu" + std::to_string(iLep + 1) + "pt", [iLep](event_type const& event, product_type const& product) {
                return (product.m_genMuons.size() > iLep) ? product.m_genMuons[iLep]->p4.Pt()
                                                          : DefaultValues::UndefinedFloat;
            });
        LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
            "genmu" + std::to_string(iLep + 1) + "eta", [iLep](event_type const& event, product_type const& product) {
                return (product.m_genMuons.size() > iLep) ? product.m_genMuons[iLep]->p4.Eta()
                                                          : DefaultValues::UndefinedFloat;
            });
        LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
            "genmu" + std::to_string(iLep + 1) + "phi", [iLep](event_type const& event, product_type const& product) {
                return (product.m_genMuons.size() > iLep) ? product.m_genMuons[iLep]->p4.Phi()
                                                          : DefaultValues::UndefinedFloat;
            });
        LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
            "genmu" + std::to_string(iLep + 1) + "mass", [iLep](event_type const& event, product_type const& product) {
                return (product.m_genMuons.size() > iLep) ? product.m_genMuons[iLep]->p4.mass()
                                                          : DefaultValues::UndefinedFloat;
            });

        // gen electron pt, eta, phi
        LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
            "gene" + std::to_string(iLep + 1) + "pt", [iLep](event_type const& event, product_type const& product) {
                return (product.m_genElectrons.size() > iLep) ? product.m_genElectrons[iLep]->p4.Pt()
                                                              : DefaultValues::UndefinedFloat;
            });
        LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
            "gene" + std::to_string(iLep + 1) + "eta", [iLep](event_type const& event, product_type const& product) {
                return (product.m_genElectrons.size() > iLep) ? product.m_genElectrons[iLep]->p4.Eta()
                                                              : DefaultValues::UndefinedFloat;
            });
        LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
            "gene" + std::to_string(iLep + 1) + "phi", [iLep, settings](event_type const& event, product_type const& product) {
                return (product.m_genElectrons.size() > iLep) ? product.m_genElectrons[iLep]->p4.Phi()
                                                              : DefaultValues::UndefinedFloat;
            });
    }

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genmupluspt", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin();
                 genMuon != product.m_genMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() > 0)
                    return (*genMuon)->p4.Pt();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genmupluseta", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin();
                 genMuon != product.m_genMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() > 0)
                    return (*genMuon)->p4.Eta();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genmuplusphi", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin();
                 genMuon != product.m_genMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() > 0)
                    return (*genMuon)->p4.Phi();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genmuplusmass", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin();
                 genMuon != product.m_genMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() > 0)
                    return (*genMuon)->p4.mass();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genmuminuspt", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin();
                 genMuon != product.m_genMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() < 0)
                    return (*genMuon)->p4.Pt();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genmuminuseta", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin();
                 genMuon != product.m_genMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() < 0)
                    return (*genMuon)->p4.Eta();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genmuminusphi", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin();
                 genMuon != product.m_genMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() < 0)
                    return (*genMuon)->p4.Phi();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genmuminusmass", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin();
                 genMuon != product.m_genMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() < 0)
                    return (*genMuon)->p4.mass();
            }
            return DefaultValues::UndefinedFloat;
        });
    // true muons
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truemupluspt", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_validGenMuons.begin();
                 genMuon != product.m_validGenMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() > 0)
                    return (*genMuon)->p4.Pt();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truemupluseta", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_validGenMuons.begin();
                 genMuon != product.m_validGenMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() > 0)
                    return (*genMuon)->p4.Eta();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truemuplusphi", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_validGenMuons.begin();
                 genMuon != product.m_validGenMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() > 0)
                    return (*genMuon)->p4.Phi();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truemuplusmass", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_validGenMuons.begin();
                 genMuon != product.m_validGenMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() > 0)
                    return (*genMuon)->p4.mass();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truemuminuspt", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_validGenMuons.begin();
                 genMuon != product.m_validGenMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() < 0)
                    return (*genMuon)->p4.Pt();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truemuminuseta", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_validGenMuons.begin();
                 genMuon != product.m_validGenMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() < 0)
                    return (*genMuon)->p4.Eta();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truemuminusphi", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_validGenMuons.begin();
                 genMuon != product.m_validGenMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() < 0)
                    return (*genMuon)->p4.Phi();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "truemuminusmass", [](ZJetEvent const& event, ZJetProduct const& product) {
            for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_validGenMuons.begin();
                 genMuon != product.m_validGenMuons.end(); ++genMuon) {
                if ((*genMuon)->charge() < 0)
                    return (*genMuon)->p4.mass();
            }
            return DefaultValues::UndefinedFloat;
        });

    // Reco muon - gen muon matches
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenmuon1pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genMuon = product.GetMatchedGenMuon(event, settings, 0);
            return (genMuon != nullptr) ? genMuon->p4.Pt() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenmuon2pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genMuon = product.GetMatchedGenMuon(event, settings, 1);
            return (genMuon != nullptr) ? genMuon->p4.Pt() : DefaultValues::UndefinedFloat;
        });
        
    // deltaR for muons
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "deltarmu1genmu1", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genMuons.size() >= 1 && product.m_validMuons.size() >= 1
                    ? ROOT::Math::VectorUtil::DeltaR(product.m_genMuons[0]->p4, product.m_validMuons[0]->p4)
                    : DefaultValues::UndefinedFloat);
    }); 
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "deltarmu2genmu2", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genMuons.size() >= 2 && product.m_validMuons.size() >= 2
                    ? ROOT::Math::VectorUtil::DeltaR(product.m_genMuons[1]->p4, product.m_validMuons[1]->p4)
                    : DefaultValues::UndefinedFloat);
    }); 
    // Invalid muons
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "nmuonsinv", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.m_invalidMuons.size();
        });
    // invalid muon 1
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muinv1pt", [](event_type const& event, product_type const& product) {
            return product.m_invalidMuons.size() >= 1 ? product.m_invalidMuons[0]->p4.Pt()
                                                      : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muinv1iso", [](event_type const& event, product_type const& product) {
            return product.m_invalidMuons.size() >= 1 ? product.m_invalidMuons[0]->pfIso()
                                                      : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muinv1sumchpt", [](event_type const& event, product_type const& product) {
            return product.m_invalidMuons.size() >= 1
                       ? product.m_invalidMuons[0]->sumChargedHadronPt
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muinv1sumnhet", [](event_type const& event, product_type const& product) {
            return product.m_invalidMuons.size() >= 1
                       ? product.m_invalidMuons[0]->sumNeutralHadronEt
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muinv1sumpet", [](event_type const& event, product_type const& product) {
            return product.m_invalidMuons.size() >= 1 ? product.m_invalidMuons[0]->sumPhotonEt
                                                      : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muinv1sumpupt", [](event_type const& event, product_type const& product) {
            return product.m_invalidMuons.size() >= 1 ? product.m_invalidMuons[0]->sumPUPt
                                                      : DefaultValues::UndefinedFloat;
        });
    // invalid muon 2
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muinv2pt", [](event_type const& event, product_type const& product) {
            return product.m_invalidMuons.size() >= 2 ? product.m_invalidMuons[1]->p4.Pt()
                                                      : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muinv2iso", [](event_type const& event, product_type const& product) {
            return product.m_invalidMuons.size() >= 2 ? product.m_invalidMuons[1]->pfIso()
                                                      : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muinv2sumchpt", [](event_type const& event, product_type const& product) {
            return product.m_invalidMuons.size() >= 2
                       ? product.m_invalidMuons[1]->sumChargedHadronPt
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muinv2sumnhet", [](event_type const& event, product_type const& product) {
            return product.m_invalidMuons.size() >= 2
                       ? product.m_invalidMuons[1]->sumNeutralHadronEt
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muinv2sumpet", [](event_type const& event, product_type const& product) {
            return product.m_invalidMuons.size() >= 2 ? product.m_invalidMuons[1]->sumPhotonEt
                                                      : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "muinv2sumpupt", [](event_type const& event, product_type const& product) {
            return product.m_invalidMuons.size() >= 2 ? product.m_invalidMuons[1]->sumPUPt
                                                      : DefaultValues::UndefinedFloat;
        });

    ///////////////
    // ELECTRONS //
    ///////////////
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "nelectrons", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.m_validElectrons.size();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e1pt", [](event_type const& event, product_type const& product) {
            return product.m_validElectrons.size() >= 1 ? product.m_validElectrons[0]->p4.Pt()
                                                        : DefaultValues::UndefinedFloat;
        });
    // Basic kinematics
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e1phi", [](event_type const& event, product_type const& product) {
            return product.m_validElectrons.size() >= 1 ? product.m_validElectrons[0]->p4.Phi()
                                                        : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e1eta", [](event_type const& event, product_type const& product) {
            return product.m_validElectrons.size() >= 1 ? product.m_validElectrons[0]->p4.Eta()
                                                        : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e2pt", [](event_type const& event, product_type const& product) {
            return product.m_validElectrons.size() >= 2 ? product.m_validElectrons[1]->p4.Pt()
                                                        : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e2phi", [](event_type const& event, product_type const& product) {
            return product.m_validElectrons.size() >= 2 ? product.m_validElectrons[1]->p4.Phi()
                                                        : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e2eta", [](event_type const& event, product_type const& product) {
            return product.m_validElectrons.size() >= 2 ? product.m_validElectrons[1]->p4.Eta()
                                                        : DefaultValues::UndefinedFloat;
        });

    // -- electron IDs

    const std::string electronVID = settings.GetElectronVIDName();
    const std::string electronVIDType = boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetElectronVIDType()));
    bool q_writeOutVIDs = true;
    if (electronVID == "") {
        q_writeOutVIDs = false;
    }

    // write out cutbased VIDs

    std::string electronVID_looseTag;
    std::string electronVID_mediumTag;
    std::string electronVID_tightTag;
    std::string electronVID_vetoTag;

    if (electronVIDType != "cutbased_v2")
    {
        electronVID_looseTag = "egmGsfElectronIDs:cutBasedElectronID-" + electronVID + "-loose";
        electronVID_mediumTag = "egmGsfElectronIDs:cutBasedElectronID-" + electronVID + "-medium";
        electronVID_tightTag = "egmGsfElectronIDs:cutBasedElectronID-" + electronVID + "-tight";
        electronVID_vetoTag = "egmGsfElectronIDs:cutBasedElectronID-" + electronVID + "-veto";
    }
    else
    {
        electronVID_looseTag = "cutBasedElectronID-" + electronVID + "-loose:";
        electronVID_mediumTag = "cutBasedElectronID-" + electronVID + "-medium:";
        electronVID_tightTag = "cutBasedElectronID-" + electronVID + "-tight:";
        electronVID_vetoTag = "cutBasedElectronID-" + electronVID + "-veto:";
    }

    // first electron VIDs

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e1idloose", [q_writeOutVIDs, electronVID_looseTag](event_type const& event, product_type const& product) {
            if (q_writeOutVIDs) {
                return product.m_validElectrons.size() >= 1 ?
                    product.m_validElectrons[0]->getId(
                        electronVID_looseTag, event.m_electronMetadata
                    ) : DefaultValues::UndefinedFloat;
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e1idmedium", [q_writeOutVIDs, electronVID_mediumTag](event_type const& event, product_type const& product) {
            if (q_writeOutVIDs) {
                return product.m_validElectrons.size() >= 1 ?
                    product.m_validElectrons[0]->getId(
                        electronVID_mediumTag, event.m_electronMetadata
                    ) : DefaultValues::UndefinedFloat;
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e1idtight", [q_writeOutVIDs, electronVID_tightTag](event_type const& event, product_type const& product) {
            if (q_writeOutVIDs) {
                return product.m_validElectrons.size() >= 1 ?
                    product.m_validElectrons[0]->getId(
                        electronVID_tightTag, event.m_electronMetadata
                    ) : DefaultValues::UndefinedFloat;
            }
            return DefaultValues::UndefinedFloat;
        });

    // second electron VIDs

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e2idloose", [q_writeOutVIDs, electronVID_looseTag](event_type const& event, product_type const& product) {
            if (q_writeOutVIDs) {
                return product.m_validElectrons.size() >= 2 ?
                    product.m_validElectrons[1]->getId(
                        electronVID_looseTag, event.m_electronMetadata
                    ) : DefaultValues::UndefinedFloat;
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e2idmedium", [q_writeOutVIDs, electronVID_mediumTag](event_type const& event, product_type const& product) {
            if (q_writeOutVIDs) {
                return product.m_validElectrons.size() >= 2 ?
                    product.m_validElectrons[1]->getId(
                        electronVID_mediumTag, event.m_electronMetadata
                    ) : DefaultValues::UndefinedFloat;
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e2idtight", [q_writeOutVIDs, electronVID_tightTag](event_type const& event, product_type const& product) {
            if (q_writeOutVIDs) {
                return product.m_validElectrons.size() >= 2 ?
                    product.m_validElectrons[1]->getId(
                        electronVID_tightTag, event.m_electronMetadata
                    ) : DefaultValues::UndefinedFloat;
            }
            return DefaultValues::UndefinedFloat;
        });

    // -- non-VID electron IDs

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e1mvatrig", [](event_type const& event, product_type const& product) {
            return ValidElectronsProducer<ZJetTypes>::IsMVATrigElectron(product.m_validElectrons[0],
                                                                        event.m_electronMetadata);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e1mvanontrig", [](event_type const& event, product_type const& product) {
            return ValidElectronsProducer<ZJetTypes>::IsMVANonTrigElectron(
                product.m_validElectrons[0], event.m_electronMetadata);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e2mvatrig", [](event_type const& event, product_type const& product) {
            return ValidElectronsProducer<ZJetTypes>::IsMVATrigElectron(product.m_validElectrons[1],
                                                                        event.m_electronMetadata);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "e2mvanontrig", [](event_type const& event, product_type const& product) {
            return ValidElectronsProducer<ZJetTypes>::IsMVANonTrigElectron(
                product.m_validElectrons[1], event.m_electronMetadata);
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "epluspt", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KElectron*>::const_iterator electron =
                     product.m_validElectrons.begin();
                 electron != product.m_validElectrons.end(); ++electron) {
                if ((*electron)->charge() > 0)
                    return (*electron)->p4.Pt();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "epluseta", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KElectron*>::const_iterator electron =
                     product.m_validElectrons.begin();
                 electron != product.m_validElectrons.end(); ++electron) {
                if ((*electron)->charge() > 0)
                    return (*electron)->p4.Eta();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "eplusphi", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KElectron*>::const_iterator electron =
                     product.m_validElectrons.begin();
                 electron != product.m_validElectrons.end(); ++electron) {
                if ((*electron)->charge() > 0)
                    return (*electron)->p4.Phi();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "eplusiso", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KElectron*>::const_iterator electron =
                     product.m_validElectrons.begin();
                 electron != product.m_validElectrons.end(); ++electron) {
                if ((*electron)->charge() > 0)
                    return (*electron)->pfIso();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "eminuspt", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KElectron*>::const_iterator electron =
                     product.m_validElectrons.begin();
                 electron != product.m_validElectrons.end(); ++electron) {
                if ((*electron)->charge() < 0)
                    return (*electron)->p4.Pt();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "eminuseta", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KElectron*>::const_iterator electron =
                     product.m_validElectrons.begin();
                 electron != product.m_validElectrons.end(); ++electron) {
                if ((*electron)->charge() < 0)
                    return (*electron)->p4.Eta();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "eminusphi", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KElectron*>::const_iterator electron =
                     product.m_validElectrons.begin();
                 electron != product.m_validElectrons.end(); ++electron) {
                if ((*electron)->charge() < 0)
                    return (*electron)->p4.Phi();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "eminusiso", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KElectron*>::const_iterator electron =
                     product.m_validElectrons.begin();
                 electron != product.m_validElectrons.end(); ++electron) {
                if ((*electron)->charge() < 0)
                    return (*electron)->pfIso();
            }
            return DefaultValues::UndefinedFloat;
        });
    // gen electrons
    LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity(
        "ngenelectrons", [](ZJetEvent const& event, ZJetProduct const& product) {
            return product.m_genElectrons.size();
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genepluspt", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KGenParticle*>::const_iterator genElectron =
                     product.m_genElectrons.begin();
                 genElectron != product.m_genElectrons.end(); ++genElectron) {
                if ((*genElectron)->charge() > 0)
                    return (*genElectron)->p4.Pt();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "genepluseta", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KGenParticle*>::const_iterator genElectron =
                     product.m_genElectrons.begin();
                 genElectron != product.m_genElectrons.end(); ++genElectron) {
                if ((*genElectron)->charge() > 0)
                    return (*genElectron)->p4.Eta();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "geneplusphi", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KGenParticle*>::const_iterator genElectron =
                     product.m_genElectrons.begin();
                 genElectron != product.m_genElectrons.end(); ++genElectron) {
                if ((*genElectron)->charge() > 0)
                    return (*genElectron)->p4.Phi();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "geneminuspt", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KGenParticle*>::const_iterator genElectron =
                     product.m_genElectrons.begin();
                 genElectron != product.m_genElectrons.end(); ++genElectron) {
                if ((*genElectron)->charge() < 0)
                    return (*genElectron)->p4.Pt();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "geneminuseta", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KGenParticle*>::const_iterator genElectron =
                     product.m_genElectrons.begin();
                 genElectron != product.m_genElectrons.end(); ++genElectron) {
                if ((*genElectron)->charge() < 0)
                    return (*genElectron)->p4.Eta();
            }
            return DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "geneminusphi", [](ZJetEvent const& event, ZJetProduct const& product) -> float {
            for (std::vector<KGenParticle*>::const_iterator genElectron =
                     product.m_genElectrons.begin();
                 genElectron != product.m_genElectrons.end(); ++genElectron) {
                if ((*genElectron)->charge() < 0)
                    return (*genElectron)->p4.Phi();
            }
            return DefaultValues::UndefinedFloat;
        });
    // Reco muon - gen muon matches
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenelectron1pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genElectron = product.GetMatchedGenElectron(event, settings, 0);
            return (genElectron != nullptr) ? genElectron->p4.Pt() : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "matchedgenelectron2pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            KGenParticle* genElectron = product.GetMatchedGenElectron(event, settings, 1);
            return (genElectron != nullptr) ? genElectron->p4.Pt() : DefaultValues::UndefinedFloat;
        });

    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "ngenneutrinos", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return product.n_neutrinos;
        });
        
        
    // deltaR for electrons
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "deltare1gene1", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genElectrons.size() >= 1 && product.m_validElectrons.size() >= 1
                    ? ROOT::Math::VectorUtil::DeltaR(product.m_genElectrons[0]->p4, product.m_validElectrons[0]->p4)
                    : DefaultValues::UndefinedFloat);
    }); 
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "deltare2gene2", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genElectrons.size() >= 2 && product.m_validElectrons.size() >= 2
                    ? ROOT::Math::VectorUtil::DeltaR(product.m_genElectrons[1]->p4, product.m_validElectrons[1]->p4)
                    : DefaultValues::UndefinedFloat);
    });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "deltarzl1genzl1", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genLeptonsFromBosonDecay.size() >= 1 && product.m_zValid
                    ? ROOT::Math::VectorUtil::DeltaR(product.m_genLeptonsFromBosonDecay[0]->p4, product.m_zLeptons.first->p4)
                    : DefaultValues::UndefinedFloat);
    });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "deltarzl2genzl2", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_genLeptonsFromBosonDecay.size() >= 2 && product.m_zValid
                    ? ROOT::Math::VectorUtil::DeltaR(product.m_genLeptonsFromBosonDecay[1]->p4, product.m_zLeptons.second->p4)
                    : DefaultValues::UndefinedFloat);
    });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "invalidjet1pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetInvalidJetCount(settings, event) > 0)
                       ? product.GetInvalidJet(settings, event, 0)->p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "invalidjet1eta", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetInvalidJetCount(settings, event) > 0)
                       ? product.GetInvalidJet(settings, event, 0)->p4.Eta()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "invalidjet1y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetInvalidJetCount(settings, event) > 0)
                       ? product.GetInvalidJet(settings, event, 0)->p4.Rapidity()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "invalidjet1phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetInvalidJetCount(settings, event) > 0)
                       ? product.GetInvalidJet(settings, event, 0)->p4.Phi()
                       : DefaultValues::UndefinedFloat;
        });	
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "invalidjet1idloose", [settings](event_type const& event, product_type const& product) {
            return (product.GetInvalidJetCount(settings, event) > 0)
                    ? ValidJetsProducer::passesJetID(product.m_invalidJets[0],
                        KappaEnumTypes::JetIDVersion::ID2016, KappaEnumTypes::JetID::LOOSE, settings)
                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "invalidjet2pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetInvalidJetCount(settings, event) > 1)
                       ? product.GetInvalidJet(settings, event, 1)->p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "invalidjet2idloose", [settings](event_type const& event, product_type const& product) {
            return (product.GetInvalidJetCount(settings, event) > 1)
                    ? ValidJetsProducer::passesJetID(product.m_invalidJets[1],
                        KappaEnumTypes::JetIDVersion::ID2016, KappaEnumTypes::JetID::LOOSE, settings)
                    : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "invalidjet3pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.GetInvalidJetCount(settings, event) > 2)
                       ? product.GetInvalidJet(settings, event, 2)->p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "invalidjet3idloose", [settings](event_type const& event, product_type const& product) {
            return (product.GetInvalidJetCount(settings, event) > 2)
                    ? ValidJetsProducer::passesJetID(product.m_invalidJets[2],
                        KappaEnumTypes::JetIDVersion::ID2016, KappaEnumTypes::JetID::LOOSE, settings)
                    : DefaultValues::UndefinedFloat;
        });
    // incoming partons
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "parton1pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_partons.size() > 0 && product.m_partons.at(0) != nullptr)
                       ? product.m_partons.at(0)->p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "parton1y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_partons.size() > 0 && product.m_partons.at(0) != nullptr)
                       ? product.m_partons.at(0)->p4.Rapidity()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "parton1phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_partons.size() > 0 && product.m_partons.at(0) != nullptr)
                       ? product.m_partons.at(0)->p4.Phi()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "parton1mass", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_partons.size() > 0 && product.m_partons.at(0) != nullptr)
                       ? product.m_partons.at(0)->p4.mass()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "parton1flavour", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_partons.size() > 0 && product.m_partons.at(0) != nullptr)
                       ? product.m_partons.at(0)->pdgId
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "parton2pt", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_partons.size() > 1 && product.m_partons.at(1) != nullptr)
                       ? product.m_partons.at(1)->p4.Pt()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "parton2y", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_partons.size() > 1 && product.m_partons.at(1) != nullptr)
                       ? product.m_partons.at(1)->p4.Rapidity()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "parton2phi", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_partons.size() > 1 && product.m_partons.at(1) != nullptr)
                       ? product.m_partons.at(1)->p4.Phi()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "parton2mass", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_partons.size() > 1 && product.m_partons.at(1) != nullptr)
                       ? product.m_partons.at(1)->p4.mass()
                       : DefaultValues::UndefinedFloat;
        });
    LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity(
        "parton2flavour", [settings](ZJetEvent const& event, ZJetProduct const& product) {
            return (product.m_partons.size() > 1 && product.m_partons.at(1) != nullptr)
                       ? product.m_partons.at(1)->pdgId
                       : DefaultValues::UndefinedFloat;
        });
    // Needs to be called at the end
    KappaLambdaNtupleConsumer::Init(settings);

}
