#include "ZJetFactory.h"

// producers
#include "Producers/ValidZllJetsProducer.h"
#include "Producers/TypeIMETProducer.h"
#include "Producers/ZJetCorrectionsProducer.h"
#include "Producers/JetSorter.h"
#include "Producers/RecoJetGenPartonMatchingProducer.h"
#include "Producers/RecoJetGenJetMatchingProducer.h"
#include "Producers/NPUProducer.h"
#include "Producers/ZJetNumberGeneratedEventsWeightProducer.h"
#include "Producers/ZJetValidElectronsProducer.h"
#include "Producers/MuonCorrector.h"
#include "Producers/NeutrinoCounter.h"

// filters
#include "Filters/ZJetCutsFilter.h"

// consumers
#include "Consumers/ZJetTreeConsumer.h"

ProducerBaseUntemplated* ZJetFactory::createProducer(std::string const& id)
{
    if (id == ValidZllJetsProducer().GetProducerId())
        return new ValidZllJetsProducer();
    else if (id == TypeIMETProducer().GetProducerId())
        return new TypeIMETProducer();
    else if (id == ZJetCorrectionsProducer().GetProducerId())
        return new ZJetCorrectionsProducer();
    else if (id == JetSorter().GetProducerId())
        return new JetSorter();
    else if (id == RecoJetGenPartonMatchingProducer().GetProducerId())
        return new RecoJetGenPartonMatchingProducer();
    else if (id == RecoJetGenJetMatchingProducer().GetProducerId())
        return new RecoJetGenJetMatchingProducer();
    else if (id == NPUProducer().GetProducerId())
        return new NPUProducer();
    else if (id == ZJetNumberGeneratedEventsWeightProducer().GetProducerId())
        return new ZJetNumberGeneratedEventsWeightProducer();
    else if (id == ZJetValidElectronsProducer().GetProducerId())
        return new ZJetValidElectronsProducer();
    else if (id == MuonCorrector().GetProducerId())
        return new MuonCorrector();
    else if (id == NeutrinoCounter().GetProducerId())
        return new NeutrinoCounter();
    else
        return KappaFactory::createProducer(id);
}

FilterBaseUntemplated* ZJetFactory::createFilter(std::string const& id)
{
    if (id == MinNLeptonsCut().GetFilterId())
        return new MinNLeptonsCut();
    else if (id == MaxNLeptonsCut().GetFilterId())
        return new MaxNLeptonsCut();
    else if (id == LeadingLeptonPtCut().GetFilterId())
        return new LeadingLeptonPtCut();
    else if (id == MuonPtCut().GetFilterId())
        return new MuonPtCut();
    else if (id == MuonEtaCut().GetFilterId())
        return new MuonEtaCut();
    else if (id == ElectronPtCut().GetFilterId())
        return new ElectronPtCut();
    else if (id == ElectronEtaCut().GetFilterId())
        return new ElectronEtaCut();
    else if (id == LeadingJetPtCut().GetFilterId())
        return new LeadingJetPtCut();
    else if (id == LeadingJetEtaCut().GetFilterId())
        return new LeadingJetEtaCut();
    else if (id == ZPtCut().GetFilterId())
        return new ZPtCut();
    else if (id == BackToBackCut().GetFilterId())
        return new BackToBackCut();
    else if (id == MinNMuonsCut().GetFilterId())
        return new MinNMuonsCut();
    else if (id == MaxNMuonsCut().GetFilterId())
        return new MaxNMuonsCut();
    else if (id == AlphaCut().GetFilterId())
        return new AlphaCut();
    else
        return KappaFactory::createFilter(id);
}

ConsumerBaseUntemplated* ZJetFactory::createConsumer(std::string const& id)
{
    if (id == ZJetTreeConsumer().GetConsumerId())
        return new ZJetTreeConsumer();
    else
        return KappaFactory::createConsumer(id);
}
