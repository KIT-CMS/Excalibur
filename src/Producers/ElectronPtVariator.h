#pragma once

#include "ZJetTypes.h"

class ElectronPtVariator : public ZJetProducerBase
{
  public:
    std::string GetProducerId() const override;

    ElectronPtVariator() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  private:
    float m_sf[12][12] = {};
    std::vector<float> m_etabins = {};
    std::vector<float> m_ptbins = {};

    virtual float GetScaleFactor(KLV* electron) const
    {
        for (unsigned int index_eta = 0; index_eta < m_etabins.size() - 1; ++index_eta) {
            if (std::abs(electron->p4.Eta()) >= m_etabins.at(index_eta) &&
                std::abs(electron->p4.Eta()) < m_etabins.at(index_eta + 1)) {
                for (unsigned int index_pt = 0; index_pt < m_ptbins.size() - 1; ++index_pt) {
                    if ((electron->p4.Pt()) >= m_ptbins.at(index_pt) &&
                        (electron->p4.Pt()) < m_ptbins.at(index_pt + 1)) {
                        return m_sf[index_pt][index_eta];
                    }
                }
                return 1.0f;  // not in pt bins
            }
        }
        return 1.0f;
    }
};
