#include "Excalibur/Compile/interface/Producers/ZJetDressedMuonsProducer.h"
/*
 * ZJetDressedMuonsProducer
 * ==========================
 *
 * Extends the Artus/KappaAnalysis ValidMuonsProducer.
 *
 * Implements the following dressed muon definition:
 *    - dressed muons include the surrounding photons
 *      -> FSR can be accounted for
 *
 */

std::string ZJetDressedMuonsProducer::GetProducerId() const { return "ZJetDressedMuonsProducer"; }

void ZJetDressedMuonsProducer::Init(ZJetSettings const& settings)
{
    maxZJetDressedMuonDeltaR = settings.GetMaxZJetDressedMuonDeltaR();

}

void ZJetDressedMuonsProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    //std::cout << "no. of pfcandidates: " << ((KPFCandidates*) event.m_packedPFCandidates)->size() << std::endl;
    //std::cout << "no. of photons: " << (std::vector<const KPFCandidate*> product.m_pfPhotons)->size() << std::endl;
    //std::cout << "no. of photons: " <<  product.m_pfPhotons.size() << std::endl;
    for (unsigned int imu=0; imu < product.m_validMuons.size(); imu++) {
        // KLV dressedMuon;
        KLV photon;
        //product.m_dressedMuons = KLV();
        // dressedMuon.p4 = product.m_validMuons[imu]->p4;
        //std::cout << "muon " << imu+1 << " before dressing: " << product.m_validMuons[imu]->p4 << std::endl;
        for (unsigned int iph=0; iph<product.m_pfPhotons.size(); iph++) {
            //if (std::abs(pfCandidate->pdgId) == 211) { 
            photon.p4 = product.m_pfPhotons[iph]->p4;
            if (ROOT::Math::VectorUtil::DeltaR( product.m_validMuons[imu]->p4, photon.p4) < maxZJetDressedMuonDeltaR) {
                //std::cout << "photon candidate: " << pfCandidate->pdgId << std::endl;}
                /*std::cout << "photon cone to muon: "
                    << ROOT::Math::VectorUtil::DeltaR( product.m_validMuons[imu]->p4, photon.p4 ) 
                    << std::endl;*/
                product.m_validMuons[imu]->p4 += photon.p4;
            }
        }
        //std::cout << "muon " << imu+1 << " after dressing: " << product.m_validMuons[imu]->p4 << std::endl;
        //product.m_dressedMuons.push_back(&dressedMuon);
        //std::cout << product.m_dressedMuons[imu] << std::endl;
        //product.m_dressedMuons.push_back(&((KLV*)product.m_validMuons[imu])->p4);
    }
}

std::string ZJetDressedGenMuonsProducer::GetProducerId() const { return "ZJetDressedGenMuonsProducer"; }

void ZJetDressedGenMuonsProducer::Init(ZJetSettings const& settings)
{
    // requires ZJetGenPhotonsProducer!
    maxZJetDressedMuonDeltaR = settings.GetMaxZJetDressedMuonDeltaR();

}

void ZJetDressedGenMuonsProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    for (unsigned int imu=0; imu < product.m_genMuons.size(); imu++) {
        // KLV dressedMuon;
        KLV photon;
        //product.m_dressedMuons = KLV();
        // dressedMuon.p4 = product.m_validMuons[imu]->p4;
        //std::cout << "muon " << imu+1 << " before dressing: " << product.m_validMuons[imu]->p4 << std::endl;
        for (unsigned int iph=0; iph<product.m_genPhotons.size(); iph++) {
            //if (std::abs(pfCandidate->pdgId) == 211) { 
            photon.p4 = product.m_genPhotons[iph]->p4;
            if (ROOT::Math::VectorUtil::DeltaR( product.m_genMuons[imu]->p4, photon.p4) < maxZJetDressedMuonDeltaR) {
                //std::cout << "photon candidate: " << pfCandidate->pdgId << std::endl;}
                /*std::cout << "photon cone to muon: "
                    << ROOT::Math::VectorUtil::DeltaR( product.m_validMuons[imu]->p4, photon.p4 ) 
                    << std::endl;*/
                product.m_genMuons[imu]->p4 += photon.p4;
            }
        }
        //std::cout << "muon " << imu+1 << " after dressing: " << product.m_validMuons[imu]->p4 << std::endl;
        //product.m_dressedMuons.push_back(&dressedMuon);
        //std::cout << product.m_dressedMuons[imu] << std::endl;
        //product.m_dressedMuons.push_back(&((KLV*)product.m_validMuons[imu])->p4);
    }
}

std::string ZJetTrueGenMuonsProducer::GetProducerId() const { return "ZJetTrueGenMuonsProducer"; }

void ZJetTrueGenMuonsProducer::Init(ZJetSettings const& settings)
{
    
}

