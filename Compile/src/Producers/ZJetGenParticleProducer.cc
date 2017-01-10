
#include "Excalibur/Compile/interface/Producers/ZJetGenParticleProducer.h"
#include "Artus/Utility/interface/Utility.h"

std::string ZJetGenParticleProducer::GetProducerId() const{
	return "ZJetGenParticleProducer";
}

void ZJetGenParticleProducer::Init(ZJetSettings const& settings)
{
	ZJetProducerBase::Init(settings);

}
unsigned int ZJetGenParticleProducer::Find_mom(unsigned int idx, ZJetEvent const& event) const{
	unsigned int i = 0;
	for (KGenParticles::iterator genParticle = event.m_genParticles->begin();
		     		genParticle != event.m_genParticles->end(); ++genParticle){
		for (std::vector<unsigned int>::const_iterator decayParticleIndex = genParticle->daughterIndices.begin();
		     decayParticleIndex != genParticle->daughterIndices.end(); ++decayParticleIndex){
			if(*decayParticleIndex == idx)
				return i;
		}
		i++;
	}
	return -1000;
	

}

void ZJetGenParticleProducer::Produce(ZJetEvent const& event, ZJetProduct& product,
                     ZJetSettings const& settings) const
{
	unsigned int idx = 0;
	unsigned int mom_idx = 0;
	unsigned int daughter_idx = 0;
	/*for (KGenParticles::iterator genParticle = event.m_genParticles->begin();
	     genParticle != event.m_genParticles->end(); ++genParticle)
	{
		std::cout << idx << "\t" << genParticle->pdgId << "\t" << genParticle->status() << "\t" << std::setprecision(3) << genParticle->p4.Pt()<<  "\t" << std::setprecision(3) << genParticle->p4.Eta()<< "\t"<< std::setprecision(3) << genParticle->p4.Phi() << "\t(";
				for (std::vector<unsigned int>::const_iterator decayParticleIndex = genParticle->daughterIndices.begin();
		     decayParticleIndex != genParticle->daughterIndices.end(); ++decayParticleIndex)
					std::cout << *decayParticleIndex << " ";
				std::cout << ")" << std::endl;
	idx++;
	}
	std::cout << "_________________________________________________________________" << std::endl;
	idx = 0;*/
	for (KGenParticles::iterator genParticle = event.m_genParticles->begin();
	     genParticle != event.m_genParticles->end(); ++genParticle)
	{
		if ((std::abs(genParticle->pdgId) == DefaultValues::pdgIdMuon)&&(genParticle->status() == 1))
		{
			//std::cout << "Status 1 muon:" << idx << std::endl;
			mom_idx = idx;
			while(std::abs((*event.m_genParticles).at(mom_idx).pdgId) == DefaultValues::pdgIdMuon){
				daughter_idx = mom_idx;	
				mom_idx = Find_mom(daughter_idx, event);
				//std::cout << "Search Mother for: " << idx << " found: " << mom_idx << std::endl;
			}
			if(std::abs((*event.m_genParticles).at(mom_idx).pdgId) != DefaultValues::pdgIdTau)
				//std::cout << "Added to ValidMuons:" << daughter_idx << " with Mother: " << mom_idx << std::endl;
				product.m_genMuons.push_back(&(*event.m_genParticles).at(daughter_idx));		
		}
			idx++;
	}
}

