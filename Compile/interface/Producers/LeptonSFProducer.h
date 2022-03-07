#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"

#include "TH2.h"

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
    std::string m_sffile;
    std::string histoname;
    std::string weightName;
    bool m_reversed_axes;
    bool m_absoluteEta;
    TH2F* sfhisto;

    virtual void SetEtaAxis2D(std::string histoname);
    virtual void SetOverflowPtBin();
    virtual std::tuple<float, float> GetScaleFactorAndUnc(KLV const& lepton) const;
};

class LeptonIDSFProducer : public LeptonSFProducer
{
  public:
    std::string GetProducerId() const override;
    LeptonIDSFProducer() : LeptonSFProducer() {}
    void Init(ZJetSettings const& settings) override;
};

class LeptonIsoSFProducer : public LeptonSFProducer
{
  public:
    std::string GetProducerId() const override;
    LeptonIsoSFProducer() : LeptonSFProducer() {}
    void Init(ZJetSettings const& settings) override;
};

class LeptonTriggerSFProducer : public LeptonSFProducer
{
  public:
    std::string GetProducerId() const override;
    LeptonTriggerSFProducer() : LeptonSFProducer() {}
    void Init(ZJetSettings const& settings) override;
    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;
};

class LeptonTrackingSFProducer : public LeptonSFProducer
{
  public:
    std::string GetProducerId() const override;
    LeptonTrackingSFProducer() : LeptonSFProducer() {}
    void Init(ZJetSettings const& settings) override;
};

class LeptonRecoSFProducer : public LeptonSFProducer
{
  public:
    std::string GetProducerId() const override;
    LeptonRecoSFProducer() : LeptonSFProducer() {}
    void Init(ZJetSettings const& settings) override;

  protected:
    void SetOverflowPtBin() override;
    std::tuple<float, float> GetScaleFactorAndUnc(KLV const& lepton) const override;
    std::tuple<float, float> GetHighPtEff(KLV const& lepton) const;
    std::string m_year;

};
