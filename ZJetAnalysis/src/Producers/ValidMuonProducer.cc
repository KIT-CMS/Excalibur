#include "ZJet/ZJetAnalysis/interface/Producers/ValidMuonProducer.h"


void ValidMuonProducer::Produce(ZJetEvent const& event, ZJetProduct& product,
		ZJetSettings const& settings) const
{
	for (KDataMuons::iterator it = event.m_muons->begin();
			 it != event.m_muons->end(); it++)
	{
		bool good_muon = true;

		// Own loose cuts on muons and muon isolation
		good_muon = good_muon
					&& it->p4.Pt() > settings.GetMuonPtMin()
					&& std::abs(it->p4.Eta()) < settings.GetMuonEtaMax()
					&& it->trackIso03 < 3.0;

		// Tight MuonID 2012
		// [twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Tight_Muon)
		// The comments describe, how CMSSW treats the recoMu.
		/// version of MuonID
		bool is2011 = settings.GetMuonID2011();
		good_muon = good_muon
					&& it->isGlobalMuon()
					// use PF muons
					&& it->isPFMuon()
					// normalizedChi2
					&& it->globalTrack.chi2 / it->globalTrack.nDOF < 10.
					// hitPattern().numberOfvalidmuonHits
					&& it->globalTrack.nValidMuonHits > 0
					// numberOfMatchedStations
					&& it->nMatches > 1
					// fabs(muonBestTrack()->dxy(vertex->position))
					&& std::abs(it->bestTrack.getDxy(&event.m_vertexSummary->pv)) < 0.2
					// fabs(muonBestTrack()->dz(vertex->position)) // not in 2011
					&& std::abs(it->bestTrack.getDz(&event.m_vertexSummary->pv)) < 0.5 + 99999. * is2011
					// hitPattern().numberOfValidPixelHits()
					&& it->innerTrack.nValidPixelHits > 0
					// hitPattern().trackerLayersWithMeasurement() // 8 in 2011
					&& it->track.nPixelLayers + it->track.nStripLayers > 5 + 3 * is2011;

		if (good_muon)
			product.m_validmuons.push_back(*it);
		else
			product.m_invalidmuons.push_back(*it);
	}

}


