#include "KappaTools/Toolbox/interface/StringTools.h"

#include "Excalibur/Compile/interface/Producers/ZJetCorrectionsProducer.h"

std::string ZJetCorrectionsProducer::GetProducerId() const { return "ZJetCorrectionsProducer"; }

void ZJetCorrectionsProducer::Init(ZJetSettings const& settings)
{
    ZJetProducerBase::Init(settings);

    // convert usual algo name (ak5PFJetsCHS) to txt file algo name (AK5PFchs)
    std::string jetName = "Jets";
    if (settings.GetTaggedJets().find("Tagged") !=
        std::string::npos)  // to be removed after transition phase
        jetName = "TaggedJets";
    std::string algoName;
    std::vector<std::string> algoNameAndType = KappaTools::split(settings.GetTaggedJets(), jetName);
    if (algoNameAndType[0] == "ak4Calo"){ //CaloJets don"t follow this naming convention
        algoName = "AK4Calo";
    }
    else{
        std::string algoType = KappaTools::tolower(algoNameAndType[1]);
        if (KappaTools::tolower(algoNameAndType[1]) == "puppi") {
            algoType = "Puppi";
        }
        algoName = KappaTools::toupper(algoNameAndType[0].substr(0, 2)) +
                           algoNameAndType[0].substr(2, std::string::npos);
        if (algoNameAndType.size()>1) {
            algoName+=algoType;
        }
    }
    LOG(INFO) << "\t -- Jet corrections enabled for " << algoName
       	      << " jets using the following JEC files:";

    // JEC initialization
    std::vector<JetCorrectorParameters> jecParameters;

    // L1 depending on config parameter
    LOG(INFO) << "\t -- " << settings.GetJec() << "_" << settings.GetL1Correction() << "_"
              << algoName << ".txt";
    jecParameters.push_back(JetCorrectorParameters(
        settings.GetJec() + "_" + settings.GetL1Correction() + "_" + algoName + ".txt"));
    m_l1 = new FactorizedJetCorrector(jecParameters);
    jecParameters.clear();

    // RC
    if (settings.GetRC()) {
        // run2 naming convention
        if (settings.GetYear() >= 2015) {
            LOG(INFO) << "\t -- " << settings.GetJec() << "_"
                      << "L1RC"
                      << "_" << algoName << ".txt";
            jecParameters.push_back(
                JetCorrectorParameters(settings.GetJec() + "_" + "L1RC" + "_" + algoName + ".txt"));
        }
        // run1 naming convention
        else {
            LOG(INFO) << "\t -- " << settings.GetJec() << "_"
                      << "RC"
                      << "_" << algoName << ".txt";
            jecParameters.push_back(
                JetCorrectorParameters(settings.GetJec() + "_" + "RC" + "_" + algoName + ".txt"));
        }
        m_rc = new FactorizedJetCorrector(jecParameters);
        jecParameters.clear();
    }

    // L2Relative
    LOG(INFO) << "\t -- " << settings.GetJec() << "_"
              << "L2Relative"
              << "_" << algoName << ".txt";
    jecParameters.push_back(
        JetCorrectorParameters(settings.GetJec() + "_" + "L2Relative" + "_" + algoName + ".txt"));
    m_l2 = new FactorizedJetCorrector(jecParameters);
    jecParameters.clear();

    // L3Absolute
    LOG(INFO) << "\t -- " << settings.GetJec() << "_"
              << "L3Absolute"
              << "_" << algoName << ".txt";
    jecParameters.push_back(
        JetCorrectorParameters(settings.GetJec() + "_" + "L3Absolute" + "_" + algoName + ".txt"));
    m_l3 = new FactorizedJetCorrector(jecParameters);
    jecParameters.clear();

    // Flavor based corrections
    if (settings.GetFlavourCorrections()) {
        LOG(INFO) << "\t -- " << settings.GetJec() << "_"
                  << "L5Flavor_qJ"
                  << "_" << algoName << ".txt";
        jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L5Flavor_qJ" +
                                                       "_" + algoName + ".txt"));
        m_l5q = new FactorizedJetCorrector(jecParameters);
        jecParameters.clear();
        LOG(INFO) << "\t -- " << settings.GetJec() << "_"
                  << "L5Flavor_gJ"
                  << "_" << algoName << ".txt";
        jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L5Flavor_gJ" +
                                                       "_" + algoName + ".txt"));
        m_l5g = new FactorizedJetCorrector(jecParameters);
        jecParameters.clear();
        LOG(INFO) << "\t -- " << settings.GetJec() << "_"
                  << "L5Flavor_cJ"
                  << "_" << algoName << ".txt";
        jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L5Flavor_cJ" +
                                                       "_" + algoName + ".txt"));
        m_l5c = new FactorizedJetCorrector(jecParameters);
        jecParameters.clear();
        LOG(INFO) << "\t -- " << settings.GetJec() << "_"
                  << "L5Flavor_bJ"
                  << "_" << algoName << ".txt";
        jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L5Flavor_bJ" +
                                                       "_" + algoName + ".txt"));
        m_l5b = new FactorizedJetCorrector(jecParameters);
        jecParameters.clear();
    }

    // L2Residual
    if (settings.GetInputIsData() && settings.GetProvideL2ResidualCorrections()) {
        LOG(INFO) << "\t -- " << settings.GetJec() << "_"
                  << "L2Residual"
                  << "_" << algoName << ".txt";
        jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L2Residual" +
                                                       "_" + algoName + ".txt"));
        m_l2res = new FactorizedJetCorrector(jecParameters);
        jecParameters.clear();
    }
    // L2L3Residual
    if (settings.GetInputIsData() && settings.GetProvideL2L3ResidualCorrections()) {
        LOG(INFO) << "\t -- " << settings.GetJec() << "_"
                  << "L2L3Residual"
                  << "_" << algoName << ".txt";
        jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L2L3Residual" +
                                                       "_" + algoName + ".txt"));
        m_l2l3res = new FactorizedJetCorrector(jecParameters);
        jecParameters.clear();
    }
    // JEU initialization
    if (settings.GetJetEnergyCorrectionUncertaintyShift() != 0.0) {
        LOG(INFO) << "\t -- Enabling JEC Uncertainty...";
        JetCorrectorParameters* jecUncertaintyParameters = nullptr;
        std::string fname_unc = settings.GetJec() + "_" + "UncertaintySources" + "_" + algoName + ".txt";
        if (settings.GetJetEnergyCorrectionUncertaintySource().empty()) {
            LOG(FATAL) << "Undefined JetEnergyCorrectionUncertaintySource. Use 'Total' for full uncertainty.";
        }
        jecUncertaintyParameters = new JetCorrectorParameters(fname_unc, settings.GetJetEnergyCorrectionUncertaintySource());
        if ((!jecUncertaintyParameters->isValid()) || (jecUncertaintyParameters->size() == 0)) {
            LOG(FATAL) << "Invalid definition " << settings.GetJetEnergyCorrectionUncertaintySource() << " in file " << fname_unc;
        }
        LOG(INFO) << "\t\t" << "Using JEC uncertainty " << settings.GetJetEnergyCorrectionUncertaintySource();
        LOG(INFO) << "\t\t" << "From file" << fname_unc;
        correctionUncertainty = new JetCorrectionUncertainty(*jecUncertaintyParameters);
    }
    else {
        LOG(INFO) << "\t -- Using mean JEC values. No JetEnergyCorrectionUncertaintyParameters and/or JetEnergyCorrectionUncertaintyShift supplied.";
    }
}

