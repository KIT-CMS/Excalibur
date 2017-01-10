#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"

class LeptonSFProducer : public ZJetProducerBase
{
  public:
    std::string GetProducerId() const override;

    LeptonSFProducer() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  protected:
    float m_sf[12][12][12] = {};
    std::vector<float> m_xbins = {};
    std::vector<float> m_ybins = {};
    std::vector<float>* m_etabins = {};
    std::vector<float>* m_ptbins = {};
    std::string m_sffile;
    std::string m_id;
    std::vector<int> runs;
    bool m_reversed_axes = false;
    bool m_absoluteeta = false;

    virtual float GetScaleFactor(int run_index, KLV const& lepton) const
    {
        for (unsigned int index_eta = 0; index_eta < m_etabins->size() - 1; ++index_eta) {
            if (GetEta(lepton) >= m_etabins->at(index_eta) &&
                GetEta(lepton) < m_etabins->at(index_eta + 1)) {
                for (unsigned int index_pt = 0; index_pt < m_ptbins->size() - 1; ++index_pt) {
                    if ((lepton.p4.Pt()) >= m_ptbins->at(index_pt) &&
                        (lepton.p4.Pt()) < m_ptbins->at(index_pt + 1)) {
                        if (m_reversed_axes) {
                            return m_sf[run_index][index_pt][index_eta];
                        } else {
                            return m_sf[run_index][index_eta][index_pt];
                        }
                    }
                }
		if (m_reversed_axes) {
		    return m_sf[run_index][m_ptbins->size()-2][index_eta];
                } 
                else {
		    return m_sf[run_index][index_eta][m_ptbins->size()-2];
                }
            }
        }
        return 1.0f;
    }

    virtual float GetEta(KLV const& l) const
    {
        if (m_absoluteeta)
            return std::abs(l.p4.Eta());
        else
            return l.p4.Eta();
    }
};

class LeptonTriggerSFProducer : public LeptonSFProducer{
    public:
    	std::string GetProducerId() const override;
    	LeptonTriggerSFProducer() : LeptonSFProducer() {}
	void Init(ZJetSettings const& settings) override;
	void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;
};
