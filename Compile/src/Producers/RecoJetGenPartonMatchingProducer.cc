#include "Excalibur/Compile/interface/Producers/RecoJetGenPartonMatchingProducer.h"

std::string RecoJetGenPartonMatchingProducer::GetProducerId() const
{
    return "RecoJetGenPartonMatchingProducer";
}

void RecoJetGenPartonMatchingProducer::Produce(KappaEvent const& event,
                                               KappaProduct& product,
                                               KappaSettings const& settings) const
{
    // Make ZJet specific product and event available
    ZJetEvent const& zJetEvent = static_cast<ZJetEvent const&>(event);
    ZJetProduct& zJetProduct = static_cast<ZJetProduct&>(product);
    ZJetSettings const& zJetSettings = static_cast<ZJetSettings const&>(settings);

    // Raw jets
    // Iterate over all jets and match them to partons
    for (std::vector<KBasicJet*>::const_iterator recoJet = zJetProduct.m_validJets.begin();
         recoJet != zJetProduct.m_validJets.end(); ++recoJet) {
        //std::cout << recoJet << std::endl;
        // Use Artus reco jet gen particle matcher
        KGenParticle* matchedParton =
            Match(zJetEvent, zJetProduct, zJetSettings, static_cast<KLV*>(*recoJet));
        if (matchedParton != nullptr) {
            // Map of reco jets and matched gen partons for all requested correction levels
            zJetProduct.m_matchedGenPartons["None"][static_cast<KJet*>(*recoJet)] = matchedParton;
        }
    }

    // Iterate over all jet correction levels
    for (std::map<std::string, std::vector<std::shared_ptr<KJet>>>::const_iterator itlevel =
             zJetProduct.m_correctedZJets.begin();
         itlevel != zJetProduct.m_correctedZJets.end(); ++itlevel) {
        // Iterate over all jets and match them to partons
        for (std::vector<std::shared_ptr<KJet>>::const_iterator recoJet = itlevel->second.begin();
             recoJet != itlevel->second.end(); ++recoJet) {
            //std::cout << recoJet << std::endl;
            // Use Artus reco jet gen particle matcher
            KGenParticle* matchedParton =
                Match(zJetEvent, zJetProduct, zJetSettings, static_cast<KLV*>((*recoJet).get()));
            if (matchedParton != nullptr) {
                // Map of reco jets and matched gen partons for all requested correction levels
                zJetProduct.m_matchedGenPartons[itlevel->first][(*recoJet).get()] = matchedParton;
            }
        }
    }
}

std::string GenJetGenPartonMatchingProducer::GetProducerId() const
{
    return "GenJetGenPartonMatchingProducer";
}

void GenJetGenPartonMatchingProducer::Produce(KappaEvent const& event,
                                               KappaProduct& product,
                                               KappaSettings const& settings) const
{
    // Make ZJet specific product and event available
    ZJetEvent const& zJetEvent = static_cast<ZJetEvent const&>(event);
    ZJetProduct& zJetProduct = static_cast<ZJetProduct&>(product);
    ZJetSettings const& zJetSettings = static_cast<ZJetSettings const&>(settings);

    // Raw jets
    // Iterate over all gen jets and match them to partons
    if (product.m_simpleGenJets.size() > 0) {
        for (unsigned int i=0; i<zJetProduct.m_simpleGenJets.size(); i++) {
            // Use Artus gen jet gen particle matcher
            KGenParticle* matchedParton =
                Match(zJetEvent, zJetProduct, zJetSettings, zJetProduct.m_simpleGenJets.at(i));
            zJetProduct.m_genPartons.push_back(matchedParton);
        }
    }
}
