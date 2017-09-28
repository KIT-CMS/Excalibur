#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"

#include "Artus/KappaAnalysis/interface/Producers/NumberGeneratedEventsWeightProducer.h"

/*
    This producer does the reweighting with the NumberGeneratedEvents.

    If 'SampleReweighting' is true, the internal cross section is compared to the
    values given in the settings-list 'SampleReweightingCrossSections'. If both
    math within n_tolerance, the NumberGeneratedEvents is taken from the list
    'SampleReweightingNEvents' with the index i of the matching cross-section.

    This allows to process different datasets with different cross-sections,  e.g.
    binned QCD samples, in one Artus run.
*/

class ZJetNumberGeneratedEventsWeightProducer : public NumberGeneratedEventsWeightProducer
{
  public:
    ZJetNumberGeneratedEventsWeightProducer() {}

    std::string GetProducerId() const override { return "ZJetNumberGeneratedEventsWeightProducer"; }

    void Init(KappaSettings const& settings) override { m_tolerance = 0.1; }

    void Produce(KappaEvent const& event,
                 KappaProduct& product,
                 KappaSettings const& settings) const override
    {
        ZJetSettings const& specSettings = static_cast<ZJetSettings const&>(settings);

        if (specSettings.GetSampleReweighting()) {
            std::vector<double> const& xsections = specSettings.GetSampleReweightingCrossSections();
            std::vector<int> const& nevents = specSettings.GetSampleReweightingNEvents();
            assert(xsections.size() == nevents.size());

            // iterate over xsecs, find matching and get NEvents
            for (unsigned int i = 0; i < xsections.size(); ++i) {
                if (std::abs(1.0 - event.m_genRunInfo->xSectionInt / xsections[i]) < m_tolerance) {
                    product.m_weights["numberGeneratedEventsWeight"] = 1.0 / nevents.at(i);
                    return;
                }
            }
            LOG(FATAL) << "No reweighting possible for internal cross-section "
                       << event.m_genRunInfo->xSectionInt;
        } else {
            NumberGeneratedEventsWeightProducer::Produce(event, product, settings);
        }
    }

  private:
    double m_tolerance = 0;
};