void ZJetCorrectionsProducer::Produce(ZJetEvent const& event,
                                      ZJetProduct& product,
                                      ZJetSettings const& settings) const
{
    // TODO(gfleig): Do we need more assertions?
    assert(event.m_pileupDensity);
    assert(event.m_vertexSummary);
    LOG(DEBUG) << "\n[" << this->GetProducerId() << "]";
    CorrectJetCollection("None", "L1", m_l1, event, product, settings);
    if (settings.GetRC()) {
        CorrectJetCollection("None", "RC", m_rc, event, product, settings);
    }

    // deep copy corrected L1 Jets for Type I MET calculation
    /****
     * For the TypeIMet it is necessary to use the unsmeared L1 jets (L1RC).
     * Therefore, we have to disentangle the shared pointer construct of the m_correctedZJets,
     * since the JERSmearer runs before the TypeIMetProducer
     * PS: there must be a better way... TODO
     ****/

    product.m_unsmearedL1Jets = product.m_correctedZJets;
    // loop over all map keys
    for (const auto& map_entry : product.m_unsmearedL1Jets) {
        std::vector<std::shared_ptr<KJet>> newJets;  // create new vector to store the new, independent
                                                     // pointers
        // loop over each vector element to dereference the values to get rid of the old pointers...
        for (const auto& v : map_entry.second) {
            KJet temp = *v;
            auto newShared = std::shared_ptr<KJet>(new KJet(temp));
            newJets.push_back(newShared);  // push_back new pointers
        }
        // add each iteration to the new map
        product.m_unsmearedL1Jets[map_entry.first] = newJets;
        newJets.clear();
    }

    CorrectJetCollection("L1", "L1L2L3", m_l2, event, product,
                         settings);  // Output is named L1L2L3 since L1L2 -> L1L2L3 does not do
                                     // anything and we need L1L2L3 for further corrections/access
    // CorrectJetCollection("L1L2", "L1L2L3", m_l3, event, product, settings); // L3Absolute does
    // not do anything yet..
    if (settings.GetFlavourCorrections()) {
        CorrectJetCollection("L1L2L3", "L1L2L3L5q", m_l5q, event, product, settings);
        CorrectJetCollection("L1L2L3", "L1L2L3L5g", m_l5g, event, product, settings);
        CorrectJetCollection("L1L2L3", "L1L2L3L5c", m_l5c, event, product, settings);
        CorrectJetCollection("L1L2L3", "L1L2L3L5b", m_l5b, event, product, settings);
    }
    if (settings.GetInputIsData() && settings.GetProvideL2ResidualCorrections()) {
        CorrectJetCollection("L1L2L3", "L1L2Res", m_l2res, event, product, settings);
    }
    if (settings.GetInputIsData() && settings.GetProvideL2L3ResidualCorrections()) {
        CorrectJetCollection("L1L2L3", "L1L2L3Res", m_l2l3res, event, product, settings);
    }

    // write to product so the consumer can access the jet pt of the UNSORTED jets
    if (product.m_validJets.size() > 0) {
        product.jetpt_l1 = product.m_correctedZJets["L1"][0]->p4.Pt();
        product.jetpt_l1l2l3 = product.m_correctedZJets["L1L2L3"][0]->p4.Pt();
        if (settings.GetRC()) {
            product.jetpt_rc = product.m_correctedZJets["RC"][0]->p4.Pt();
        }
        if (settings.GetProvideL2L3ResidualCorrections()) {
            product.jetpt_l1l2l3res = product.m_correctedZJets["L1L2L3Res"][0]->p4.Pt();
        }
    }
}

