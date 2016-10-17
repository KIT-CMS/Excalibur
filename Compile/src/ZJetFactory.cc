#include "Excalibur/Compile/interface/ZJetFactory.h"

// producers
#include "Excalibur/Compile/interface/Producers/ValidZllJetsProducer.h"
#include "Excalibur/Compile/interface/Producers/TypeIMETProducer.h"
#include "Excalibur/Compile/interface/Producers/ZJetCorrectionsProducer.h"
#include "Excalibur/Compile/interface/Producers/JetSorter.h"
#include "Excalibur/Compile/interface/Producers/RecoJetGenPartonMatchingProducer.h"
#include "Excalibur/Compile/interface/Producers/RecoJetGenJetMatchingProducer.h"
#include "Excalibur/Compile/interface/Producers/NPUProducer.h"
#include "Excalibur/Compile/interface/Producers/ZJetNumberGeneratedEventsWeightProducer.h"
#include "Excalibur/Compile/interface/Producers/ZJetValidElectronsProducer.h"
#include "Excalibur/Compile/interface/Producers/NeutrinoCounter.h"
#include "Excalibur/Compile/interface/Producers/LeptonSFProducer.h"
// filters
#include "Excalibur/Compile/interface/Filters/ZJetCutsFilter.h"

// consumers
#include "Excalibur/Compile/interface/Consumers/ZJetTreeConsumer.h"

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
    else if (id == NeutrinoCounter().GetProducerId())
        return new NeutrinoCounter();
    else if (id == LeptonSFProducer().GetProducerId())
        return new LeptonSFProducer();
    else if (id == LeptonTriggerSFProducer().GetProducerId())
        return new LeptonTriggerSFProducer();
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
