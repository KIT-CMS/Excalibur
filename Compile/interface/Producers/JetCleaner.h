#pragma once

#include <TH2.h>
#include "Excalibur/Compile/interface/ZJetTypes.h"

/** Generic producer for cleaning all corrected jet collections
 *
 *  Derived classes must implement the DoesJetPass(const KJet*) method, which
 *  is then applied to each jet in the jet collection for every JEC correction
 *  level. Jets for which this method returns false are removed from the
 *  collection.
 *
 *  Note: Needs to run after the JEC producer.
 */
class JetCleanerBase : public ZJetProducerBase {

  public:
    virtual std::string GetProducerId() const = 0;

    JetCleanerBase() : ZJetProducerBase() {};

    void Init(ZJetSettings const& settings) {
        ZJetProducerBase::Init(settings);
    };

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override {

        // Iterate over all JEC levels
        for (std::pair<const std::string, std::vector<std::shared_ptr<KJet>>>& jecLevelJetCollection : product.m_correctedZJets) {
            // remove all jets for which DoesJetPass() returns false
            jecLevelJetCollection.second.erase(
                std::remove_if(
                    jecLevelJetCollection.second.begin(),
                    jecLevelJetCollection.second.end(),
                    [this](auto jetSharedPtr){
                        return !this->DoesJetPass(jetSharedPtr.get());
                    }
                ),
                jecLevelJetCollection.second.end()
            );
        }
    };

    virtual bool DoesJetPass(const KJet* jet) const = 0;

};


/** Producer for invalidating jets in particular eta-phi regions
 *
 *  Settings:
 *      JetEtaPhiCleanerFile (string) :
 *          path to ROOT file used for cleaning
 *      JetEtaPhiCleanerHistogramNames (list of string) :
 *          names of histograms that should used for cleaning
 *      JetEtaPhiCleanerHistogramValueMaxValid (double) :
 *          jets are rejected if the value of the corresponding bin (in any of the configured histograms) is greater than this
 *
 *  Note: Needs to run after the JEC producer.
 */
class JetEtaPhiCleaner : public JetCleanerBase {

  public:
    virtual std::string GetProducerId() const override;

    JetEtaPhiCleaner() : JetCleanerBase() {};

    void Init(ZJetSettings const& settings);

    virtual bool DoesJetPass(const KJet* jet) const;

  protected:

    std::vector<TH2D*> m_cleaningHistograms;
    double m_cleaningHistogramsValueMaxValid;
};
