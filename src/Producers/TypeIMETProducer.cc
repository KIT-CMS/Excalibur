#include "Producers/TypeIMETProducer.h"

std::string TypeIMETProducer::GetProducerId() const { return "TypeIMETProducer"; }

void TypeIMETProducer::Init(ZJetSettings const& settings)
{
	ZJetProducerBase::Init(settings);
	
	m_metPhiCorrectionParameters = settings.GetMetPhiCorrectionParameters();

	// Use random cone?
	m_l1Corr = settings.GetRC() ? "RC" : "L1";

	m_corrLevels.emplace_back("L1L2L3");
	
	// Residual correctiuons if input is data
	if (settings.GetInputIsData())
	{
		m_corrLevels.emplace_back("L1L2L3Res");
	}
	
	// Flavor based corrections
	if (settings.GetFlavourCorrections())
	{
		m_corrLevels.emplace_back("L1L2L3L5Algo");
		m_corrLevels.emplace_back("L1L2L3L5Phys");
	}
}

void TypeIMETProducer::Produce(ZJetEvent const& event, ZJetProduct& product,
                               ZJetSettings const& settings) const
{
	KMET* rawmet;
	float sumEt_correction = 0;

	rawmet = event.m_met;

	// Iterate over the jet collection and sum up the differences between L1L2L3(Res) and L1
	for (unsigned int corrLevelIndex = 0; corrLevelIndex < m_corrLevels.size(); corrLevelIndex++)
	{
		KLV correction;
		for (unsigned int jetIndex = 0; jetIndex < product.m_correctedZJets.at(m_corrLevels[corrLevelIndex]).size(); ++jetIndex)
		{
			KLV* corrjet = (SafeMap::Get(product.m_correctedZJets, m_corrLevels[corrLevelIndex]).at(jetIndex)).get();

			if (corrjet->p4.Pt() > settings.GetJetPtMin())
			{
				KLV* l1jet = (SafeMap::Get(product.m_correctedZJets, m_l1Corr).at(jetIndex)).get();
				correction.p4 +=  l1jet->p4 - corrjet->p4;
				sumEt_correction += correction.p4.Pt();
			}
		}

		KMET corrmet = * rawmet;
		corrmet.p4 += correction.p4;

		// Eta of MET is always zero
		corrmet.p4.SetEta(0.0f);
		corrmet.sumEt = rawmet->sumEt + sumEt_correction;

		// Apply MET-phi-corrections
		if (settings.GetEnableMetPhiCorrection())
		{
			double px = corrmet.p4.Px();
			double py = corrmet.p4.Py();

			px = px - (m_metPhiCorrectionParameters.at(0) + m_metPhiCorrectionParameters.at(1) * event.m_vertexSummary->nVertices);
			py = py - (m_metPhiCorrectionParameters.at(2) + m_metPhiCorrectionParameters.at(3) * event.m_vertexSummary->nVertices);

			corrmet.p4.SetPt(sqrt(px * px + py * py));
			corrmet.p4.SetPhi(atan2(py, px));
		}
		product.m_corrMET[m_corrLevels[corrLevelIndex]] = corrmet;
	}

}
