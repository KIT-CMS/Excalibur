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

        LOG(DEBUG) << "\n[" << this->GetProducerId() << "]";                       
        if (settings.GetCutVetoCleanedEvents()) {
            LOG(DEBUG) << "Check the first "<< settings.GetCutVetoNJets() 
                       << " jets (all have to be above " << settings.GetCutVetoJetsAbove()
                       << "GeV) for the JetEtaPhiCleanerCut.";
        }

/******************************************************************************
 * For JEC it is necessary to check if the leading jet at full correction
 * level is removed by the JetEtaPhiCleaner.
 * Unfortunately the jets must not be sorted at this stage since the current
 * implementation does not allow to do this before the TypeIMetProducer.
 * Therefore, it is necessary to first find the leading jet if the event should
 * be vetoed beacause of the removal of the first N leading jets.
 *
 * For this, the allready implemented functionality is reused ( I know it is 
 * ugly but as ever: time is short, sorry ...)
 * I copy and pasted the loop and check whether there are N jets with greater
 * pT then the one which should be removed. This has to be done in a separate
 * loop since the immidiate removal would prevent this.
 * => we set the veto flag, if no N jets can be found that are grater than the 
 * one which is checked.
 *
 * In the end, the remove is always gets a false since this should only happen 
 * in the next loop...
 *****************************************************************************/
        std::string targetLevel;
        if (settings.GetInputIsData()) {
            targetLevel = "L1L2L3Res";  // highest corr level
            LOG(DEBUG) << "Input is data: use L1L2L3Res for vetoing...";
        } else {
            targetLevel = "L1L2L3";  // for MC, use L1L2L3
            LOG(DEBUG) << "Input is MC: use L1L2L3 for vetoing...";
        }
        // Iterate over all JEC levels
        for (std::pair<const std::string, std::vector<std::shared_ptr<KJet>>>& jecLevelJetCollection : product.m_correctedZJets) {
            if (settings.GetDebugVerbosity() > 1) {
                LOG(DEBUG) << "Cleaning " << jecLevelJetCollection.first;
                LOG(DEBUG) << "Before: " << jecLevelJetCollection.second.size() << " Jets";
            }
            // check if N leading jets are cleaned at highest corr level
            if (settings.GetCutVetoCleanedEvents() && jecLevelJetCollection.first == targetLevel) {
                jecLevelJetCollection.second.erase(
                    std::remove_if(
                        jecLevelJetCollection.second.begin(),
                        jecLevelJetCollection.second.end(),
                        [&, this](auto jetSharedPtr){
                            bool removeJet = !this->DoesJetPass(jetSharedPtr.get(), event, product, settings);  // jet removed if true -> jet does not pass
                            if (settings.GetCutVetoCleanedEvents() && jecLevelJetCollection.first == targetLevel && !product.m_etaPhiCleaned) {  // only check on max corr level
                                auto jet_pt = jetSharedPtr.get()->p4.Pt();
                                int count = 0;
                                if ( jet_pt > settings.GetCutVetoJetsAbove()  // check all jets above value
                                    && (removeJet) ) {
                                    // loop over all jets and check the index of the one to be removed...
                                    for (auto jet = jecLevelJetCollection.second.begin(); jet != jecLevelJetCollection.second.end() && !product.m_etaPhiCleaned; jet++) {
                                        if ( (*jet)->p4.Pt() > jet_pt ) {
                                            count++;
                                        }
                                    }
                                    if ( count < settings.GetCutVetoNJets() && !product.m_etaPhiCleaned ) { // a relevant jet was cleaned => Veto event!
                                        product.m_etaPhiCleaned = true;
                                        if (settings.GetDebugVerbosity() > 1) {
                                            LOG(DEBUG) << "VetoCleanedEvent: True ";
                                            LOG(DEBUG) << "LEVEL: " << jecLevelJetCollection.first;
                                            LOG(DEBUG) << "The " << count + 1 << ". jet will be cleaned! P4:" << jetSharedPtr.get()->p4;
                                        }
                                    }
                                }
                            }
                            return false;
                        }
                    ),
                    jecLevelJetCollection.second.end()
                );
            }

            // remove all jets for which DoesJetPass() returns false
            jecLevelJetCollection.second.erase(
                std::remove_if(
                    jecLevelJetCollection.second.begin(),
                    jecLevelJetCollection.second.end(),
                    [&, this](auto jetSharedPtr){
                        bool removeJet = !this->DoesJetPass(jetSharedPtr.get(), event, product, settings);
                        if (settings.GetDebugVerbosity() > 1 && removeJet) {
                            LOG(DEBUG) << "Remove: LEVEL: " << jecLevelJetCollection.first << (jetSharedPtr.get()->p4);
                        }
                        return removeJet;
                    }
                ),
                jecLevelJetCollection.second.end()
            );
                if (settings.GetDebugVerbosity() > 1) {
                    LOG(DEBUG) << "After: " << jecLevelJetCollection.second.size() << " Jets";
                }
        }
    };

    virtual bool DoesJetPass(const KJet* jet, ZJetEvent const& event, ZJetProduct const& product, ZJetSettings const& settings) const = 0;

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

    virtual bool DoesJetPass(const KJet* jet, ZJetEvent const& event, ZJetProduct const& product, ZJetSettings const& settings) const;

  protected:

    std::vector<TH2D*> m_cleaningHistograms;
    double m_cleaningHistogramsValueMaxValid;
};
