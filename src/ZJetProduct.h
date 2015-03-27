#pragma once

#include "Artus/KappaAnalysis/interface/KappaProduct.h"
#include "Artus/Utility/interface/SafeMap.h"

#include <boost/ptr_container/ptr_map.hpp>

/**
   \brief Container class for everything that can be produced in pipeline.

   Defines any outcome that could be produced by a KappaProducer during a common analysis chain in a 
   given KappaPipeline. Via the PipelineRunner the KappaProduct all extra products in the analysis 
   chain will be passed on to subsequent Producers, Filters and Consumers.
*/

class ZJetProduct : public KappaProduct
{
  public:
	ZJetProduct() : KappaProduct(){};

	// added by ZProducer
	IMPL_PROPERTY(bool, ValidZ)
	IMPL_PROPERTY(KLV, Z)
	
	// added by ZJetValidJetsProducer
	//mutable std::map<std::string, std::vector<KJet*> > m_validZJets;
	//mutable std::map<std::string, std::vector<KJet*> > m_invalidZJets;
	
	// added by ZJetCorrectionsProducer, shared pointers are necessary to keep the jets in the product after creation
	mutable std::map<std::string, std::vector<std::shared_ptr<KJet> > > m_correctedZJets;


	double GetMPF(const KLV* met) const
	{
		double scalPtEt =
		    GetRefZ().p4.Px() * met->p4.Px() + GetRefZ().p4.Py() * met->p4.Py();

		double scalPtSq = GetRefZ().p4.Px() * GetRefZ().p4.Px() +
		                  GetRefZ().p4.Py() * GetRefZ().p4.Py();

		return 1.0f + scalPtEt / scalPtSq;
	}

	// Access to valid jets
	unsigned int GetValidJetCount(ZJetSettings const& settings,
								  ZJetEvent const& event,
								  std::string corrLevel) const
	{
		// Gen jets are always valid
		if (corrLevel == "Gen") {
			return event.m_genJets->size();
		}
		// Uncorrected valid jet
		else if (corrLevel == "None") {
			return m_validJets.size();
		}
		// Corrected valid jet
		else {
			return SafeMap::Get(m_correctedZJets, corrLevel).size();
		}
	}

	unsigned int GetValidJetCount(ZJetSettings const& settings,
								  ZJetEvent const& event) const
	{
		return GetValidJetCount(settings, event, settings.GetCorrectionLevel());
	}

	KLV* GetValidJet(ZJetSettings const& settings,
					 ZJetEvent const& event,
					 unsigned int index,
					 std::string corrLevel) const
	{
		assert(GetValidJetCount(settings, event, corrLevel) > index);
		
		// Gen jets
		if (corrLevel == "Gen") {
			return &(event.m_genJets->at(index));
		}
		// Uncorrected valid jet
		else if (corrLevel == "None") {
			return static_cast<KLV*>(m_validJets[index]);
		}
		// Corrected valid jet
		else {
			return (SafeMap::Get(m_correctedZJets, corrLevel)[index]).get();
		}
	}

	KLV* GetValidPrimaryJet(ZJetSettings const& settings,
								ZJetEvent const& event) const
	{
		return GetValidJet(settings, event, 0);
	}

	KLV* GetValidJet(ZJetSettings const& settings,
						 ZJetEvent const& event,
						 unsigned int index) const
	{
		return GetValidJet(settings, event, index, settings.GetCorrectionLevel());
	}
};
