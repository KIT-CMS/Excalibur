#include "ZJetEventProvider.h"

/**
\brief class to connect the analysis specific event content to the pipelines.
*/

ZJetEventProvider::ZJetEventProvider(FileInterface2& fileInterface, InputTypeEnum inpType)
    : KappaEventProvider<ZJetTypes>(fileInterface, inpType)
{
}

void ZJetEventProvider::WireEvent(setting_type const& settings)
{
    KappaEventProvider::WireEvent(settings);

    /*
     * This is code for multiple jet collections
    // Wire all the jet types requested via GlobalAlgorithms
    // Gen jets (KLV) and untagged jets (KBasicJet) will be casted to KJet so they can be handled
    uniformly
    // TODO: Is this okay? Now gen jets could also be stored in m_jets if needed
    for (unsigned int i = 0; i < settings.GetGlobalAlgorithms().size(); ++i)
    {
    //LOG(WARNING) << settings.GetGlobalAlgorithms()[i];
    if (settings.GetGlobalAlgorithms()[i].find("Gen") == std::string::npos)
    { // Reco jets
        if (settings.GetGlobalAlgorithms()[i].find("Tagged") == std::string::npos)
        { // Untagged reco jets
        if (settings.GetGlobalAlgorithms()[i].find("chs") == std::string::npos)
        { // Untagged reco jets without CHS
            this->m_event.m_jets[settings.GetGlobalAlgorithms()[i] + "Jets"] =
    (std::vector<KJet>*)(this->template
    SecureFileInterfaceGet<KBasicJets>(settings.GetGlobalAlgorithms()[i] + "Jets"));
        }
        else
        { // Untagged reco jets with CHS
            this->m_event.m_jets[settings.GetGlobalAlgorithms()[i].substr(0, 5) + "JetsCHS"] =
    (std::vector<KJet>*)(this->template
    SecureFileInterfaceGet<KBasicJets>(settings.GetGlobalAlgorithms()[i].substr(0, 5) + "JetsCHS"));
        }
        }
        else
        { // Tagged reco jets
        if (settings.GetGlobalAlgorithms()[i].find("chs") == std::string::npos)
        { // Tagged reco jets without CHS
            this->m_event.m_jets[settings.GetGlobalAlgorithms()[i] + "Jets"] = this->template
    SecureFileInterfaceGet<KJets>(settings.GetGlobalAlgorithms()[i] + "Jets");
        }
        else
        { // Tagged reco jets with CHS
            this->m_event.m_jets[settings.GetGlobalAlgorithms()[i].substr(0, 5) + "TaggedJetsCHS"] =
    this->template SecureFileInterfaceGet<KJets>(settings.GetGlobalAlgorithms()[i].substr(0, 5) +
    "TaggedJetsCHS");
        }
        }
    }
    else
    { // Gen jets
        this->m_event.m_genZJets[settings.GetGlobalAlgorithms()[i] + "Jets"] =
    (std::vector<KJet>*)(this->template
    SecureFileInterfaceGet<KLVs>(settings.GetGlobalAlgorithms()[i] + "Jets"));
    }
    }
    */
}
