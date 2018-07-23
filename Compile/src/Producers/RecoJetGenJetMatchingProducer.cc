#include "Excalibur/Compile/interface/Producers/RecoJetGenJetMatchingProducer.h"

std::string RecoJetGenJetMatchingProducer::GetProducerId() const
{
    return "RecoJetGenJetMatchingProducer";
}

void RecoJetGenJetMatchingProducer::Init(ZJetSettings const& settings)
{
    ZJetProducerBase::Init(settings);
}

void RecoJetGenJetMatchingProducer::Produce(ZJetEvent const& event,
                                            ZJetProduct& product,
                                            ZJetSettings const& settings) const
{
    // TODO(gfleig): raw jets should be added to m_correctedZJets if more hacks like this are needed

    // Match raw jets
    MatchCollection(event, product, settings, "None", settings.GetDeltaRMatchingRecoJetGenJet());

    // Iterate over all jet correction levels
    for (std::map<std::string, std::vector<std::shared_ptr<KJet>>>::const_iterator itlevel =
             product.m_correctedZJets.begin();
         itlevel != product.m_correctedZJets.end(); ++itlevel) {
        MatchCollection(event, product, settings, itlevel->first,
                        settings.GetDeltaRMatchingRecoJetGenJet());
    }
}

void RecoJetGenJetMatchingProducer::MatchCollection(ZJetEvent const& event,
                                                    ZJetProduct& product,
                                                    ZJetSettings const& settings,
                                                    std::string const& corrLevel,
                                                    double const deltaR) const
{
    // Iterate over all corrected jets to copy them in local object since they are shared pointers
    // and we need actual jets
    unsigned long jetCount = product.GetValidJetCount(settings, event, corrLevel);
    KJets recoJets(jetCount);
    for (unsigned long jetIndex = 0; jetIndex < jetCount; ++jetIndex) {
        recoJets[jetIndex] =
            *(static_cast<KJet*>(product.GetValidJet(settings, event, jetIndex, corrLevel)));
    }
    // Iterate over all gen jets to copy them in local object since they are shared pointers
    unsigned long genJetCount = product.m_simpleGenJets.size();
    KLVs genJets(genJetCount);
    for (unsigned long jetIndex = 0; jetIndex < genJetCount; ++jetIndex) {
        genJets[jetIndex] =
            //*(static_cast<KLV*>(product.GetValidJet(settings, event, jetIndex, corrLevel)));
            *(static_cast<KLV*>(product.m_simpleGenJets[jetIndex]));
    }

    // Make use of KappaTools matcher
    std::vector<int> matchResult = matchSort_Matrix<KLV, KJet>(genJets, genJetCount, recoJets, jetCount, deltaR);
    // Store result in product
    product.m_matchedGenJets[corrLevel] = matchResult;
}
