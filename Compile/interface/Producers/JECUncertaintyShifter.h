#pragma once

#include <memory>

#include "Excalibur/Compile/interface/ZJetTypes.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

/** Producer applying the JEC uncertainty shift to the corrected jets
 *
 *  Each jet of every correction level derived from L1L2L3 (all levels except L1 and RC) is
 *  scaled by (1 + shift * u), with u evaluated at the jet's current pT and eta. Running after
 *  the JERSmearer, this is the smeared nominal pT, as in nanoAOD-tools and coffea.
 *
 *  Configuration settings:
 *  - JetEnergyCorrectionUncertaintySource (name of the source, 'Total' for the full uncertainty)
 *  - JetEnergyCorrectionUncertaintyShift (direction and scale of the shift; 0: do nothing)
 *
 *  Must run after the ZJetCorrectionsProducer and the JERSmearer (if present) and before the
 *  TypeIMETProducer, so that the type-I MET follows the shifted jets.
 */

class JECUncertaintyShifter : public ZJetProducerBase
{
  public:
    std::string GetProducerId() const override;

    JECUncertaintyShifter() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  private:
    std::unique_ptr<JetCorrectionUncertainty> m_correctionUncertainty;
};
