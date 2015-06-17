#include "Producers/RadiationJetProducer.h"

std::string RadiationJetProducer::GetProducerId() const { return "RadiationJetProducer"; }

void RadiationJetProducer::Init(ZJetSettings const& settings)
{
	ZJetProducerBase::Init(settings);
	m_deltaR = settings.GetDeltaRRadiationJet();
}

void RadiationJetProducer::Produce(ZJetEvent const& event,
			ZJetProduct& product, ZJetSettings const& settings) const
{
	// Get radiation jets for no corrections
	GetRadiationJets("None", event, product, settings);
	
	// Iterate over all jet correction levels
	for (std::map<std::string, std::vector<std::shared_ptr<KJet> > >::const_iterator
	     itlevel = product.m_correctedZJets.begin();
	     itlevel != product.m_correctedZJets.end(); ++itlevel)
	{
		GetRadiationJets(itlevel->first, event, product, settings);
	}
	
}

void RadiationJetProducer::GetRadiationJets(std::string corrLevel, ZJetEvent const& event,
                                            ZJetProduct& product, ZJetSettings const& settings) const
{
	unsigned int jetCount = product.GetValidJetCount(settings, event, corrLevel);
	// Reserve memory for 10 radiation jets to avoid reallocation
	product.m_radiationJets[corrLevel].clear();
	product.m_radiationJets[corrLevel].reserve(10);
	product.m_radiationJetsIndex[corrLevel].clear();
	product.m_radiationJetsIndex[corrLevel].reserve(10);

	KJet* primaryJet = static_cast<KJet*>(product.GetValidJet(settings, event, 0, corrLevel));
	for (unsigned int jetIndex = 1; jetIndex < jetCount; ++jetIndex)
	{
		KJet* jet = static_cast<KJet*>(product.GetValidJet(settings, event, jetIndex, corrLevel));
		double jetDeltaR = ROOT::Math::VectorUtil::DeltaR(jet->p4, primaryJet->p4);
		if (jetDeltaR < m_deltaR)
		{
			product.m_radiationJets[corrLevel].push_back(jet);
			product.m_radiationJetsIndex[corrLevel].push_back(jetIndex);
		}
	}
}
