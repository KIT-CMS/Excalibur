#pragma once

#include "ZJetTypes.h"
#include "MuScleFitCorrection/MuScleFitCorrector.h"
#include <Math/LorentzVector.h>

/*
This producer corrects muon momenta
*/

class MuonCorrector : public ZJetProducerBase
{
  public:
    std::string GetProducerId() const override;

    MuonCorrector() : ZJetProducerBase() {}

    ~MuonCorrector()
    {
        delete m_corrector;
        delete m_correctorRunD;
    }

    void Init(ZJetSettings const& settings) override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  private:
    long m_startRunD = 203770;
    bool m_smearing;
    bool m_deterministic;
    bool m_radiationcorr;

    std::string m_parameterfile;
    std::string m_parameterfileRunD;

    MuScleFitCorrector* m_corrector = nullptr;
    MuScleFitCorrector* m_correctorRunD = nullptr;
};
