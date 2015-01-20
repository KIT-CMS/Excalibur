#include "ZJetEventProvider.h"

/**
\brief class to connect the analysis specific event content to the pipelines.
*/

ZJetEventProvider::ZJetEventProvider(FileInterface2& fileInterface,
                                     InputTypeEnum inpType)
    : KappaEventProvider<ZJetTypes>(fileInterface, inpType)
{
}

void ZJetEventProvider::WireEvent(setting_type const& settings)
{
	KappaEventProvider::WireEvent(settings);
}