void ZJetCorrectionsProducer::CorrectJetCollection(std::string inCorrLevel,
                                                   std::string outCorrLevel,
                                                   FactorizedJetCorrector* factorizedJetCorrector,
                                                   ZJetEvent const& event,
                                                   ZJetProduct& product,
                                                   ZJetSettings const& settings) const
{
    // Create a copy of all jets in the event (first temporarily for the JEC)
    unsigned long validJetCount = product.GetValidJetCount(settings, event, inCorrLevel);
    std::vector<KJet> correctJetsForJecTools(validJetCount);
    for (unsigned long jetIndex = 0; jetIndex < validJetCount; ++jetIndex) {
        correctJetsForJecTools[jetIndex] =
            *(static_cast<KJet*>(product.GetValidJet(settings, event, jetIndex, inCorrLevel)));
    }
    unsigned long invalidJetCount = product.GetInvalidJetCount(settings, event, inCorrLevel);
    std::vector<KJet> correctInvalidJetsForJecTools(invalidJetCount);
    for (unsigned long jetIndex = 0; jetIndex < invalidJetCount; ++jetIndex) {
        correctInvalidJetsForJecTools[jetIndex] =
            *(static_cast<KJet*>(product.GetInvalidJet(settings, event, jetIndex, inCorrLevel)));
    }

    // Apply jet energy corrections and uncertainty shift
    correctJets(&correctJetsForJecTools, factorizedJetCorrector, correctionUncertainty,
                event.m_pileupDensity->rho, static_cast<int>(event.m_vertexSummary->nVertices),
                -1.0f, settings.GetJetEnergyCorrectionUncertaintyShift(), false);
    correctJets(&correctInvalidJetsForJecTools, factorizedJetCorrector, correctionUncertainty,
                event.m_pileupDensity->rho, static_cast<int>(event.m_vertexSummary->nVertices),
                -1.0f, settings.GetJetEnergyCorrectionUncertaintyShift(), false);

    // Create shared pointers and store them in the product
    product.m_correctedZJets[outCorrLevel].clear();
    product.m_correctedZJets[outCorrLevel].resize(correctJetsForJecTools.size());
    unsigned long jetIndex = 0;
    for (typename std::vector<KJet>::const_iterator jet = correctJetsForJecTools.begin();
         jet != correctJetsForJecTools.end(); ++jet) {
        product.m_correctedZJets[outCorrLevel][jetIndex] = std::shared_ptr<KJet>(new KJet(*jet));
        ++jetIndex;
    }
    product.m_correctedInvalidJets[outCorrLevel].clear();
    product.m_correctedInvalidJets[outCorrLevel].resize(correctInvalidJetsForJecTools.size());
    unsigned long invalidJetIndex = 0;
    for (typename std::vector<KJet>::const_iterator jet = correctInvalidJetsForJecTools.begin();
         jet != correctInvalidJetsForJecTools.end(); ++jet) {
        product.m_correctedInvalidJets[outCorrLevel][invalidJetIndex] = std::shared_ptr<KJet>(new KJet(*jet));
        ++invalidJetIndex;
    }
}
