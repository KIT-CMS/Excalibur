#include "ZJet/ZJetAnalysis/interface/Producers/GenZProducer.h"


void GenZProducer::ProduceGlobal(ZJetEvent const& event, ZJetProduct& product,
                                         ZJetGlobalSettings const& globalSettings) const
{

	std::vector<KDataLV> genz_candidates;

	// Loop over gen particles
	LOG(INFO) << event.m_genParticles->size();
	for (KGenParticles::iterator it = event.m_genParticles->begin(); it != event.m_genParticles->end(); ++it)
	{
		if (it->pdgid == 23)
			genz_candidates.push_back(*it);
	}

	// no ambiguous Z reconstruction:
	if (genz_candidates.size() != 1)
	{
		product.has_valid_genz = false;
	}
	else
	{
		product.GenZ = genz_candidates[0];
		product.has_valid_genz = true;
	}

}


