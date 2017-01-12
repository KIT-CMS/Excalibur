
#include "Excalibur/Compile/interface/Producers/ZJetGenParticleProducer.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"

void ZJetGenParticleProducer::Init(ZJetSettings const& settings)
{
	ZJetProducerBase::Init(settings);

}
unsigned int ZJetGenParticleProducer::FindMom(unsigned int idx, ZJetEvent const& event) const{
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
	bool valid = true;
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
	idx = 0;*/
	std::cout << "_________________________________________________________________" << std::endl;
	for (KGenParticles::iterator genParticle = event.m_genParticles->begin();
	     genParticle != event.m_genParticles->end(); ++genParticle)
	{
		if ((std::abs(genParticle->pdgId) == PdgId)&&(genParticle->status() == 1))
		{
			valid = true;
			std::cout << "Status 1 muon:" << idx << " with pt: " << (*event.m_genParticles).at(idx).p4.Pt() << " and Eta: " << (*event.m_genParticles).at(idx).p4.Eta() << std::endl;
			mom_idx = idx;
			if((*event.m_genParticles).at(idx).p4.Pt() > 22 && std::abs((*event.m_genParticles).at(idx).p4.Eta()) < 2.3){
				std::cout << "Added to GenMuons:" << idx << std::endl;
				product.m_genMuons.push_back(&(*event.m_genParticles).at(idx)); //Put status 1 muons in m_genMuons 
			}
			while(std::abs((*event.m_genParticles).at(mom_idx).pdgId) == PdgId){
				daughter_idx = mom_idx;	
				if ((*event.m_genParticles).at(daughter_idx).p4.Pt() < 22 || std::abs((*event.m_genParticles).at(daughter_idx).p4.Eta()) >2.3){
					valid = false;
					std::cout << "Didn't pass Cuts: " << daughter_idx << " with pt: " << (*event.m_genParticles).at(daughter_idx).p4.Pt() << " and Eta: " << (*event.m_genParticles).at(daughter_idx).p4.Eta() << std::endl;
					break;
				}
				mom_idx = FindMom(daughter_idx, event);
				std::cout << "Search Mother for: " << daughter_idx << " found: " << mom_idx << std::endl;
			}
			if(std::abs(((*event.m_genParticles).at(mom_idx).pdgId) != DefaultValues::pdgIdTau)&&(valid)){
				std::cout << "Added to ValidMuons:" << daughter_idx << " with Mother: " << mom_idx << std::endl;
				(product.*leptons).push_back(&(*event.m_genParticles).at(daughter_idx)); //Put original muons in m_validGenMuons
			}	
		}
			idx++;
	}
}

