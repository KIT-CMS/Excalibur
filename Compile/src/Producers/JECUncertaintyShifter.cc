#include <algorithm>
#include <cmath>

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"

#include "Excalibur/Compile/interface/Producers/JECUncertaintyShifter.h"
#include "Excalibur/Compile/interface/Producers/ZJetCorrectionsProducer.h"

std::string JECUncertaintyShifter::GetProducerId() const { return "JECUncertaintyShifter"; }

void JECUncertaintyShifter::Init(ZJetSettings const& settings)
{
    ZJetProducerBase::Init(settings);

    // check the position in the processor chain
    std::vector<std::string> processors = settings.GetGlobalProcessors();
    auto position = [&processors](std::string const& name) {
        return std::find(processors.begin(), processors.end(), name) - processors.begin();
    };
    const long self = position("producer:" + GetProducerId());
    const long nProcessors = processors.size();
    if (position("producer:ZJetCorrectionsProducer") >= self) {
        LOG(FATAL) << GetProducerId() << " must run after the ZJetCorrectionsProducer.";
    }
    if (position("producer:JERSmearer") < nProcessors && position("producer:JERSmearer") > self) {
        LOG(FATAL) << GetProducerId() << " must run after the JERSmearer.";
    }
    if (position("producer:TypeIMETProducer") < self) {
        LOG(FATAL) << GetProducerId() << " must run before the TypeIMETProducer.";
    }

    if (settings.GetJetEnergyCorrectionUncertaintyShift() == 0.0) {
        LOG(INFO) << "\t -- Using mean JEC values. No JetEnergyCorrectionUncertaintyShift supplied.";
        return;
    }
    std::string fname_unc = settings.GetJec() + "_UncertaintySources_" +
                            ZJetCorrectionsProducer::GetJecAlgoName(settings) + ".txt";
    if (settings.GetJetEnergyCorrectionUncertaintySource().empty()) {
        LOG(FATAL) << "Undefined JetEnergyCorrectionUncertaintySource. Use 'Total' for full uncertainty.";
    }
    JetCorrectorParameters jecUncertaintyParameters(fname_unc, settings.GetJetEnergyCorrectionUncertaintySource());
    if ((!jecUncertaintyParameters.isValid()) || (jecUncertaintyParameters.size() == 0)) {
        LOG(FATAL) << "Invalid definition " << settings.GetJetEnergyCorrectionUncertaintySource() << " in file " << fname_unc;
    }
    LOG(INFO) << "\t -- Enabling JEC Uncertainty " << settings.GetJetEnergyCorrectionUncertaintySource()
              << " (shift " << settings.GetJetEnergyCorrectionUncertaintyShift() << ") from file " << fname_unc;
    m_correctionUncertainty.reset(new JetCorrectionUncertainty(jecUncertaintyParameters));
}

void JECUncertaintyShifter::Produce(ZJetEvent const& event,
                                    ZJetProduct& product,
                                    ZJetSettings const& settings) const
{
    const float shift = settings.GetJetEnergyCorrectionUncertaintyShift();
    if (shift == 0.0f) {
        return;
    }
    for (auto* jetsPerLevel : {&product.m_correctedZJets, &product.m_correctedInvalidJets}) {
        for (auto& level : *jetsPerLevel) {
            if (level.first == "L1" || level.first == "RC") {
                continue;
            }
            for (auto& jet : level.second) {
                // same eta range as KappaTools correctJets
                if (std::abs(jet->p4.Eta()) < 5.4f) {
                    m_correctionUncertainty->setJetEta(jet->p4.Eta());
                    m_correctionUncertainty->setJetPt(jet->p4.Pt());
                    jet->p4 *= static_cast<float>(1.0f + shift * m_correctionUncertainty->getUncertainty(shift > 0.0f));
                }
            }
        }
    }
}
