#pragma once

#include "TH2F.h"
#include "Excalibur/Compile/interface/ZJetTypes.h"
#include "Excalibur/Compile/interface/Producers/JetCleaner.h"


/**
 *  \brief Producer for valid jets given the constraints of Z->ll+Jet analyses
 *
 *  This producer modifies the collection of valid jets (`product.m_validJets`) to
 *  conform to the specific requirements of the Z->ll+Jets analyses.
 *  This producer should be run after any ValidJetsProducers and the JEC Producer as it vetoes
 *  previously produced jets. and PUJetID requires fully corrected Jets.
 *
 *  Configuration settings:
 *
 *  MinZllJetDeltaRVeto (type: float) :
 *      minimal required distance between jets and leptons from Z decay
 *
 *  PUJetID (type: string) : one of {'loose', 'medium', 'tight', 'value', 'file'}
 *      sets working point of puJetID.
 *
 *      If 'loose', 'medium' or 'tight', a pre-computed working point is used (needs to exist in the skim,
 *      typically as 'pileupJetId:fullId' under jet metadata).
 *
 *      If 'value', a cut is applied on the full pileup jet ID MVA discriminant (needs to exist in the skim,
 *      typically as 'pileupJetId:fullDiscriminant' under jet metadata). Jets with a full discriminant larger
 *      than this value are considered valid/non-pileup jets. The same value is used in all phase space
 *      regions and can be configured via the setting 'MinPUJetID'.
 *
 *      If 'file', the same procedure as for 'value' is used, but the minimal cut value is read from a ROOT
 *      file depending on the depending on the jet pT/eta. The filename and histogram name can be configured
 *      via the settings 'MinPUJetIDFile' and 'MinPUJetIDHistogramName', respectively.
 *
 *  MinPUJetID (type: float) :
 *      minimal required value of 'pile-up jet ID' for jet to be valid. Only used if 'PUJetID' is set to 'value'
 *
 *  MinPUJetIDFile (type: string) :
 *      ROOT file containing pT and eta-dependent minimal values of 'pile-up jet ID' for jet to be valid.
 *      Only used if 'PUJetID' is set to 'file'.
 *
 *  MinPUJetIDHistogramName (type: string) :
 *      name of a TH2F with inside `MinPUJetIDFile` from which to obtain the minimum value of the pileup jet ID
 *      full MVA discriminant. The 'x' and 'y' axes must correspond to the 'pT' and 'absEta' of the jet.
 *
 *  Note: for the lepton veto to work, the Z-boson must be present in the product.
 *        This requires running either the `ZmmProducer` or the `ZeeProducer`
 *        beforehand.
 *  Note2: for the PUJetID veto to work, the jets contained in `product.m_validJets` must
 *         be `KJet`s (i.e. upcasting via `dynamic_cast<KJet*>(product.m_validJets[i])` must
 *         not return a nullptr). If this is not the case, no PUJetID veto is performed.
 */
class ValidZllJetsProducer : public JetCleanerBase {

  public:
    // can choose between different pileup jet ID working points
    enum class PUJetIDWorkingPoint : int {
        LOOSE = 1,
        MEDIUM = 2,
        TIGHT = 3,
        VALUE = 4,
        FILE = 5
    };

    virtual std::string GetProducerId() const override;

    ValidZllJetsProducer() : JetCleanerBase() {};

    void Init(ZJetSettings const& settings);

    // this should return true if a jet is valid
    virtual bool DoesJetPass(const KJet* jet, ZJetEvent const& event, ZJetProduct const& product, ZJetSettings const& settings) const;

  private:
    float minZllJetDeltaRVeto;

    PUJetIDWorkingPoint m_puJetIDWorkingPoint;
    std::string m_puJetIDMetadataTag;
    TH2F* m_puJetIDMinValueHistogram;
    float m_puJetIDMinValue;

    float maxLeadingJetY;
    bool  objectJetY;
    float maxJetEta;
    bool objectJetEta;
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
    float maxJetEta;
    bool objectJetEta;
};
