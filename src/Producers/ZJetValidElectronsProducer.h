
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/ValidElectronsProducer.h"

class ZJetValidElectronsProducer : public ValidElectronsProducer<ZJetTypes>
{
  public:
    virtual std::string GetProducerId() const override { return "ZJetValidElectronsProducer"; }

  protected:
    // ZJet specific additional definitions
    virtual bool AdditionalCriteria(KElectron* electron,
                                    event_type const& event,
                                    product_type& product,
                                    setting_type const& settings) const override
    {
        // TODO make this configurable?
        return (std::abs(electron->p4.Eta()) < 1.4442f || std::abs(electron->p4.Eta()) > 1.566f);
    }
};
