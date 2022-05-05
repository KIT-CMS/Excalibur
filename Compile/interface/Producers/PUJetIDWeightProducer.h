#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"
#include "TH2.h"

/**
 *  \brief Producer to create weight to consider PUJetID efficiency 
 *
 *  This producer create an additional weight to data based corrected leading jets.
 *  Configuration settings:
 *
 *  PUJetID (type: string):
 *      sets working point of puJetID to 'loose', 'medium', 'tight'. Choose 'none' to use a minimal value of 'pile-up jet ID'.
 *      Needs to be defined in skim file, typically as 'pileupJetId:fullId'
 * 
 *  PUJetIDSelectionMaxPt (type: float):
 *      PUJetID weight only applied on events with leading jet Pt below that value.
 *      
 *  PUEffFilename (type: string):
 *      Name of file which contains the scalefactors for the PUJetID
 *
 *  Note: PUJetID should be only applied on corrected jets.
 *      Therefore, JetCorrectionProducer must run before this producer.
 *      To  get the correct leading jet, this producer have to run after the JetSorter.
 *
 */

class PUJetIDWeightProducer : public ZJetProducerBase {

  public:
    PUJetIDWeightProducer() : ZJetProducerBase() {}

    void Init(ZJetSettings const& settings) override;

    std::string GetProducerId() const override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  private:
    TH2F* m_sfhisto;
    TH2F* m_errhisto;
};
