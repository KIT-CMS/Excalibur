#include "Consumers/ZJetLambdaNtupleConsumer.h"

std::string ZJetLambdaNtupleConsumer::GetConsumerId() const
{
	return "ZJetLambdaNtupleConsumer";
}

void ZJetLambdaNtupleConsumer::Init(ZJetSettings const& settings)
{
	// Add possible quantities for the lambda ntuples consumers
	
	///////
	// Z //
	///////
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zPt", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Pt();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zEta", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Eta();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zPhi", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Phi();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zY", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Rapidity();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zMass", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.mass();
	} );
	
	//////////
	// Jets //
	//////////
	
	// Leading jet
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1Pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetValidPrimaryJet(settings, event)->p4.Pt();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1Eta", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetValidPrimaryJet(settings, event)->p4.Eta();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1Y", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetValidPrimaryJet(settings, event)->p4.Rapidity();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1Phi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetValidPrimaryJet(settings, event)->p4.Phi();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1PhotonFraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->photonFraction;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1ElectronFraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->electronFraction;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1ChargedHadFraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->chargedHadronFraction;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1NeutralHadFraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->neutralHadronFraction;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1MuonFraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->muonFraction;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1HFHadFraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->hfHadronFraction;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1HFEMFraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->hfEMFraction;
	} );
	/*
	 * TODO
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1unc", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->??;
	} );
	*/

	// Second leading jet
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet2Pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 1) ? product.GetValidJet(settings, event, 1)->p4.Pt() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet2Phi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 1) ? product.GetValidJet(settings, event, 1)->p4.Phi() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet2Eta", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 1) ? product.GetValidJet(settings, event, 1)->p4.Eta() : DefaultValues::UndefinedDouble;
	} );
	
	// General jet stuff
	// nJets, nJets30 already implemented by Artus
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("nJetsInv", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetInvalidJetCount(settings, event);
	} );
	
	// TODO if needed
	// njets30barrel, genjet1pt, genjet1ptneutrinos, genjet1eta, genjet1phi, matchedgenjet1pt,
	// matchedgenjet2pt, genjet2pt, deltaRgenjet1genjet2, deltaRjet1jet2, deltaRjet1genjet1, deltaRjet2genjet2
	
	/////////
	// MET //
	/////////
	
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("metPt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event)->p4.Pt();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("metPhi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event)->p4.Phi();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("sumEt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event)->sumEt;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("rawMETPt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event, "None")->p4.Pt();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("rawMETPhi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event, "None")->p4.Phi();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mpf", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMPF(product.GetMet(settings, event));
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("rawMPF", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMPF(product.GetMet(settings, event, "None"));
	} );
	
	///////////
	// MUONS //
	///////////
	
	// nMuons already implemented by Artus
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muPlusPt", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == 1) return (*muon)->p4.Pt();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muPlusEta", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == 1) return (*muon)->p4.Eta();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muPlusPhi", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == 1) return (*muon)->p4.Phi();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muPlusIso", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == 1) return (*muon)->pfIso03;
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muMinusPt", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->p4.Pt();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muMinusEta", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->p4.Eta();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muMinusPhi", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->p4.Phi();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muMinusIso", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->pfIso03;
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muMinusIso", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->pfIso03;
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mu1Pt", [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mu1Phi", [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mu1Eta", [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mu2Pt", [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mu2Phi", [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mu2Eta", [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	
	// TODO if needed
	// genmupluspt, genmupluseta, genmuplusphi, genminuspt, genminuseta, genminusphi
	// ngenmuons, ninternalmuons, nintermediatemuons, ptdiff13, ptdiff12, ptdiff23


	// Needs to be called at the end
	KappaLambdaNtupleConsumer::Init(settings);
}
