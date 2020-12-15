#pragma once

#include <memory>

#include "Excalibur/Compile/interface/ZJetTypes.h"
#include "TH2F.h"

enum fluctuations { central = 0, up, down };


class PrefiringWeightProducer : public ZJetProducerBase
{
    public:
        std::string GetProducerId() const override;
        PrefiringWeightProducer() : ZJetProducerBase() {};
        void Init(ZJetSettings const& settings);
        void Produce(ZJetEvent const& event,
                     ZJetProduct& product,
                     ZJetSettings const& settings) const override;
        enum fluctuations { central = 0, up, down };

    private:
        double m_prefiringRateSysUnc;
        double m_maxPt;
 
        TH2F* h_prefmap_photon;
        TH2F* h_prefmap_jet;
        double getPrefiringRate(double eta, double pt, TH2F* h_prefmap, fluctuations var) const;
        double prefiringRateSystUnc_;
};
