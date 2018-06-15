#include "Excalibur/Compile/interface/ZJetFactory.h"

// producers
#include "Excalibur/Compile/interface/Producers/ValidZllJetsProducer.h"
#include "Excalibur/Compile/interface/Producers/TypeIMETProducer.h"
#include "Excalibur/Compile/interface/Producers/ZJetCorrectionsProducer.h"
#include "Excalibur/Compile/interface/Producers/JetSorter.h"
#include "Excalibur/Compile/interface/Producers/JetCleaner.h"
#include "Excalibur/Compile/interface/Producers/JetRecoilProducer.h"
#include "Excalibur/Compile/interface/Producers/RecoJetGenPartonMatchingProducer.h"
#include "Excalibur/Compile/interface/Producers/RecoJetGenJetMatchingProducer.h"
#include "Excalibur/Compile/interface/Producers/NPUProducer.h"
#include "Excalibur/Compile/interface/Producers/ZJetNumberGeneratedEventsWeightProducer.h"
#include "Excalibur/Compile/interface/Producers/ZJetValidElectronsProducer.h"
#include "Excalibur/Compile/interface/Producers/NeutrinoCounter.h"
#include "Excalibur/Compile/interface/Producers/LeptonSFProducer.h"
#include "Excalibur/Compile/interface/Producers/ZProducer.h"
#include "Excalibur/Compile/interface/Producers/ZJetGenParticleProducer.h"
// filters
#include "Excalibur/Compile/interface/Filters/ZJetCutsFilter.h"

// consumers
#include "Excalibur/Compile/interface/Consumers/ZJetTreeConsumer.h"

ProducerBaseUntemplated* ZJetFactory::createProducer(std::string const& id)
{
    if (id == ValidZllJetsProducer().GetProducerId())
        return new ValidZllJetsProducer();
    else if (id == ValidZllGenJetsProducer().GetProducerId())
        return new ValidZllGenJetsProducer();
    else if (id == TypeIMETProducer().GetProducerId())
        return new TypeIMETProducer();
    else if (id == ZJetCorrectionsProducer().GetProducerId())
        return new ZJetCorrectionsProducer();
    else if (id == JetSorter().GetProducerId())
        return new JetSorter();
    else if (id == JetEtaPhiCleaner().GetProducerId())
        return new JetEtaPhiCleaner();
    else if (id == JetRecoilProducer().GetProducerId())
        return new JetRecoilProducer();
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
    else if (id == LeptonIDSFProducer().GetProducerId())
        return new LeptonIDSFProducer();
    else if (id == LeptonIsoSFProducer().GetProducerId())
        return new LeptonIsoSFProducer();
    else if (id == LeptonTrackingSFProducer().GetProducerId())
        return new LeptonTrackingSFProducer();
    else if (id == LeptonTriggerSFProducer().GetProducerId())
        return new LeptonTriggerSFProducer();
    else if(id == RecoZmmProducer().GetProducerId())
        return new RecoZmmProducer();
    else if(id == RecoZeeProducer().GetProducerId())
        return new RecoZeeProducer();
    else if(id == RecoZemProducer().GetProducerId())
        return new RecoZemProducer();
    else if(id == RecoZeemmProducer().GetProducerId())
        return new RecoZeemmProducer();
    else if(id == GenZmmProducer().GetProducerId())
        return new GenZmmProducer();
    else if(id == ValidGenZmmProducer().GetProducerId())
        return new ValidGenZmmProducer();	
    else if(id == GenZeeProducer().GetProducerId())
        return new GenZeeProducer();
    else if(id == GenZemProducer().GetProducerId())
        return new GenZemProducer();
    else if(id == GenZeemmProducer().GetProducerId())
        return new GenZeemmProducer();
    else if(id == ZJetGenMuonProducer().GetProducerId())
        return new ZJetGenMuonProducer();
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
    else if (id == GenMuonPtCut().GetFilterId())
        return new GenMuonPtCut();
    else if (id == GenMuonEtaCut().GetFilterId())
        return new GenMuonEtaCut();
    else if (id == ElectronPtCut().GetFilterId())
        return new ElectronPtCut();
    else if (id == ElectronEtaCut().GetFilterId())
        return new ElectronEtaCut();
    else if (id == LeadingJetPtCut().GetFilterId())
        return new LeadingJetPtCut();
    else if (id == LeadingJetEtaCut().GetFilterId())
        return new LeadingJetEtaCut();
    else if (id == LeadingGenJetYCut().GetFilterId())
        return new LeadingGenJetYCut();
    else if (id == LeadingJetYCut().GetFilterId())
        return new LeadingJetYCut();
    else if (id == ZPtCut().GetFilterId())
        return new ZPtCut();
    else if (id == GenZPtCut().GetFilterId())
        return new GenZPtCut();
    else if (id == GenHTCut().GetFilterId())
		return new GenHTCut();
	else if (id == BackToBackCut().GetFilterId())
        return new BackToBackCut();
    else if (id == EtaPhiCleaningCut().GetFilterId())
        return new EtaPhiCleaningCut();
    else if (id == JetIDCut().GetFilterId())
        return new JetIDCut();
    else if (id == MinNMuonsCut().GetFilterId())
        return new MinNMuonsCut();
    else if (id == MaxNMuonsCut().GetFilterId())
        return new MaxNMuonsCut();
    else if (id == MinNGenMuonsCut().GetFilterId())
        return new MinNGenMuonsCut();
    else if (id == MaxNGenMuonsCut().GetFilterId())
        return new MaxNGenMuonsCut();
    else if (id == AlphaCut().GetFilterId())
        return new AlphaCut();
    else if (id == ValidZCut().GetFilterId())
        return new ValidZCut();
    else if (id == ValidGenZCut().GetFilterId())
        return new ValidGenZCut();
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
