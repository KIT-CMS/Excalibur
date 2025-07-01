#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"

#include "Artus/KappaAnalysis/interface/Producers/ValidMuonsProducer.h"
/*
 * ZJetDressedMuonsProducer
 * ==========================
 *
 * Extends the Artus/KappaAnalysis ValidMuonsProducer.
 *
 * Implements the following dressed muon definition:
 *    - dressed muons include the surrounding photons
 *      -> FSR can be estimated
 *    - applies object-level cuts after dressing:
 *      -> MinMuonPt: minimum pT cut (if UseObjectMuonPtCut enabled)
 *      -> MaxMuonEta: maximum eta cut (if UseObjectMuonEtaCut enabled)
 *
 */

class ZJetDressedMuonsProducer : public ZJetProducerBase
{
  public:
    std::string GetProducerId() const override;
    
    ZJetDressedMuonsProducer() : ZJetProducerBase() {}
        
    void Init(ZJetSettings const& settings) override;


    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  private:
    float maxZJetDressedMuonDeltaR;
    float m_minMuonPt;
    float m_maxMuonEta;
    bool m_useObjectMuonPtCut;
    bool m_useObjectMuonEtaCut;
};

class ZJetDressedGenMuonsProducer : public ZJetProducerBase
{
  public:
    ZJetDressedGenMuonsProducer() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    std::string GetProducerId() const override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;
                 
private:
    float maxZJetDressedMuonDeltaR;
    float m_minMuonPt;
    float m_maxMuonEta;
    bool m_useObjectMuonPtCut;
    bool m_useObjectMuonEtaCut;
    bool m_objectTauMuons;
};

class ZJetTrueGenMuonsProducer : public ZJetProducerBase
{
  public:
    ZJetTrueGenMuonsProducer() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    std::string GetProducerId() const override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;
                 
    int FindMom(int idx, ZJetEvent const& event) const;
};

class ZJetGenPhotonsProducer : public ZJetProducerBase
{
  public:
    ZJetGenPhotonsProducer() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    std::string GetProducerId() const override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

};




