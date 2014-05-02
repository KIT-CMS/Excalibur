#include "ZJet/ZJetAnalysis/interface/Producers/GenZProducer.h"


void GenZProducer::ProduceGlobal(ZJetEvent const& event, ZJetProduct& product,
                                         ZJetGlobalSettings const& globalSettings) const
{

	KGenParticles genz_candidates;

	// Loop over gen particles
	for (KGenParticles::iterator it = event.m_genParticles->begin(); it != event.m_genParticles->end(); ++it)
	{
		if (it->pdgId() == 23)
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


