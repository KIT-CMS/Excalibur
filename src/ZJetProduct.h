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

	// Added by ZProducer
	bool m_validZ = false;
	KLV m_z;
	
	// Added by ZJetValidJetsProducer
	//mutable std::map<std::string, std::vector<KJet*> > m_validZJets;
	//mutable std::map<std::string, std::vector<KJet*> > m_invalidZJets;
	
	// Added by ZJetCorrectionsProducer, shared pointers are necessary to keep the jets in the product after creation
	std::map<std::string, std::vector<std::shared_ptr<KJet> > > m_correctedZJets;
	
	// Added by TypeIMETProducer
	std::map<std::string, KMET> m_corrMET;
	
	// Added by RecoJetGenPartonMatchingProducer
	std::map<std::string, std::map<KJet*, KGenParticle*> > m_matchedGenPartons;
	
	// Added by RecoJetGenJetMatchingProducer
	boost::ptr_map<std::string, std::vector<int> > m_matchedGenJets;

	// Added by RadiationJetsProducer
	std::map<std::string, std::vector<KJet*> > m_radiationJets;
	std::map<std::string, std::vector<int> > m_radiationJetsIndex;

	double npudata;

	/////////////////////////////
	// Functions for Consumers //
	/////////////////////////////
	
	// Access to valid/corrected jets
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

	KLV* GetValidJet(ZJetSettings const& settings,
	                 ZJetEvent const& event,
	                 unsigned int index) const
	{
		return GetValidJet(settings, event, index, settings.GetCorrectionLevel());
	}

	KLV* GetValidPrimaryJet(ZJetSettings const& settings,
	                        ZJetEvent const& event) const
	{
		return GetValidJet(settings, event, 0, settings.GetCorrectionLevel());
	}
	
	// Access to radiation jets
	unsigned int GetRadiationJetCount(ZJetSettings const& settings,
								  ZJetEvent const& event,
								  std::string corrLevel) const
	{
		// Gen jets are always radiation jets
		if (corrLevel == "Gen") {
			return (event.m_genJets->size() - 1);
		}
		else {
			return SafeMap::Get(m_radiationJets, corrLevel).size();
		}
	}
	
	unsigned int GetRadiationJetCount(ZJetSettings const& settings,
								  ZJetEvent const& event) const
	{
		return GetRadiationJetCount(settings, event, settings.GetCorrectionLevel());
	}
	
	unsigned int GetRadiationJetIndex(ZJetSettings const& settings,
					 ZJetEvent const& event,
					 unsigned int index,
					 std::string corrLevel) const
	{
		assert(GetRadiationJetCount(settings, event, corrLevel) > index);
		
		// Gen jets are always radiation jets
		if (corrLevel == "Gen") {
			return index;
		}
		else {
			return SafeMap::Get(m_radiationJetsIndex, corrLevel)[index];
		}
	}
	
	unsigned int GetRadiationJetIndex(ZJetSettings const& settings,
	                 ZJetEvent const& event,
	                 unsigned int index) const
	{
		return GetRadiationJetIndex(settings, event, index, settings.GetCorrectionLevel());
	}
	
	KLV* GetRadiationJet(ZJetSettings const& settings,
					 ZJetEvent const& event,
					 unsigned int index,
					 std::string corrLevel) const
	{
		assert(GetRadiationJetCount(settings, event, corrLevel) > index);
		
		// Gen jets
		if (corrLevel == "Gen") {
			return &(event.m_genJets->at(index));
		}
		else {
			return (SafeMap::Get(m_radiationJets, corrLevel)[index]);
		}
	}

	KLV* GetRadiationJet(ZJetSettings const& settings,
	                 ZJetEvent const& event,
	                 unsigned int index) const
	{
		return GetRadiationJet(settings, event, index, settings.GetCorrectionLevel());
	}
	

	// Access to invalid jets
	unsigned int GetInvalidJetCount(ZJetSettings const& settings,
								  ZJetEvent const& event,
								  std::string corrLevel) const
	{
		// Gen jets are always valid
		if (corrLevel == "Gen") {
			return 0;
		}
		// Invalid jets, no need for different correction levels
		else {
			return m_invalidJets.size();
		}
	}

	unsigned int GetInvalidJetCount(ZJetSettings const& settings,
									ZJetEvent const& event) const
	{
		return GetInvalidJetCount(settings, event, settings.GetCorrectionLevel());
	}
	
	// Access to (un)corrected MET
	KMET* GetMet(ZJetSettings const& settings, ZJetEvent const& event, std::string corrLevel) const
	{
		// Only L3 is corrected in TypeIMETProducer
		if (std::string::npos != corrLevel.find("L3"))
		{
			return const_cast<KMET*>(&(m_corrMET.at(corrLevel)));
		}
		else
		{
			return event.m_met;
		}
	}

	KMET* GetMet(ZJetSettings const& settings, ZJetEvent const& event) const
	{
		return GetMet(settings, event, settings.GetCorrectionLevel());
	}

	// Calculate MPF
	double GetMPF(const KLV* met) const
	{
		double scalPtEt = m_z.p4.Px() * met->p4.Px() + m_z.p4.Py() * met->p4.Py();
		double scalPtSq = m_z.p4.Px() * m_z.p4.Px() + m_z.p4.Py() * m_z.p4.Py();
		return 1.0f + scalPtEt / scalPtSq;
	}

	// Reco jet - gen parton matching result
	KGenParticle* GetMatchedGenParton(ZJetEvent const& event, ZJetSettings const& settings, unsigned int index) const
	{
		if (GetValidJetCount(settings, event) > index)
			return SafeMap::GetWithDefault(SafeMap::GetWithDefault(m_matchedGenPartons,
			                                                       settings.GetCorrectionLevel(),
			                                                       std::map<KJet*, KGenParticle*>()),
			                               static_cast<KJet*>(GetValidJet(settings, event, index)),
			                               (KGenParticle*)(0));
		else
			return NULL;
	}

	// Reco jet - gen jet matching result
	KLV* GetMatchedGenJet(ZJetEvent const& event, ZJetSettings const& settings, unsigned int index) const
	{
		std::vector<int> defaultValue = std::vector<int>(0);
		std::vector<int> jetList = SafeMap::GetPtrMapWithDefault(m_matchedGenJets, settings.GetCorrectionLevel(), defaultValue);

		if (index >= jetList.size())
			return NULL;

		unsigned int matchedJet = jetList.at(index);

		if (GetValidJetCount(settings, event, "Gen") >= matchedJet)
			return GetValidJet(settings, event, matchedJet, "Gen");
		else
			return NULL;
	}
	
	// Access to gen Z
	KGenParticle* GetGenZ() const
	{
		std::vector<KGenParticle*> genZs = SafeMap::GetWithDefault(m_genParticlesMap, 23, (std::vector<KGenParticle*>)(0));
		return (genZs.size() > 0) ? genZs[0] : NULL;
	}

	// Reco muon - gen muon matching result
	KGenParticle* GetMatchedGenMuon(ZJetEvent const& event, ZJetSettings const& settings, unsigned int index) const
	{
		if (m_validMuons.size() > index)
			return SafeMap::GetWithDefault(m_genParticleMatchedMuons, m_validMuons.at(index), (KGenParticle*)(0));
		else
			return NULL;
	}
};
