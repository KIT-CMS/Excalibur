#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"

#include "Artus/KappaAnalysis/interface/Producers/ValidElectronsProducer.h"
/*
 * ZJetValidElectronsProducer
 * ==========================
 *
 * Extends the Artus/KappaAnalysis ValidElectronsProducer.
 *
 * Implements the following additional criteria for electrons to be considered
 * valid:
 *    - electron must pass versioned ID (VID)
 *    - electron must not land in ECAL gap (1.442 <= eta <= 1.566)
 *
 * Settings used by this producer:
 *    - ExcludeECALGap (bool) :
 *          If true, only electrons reconstructed outside the ECAL
 *          gap are marked as valid.
 *    - ApplyElectronVID (bool) :
 *          If true, only electrons passing the VID are marked as valid.
 *    - ElectronVIDName (string) : name of the electron VID to apply
 *          (only used if ApplyElectronVID is true)
 *    - ElectronVIDType (string) : VID type {"CutBased", "MVA"}
 *          (only used if ApplyElectronVID is true)
 *    - ElectronVIDWorkingPoint (string) : VID working point
 *          {"veto", "loose", "medium", "tight"} for CutBased ID
 *          {"wp90", "wp80", "wpLoose"} for MVA ID
 *          (only used if ApplyElectronVID is true)
 */

class ZJetValidElectronsProducer : public ValidElectronsProducer<ZJetTypes>
{
  public:
    std::string GetProducerId() const override { return "ZJetValidElectronsProducer"; }

    virtual void Init(setting_type const& settings) override
    {
        ValidElectronsProducer<ZJetTypes>::Init(settings);
        m_excludeECALgap = settings.GetExcludeECALGap();
        m_applyElectronVID = (settings.GetApplyElectronVID());

        const std::string electronVIDName = settings.GetElectronVIDName();
        const std::string electronVIDType = boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetElectronVIDType()));
        const std::string electronVIDWorkingPoint = boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetElectronVIDWorkingPoint()));

        // determine and save full VID tag
        if (m_applyElectronVID) {
            if (electronVIDName == "") {
                LOG(ERROR) << "[ZJetValidElectronsProducer] Requested application of electron "
                           << "VID, but config key 'ElectronVIDName' is empty string!";
                exit(39225);
            }
            if (electronVIDType == "cutbased") {
                if ((electronVIDWorkingPoint != "veto") &&
                    (electronVIDWorkingPoint != "loose") &&
                    (electronVIDWorkingPoint != "medium") &&
                    (electronVIDWorkingPoint != "tight")) {

                    LOG(WARNING) << "[ZJetValidElectronsProducer] Unknown CutBased VID "
                              << "working point '" << electronVIDWorkingPoint << "': "
                              << "continuing, but could fail later...";
                }
                m_electronVID_fullTag = "egmGsfElectronIDs:cutBasedElectronID-" + electronVIDName + "-" + electronVIDWorkingPoint;
            }
            else if (electronVIDType == "mva") {
                if ((electronVIDWorkingPoint != "wp90") &&
                    (electronVIDWorkingPoint != "wp80") &&
                    (electronVIDWorkingPoint != "wpLoose")) {

                    LOG(WARNING) << "[ZJetValidElectronsProducer] Unknown MVA VID "
                              << "working point '" << electronVIDWorkingPoint << "': "
                              << "continuing, but could fail later...";
                }
                m_electronVID_fullTag = "egmGsfElectronIDs:mvaEleID-" + electronVIDName + "-" + electronVIDWorkingPoint;
            }
            else if (electronVIDType == "cutbased_v2") {
                if ((electronVIDWorkingPoint != "veto") &&
                    (electronVIDWorkingPoint != "loose") &&
                    (electronVIDWorkingPoint != "medium") &&
                    (electronVIDWorkingPoint != "tight")) {

                    LOG(WARNING) << "[ZJetValidElectronsProducer] Unknown CutBased VID "
                              << "working point '" << electronVIDWorkingPoint << "': "
                              << "continuing, but could fail later...";
                }
                m_electronVID_fullTag = "cutBasedElectronID-" + electronVIDName + "-" + electronVIDWorkingPoint + ":";
            }
            else {
                LOG(ERROR) << "[ZJetValidElectronsProducer] Unknown VID type '"
                           << electronVIDType << "': expected one of {'CutBased', 'MVA'}";
                exit(39225);
            }

            LOG(DEBUG) << "[ZJetValidElectronsProducer] Applying VID with tag: '"
                       << m_electronVID_fullTag << "'";
        }
        else {
            LOG(DEBUG) << "[ZJetValidElectronsProducer] Not applying VID";
        }
    }

  protected:
    // ZJet specific additional definitions
    bool AdditionalCriteria(KElectron* electron,
                            event_type const& event,
                            product_type& product,
                            setting_type const& settings) const override
    {
        bool _qPasses = true;

        // if m_excludeECALgap is true, check electron eta
        if (_qPasses && m_excludeECALgap) {
            _qPasses = _qPasses && (std::abs(electron->p4.Eta()) < 1.442f || std::abs(electron->p4.Eta()) > 1.566f);
        }

        // if electron passes so far, and instructed to apply VID -> check if it passes VID
        if (_qPasses && m_applyElectronVID) {
            _qPasses = _qPasses && electron->getId(m_electronVID_fullTag, event.m_electronMetadata);
        }

        return _qPasses;
    }

    bool m_excludeECALgap;

    bool m_applyElectronVID;
    std::string m_electronVID_fullTag;
};