int ZJetTrueGenMuonsProducer::FindMom(int idx, ZJetEvent const& event) const{
    
    for (unsigned int ip=0; ip < event.m_genParticles->size(); ip++) {
        for (unsigned int id=0; id < event.m_genParticles->at(ip).nDaughters(); id++) {
            if(event.m_genParticles->at(ip).daughterIndex(id) == idx) {
                return ip;
            }
        }
    }
    return -1000;
}

void ZJetTrueGenMuonsProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    //std::cout << "no. of genParticles: " << event.m_genParticles->size() << std::endl;
    //std::cout << "no. of genPhotons: " << product.m_genPhotons.size() << std::endl;
    int im=0;
    // loop over genMuons
    for (unsigned int imu=0; imu < product.m_genMuons.size(); imu++) {
        //std::cout << "muon no. " << imu << std::endl;
        // loop over genParticles
        for (unsigned int ip=0; ip < event.m_genParticles->size(); ip++) {
            //std::cout << event.m_genParticles->at(ip).pdgId << std::endl;
            // find the genMuons' mother particle index
            if (event.m_genParticles->at(ip).p4 == product.m_genMuons[imu]->p4) {
                im = ip;
                //std::cout << event.m_eventInfo->nEvent << std::endl;
                assert(abs(event.m_genParticles->at(im).pdgId) == 13);
                //std::cout << "particle at index " << im << " with pdgId " << event.m_genParticles->at(im).pdgId << std::endl;
                //std::cout << event.m_genParticles->at(im).p4 << std::endl;
                while (FindMom(im, event) != -1000 && abs(event.m_genParticles->at(FindMom(im, event)).pdgId) == 13) {
                    im = FindMom(im, event);
                    //std::cout << "new mom found at index " << im << " with pdgId " << event.m_genParticles->at(im).pdgId << std::endl;
                    //std::cout << event.m_genParticles->at(im).p4 << std::endl;
                    //std::cout << FindMom(im, event) << std::endl;
                    /*if (FindMom(im, event) == -1000){
                        break;
                    }*/
                    
                    /*im = FindMom(im, event);
                    std::cout << "new mom found at index " << im << " with pdgId " << event.m_genParticles->at(im).pdgId << std::endl;
                    std::cout << event.m_genParticles->at(im).p4 << std::endl;
                    im = FindMom(im, event);
                    std::cout << "new mom found at index " << im << " with pdgId " << event.m_genParticles->at(im).pdgId << std::endl;
                    std::cout << event.m_genParticles->at(im).p4 << std::endl;
                */
                    //im = FindMom(im, event);
                    //std::cout << std::endl << "found new mom: " << event.m_genParticles->at(im).p4;
                }
                //product.m_genz.p4 = event.m_genParticles->at(im).p4;
                //std::cout << event.m_genParticles->at(im).p4 << std::endl;
                product.m_validGenMuons[imu]->p4 = event.m_genParticles->at(im).p4;
            }
            /*if (event.m_genParticles->at(ip).nDaughters()>1 && 
                event.m_genParticles->at(event.m_genParticles->at(ip).daughterIndex(0)).p4 == product.m_genMuons[imu]->p4 &&
                event.m_genParticles->at(event.m_genParticles->at(ip).daughterIndex(1)).pdgId == 22) {
                    assert(abs(event.m_genParticles->at(event.m_genParticles->at(ip).daughterIndex(0)).pdgId) == 13);
                    //product.m_genMuons[imu]->p4 += event.m_genParticles->at(event.m_genParticles->at(ip).daughterIndex(1)).p4;
                    product.m_genMuons[imu]->p4 = event.m_genParticles->at(ip).p4; // assumes that each muon radiates at most once!
            }*/
                    
                    /*
                    std::cout << "genParticle no " << ip << " with pdgId "
                    << event.m_genParticles->at(ip).pdgId << ", status "
                    << event.m_genParticles->at(ip).status() << " and p4="
                    << event.m_genParticles->at(ip).p4 << " has the following daughters:" << std::endl;
                    for (unsigned int id=0; id<event.m_genParticles->at(ip).nDaughters(); id++) {
                        std::cout << "daughter no. " << id << " is genParticle no " 
                        << event.m_genParticles->at(ip).daughterIndex(id) << " with pdgId "
                        << event.m_genParticles->at(event.m_genParticles->at(ip).daughterIndex(id)).pdgId << ", status "
                        << event.m_genParticles->at(event.m_genParticles->at(ip).daughterIndex(id)).status() << " and p4="
                        << event.m_genParticles->at(event.m_genParticles->at(ip).daughterIndex(id)).p4 << std::endl;
                    }*/
        /*if (event.m_genParticles->at(ip).status()==1 || event.m_genParticles->at(ip).nDaughters() ==0) {
            std::cout << "final state genParticle candidate: " << ip << " pdgId, status, nDaughters: " 
                << event.m_genParticles->at(ip).pdgId << " "
                << event.m_genParticles->at(ip).status() << " "
                << event.m_genParticles->at(ip).nDaughters() << std::endl;
        }*/
        /*if (abs(event.m_genParticles->at(ip).pdgId)==13) {
            std::cout << "genmuon found at index " << ip << " with status "
                << event.m_genParticles->at(ip).status() << " and "
                << event.m_genParticles->at(ip).nDaughters() << " Daughters " <<std::endl;
            for (unsigned int id=0; id<event.m_genParticles->at(ip).nDaughters(); id++) {
                std::cout << "genmuon daughter no. " << id << " at index "
                    << event.m_genParticles->at(ip).daughterIndex(id) << " of type "
                    << event.m_genParticles->at(event.m_genParticles->at(ip).daughterIndex(id)).pdgId << std::endl;
            }
        }*/
            /*if (event.m_genParticles->at(ip).p4 == product.m_genMuons[imu]->p4) {
                std::cout << "genmuon found at index " << ip << " with status "
                << event.m_genParticles->at(ip).status() << " and "
                << event.m_genParticles->at(ip).nDaughters() << " Daughters " <<std::endl;
                for (unsigned int id=0; id < event.m_genParticles->size(); id++) {
                    if (event.m_genParticles->at(ip).daughterIndex())
                }
            }*/
        }
    }
    //std::cout << "no. of genPhotons: " << (std::vector<const KPFCandidate*> product.m_pfPhotons)->size() << std::endl;
    //std::cout << "no. of photons: " <<  product.m_pfPhotons.size() << std::endl;
    //
        // KLV dressedMuon;
        //KLV photon;
        //product.m_dressedMuons = KLV();
        // dressedMuon.p4 = product.m_validMuons[imu]->p4;
        //std::cout << "muon " << imu+1 << " before dressing: " << product.m_validMuons[imu]->p4 << std::endl;
        //for (unsigned int iph=0; iph<product.m_pfPhotons.size(); iph++) {
            //if (std::abs(pfCandidate->pdgId) == 211) { 
            //photon.p4 = product.m_pfPhotons[iph]->p4;
            //if (ROOT::Math::VectorUtil::DeltaR( product.m_validMuons[imu]->p4, photon.p4) < maxZJetDressedMuonDeltaR) {
                //std::cout << "photon candidate: " << pfCandidate->pdgId << std::endl;}
                /*std::cout << "photon cone to muon: "
                    << ROOT::Math::VectorUtil::DeltaR( product.m_validMuons[imu]->p4, photon.p4 ) 
                    << std::endl;*/
                //product.m_validMuons[imu]->p4 += photon.p4;
            //}
        //}
        //std::cout << "muon " << imu+1 << " after dressing: " << product.m_validMuons[imu]->p4 << std::endl;
        //product.m_dressedMuons.push_back(&dressedMuon);
        //std::cout << product.m_dressedMuons[imu] << std::endl;
        //product.m_dressedMuons.push_back(&((KLV*)product.m_validMuons[imu])->p4);
    //}
}

