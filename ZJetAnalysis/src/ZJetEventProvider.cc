#include "ZJet/ZJetAnalysis/interface/ZJetEventProvider.h"

/**
\brief class to connect the analysis specific event content to the pipelines.
*/


ZJetEventProvider::ZJetEventProvider(FileInterface2 & fileInterface, InputTypeEnum inpType) :
	KappaEventProvider<ZJetTypes>(fileInterface, inpType)
{}

void ZJetEventProvider::WireEvent(global_setting_type const& globalSettings)
{
	KappaEventProvider::WireEvent(globalSettings);
}


