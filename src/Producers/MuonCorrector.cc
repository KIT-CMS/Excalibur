#include "MuonCorrector.h"

std::string MuonCorrector::GetProducerId() const { return "MuonCorrector"; }

void MuonCorrector::Init(ZJetSettings const& settings)
{
    LOG(INFO) << "muon corr init" << settings.GetMuonCorrectionParameters();

    m_deterministic = false;  // TODO make this configurable?
    m_smearing = settings.GetMuonSmearing();
    m_radiationcorr = settings.GetMuonRadiationCorrection();
    m_parameterfile = settings.GetMuonCorrectionParameters();
    m_parameterfileRunD = settings.GetMuonCorrectionParametersRunD();

    m_corrector = new MuScleFitCorrector(m_parameterfile);
    if (m_parameterfileRunD == "None") {
        m_correctorRunD = new MuScleFitCorrector(m_parameterfile);
    } else {
        m_correctorRunD = new MuScleFitCorrector(m_parameterfileRunD);
    }

    if (m_parameterfile == "")
        LOG(FATAL) << "Muon corrections enabled but no parameters given.";
    if (m_smearing && m_deterministic)
        LOG(INFO) << "Loading muon corrections (smeared, deterministic):";
    if (m_smearing && !m_deterministic)
        LOG(INFO) << "Loading muon corrections (smeared, random):";
    if (!m_smearing)
        LOG(INFO) << "Loading muon corrections (not smeared):";

    LOG(INFO) << "  " << m_parameterfile;
    if (m_parameterfileRunD != "None")
        LOG(INFO) << "  " << m_parameterfileRunD;
}

void MuonCorrector::Produce(ZJetEvent const& event,
                            ZJetProduct& product,
                            ZJetSettings const& settings) const
{
    bool isRunD = (settings.GetInputIsData() && event.m_eventInfo->nRun > m_startRunD);
    double corrPt = 0;
    double smearedPt = 0;
    if (isRunD) {
        if (m_parameterfileRunD == "None")
            LOG(FATAL) << "Tried to correct muons in Run D, but no parameters given!";
    }

    // loop over valid muons an correct in place
    for (auto& mu : product.m_validMuons) {
        if (isRunD) {
            corrPt = m_correctorRunD->getCorrectPt(mu->p4, mu->charge());
        } else {
            corrPt = m_corrector->getCorrectPt(mu->p4, mu->charge());
        }
        mu->p4.SetPt(corrPt);

        if (m_smearing) {
            if (isRunD) {
                smearedPt = m_correctorRunD->getSmearedPt(mu->p4, mu->charge(), m_deterministic);
            } else {
                smearedPt = m_corrector->getSmearedPt(mu->p4, mu->charge(), m_deterministic);
            }
            mu->p4.SetPt(smearedPt);
        }

        if (m_radiationcorr) {
            mu->p4.SetPt(1.004f * mu->p4.Pt());
        }
    }
}
