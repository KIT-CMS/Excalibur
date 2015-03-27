/*
 * 
 * Code for multiple jet collections.
 * This requires a small change in ValidJetsProducer in Artus (outsourcing the actual jet validation).
 * 
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/ValidJetsProducer.h"

#include "ZJetTypes.h"


// Producer for valid tagged jets.
   
class ZJetValidTaggedJetsProducer: public ValidTaggedJetsProducer
{

public:

	// TODO: Init function needs to be overwritten too since it uses m_validJets which is a map in our case

	void Produce(KappaEvent const& event, KappaProduct& product,
	             KappaSettings const& settings) const
	{
		// Make ZJet specific product and event available
		ZJetProduct const& specProduct = static_cast<ZJetProduct const&>(product);
		ZJetEvent const& specEvent = static_cast<ZJetEvent const&>(event);
		
		// Iterate over all jet collections
		for (std::map<std::string, KJets*>::const_iterator italgo = specEvent.m_jets.begin(); italgo != specEvent.m_jets.end(); ++italgo)
		{
			// create local temporary jet vectors
			std::vector<KJet*> validJets;
			std::vector<KJet*> invalidJets;

			// Iterate over all jets in collection and validate them
			for (std::vector<KJet>::iterator jet = italgo->second->begin(); jet != italgo->second->end(); ++jet)
			{
				if (IsValidJet(&(*jet), event, product, settings))
				{
					validJets.push_back(&(*jet));
				}
				else
				{
					invalidJets.push_back(&(*jet));
				}
			}

			// Store valid and invalid jets in product
			specProduct.m_validZJets[italgo->first] = validJets;
			specProduct.m_invalidZJets[italgo->first] = invalidJets;

			LOG(INFO) << "valid jets: " << specProduct.m_validZJets[italgo->first].size() << " invalid jets: " << specProduct.m_invalidZJets[italgo->first].size();
		}
	}
};
*/
