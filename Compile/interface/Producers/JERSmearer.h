#pragma once

#include <random>

#include "Excalibur/Compile/interface/ZJetTypes.h"

#include "JetMETCorrections/Modules/interface/JetResolution.h"



/** Producer implementing Jet Energy Resolution (JER) smearing for Monte Carlo
 *
 *  The smearing procedure is implemented here as described in:
 *      https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution#Smearing_procedures
 *      [2018-10-09]
 * 
 *  Configuration settings:
 *
 *  JER (type: string) :
 *      path to the directory containing the Jet Energy Resolution
 *      (e.g. '../JRDataBase/textFiles/Summer16_25nsV1')
 * 
 *  JERMethod (type: string) : one of {'stochastic', 'hybrid'}
 *      the JER smearing method to use. In the 'stochastic' method, the
 *      jet pT is scaled with a random number drawn from a Gaussian
 *      distribution with a scale parameter determined from the
 *      pT resolution and the mc/data resolution scale factor.
 *      The 'hybrid' method requires a generator-level jet match for the
 *      leading reconstructed jet and scales the jet pT by a factor
 *      depending on the gen-reco pT difference and the the mc/data
 *      resolution scale factor. If no match is available for a jet,
 *      the smearing is done using the 'stochastic' method.
 * 
 *  JERSmearerSeed (type: int) :
 *      seed used for the random number generator
 *
 *  Note: This needs to run after the JEC producer.
 *  Additionally, if the 'hybrid' smearing method is chosen, the
 * `RecoJetGenJetMatchingProducer` must also run before this one.
 */

class JERSmearer : public ZJetProducerBase
{
  public:
    // can choose between three different scaling methods
    enum class SmearingMethod : int {
        STOCHASTIC = 1,
        HYBRID     = 2
    };
  
    std::string GetProducerId() const override;

    JERSmearer() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  private:
    SmearingMethod m_smearingMethod;
    Variation m_systematic_variation;
    std::unique_ptr<JME::JetResolution> m_jetResolution;
    std::unique_ptr<JME::JetResolutionScaleFactor> m_jetResolutionScaleFactor;

    mutable std::mt19937 m_randomNumberGenerator;
};
