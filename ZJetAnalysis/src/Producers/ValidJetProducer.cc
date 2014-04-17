#include "ZJet/ZJetAnalysis/interface/Producers/ValidJetProducer.h"


void ValidJetProducer::ProduceGlobal(ZJetEvent const& event, ZJetProduct& product,
		ZJetGlobalSettings const& globalSettings) const
{
	std::string jetalgo;
	if(! globalSettings.GetTaggedJets().empty())
		jetalgo = globalSettings.GetTaggedJets();
	else if (! globalSettings.GetJets().empty())
		jetalgo = globalSettings.GetJets();
	else
		LOG(FATAL) << "No jets found! Check your config file!";


	for (auto jet = event.m_tjets->begin(); jet != event.m_tjets->end(); jet++)
	{
		bool good_jet = true;

		// 5 GeV minimum pT
		good_jet = good_jet && ((*jet).p4.Pt() > 5);

		//isolation DeltaR > 0.5
		float dr1, dr2;
		dr1 = 99999.0f;
		dr2 = 99999.0f;

		dr1 = ROOT::Math::VectorUtil::DeltaR((*jet).p4,
											 product.m_decaymuons[0]->p4);
		dr2 = ROOT::Math::VectorUtil::DeltaR((*jet).p4,
											 product.m_decaymuons[1]->p4);
		good_jet = good_jet && (dr1 > 0.5) && (dr2 > 0.5);

		// JetID
		// https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID
		//// PFJets, all eta
		good_jet = good_jet
				   && (*jet).neutralHadFraction + (*jet).HFHadFraction < 0.99
				   && (*jet).neutralEMFraction < 0.99
				   && (*jet).nConst > 1;
		//// PFJets, |eta| < 2.4 (tracker)
		if (std::abs((*jet).p4.eta()) < 2.4)
		{
			good_jet = good_jet
					   && (*jet).chargedHadFraction > 0.0
					   && (*jet).nCharged > 0
					   && (*jet).chargedEMFraction < 0.99;
		}

		if (globalSettings.GetVetoPileupJets())
		{
			bool puID = (*jet).getpuJetID("puJetIDFullMedium", event.m_taggermetadata);
			good_jet = good_jet && puID;
		}

		if (good_jet)
			product.m_validjets[jetalgo].push_back(*jet);
		else
			product.m_invalidjets[jetalgo].push_back(*jet);
		}
		
				
}


