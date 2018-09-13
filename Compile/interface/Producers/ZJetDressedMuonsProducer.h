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




