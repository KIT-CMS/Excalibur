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
    float m_sf[30][30] = {};
    float m_er[30][30] = {};
    float m_sfdata[30][30] = {};
    float m_erdata[30][30] = {};
    float m_sfmc[30][30] = {};
    float m_ermc[30][30] = {};
    std::vector<float> m_xbins = {};
    std::vector<float> m_ybins = {};
    std::vector<float>* m_etabins = {};
    std::vector<float>* m_ptbins = {};
    std::string m_sffile;
    std::string m_id;
    std::string histoname;
    std::vector<int> runs;
    bool m_reversed_axes = false;
    bool m_absoluteeta = true;
    bool m_etaonly;

    virtual float GetScaleFactor(int type, float err_shift, KLV const& lepton) const
    {
        for (unsigned int index_eta = 0; index_eta < m_etabins->size() - 1; ++index_eta) {
            if (GetEta(lepton) >= m_etabins->at(index_eta) &&
                GetEta(lepton) < m_etabins->at(index_eta + 1)) {
                for (unsigned int index_pt = 0; index_pt < m_ptbins->size() - 1; ++index_pt) {
                    if ((lepton.p4.Pt()) >= m_ptbins->at(index_pt) &&
                        (lepton.p4.Pt()) < m_ptbins->at(index_pt + 1)) {
                        if (m_reversed_axes) {
                            if (type == 0)
                                return m_sf[index_pt][index_eta] + err_shift*m_er[index_pt][index_eta];
                            if (type == 1)
                                return m_sfdata[index_pt][index_eta] + err_shift*m_erdata[index_pt][index_eta];
                            if (type == 2)
                                return m_sfmc[index_pt][index_eta] + err_shift*m_ermc[index_pt][index_eta];
                        }
                        else {
                            if (type == 0)
                                return m_sf[index_eta][index_pt] + err_shift*m_er[index_eta][index_pt];
                            if (type == 1)
                                return m_sfdata[index_eta][index_pt] + err_shift*m_erdata[index_eta][index_pt];
                            if (type == 2)
                                return m_sfmc[index_eta][index_pt] + err_shift*m_ermc[index_eta][index_pt];
                        }
                    }
                }
                if (m_reversed_axes) {
                    if (type == 0)
                        return m_sf[m_ptbins->size()-2][index_eta] + err_shift*m_er[m_ptbins->size()-2][index_eta];
                    if (type == 1)
                        return m_sfdata[m_ptbins->size()-2][index_eta] + err_shift*m_erdata[m_ptbins->size()-2][index_eta];
                    if (type == 2)
                        return m_sfmc[m_ptbins->size()-2][index_eta] + err_shift*m_ermc[m_ptbins->size()-2][index_eta];
                }
                else {
                    if (type == 0)
                        return m_sf[index_eta][m_ptbins->size()-2] + err_shift*m_er[index_eta][m_ptbins->size()-2];
                    if (type == 1)
                        return m_sfdata[index_eta][m_ptbins->size()-2] + err_shift*m_erdata[index_eta][m_ptbins->size()-2];
                    if (type == 2)
                        return m_sfmc[index_eta][m_ptbins->size()-2] + err_shift*m_ermc[index_eta][m_ptbins->size()-2];
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

class LeptonIDSFProducer : public LeptonSFProducer{
    public:
        std::string GetProducerId() const override;
        LeptonIDSFProducer() : LeptonSFProducer() {}
    void Init(ZJetSettings const& settings) override;
    void Produce(ZJetEvent const& event,
                ZJetProduct& product,
                ZJetSettings const& settings) const override;
};

class LeptonIsoSFProducer : public LeptonSFProducer{
    public:
        std::string GetProducerId() const override;
        LeptonIsoSFProducer() : LeptonSFProducer() {}
    void Init(ZJetSettings const& settings) override;
    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;
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

class LeptonTrackingSFProducer : public LeptonSFProducer{
    public:
        std::string GetProducerId() const override;
        LeptonTrackingSFProducer() : LeptonSFProducer() {}
    void Init(ZJetSettings const& settings) override;
    void Produce(ZJetEvent const& event,
                ZJetProduct& product,
                ZJetSettings const& settings) const override;
 };
