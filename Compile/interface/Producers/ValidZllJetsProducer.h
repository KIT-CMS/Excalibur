#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"

class ValidZllJetsProducer : public ZJetProducerBase
{
  public:
    ValidZllJetsProducer() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    std::string GetProducerId() const override;
    
    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override {

        product.m_validJets.erase( 
                std::remove_if( product.m_validJets.begin(),product.m_validJets.end(), 
                    [&, this](auto jetSharedPtr){
                        return !this->DoesntJetPass(jetSharedPtr, event, product, settings);
                    }),
                product.m_validJets.end()
            );
    };
    virtual bool DoesntJetPass(const KBasicJet* jet, ZJetEvent const& event, ZJetProduct const& product, ZJetSettings const& settings) const;

  private:
    float minZllJetDeltaRVeto;
    float minPUJetID;
};

class ValidZllGenJetsProducer : public ZJetProducerBase
{
  public:
    ValidZllGenJetsProducer() : ZJetProducerBase(), minZllJetDeltaRVeto(0) {}

    void Init(ZJetSettings const& settings) override;

    std::string GetProducerId() const override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  private:
    float minZllJetDeltaRVeto;
};
