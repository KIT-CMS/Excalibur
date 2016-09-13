#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"

#include "Artus/KappaAnalysis/interface/Producers/ValidElectronsProducer.h"

class ZJetValidElectronsProducer : public ValidElectronsProducer<ZJetTypes>
{
  public:
    std::string GetProducerId() const override { return "ZJetValidElectronsProducer"; }

    virtual void Init(setting_type const& settings) override
    {
        ValidElectronsProducer<ZJetTypes>::Init(settings);
        m_excludeECALgap = settings.GetExcludeECALGap();
    }

  protected:
    // ZJet specific additional definitions
    bool AdditionalCriteria(KElectron* electron,
                            event_type const& event,
                            product_type& product,
                            setting_type const& settings) const override
    {
        // either m_excludeECALgap is false (directly return true) or check electron eta
        return ((!m_excludeECALgap) ||
                (std::abs(electron->p4.Eta()) < 1.442f || std::abs(electron->p4.Eta()) > 1.566f));
    }

    bool m_excludeECALgap;
};
