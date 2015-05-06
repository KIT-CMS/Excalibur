
#pragma once

#include "ZJetTypes.h"

#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"

#define USE_JEC
#include "KappaTools/RootTools/JECTools.h"


/**
   \brief Producer for tagged jet corrections (mainly JEC)
   
   Required config tags:
   - JEC (path and prefix of the correction files)
   Not yet implemented:
   (- JetEnergyCorrectionUncertaintyParameters (default: empty))
   (- JetEnergyCorrectionUncertaintySource (default ""))
   (- JetEnergyCorrectionUncertaintyShift (default 0.0))
   
   Required packages (unfortunately, nobody knows a tag):
   git cms-addpkg CondFormats/JetMETObjects
   
   Documentation:
   https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#JetEnCorFWLite

*/

class ZJetCorrectionsProducer : public ZJetProducerBase
{
  public:
    virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE;
    
	ZJetCorrectionsProducer() : ZJetProducerBase()
	{
	}
	
	~ZJetCorrectionsProducer()
	{
		delete m_l1;
		delete m_rc;
		delete m_l2;
		delete m_l3;
		delete m_l5g;
		delete m_l5q;
		delete m_l5b;
		delete m_l5c;
		delete m_l2l3res;
	}
	
	void Init(ZJetSettings const& settings);

	void Produce(ZJetEvent const& event, ZJetProduct& product,
				 ZJetSettings const& settings) const;

	void CorrectJetCollection(std::string inCorrLevel, std::string outCorrLevel,
							  FactorizedJetCorrector* factorizedJetCorrector,
							  ZJetEvent const& event, ZJetProduct& product,
							  ZJetSettings const& settings) const;

  private:
	FactorizedJetCorrector* m_l1 = 0;
	FactorizedJetCorrector* m_rc = 0;
	FactorizedJetCorrector* m_l2 = 0;
	FactorizedJetCorrector* m_l3 = 0;
	FactorizedJetCorrector* m_l5g = 0;
	FactorizedJetCorrector* m_l5q = 0;
	FactorizedJetCorrector* m_l5b = 0;
	FactorizedJetCorrector* m_l5c = 0;
	FactorizedJetCorrector* m_l2l3res = 0;
	
	JetCorrectionUncertainty* correctionUncertainty = 0;
};