/*std::string GenZJetDressedMuonsProducer::GetProducerId() const { return "ValidZllGenJetsProducer"; }
void ValidZllGenJetsProducer::Init(ZJetSettings const& settings)
{
    minZllJetDeltaRVeto = settings.GetMinZllJetDeltaRVeto();
}

void ValidZllGenJetsProducer::Produce(ZJetEvent const& event,
                                   ZJetProduct& product,
                                   ZJetSettings const& settings) const
{
    assert(event.m_genJets);
    for (unsigned int jet=0; jet < ((KLVs*) event.m_genJets)->size(); ++jet) {
        bool validjet = true;
        for (unsigned int lep=0; lep<product.m_genLeptonsFromBosonDecay.size(); ++lep) {
            validjet = validjet && ROOT::Math::VectorUtil::DeltaR( ((KLVs*) event.m_genJets)->at(jet).p4, product.m_genLeptonsFromBosonDecay[lep]->p4) > minZllJetDeltaRVeto;
        }
        if (validjet) {
            product.m_simpleGenJets.push_back(&((KLVs*) event.m_genJets)->at(jet));
        }
    }
}
*/

std::string ZJetGenPhotonsProducer::GetProducerId() const { return "ZJetGenPhotonsProducer"; }

void ZJetGenPhotonsProducer::Init(ZJetSettings const& settings)
{
    
}

void ZJetGenPhotonsProducer::Produce(ZJetEvent const& event,
                                 ZJetProduct& product,
                                 ZJetSettings const& settings) const
{
    // create collection of gen photons with status 1
    for (KGenParticles::iterator part = event.m_genParticles->begin(); part != event.m_genParticles->end(); ++part){
        if (std::abs(part->pdgId) == 22 && part->status()==1) {
            product.m_genPhotons.push_back(&(*part));
        }
    }
}
