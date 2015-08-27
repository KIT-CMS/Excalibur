#include "Producers/JetSorter.h"

std::string JetSorter::GetProducerId() const { return "JetSorter"; }

void JetSorter::Produce(ZJetEvent const& event,
                        ZJetProduct& product,
                        ZJetSettings const& settings) const
{
    // Iterate over all jet correction levels
    for (std::map<std::string, std::vector<std::shared_ptr<KJet>>>::const_iterator itlevel =
             product.m_correctedZJets.begin();
         itlevel != product.m_correctedZJets.end(); ++itlevel) {
        std::sort(product.m_correctedZJets[itlevel->first].begin(),
                  product.m_correctedZJets[itlevel->first].end(),
                  [](std::shared_ptr<KJet> jet1, std::shared_ptr<KJet> jet2)
                      -> bool { return jet1->p4.Pt() > jet2->p4.Pt(); });
    }
}
