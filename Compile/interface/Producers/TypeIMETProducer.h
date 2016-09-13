#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"

/** Apply TypeI corrections to MET: Iterate over jets and subtract L2L3(Res)
 *
 *	https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMetAnalysis#Type_I_Correction
 */

class TypeIMETProducer : public ZJetProducerBase
{
  public:
    std::string GetProducerId() const;

    TypeIMETProducer() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings);

    void Produce(ZJetEvent const& event, ZJetProduct& product, ZJetSettings const& settings) const;

  private:
    std::string m_l1Corr;
    std::vector<std::string> m_corrLevels;
    std::vector<double> m_metPhiCorrectionParameters;
};
