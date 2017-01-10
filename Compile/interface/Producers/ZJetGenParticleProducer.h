
#pragma once

#include <Math/VectorUtil.h>

#include "Kappa/DataFormats/interface/Kappa.h"
#include "Excalibur/Compile/interface/ZJetTypes.h"

/**
   Looks for Status 1 Muons/Electrons, searches for mother particle until it is no muon/electron and moves the last found muon/electron to product.m_genMuons/product.m_electrons
   Removes particles originating vom Taus
   pdgIds can be found here http://pdg.lbl.gov/2002/montecarlorpp.pdf
*/

class ZJetGenParticleProducer: public ZJetProducerBase
{
   public:

	std::string GetProducerId() const override;

	void Init(ZJetSettings const& settings) override;
 
	void Produce(ZJetEvent const& event, ZJetProduct& product,
	                     ZJetSettings const& settings) const override;

	unsigned int Find_mom(unsigned int idx, ZJetEvent const& event) const;

};

