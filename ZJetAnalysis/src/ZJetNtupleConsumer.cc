
#include "Artus/Utility/interface/Utility.h"

#include "ZJet/ZJetAnalysis/interface/ZJetNtupleConsumer.h"


void ZJetNtupleConsumer::Init(Pipeline<ZJetTypes>* pset)
{

	
	m_valueExtractorMap["npv"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return event.m_vertexSummary->nVertices; };

	m_valueExtractorMap["jet1pt"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return event.m_tjets->at(0).p4.Pt(); };

	m_valueExtractorMap["run"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return event.m_eventMetadata->nRun; };

	m_valueExtractorMap["metphi"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return event.m_met->p4.Phi(); };
	
	m_valueExtractorMap["validz"] = [](ZJetEvent const & event, ZJetProduct const & product)
	{return product.has_valid_z; };

	LambdaNtupleConsumerBase<ZJetTypes>::Init(pset);
}

std::string ZJetNtupleConsumer::GetConsumerId() const// ARTUS_CPP11_OVERRIDE
{
	return "ntuple";
}


