#include "Excalibur/Compile/interface/Producers/JERSmearer.h"

#include "KappaTools/Toolbox/interface/StringTools.h"


std::string JERSmearer::GetProducerId() const { return "JERSmearer"; }

void JERSmearer::Init(ZJetSettings const& settings) {

    ZJetProducerBase::Init(settings);

    // convert usual algo name (ak5PFJetsCHS) to txt file algo name (AK5PFchs)
    std::string jetName = "Jets";
    if (settings.GetTaggedJets().find("Tagged") != std::string::npos)
        jetName = "TaggedJets";

    std::string algoName;
    std::vector<std::string> algoNameAndType = KappaTools::split(settings.GetTaggedJets(), jetName);
    if (algoNameAndType[0] == "ak4Calo") {  // CaloJets don't follow this naming convention
        LOG(FATAL) << "[JERSmearer] Jet energy resolution smearing not available for 'AK4Calo' jets!";
    }
    else {
        std::string algoType = KappaTools::tolower(algoNameAndType[1]);
        if (KappaTools::tolower(algoNameAndType[1]) == "puppi") {
            algoType = "Puppi";
        }

        algoName = KappaTools::toupper(algoNameAndType[0].substr(0, 2)) + algoNameAndType[0].substr(2, std::string::npos);
        if (algoNameAndType.size() > 1) {
            algoName += algoType;
        }
    }

    // get and validate smearing method configuration
    if (KappaTools::tolower(settings.GetJERMethod()) == "hybrid") {
        if (settings.GetInputIsData())
            LOG(FATAL) << "[JERSmearer] JER smearing method hybrid not possible for data!!!";
        else
            m_smearingMethod = JERSmearer::SmearingMethod::HYBRID;
    }
    else if (KappaTools::tolower(settings.GetJERMethod()) == "stochastic") {
        m_smearingMethod = JERSmearer::SmearingMethod::STOCHASTIC;
    }
    else {
        LOG(FATAL) << "[JERSmearer] Unknown JER smearing method '" << settings.GetJERMethod() << "'!";
    }

    // report
    LOG(INFO) << "\n[JERSmearer] Jet energy resolution smearing using method '" << settings.GetJERMethod()
              << "' enabled for " << algoName
              << " jets using the following JER files:" << std::endl;

    LOG(INFO) << "\t -- " << settings.GetJER() + "_PtResolution_" + algoName + ".txt" << std::endl;
    LOG(INFO) << "\t -- " << settings.GetJER() + "_SF_" + algoName + ".txt" << std::endl;

    // create the resolution and resolution scale factor objects
    m_jetResolution.reset(new JME::JetResolution(settings.GetJER() + "_PtResolution_" + algoName + ".txt"));
    m_jetResolutionScaleFactor.reset(new JME::JetResolutionScaleFactor(settings.GetJER() + "_SF_" + algoName + ".txt"));

    // create the random number generator
    m_randomNumberGenerator = std::mt19937(settings.GetJERSmearerSeed());
    std::cout << "test" << std::endl;
}

void JERSmearer::Produce(ZJetEvent const& event,
                         ZJetProduct& product,
                         ZJetSettings const& settings) const {

    // iterate over all jet correction levels
    if (settings.GetInputIsData()) {
        for (std::map<std::string, std::vector<std::shared_ptr<KJet>>>::const_iterator itlevel = product.m_correctedZJets.begin();
             itlevel != product.m_correctedZJets.end();
             ++itlevel) {
    
            // shortcuts for convenience
            auto& recoJets = product.m_correctedZJets[itlevel->first];
            // go through all reco jets
            for (size_t iJet = 0; iJet < recoJets.size(); ++iJet) {
                // retrieve the (relative) pT resolution and the resolution scale factor
                double jetResolution = m_jetResolution->getResolution({
                    {JME::Binning::JetPt, recoJets[iJet]->p4.Pt()},
                    {JME::Binning::JetEta, recoJets[iJet]->p4.Eta()},
                    {JME::Binning::Rho, event.m_pileupDensity->rho}
                });
                // compute and apply the pT smearing factor
                recoJets[iJet]->p4 *= 1 + std::normal_distribution<>(0, jetResolution)(m_randomNumberGenerator);
            }
        }
    }
    else {
        for (std::map<std::string, std::vector<std::shared_ptr<KJet>>>::const_iterator itlevel = product.m_correctedZJets.begin();
             itlevel != product.m_correctedZJets.end();
             ++itlevel) {
    
            // shortcuts for convenience
            auto& recoJets = product.m_correctedZJets[itlevel->first];
            const auto& matchedGenJetIndices = product.m_matchedGenJets[itlevel->first];
            // go through all reco jets
            for (size_t iJet = 0; iJet < recoJets.size(); ++iJet) {
                // retrieve the (relative) pT resolution and the resolution scale factor
                double jetResolution = m_jetResolution->getResolution({
                    {JME::Binning::JetPt, recoJets[iJet]->p4.Pt()},
                    {JME::Binning::JetEta, recoJets[iJet]->p4.Eta()},
                    {JME::Binning::Rho, event.m_pileupDensity->rho}
                });
                double jetResolutionScaleFactor = m_jetResolutionScaleFactor->getScaleFactor({
                    {JME::Binning::JetEta, recoJets[iJet]->p4.Eta()}
                }, Variation::NOMINAL);
                // get and validate matched gen jet
                const KLV* matchedGenJet = nullptr;
                if (matchedGenJetIndices[iJet] >= 0) {
                    matchedGenJet = product.m_simpleGenJets[matchedGenJetIndices[iJet]];
    
                    // invalidate match if additional pT-criterion is not met
                    if (std::abs(recoJets[iJet]->p4.Pt() - matchedGenJet->p4.Pt()) > 3 * jetResolution * recoJets[iJet]->p4.Pt()) {
                        matchedGenJet = nullptr;
                    }
                }
    
                // compute and apply the pT smearing factor
                if ((matchedGenJet) && (m_smearingMethod == JERSmearer::SmearingMethod::HYBRID)) {
                    // match found and hybrid method requested -> smear using scaling method
                    recoJets[iJet]->p4 *= 1 + (jetResolutionScaleFactor - 1) * (recoJets[iJet]->p4.Pt() - matchedGenJet->p4.Pt())/recoJets[iJet]->p4.Pt();
                }
                else if ((m_smearingMethod == JERSmearer::SmearingMethod::STOCHASTIC) || (!matchedGenJet)) {
                    // match not found or stochastic method requested -> draw pT smearing factor from a normal distribution
                    recoJets[iJet]->p4 *= 1 + std::normal_distribution<>(0, jetResolution)(m_randomNumberGenerator) * std::sqrt(std::max(jetResolutionScaleFactor * jetResolutionScaleFactor - 1, 0.0));
                }
            }
        }
    }
}
