#include "Producers/RecoJetGenPartonMatchingProducer.h"

std::string RecoJetGenPartonMatchingProducer::GetProducerId() const {
	return "RecoJetGenPartonMatchingProducer";
}

void RecoJetGenPartonMatchingProducer::Produce(KappaEvent const& event, KappaProduct& product, KappaSettings const& settings) const
{
	// Make ZJet zJetific product and event available
	ZJetEvent const& zJetEvent = static_cast<ZJetEvent const&>(event);
	ZJetProduct const& zJetProduct = static_cast<ZJetProduct const&>(product);
	ZJetSettings const& zJetSettings = static_cast<ZJetSettings const&>(settings);
		
	// Iterate over all jet correction levels
	for (std::map<std::string, std::vector<std::shared_ptr<KJet> > >::const_iterator
	     itlevel = zJetProduct.m_correctedZJets.begin();
	     itlevel != zJetProduct.m_correctedZJets.end(); ++itlevel)
	{
		// Iterate over all jets and match them to partons
		for (std::vector<std::shared_ptr<KJet> >::const_iterator recoJet = itlevel->second.begin(); recoJet != itlevel->second.end(); ++recoJet)
		{
			// Use Artus reco jet gen particle matcher
			KGenParticle* matchedParton = Match(zJetEvent, zJetProduct, zJetSettings, static_cast<KLV*>((*recoJet).get()));
			if (matchedParton != NULL)
			{
				// Map of reco jets and matched gen partons for all requested correction levels
				zJetProduct.m_matchedGenPartons[itlevel->first][(*recoJet).get()] = matchedParton;
			}
		}
	}
}
