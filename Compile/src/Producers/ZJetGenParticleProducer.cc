
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
	std::vector<std::pair<unsigned int, float>> muons;
	for (KGenParticles::iterator genParticle = event.m_genParticles->begin();
	     genParticle != event.m_genParticles->end(); ++genParticle)
	{
		if ((std::abs(genParticle->pdgId) == PdgId)&&(genParticle->status() == 1))
		{
			mom_idx = idx;
			while(std::abs((*event.m_genParticles).at(mom_idx).pdgId) == PdgId){
				daughter_idx = mom_idx;	
				mom_idx = FindMom(daughter_idx, event);
			}
			if((*event.m_genParticles).at(daughter_idx).isPrompt()&&(*event.m_genParticles).at(daughter_idx).isHardProcess()){
				if((*event.m_genParticles).at(idx).p4.Pt() > std::stof(settings.GetGenMuonLowerPtCuts()[0]) && std::abs((*event.m_genParticles).at(idx).p4.Eta()) < std::stof(settings.GetGenMuonUpperAbsEtaCuts()[0])){
					float value = (float) (*event.m_genParticles).at(daughter_idx).p4.Pt();
					muons.push_back(std::make_pair(idx, value));
				}
				if((*event.m_genParticles).at(daughter_idx).p4.Pt() > std::stof(settings.GetGenMuonLowerPtCuts()[0]) && std::abs((*event.m_genParticles).at(daughter_idx).p4.Eta()) < std::stof(settings.GetGenMuonUpperAbsEtaCuts()[0])){
					(product.*leptons).push_back(&(*event.m_genParticles).at(daughter_idx)); //Put original muons in m_validGenMuons
				}
			}

		}
		idx++;
	}
	std::sort((product.*leptons).begin(), (product.*leptons).end(),
			[](KGenParticle const* lepton1, KGenParticle const* lepton2) -> bool
			{ return lepton1->p4.Pt() > lepton2->p4.Pt(); });
	std::sort(muons.begin(),muons.end(),[](std::pair<unsigned int,float> a, std::pair<unsigned int,float> b) -> bool{return a.second > b.second;});
	for (unsigned int i = 0; i < muons.size(); i++){
		product.m_genMuons.push_back(&(*event.m_genParticles).at(muons[i].first));
	}
}
