#include "Producers/ZJetCorrectionsProducer.h"

std::string ZJetCorrectionsProducer::GetProducerId() const {
	return "ZJetCorrectionsProducer";
}

void ZJetCorrectionsProducer::Init(ZJetSettings const& settings)
{
	ZJetProducerBase::Init(settings);
	
	// CHS oder no CHS jets?
	std::string algoName = settings.GetTaggedJets();
	if (algoName.find("chs") == std::string::npos) {
		algoName = algoName.substr(0, 5);
	}
	else
	{
		algoName = algoName.substr(0, 5) + "chs";
	}
		
	// JEC initialization
	std::vector<JetCorrectorParameters> jecParameters;
	
	// L1 depending on config parameter
	jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + settings.GetL1Correction() + "_" + algoName + ".txt"));
	m_l1 = new FactorizedJetCorrector(jecParameters);
	jecParameters.clear();
	
	// RC
	if (settings.GetRC())
	{
		jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "RC" + "_" + algoName + ".txt"));
		m_rc = new FactorizedJetCorrector(jecParameters);
		jecParameters.clear();
	}
	
	// L2Relative
	jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L2Relative" + "_" + algoName + ".txt"));
	m_l2 = new FactorizedJetCorrector(jecParameters);
	jecParameters.clear();
	
	// L3Absolute
	jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L3Absolute" + "_" + algoName + ".txt"));
	m_l3 = new FactorizedJetCorrector(jecParameters);
	jecParameters.clear();
	
	// Flavor based corrections
	if (settings.GetFlavourCorrections())
	{
		jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L5Flavor_qJ" + "_" + algoName + ".txt"));
		m_l2l3res = new FactorizedJetCorrector(jecParameters);
		jecParameters.clear();
		jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L5Flavor_gJ" + "_" + algoName + ".txt"));
		m_l2l3res = new FactorizedJetCorrector(jecParameters);
		jecParameters.clear();
		jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L5Flavor_cJ" + "_" + algoName + ".txt"));
		m_l2l3res = new FactorizedJetCorrector(jecParameters);
		jecParameters.clear();
		jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L5Flavor_bJ" + "_" + algoName + ".txt"));
		m_l2l3res = new FactorizedJetCorrector(jecParameters);
		jecParameters.clear();
	}

	// L2L3Residual
	if (settings.GetInputIsData())
	{
		jecParameters.push_back(JetCorrectorParameters(settings.GetJec() + "_" + "L2L3Residual" + "_" + algoName + ".txt"));
		m_l2l3res = new FactorizedJetCorrector(jecParameters);
		jecParameters.clear();
	}
	
	// JEU initialization
	// Not yet implemented..
}

void ZJetCorrectionsProducer::Produce(ZJetEvent const& event, ZJetProduct& product,
									  ZJetSettings const& settings) const
{
	// TODO: Do we need more assertions?
	assert(event.m_pileupDensity);
	assert(event.m_vertexSummary);
	
	CorrectJetCollection("None", "L1", m_l1, event, product, settings);
	if (settings.GetRC())
	{
		CorrectJetCollection("None", "RC", m_l1, event, product, settings);
	}
	CorrectJetCollection("L1", "L1L2", m_l2, event, product, settings);
	CorrectJetCollection("L1L2", "L1L2L3", m_l3, event, product, settings);
	if (settings.GetFlavourCorrections())
	{
		CorrectJetCollection("L1L2L3", "L1L2L3L5q", m_l5q, event, product, settings);
		CorrectJetCollection("L1L2L3", "L1L2L3L5g", m_l5g, event, product, settings);
		CorrectJetCollection("L1L2L3", "L1L2L3L5c", m_l5c, event, product, settings);
		CorrectJetCollection("L1L2L3", "L1L2L3L5b", m_l5b, event, product, settings);
	}
	if (settings.GetInputIsData())
	{
		CorrectJetCollection("L1L2L3", "L1L2L3Res", m_l2l3res, event, product, settings);
	}

		// Sort vectors of corrected jets by pt
		/*
		std::sort(product.m_correctedZJets[italgo->first + itlevel->first].begin(),
				  product.m_correctedZJets[italgo->first + itlevel->first].end(),
				  [](std::shared_ptr<KJet> jet1, std::shared_ptr<KJet> jet2) -> bool
				  { return jet1->p4.Pt() > jet2->p4.Pt(); });
		*/

}

void ZJetCorrectionsProducer::CorrectJetCollection(std::string inCorrLevel, std::string outCorrLevel,
												   FactorizedJetCorrector* factorizedJetCorrector,
												   ZJetEvent const& event, ZJetProduct& product,
												   ZJetSettings const& settings) const
{
	// Create a copy of all jets in the event (first temporarily for the JEC)
	unsigned int jetCount = product.GetValidJetCount(settings, event, inCorrLevel);
	std::vector<KJet> correctJetsForJecTools(jetCount);
	for (unsigned int jetIndex = 0; jetIndex < jetCount; ++jetIndex)
	{
		correctJetsForJecTools[jetIndex] = *(static_cast<KJet*>(product.GetValidJet(settings, event, jetIndex, inCorrLevel)));
	}

	// Apply jet energy corrections and uncertainty shift
	correctJets(&correctJetsForJecTools, factorizedJetCorrector, correctionUncertainty,
				event.m_pileupDensity->rho, event.m_vertexSummary->nVertices, -1,
				settings.GetJetEnergyCorrectionUncertaintyShift());

	// Create shared pointers and store them in the product
	product.m_correctedZJets[outCorrLevel].clear();
	product.m_correctedZJets[outCorrLevel].resize(correctJetsForJecTools.size());
	unsigned int jetIndex = 0;
	for (typename std::vector<KJet>::const_iterator jet = correctJetsForJecTools.begin(); jet != correctJetsForJecTools.end(); ++jet)
	{
		product.m_correctedZJets[outCorrLevel][jetIndex] = std::shared_ptr<KJet>(new KJet(*jet));
		++jetIndex;
	}
}
