#pragma once

#include "ZJetTypes.h"

class ElectronSFProducer : public ZJetProducerBase
{
  public:
    virtual std::string GetProducerId() const override;

    ElectronSFProducer() : ZJetProducerBase(){};

    virtual void Init(ZJetSettings const& settings) override;

    virtual void Produce(ZJetEvent const& event,
                         ZJetProduct& product,
                         ZJetSettings const& settings) const override;

  private:
    float m_sf[12][12];
    std::vector<float> m_xbins;
    std::vector<float> m_ybins;
    std::vector<float>* m_etabins;
    std::vector<float>* m_ptbins;
    std::string m_sffile;
    std::string m_id;
    bool m_reversed_axes;
    bool m_absoluteeta;

    virtual float GetScaleFactor(KLV const& electron) const
    {
        for (unsigned int index_eta = 0; index_eta < m_etabins->size() - 1; index_eta++) {
            if (GetEta(electron) >= m_etabins->at(index_eta) &&
                GetEta(electron) < m_etabins->at(index_eta + 1)) {
                for (unsigned int index_pt = 0; index_pt < m_ptbins->size() - 1; index_pt++) {
                    if ((electron.p4.Pt()) >= m_ptbins->at(index_pt) &&
                        (electron.p4.Pt()) < m_ptbins->at(index_pt + 1)) {
                        if (m_reversed_axes) {
                            return m_sf[index_pt][index_eta];
                        } else {
                            return m_sf[index_eta][index_pt];
                        }
                    }
                }
                return 1.;  // not in pt bins
            }
        }
        return 1.;
    }

    virtual float GetEta(KLV const& e) const
    {
        if (m_absoluteeta)
            return std::abs(e.p4.Eta());
        else
            return e.p4.Eta();
    }
};
