
#pragma once

#include "Artus/KappaAnalysis/interface/KappaEvent.h"

class ZJetEvent : public KappaEvent
{
  public:
	ZJetEvent() : KappaEvent(){};
	
	// Container for jets and genjets collections, only needed if multiple jet collections are required.
	//mutable std::map<std::string, KJets*> m_genZJets;
	//mutable std::map<std::string, KJets*> m_jets;
};
