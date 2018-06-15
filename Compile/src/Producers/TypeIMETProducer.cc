#include "Excalibur/Compile/interface/Producers/TypeIMETProducer.h"

std::string TypeIMETProducer::GetProducerId() const { return "TypeIMETProducer"; }

void TypeIMETProducer::Init(ZJetSettings const& settings)
{
    ZJetProducerBase::Init(settings);

    m_metPhiCorrectionParameters = settings.GetMetPhiCorrectionParameters();

    // Use random cone?
    m_l1Corr = settings.GetRC() ? "RC" : "L1";
    m_corrLevels.emplace_back("L1L2L3");

    // Residual correctiuons if input is data
    if (settings.GetInputIsData() && settings.GetProvideL2ResidualCorrections()) {
        m_corrLevels.emplace_back("L1L2Res");
    }
    if (settings.GetInputIsData() && settings.GetProvideL2L3ResidualCorrections()) {
        m_corrLevels.emplace_back("L1L2L3Res");
    }

    // Flavor based corrections
    if (settings.GetFlavourCorrections()) {
        m_corrLevels.emplace_back("L1L2L3L5q");
        m_corrLevels.emplace_back("L1L2L3L5g");
        m_corrLevels.emplace_back("L1L2L3L5c");
        m_corrLevels.emplace_back("L1L2L3L5b");
    }
}

void TypeIMETProducer::Produce(ZJetEvent const& event,
                               ZJetProduct& product,
                               ZJetSettings const& settings) const
{
    // Iterate over the jet collection
    for (unsigned int corrLevelIndex = 0; corrLevelIndex < m_corrLevels.size(); ++corrLevelIndex) {
        KLV correction;
        double sumEtCorrection = 0;

        // Iterate over individual jets and sum up the differences between L1L2L3(Res) and L1
        for (unsigned int jetIndex = 0;
             jetIndex < product.m_correctedZJets.at(m_corrLevels[corrLevelIndex]).size();
             ++jetIndex) {
            KLV* corrJet = (SafeMap::Get(product.m_correctedZJets, m_corrLevels[corrLevelIndex])
                                .at(jetIndex)).get();

            // TypeI MET modification for 2017
            if (settings.GetEnableTypeIModification()) {
                if ((corrJet->p4.Pt() < settings.GetTypeIModExcludeJetPtMax()) &&
                    (abs(corrJet->p4.Eta()) > settings.GetTypeIModExcludeJetAbsEtaMin()) &&
                    (abs(corrJet->p4.Eta()) < settings.GetTypeIModExcludeJetAbsEtaMax())) {
                    continue;  // do not include this jet in the TypeI MET correction
                }
            }

            // Only consider jets with Pt above TypeIJetPtMin
            if (corrJet->p4.Pt() > settings.GetTypeIJetPtMin()) {
                KLV* l1Jet = (SafeMap::Get(product.m_correctedZJets, m_l1Corr).at(jetIndex)).get();
                correction.p4 += l1Jet->p4 - corrJet->p4;
                sumEtCorrection += static_cast<double>(correction.p4.Pt());
            }
        }
        KMET corrMET = *event.m_met;
        corrMET.p4 += correction.p4;

        // Eta of MET is always zero
        corrMET.p4.SetEta(0.0f);
        corrMET.sumEt = event.m_met->sumEt + sumEtCorrection;

        // Apply MET-phi-corrections
        if (settings.GetEnableMetPhiCorrection()) {
            double px = corrMET.p4.Px();
            double py = corrMET.p4.Py();

            px -= m_metPhiCorrectionParameters.at(0) +
                  m_metPhiCorrectionParameters.at(1) * event.m_vertexSummary->nVertices;
            py -= m_metPhiCorrectionParameters.at(2) +
                  m_metPhiCorrectionParameters.at(3) * event.m_vertexSummary->nVertices;

            corrMET.p4.SetPt(static_cast<float>(sqrt(px * px + py * py)));
            corrMET.p4.SetPhi(static_cast<float>(atan2(py, px)));
        }

        // Store corrected MET in product
        product.m_corrMET[m_corrLevels[corrLevelIndex]] = corrMET;
    }
}
