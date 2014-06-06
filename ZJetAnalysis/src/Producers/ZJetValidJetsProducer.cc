#include "ZJet/ZJetAnalysis/interface/Producers/ZJetValidJetsProducer.h"

	bool ZJetValidJetsProducer::AdditionalCriteria(KDataPFTaggedJet* jet,
		event_type const& event, product_type& product, setting_type const& settings) const
	{
		bool validJet = true;
		// 5 GeV minimum pT
		validJet = validJet && (jet->p4.Pt() > 5);

		//isolation DeltaR > 0.5
		float dr1, dr2;
		dr1 = 99999.0f;
		dr2 = 99999.0f;

		dr1 = ROOT::Math::VectorUtil::DeltaR(jet->p4,
											 product.m_decaymuons[0]->p4);
		dr2 = ROOT::Math::VectorUtil::DeltaR(jet->p4,
											 product.m_decaymuons[1]->p4);
		validJet = validJet && (dr1 > 0.5) && (dr2 > 0.5);

		return validJet;
	}
