#include "Excalibur/Compile/interface/Producers/ZJetPartonProducer.h"
/*
 * ZJetPartonProducer
 * ==========================
 *
 * Writes out colliding partons with pt = 0
 *
 */

std::string ZJetPartonProducer::GetProducerId() const { return "ZJetPartonProducer"; }

void ZJetPartonProducer::Init(ZJetSettings const& settings)
{
    
}

void ZJetPartonProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    // create collection of partons with status 21
    for (KGenParticles::iterator part = event.m_genParticles->begin(); part != event.m_genParticles->end(); ++part){
        //if (std::abs(part->pdgId) == 22 && part->status()==1) {
        if (part->status()==21) {
            product.m_partons.push_back(&(*part));
        }
    }
}
