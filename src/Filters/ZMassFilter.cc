
#include "Filters/ZMassFilter.h"

std::string ZMassFilter::GetFilterId() const { return "ZMassFilter"; }

bool ZMassFilter::DoesEventPass(ZJetEvent const& event,
                                ZJetProduct const& product,
                                ZJetSettings const& settings) const
{
	// TODO Implement actual filter here
	return true;
}
