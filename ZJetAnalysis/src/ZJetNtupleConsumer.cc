
#include "Artus/Utility/interface/Utility.h"

#include "ZJet/ZJetAnalysis/interface/ZJetNtupleConsumer.h"


void ZJetNtupleConsumer::Init(Pipeline<ZJetTypes>* pset)
{
	algoname = pset->GetSettings().GetJetAlgorithm();
	
	m_valueExtractorMap["npv"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return event.m_vertexSummary->nVertices; };

	m_valueExtractorMap["run"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return event.m_eventMetadata->nRun; };

	m_valueExtractorMap["metphi"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return event.m_met->p4.Phi(); };
	m_valueExtractorMap["metpt"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return event.m_met->p4.Pt(); };

	m_valueExtractorMap["validz"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return product.has_valid_z; };

	m_valueExtractorMap["zmass"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return product.Z.p4.mass(); };
	m_valueExtractorMap["zpt"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return product.Z.p4.Pt(); };
	m_valueExtractorMap["zy"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return product.Z.p4.Rapidity(); };

	m_valueExtractorMap["genzmass"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return product.GenZ.p4.mass(); };
	m_valueExtractorMap["genzpt"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return product.GenZ.p4.Pt(); };
	m_valueExtractorMap["genzy"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return product.GenZ.p4.Rapidity(); };

	m_valueExtractorMap["nvalidmuons"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return product.m_validmuons.size(); };
	
	m_valueExtractorMap["jet1pt"] = [&](ZJetEvent const & event, ZJetProduct const & product)
	{return product.GetLeadingJet(algoname)->p4.Pt(); };
	m_valueExtractorMap["jet1eta"] = [&](ZJetEvent const & event, ZJetProduct const & product)
	{return product.GetLeadingJet(algoname)->p4.Eta(); };
	m_valueExtractorMap["jet1phi"] = [&](ZJetEvent const & event, ZJetProduct const & product)
	{return product.GetLeadingJet(algoname)->p4.Phi(); };

	m_valueExtractorMap["jet2pt"] = [&](ZJetEvent const & event, ZJetProduct const & product)
	{return product.GetSecondJet(algoname)->p4.Pt(); };
	m_valueExtractorMap["jet2eta"] = [&](ZJetEvent const & event, ZJetProduct const & product)
	{return product.GetSecondJet(algoname)->p4.Eta(); };
	m_valueExtractorMap["jet2phi"] = [&](ZJetEvent const & event, ZJetProduct const & product)
	{return product.GetSecondJet(algoname)->p4.Phi(); };

	m_valueExtractorMap["btag"] = [&](ZJetEvent const & event, ZJetProduct const & product)
	{return product.GetLeadingJet(algoname)->getTagger("CombinedSecondaryVertexBJetTags", event.m_taggermetadata); };
	m_valueExtractorMap["qgtag"] = [&](ZJetEvent const & event, ZJetProduct const & product)
	{return product.GetLeadingJet(algoname)->getTagger("QGlikelihood", event.m_taggermetadata); };

	m_valueExtractorMap["mpf"] = [&](ZJetEvent const & event, ZJetProduct const & product)
	{return product.GetMPF(event.m_met); };

	m_valueExtractorMap["njets"] = [&](ZJetEvent const & event, ZJetProduct const & product)
	{return product.m_validJets.size(); };

	LambdaNtupleConsumerBase<ZJetTypes>::Init(pset);
}

std::string ZJetNtupleConsumer::GetConsumerId() const// ARTUS_CPP11_OVERRIDE
{
	return "ntuple";
}


