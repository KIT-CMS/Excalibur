
#pragma once

#include <Math/VectorUtil.h>
#include "Artus/KappaAnalysis/interface/Utility/ValidPhysicsObjectTools.h"
#include "Kappa/DataFormats/interface/Kappa.h"
#include "Excalibur/Compile/interface/ZJetTypes.h"

/**
   Looks for Status 1 Muons/Electrons, searches for mother particle until it is no muon/electron and moves the last found muon/electron to product.m_genMuons/product.m_electrons
   Removes particles originating vom Taus
   pdgIds can be found here http://pdg.lbl.gov/2002/montecarlorpp.pdf
*/

class ZJetGenParticleProducer: public ZJetProducerBase, public ValidPhysicsObjectTools<ZJetTypes, KGenParticle>
{
   public:
	typedef typename ZJetTypes::event_type event_type;
	typedef typename ZJetTypes::product_type product_type;
	typedef typename ZJetTypes::setting_type setting_type;

	ZJetGenParticleProducer(std::vector<KGenParticle*> product_type::*validLeptons,
                                std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
                                std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
				int absPdgId): 
				ProducerBase(),
				ValidPhysicsObjectTools<ZJetTypes, KGenParticle>(GetLowerPtCuts, GetUpperAbsEtaCuts, validLeptons),
				leptons(validLeptons),
				PdgId(absPdgId)

	{
	}

	void Init(ZJetSettings const& settings) override;
 
	void Produce(ZJetEvent const& event, ZJetProduct& product,
	                     ZJetSettings const& settings) const override;

	unsigned int FindMom(unsigned int idx, ZJetEvent const& event) const;

    protected:
	std::vector<KGenParticle*> product_type::*leptons;
	int PdgId;
};

class ZJetGenMuonProducer: public ZJetGenParticleProducer
{

	public:
		typedef typename ZJetTypes::event_type event_type;
		typedef typename ZJetTypes::product_type product_type;
		typedef typename ZJetTypes::setting_type setting_type;

		ZJetGenMuonProducer():ZJetGenParticleProducer(&product_type::m_validGenMuons,
	                          &setting_type::GetGenMuonLowerPtCuts,
	                          &setting_type::GetGenMuonUpperAbsEtaCuts,
	                          DefaultValues::pdgIdMuon)
		{
		}
		std::string GetProducerId() const override{
			return "ZJetGenMuonProducer";		
		}
};

