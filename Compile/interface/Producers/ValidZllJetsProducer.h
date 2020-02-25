#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"


/**
 *  \brief Producer for valid jets given the constraints of Z->ll+Jet analyses
 *
 *  This producer modifies the collection of valid jets (`product.m_validJets`) to
 *  conform to the specific requirements of the Z->ll+Jets analyses.
 *  This producer should be run after any ValidJetsProducers, as it vetoes previously
 *  produced jets.
 *
 *  Configuration settings:
 *
 *  MinZllJetDeltaRVeto (type: float) :
 *      minimal required distance between jets and leptons from Z decay
 * PUJetID (type: string):
 *      sets working point of puJetID to 'loose', 'medium', 'tight'. Choose 'none' to use a minimal value of 'pile-up jet ID'.
 *      Needs to be defined in skim file, typically as 'pileupJetId:fullId'
 * MinPUJetID (type: float) :
 *      minimal required value of 'pile-up jet ID' for jet to be valid. Only used if working point is set to 'none'!
 *      Needs to be defined in skim file, typically as 'pileupJetId:fullDiscriminant'
 *
 *  Note: for the lepton veto to work, the Z-boson must be present in the product.
 *        This requires running either the `ZmmProducer` or the `ZeeProducer`
 *        beforehand.
 *  Note2: for the PUJetID veto to work, the jets contained in `product.m_validJets` must
 *         be `KJet`s (i.e. upcasting via `dynamic_cast<KJet*>(product.m_validJets[i])` must
 *         not return a nullptr). If this is not the case, no PUJetID veto is performed.
 */
class ValidZllJetsProducer : public ZJetProducerBase {

  public:
    ValidZllJetsProducer() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    std::string GetProducerId() const override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override {

        // remove jets from m_validJets if they are rejected by DoesJetPass()
        product.m_validJets.erase(
            std::remove_if(
                product.m_validJets.begin(),
                product.m_validJets.end(),
                [&, this](const KBasicJet* jetPtr){
                    return !this->DoesJetPass(jetPtr, event, product, settings);
                }),
            product.m_validJets.end()
        );
    };

    // this should return true if a jet is valid
    virtual bool DoesJetPass(const KBasicJet* jet, ZJetEvent const& event, ZJetProduct const& product, ZJetSettings const& settings) const;

  private:
    float minZllJetDeltaRVeto;
    std::string PUJetID;
    float minPUJetID;
    std::string PUJetIDModuleName;
    float maxLeadingJetY;
    bool  objectJetY;
};


/**
 *  \brief Producer for valid generator jets given the constraints of Z->ll+Jet analyses
 *
 *  This producer creates the collection of valid generator jets (`product.m_simpleGenJets`)
 *  according to the specific requirements of the Z->ll+Jets analyses.
 *
 *  Configuration settings:
 *
 *  MinZllJetDeltaRVeto (type: float) :
 *      minimal required distance between gen jets and leptons from the gen Z decay
 *
 *  Note: for the lepton veto to work, the gen-Z-boson must be present in the product.
 *        This requires running either the `GenZmmProducer` or the `GenZeeProducer`
 *        beforehand.
 *
 */
class ValidZllGenJetsProducer : public ZJetProducerBase {

  public:
    ValidZllGenJetsProducer() : ZJetProducerBase(), minZllJetDeltaRVeto(0) {}

    void Init(ZJetSettings const& settings) override;

    std::string GetProducerId() const override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override {

        product.m_simpleGenJets.clear();

        // create pointers to genjets in product.m_simpleGenJets if they are accepted by DoesJetPass()
        for (KLV& genJet : (*((KLVs*)event.m_genJets))) {
            if (DoesJetPass(genJet, event, product, settings)) {
                product.m_simpleGenJets.push_back(&genJet);
            }
        }
    };

    // this should return true if a gen jet is valid
    virtual bool DoesJetPass(const KLV& genJet, ZJetEvent const& event, ZJetProduct const& product, ZJetSettings const& settings) const;

  private:
    float minZllJetDeltaRVeto;
    float maxLeadingJetY;
    bool  objectJetY;
};
