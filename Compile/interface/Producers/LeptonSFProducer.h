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
    bool m_etarev2D[3] = {};
    bool m_reversed_axes;
    bool m_absoluteeta;
    bool m_2D;

    //virtual float GetScaleFactor(int type, float err_shift, KLV const& lepton) const
    virtual float GetScaleFactor(float err_shift, KLV const& lepton) const
    {
        // type: 0 -> Data/MC scale factor; 1 -> Data; 2 -> MC;
        for (unsigned int index_eta = 0; index_eta < m_etabins->size() - 1; ++index_eta) {
            if (GetEta(lepton) >= m_etabins->at(index_eta) &&
                GetEta(lepton) < m_etabins->at(index_eta + 1)) {
                for (unsigned int index_pt = 0; index_pt < m_ptbins->size() - 1; ++index_pt) {
                    if ((lepton.p4.Pt()) >= m_ptbins->at(index_pt) &&
                        (lepton.p4.Pt()) < m_ptbins->at(index_pt + 1)) {
                        if (m_reversed_axes) {
                            //if (type == 0)
                                return m_sf[index_pt][index_eta] + err_shift*m_er[index_pt][index_eta];
                            //if (type == 1)
                            //    return m_sfdata[index_pt][index_eta] + err_shift*m_erdata[index_pt][index_eta];
                            //if (type == 2)
                            //    return m_sfmc[index_pt][index_eta] + err_shift*m_ermc[index_pt][index_eta];
                        }
                        else {
                            //if (type == 0)
                                return m_sf[index_eta][index_pt] + err_shift*m_er[index_eta][index_pt];
                            //if (type == 1)
                            //    return m_sfdata[index_eta][index_pt] + err_shift*m_erdata[index_eta][index_pt];
                            //if (type == 2)
                            //    return m_sfmc[index_eta][index_pt] + err_shift*m_ermc[index_eta][index_pt];
                        }
                    }
                }
                if (m_reversed_axes) {
                    //if (type == 0)
                        return m_sf[m_ptbins->size()-2][index_eta] + err_shift*m_er[m_ptbins->size()-2][index_eta];
                    //if (type == 1)
                    //    return m_sfdata[m_ptbins->size()-2][index_eta] + err_shift*m_erdata[m_ptbins->size()-2][index_eta];
                    //if (type == 2)
                    //    return m_sfmc[m_ptbins->size()-2][index_eta] + err_shift*m_ermc[m_ptbins->size()-2][index_eta];
                }
                else {
                    //if (type == 0)
                        return m_sf[index_eta][m_ptbins->size()-2] + err_shift*m_er[index_eta][m_ptbins->size()-2];
                    //if (type == 1)
                    //    return m_sfdata[index_eta][m_ptbins->size()-2] + err_shift*m_erdata[index_eta][m_ptbins->size()-2];
                    //if (type == 2)
                    //    return m_sfmc[index_eta][m_ptbins->size()-2] + err_shift*m_ermc[index_eta][m_ptbins->size()-2];
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
    /*virtual bool GetReversedAxes(float err_shift, KLV const& lepton) const
    {
        
    }
    */
    virtual bool GetEtaAxis2D(bool* m_etarev2D,std::string histoname) const
    {
        // m_etarev2D contains {m_absoluteeta,m_reversed_axes,m_2D}
        // map with eta on x, pt on y is default!
        if (histoname.find("abseta") != std::string::npos) {
            m_etarev2D[0] = true;
            if (histoname.find("abseta_pt") != std::string::npos) {
                LOG(INFO) << "abs(eta)-pt map used for Lepton Trigger scale factor";
                m_etarev2D[1] = false;
                m_etarev2D[2] = true;
            }
            else if (histoname.find("pt_abseta") != std::string::npos) {
                LOG(INFO) << "pt-abs(eta) map (reversed axes) used for Lepton Trigger scale factor";
                m_etarev2D[1] = true;
                m_etarev2D[2] = true;
            }
            else {
                LOG(INFO) << "abs(eta) map used for Lepton Trigger scale factor";
                m_etarev2D[1] = false;
                m_etarev2D[2] = false;
                //LOG(ERROR) << "neither pt-abs(eta) nor abs(eta)-pt map found for Lepton Trigger scale factor";
            }
        }
        // Attention: abseta needs to be caught in advance!
        else if (histoname.find("eta") != std::string::npos) {
            m_etarev2D[0] = false;
            if ( histoname.find("eta_pt") != std::string::npos) {
                LOG(INFO) << "eta-pt map used for Lepton Trigger scale factor";
                m_etarev2D[1] = false;
                m_etarev2D[2] = true;
            }
            else if (histoname.find("pt_eta") != std::string::npos) {
                LOG(INFO) << "pt-eta map (reversed axes) used for Lepton Trigger scale factor";
                m_etarev2D[1] = true;
                m_etarev2D[2] = true;
            }
            else {
                LOG(INFO) << "eta map used for Lepton Trigger scale factor";
                m_etarev2D[1] = false;
                m_etarev2D[2] = false;
                //LOG(ERROR) << "neither pt-eta nor eta-pt map found for Lepton Trigger scale factor";
            }
        }
        else if (histoname.find("pt") != std::string::npos) {
                LOG(INFO) << "pt map used for Lepton Trigger scale factor";
                m_etarev2D[1] = true;
                m_etarev2D[2] = false;
            }
        else
            LOG(ERROR) << "neither abs(eta), eta nor pt map found for Lepton Trigger scale factor";
        return 0;
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

class LeptonRecoSFProducer : public LeptonSFProducer{
  public:
    std::string GetProducerId() const override;
    LeptonRecoSFProducer() : LeptonSFProducer() {}
    void Init(ZJetSettings const& settings) override;
    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;
};

