#include "Producers/RecoJetGenJetMatchingProducer.h"

std::string RecoJetGenJetMatchingProducer::GetProducerId() const {
	return "RecoJetGenJetMatchingProducer";
}

void RecoJetGenJetMatchingProducer::Init(ZJetSettings const& settings)
{
	ZJetProducerBase::Init(settings);
}

void RecoJetGenJetMatchingProducer::Produce(ZJetEvent const& event, ZJetProduct& product,
                                            ZJetSettings const& settings) const
{
	// Iterate over all jet correction levels
	for (std::map<std::string, std::vector<std::shared_ptr<KJet> > >::const_iterator
	     itlevel = product.m_correctedZJets.begin();
	     itlevel != product.m_correctedZJets.end(); ++itlevel)
	{
		// Iterate over all corrected jets to copy them in local object since they are shared pointers and we need actual jets
		unsigned int jetCount = product.GetValidJetCount(settings, event, itlevel->first);
		KJets recoJets(jetCount);
		for (unsigned int jetIndex = 0; jetIndex < jetCount; ++jetIndex)
		{
			recoJets[jetIndex] = *(static_cast<KJet*>(product.GetValidJet(settings, event, jetIndex, itlevel->first)));
		}

		// Make use of KappaTools matcher
		std::vector<int> matchResult = matchSort_Matrix<KLV, KJet>(*(event.m_genJets), event.m_genJets->size(), recoJets, recoJets.size(), settings.GetDeltaRMatchingRecoJetGenJet());

		// Store result in product
		product.m_matchedGenJets[itlevel->first] = matchResult;
	}
}
