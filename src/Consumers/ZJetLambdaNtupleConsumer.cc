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
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zpt", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Pt();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zeta", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Eta();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zphi", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Phi();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zy", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Rapidity();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zmass", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.mass();
	} );
	
	//////////
	// Jets //
	//////////
	
	// Leading jet
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetValidPrimaryJet(settings, event)->p4.Pt();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1eta", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetValidPrimaryJet(settings, event)->p4.Eta();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1y", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetValidPrimaryJet(settings, event)->p4.Rapidity();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1phi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetValidPrimaryJet(settings, event)->p4.Phi();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1photonfraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->photonFraction;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1electronfraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->electronFraction;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1chargedhadfraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->chargedHadronFraction;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1neutralhadfraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->neutralHadronFraction;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1muonfraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->muonFraction;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1HFhadfraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->hfHadronFraction;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1HFemfraction", [settings](ZJetEvent const& event, ZJetProduct const& product)
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
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet2pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 1) ? product.GetValidJet(settings, event, 1)->p4.Pt() : -999.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet2phi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 1) ? product.GetValidJet(settings, event, 1)->p4.Phi() : -999.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet2eta", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 1) ? product.GetValidJet(settings, event, 1)->p4.Eta() : -999.;
	} );
	
	// General jet stuff
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("njets", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetValidJetCount(settings, event);
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("njetsinv", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetInvalidJetCount(settings, event);
	} );
	
	// TODO if needed
	// njets30, njets30barrel, genjet1pt, genjet1ptneutrinos, genjet1eta, genjet1phi, matchedgenjet1pt,
	// matchedgenjet2pt, genjet2pt, deltaRgenjet1genjet2, deltaRjet1jet2, deltaRjet1genjet1, deltaRjet2genjet2
	
	/////////
	// MET //
	/////////
	
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("METpt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event)->p4.Pt();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("METphi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event)->p4.Phi();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("sumEt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event)->sumEt;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("rawMETpt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event, "None")->p4.Pt();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("rawMETphi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event, "None")->p4.Phi();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mpf", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMPF(product.GetMet(settings, event));
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("rawmpf", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMPF(product.GetMet(settings, event, "None"));
	} );

	// Needs to be called at the end
	KappaLambdaNtupleConsumer::Init(settings);
}
