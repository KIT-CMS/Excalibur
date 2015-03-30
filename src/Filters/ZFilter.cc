#include "Filters/ZFilter.h"

std::string ZFilter::GetFilterId() const { return "ZFilter"; }

bool ZFilter::DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
                            ZJetSettings const& settings) const
{
	if (product.m_validZ == false)
	{
		return false;
	}
	return true;
}
