/** \class METTrigAnalyzerMiniAOD
 *
 * See header file for documentation
 *
 *  \author Dominick Olivito
 *
 */

#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"
#include "ShortExerciseTrigger2023/ShortExerciseTrigger/interface/METTrigAnalyzerMiniAOD.h"

#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/Math/interface/deltaPhi.h"

// ROOT includes
#include "Math/VectorUtil.h"

#include <cassert>
#include <cstring>
using namespace reco;
using namespace edm;

//
// constructors and destructor
//
//____________________________________________________________________________
METTrigAnalyzerMiniAOD::METTrigAnalyzerMiniAOD(const edm::ParameterSet& ps) 
{
  using namespace std;
  using namespace edm;

  processName_ = ps.getUntrackedParameter<std::string>("processName","HLT");
  
  refTriggerName_ = ps.getUntrackedParameter<std::string>("refTriggerName","HLT_Ele32_WPTight_Gsf_v17");
  sigTriggerNames_ = ps.getUntrackedParameter<std::vector<std::string> >("sigTriggerNames");
  
  triggerResultsToken_ = consumes<edm::TriggerResults> (ps.getUntrackedParameter<edm::InputTag>("triggerResultsTag", edm::InputTag("TriggerResults", "", "HLT")));
  
  pfMetToken_ = consumes<edm::View<pat::MET> >(ps.getUntrackedParameter<edm::InputTag>("pfMetInputTag_", edm::InputTag("slimmedMETs")));
  electronToken_ = consumes<std::vector<pat::Electron> >(ps.getUntrackedParameter<edm::InputTag>("electronsInputTag_", edm::InputTag("slimmedElectrons")));
  PV_Token_ = consumes<std::vector<reco::Vertex> > (edm::InputTag("offlineSlimmedPrimaryVertices"));
  verbose_ = ps.getUntrackedParameter<bool>("verbose",false);
  
  // histogram setup
  edm::Service<TFileService> fs;
  
  hists_1d_["h_passreftrig"] = fs->make<TH1F>("h_passreftrig" , "; passed ref trigger" , 2 , 0. , 2. );
  hists_1d_["h_met_all"] = fs->make<TH1F>("h_met_all" , "; E_{T}^{miss} [GeV]" , 40, 100., 500. );
  for (unsigned int trig=0; trig<sigTriggerNames_.size(); trig++)
    {
      string h_name = "h_met_passtrig_" + sigTriggerNames_.at(trig);
      const char* hname = h_name.c_str();
      hists_1d_[hname] = fs->make<TH1F>(hname, "; E_{T}^{miss} [GeV]" , 40, 100., 500. );
    }
  hists_1d_["h_met_passtrig"] = fs->make<TH1F>("h_met_passtrig" , "; E_{T}^{miss} [GeV]" , 40, 100., 500. );

  run_=0;
  lumi_=0;
  event_=0;
  isData_=false;
}

//____________________________________________________________________________
METTrigAnalyzerMiniAOD::~METTrigAnalyzerMiniAOD()
{
}

//
// member functions
//
//____________________________________________________________________________
void
METTrigAnalyzerMiniAOD::beginRun(edm::Run const & iRun, edm::EventSetup const& iSetup)
{
  using namespace std;
  using namespace edm;

  bool changed(true);
  if (hltConfig_.init(iRun,iSetup,processName_,changed)) {
    if (changed) {
      const unsigned int n(hltConfig_.size());
      // check if trigger names in (new) config
      unsigned int refTriggerIndex(hltConfig_.triggerIndex(refTriggerName_));
      if (refTriggerIndex>=n) {
	cout << "METTrigAnalyzerMiniAOD::analyze:"
	     << " TriggerName " << refTriggerName_ 
	     << " not available in config!" << endl;
      }
      for (unsigned int itrig=0; itrig<sigTriggerNames_.size(); itrig++)
	{
	  unsigned int sigTriggerIndex(hltConfig_.triggerIndex(sigTriggerNames_.at(itrig)));
	  if (sigTriggerIndex>=n) {
	    cout << "METTrigAnalyzerMiniAOD::analyze:"
		 << " TriggerName " << sigTriggerNames_.at(itrig) 
		 << " not available in config!" << endl;
	  }
	}
    } // if changed
  } else {
    cout << "METTrigAnalyzerMiniAOD::analyze:"
	 << " config extraction failure with process name "
	 << processName_ << endl;
  }

}

//____________________________________________________________________________
// ------------ method called to produce the data  ------------
void
METTrigAnalyzerMiniAOD::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace std;
  using namespace edm;
  using namespace reco;
  using namespace trigger;

  if (verbose_) cout << endl;
  
  // Event info
  run_ = iEvent.id().run();
  lumi_= iEvent.id().luminosityBlock();
  event_=iEvent.id().event();
  isData_=iEvent.isRealData();
  
  // For debugging purposes
  if (0)
    {
      std::cout << " "<<std::endl;
      std::cout << " Event = "<<event_<<std::endl;
      std::cout << " Run = "<<run_<<std::endl;
      std::cout << " Lumi block = "<<lumi_<<std::endl; 
    }
  
  // get event products
  iEvent.getByToken(triggerResultsToken_,triggerResultsHandle_);
  if (!triggerResultsHandle_.isValid()) {
    cout << "METTrigAnalyzerMiniAOD::analyze: Error in getting TriggerResults product from Event!" << endl;
    return;
  }

  // sanity check
  assert(triggerResultsHandle_->size()==hltConfig_.size());

  // retrieve necessary containers
  Handle<edm::View<pat::MET> > pfMetHandle_;
  iEvent.getByToken( pfMetToken_ , pfMetHandle_ );
  
  float met = ( pfMetHandle_->front() ).pt();;
  float met_phi = ( pfMetHandle_->front() ).p4().phi();
  if (verbose_) cout << "met: " << met << endl;
  hists_1d_["h_met_all"]->Fill(met);
  
  edm::Handle< std::vector<pat::Electron> > electrons;
  iEvent.getByToken(electronToken_, electrons );
  
  edm::Handle<std::vector<Vertex> > theVertices;
  iEvent.getByToken(PV_Token_, theVertices);
  int nVertex = theVertices->size();
  Vertex::Point PV(0,0,0);
  if (nVertex) PV = theVertices->begin()->position();
  
  int nelectrons = 0;
  for(std::vector<pat::Electron>::const_iterator ele = (*electrons).begin(); ele !=(*electrons).end(); ele++)
    {
      double pt  = ele->pt();
      double phi = ele->phi();
      double eta = ele->eta();
      double dPhi= reco::deltaPhi(phi, met_phi);
      if (!PassOfflineElectronSelection(&*ele, PV)) continue;
      if (pt < 40.0) continue;
      if (dPhi < 0.5) continue;
      if (0) std::cout << "Electron "<<nelectrons<<" pt="<<pt<<"  eta="<<eta<<"  phi="<<phi<<"   dPhi(e, met)="<<dPhi<<"   met="<<met<<std::endl;
      nelectrons++;
    }
  
  // Require exactly one tight electron
  if (nelectrons != 1) return;
  
  if (verbose_) cout << endl;
  
  const unsigned int ntrigs(hltConfig_.size());
  const unsigned int refTriggerIndex(hltConfig_.triggerIndex(refTriggerName_));
  assert(refTriggerIndex==iEvent.triggerNames(*triggerResultsHandle_).triggerIndex(refTriggerName_));
  
  // abort on invalid trigger name
  if (refTriggerIndex>=ntrigs) {
    cout << "METTrigAnalyzerMiniAOD::analyzeTrigger: path "
	 << refTriggerName_ << " - not found!" << endl;
    return;
  }
  if (verbose_) {
    cout << "METTrigAnalyzerMiniAOD::analyzeTrigger: reference path "
	 << refTriggerName_ << " [" << refTriggerIndex << "]" << endl;
  }
  
  // Reference trigger
  bool refAccept = triggerResultsHandle_->accept(refTriggerIndex);
  if (refAccept) hists_1d_["h_passreftrig"]->Fill(1);
  else {  
    // don't consider event if reference trigger didn't fire
    hists_1d_["h_passreftrig"]->Fill(0);
    return;
  }
    
  // Signal triggers
  bool passedOR  = false;
  
  // Loop over signal triggers
  for (unsigned int itrig=0; itrig<sigTriggerNames_.size(); itrig++)
    {
      const unsigned int sigTriggerIndex(hltConfig_.triggerIndex(sigTriggerNames_.at(itrig)));
      assert(sigTriggerIndex==iEvent.triggerNames(*triggerResultsHandle_).triggerIndex(sigTriggerNames_.at(itrig)));
      if (sigTriggerIndex>=ntrigs) {
	cout << "METTrigAnalyzerMiniAOD::analyzeTrigger: path "
	     << sigTriggerNames_.at(itrig) << " - not found!" << endl;
	return;
      }
      if (verbose_) {
	cout << "METTrigAnalyzerMiniAOD::analyzeTrigger: signal path "
	     << sigTriggerNames_.at(itrig) << " [" << sigTriggerIndex << "]" << endl;
      }
            
      bool sigAccept = triggerResultsHandle_->accept(sigTriggerIndex);
      if (sigAccept) passedOR = true;

      string h_name = "h_met_passtrig_" + sigTriggerNames_.at(itrig);
      const char* hname = h_name.c_str();
      if (sigAccept) hists_1d_[hname]->Fill(met);
    }
  
  // Logical OR of all triggers
  if (passedOR) hists_1d_["h_met_passtrig"]->Fill(met);
  if (verbose_) cout << endl;
  return;
}

// From: https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun3#Offline_selection_criteria_for_v
bool METTrigAnalyzerMiniAOD::PassOfflineElectronSelection(const pat::Electron * ele, reco::Vertex::Point PV)
{
  const reco::GsfTrackRef gsfTrack = ele->gsfTrack();
  if (!gsfTrack.isNonnull()) return false;
  if(TMath::Abs(ele->superCluster()->eta()) >2.5) return false;
  else if( TMath::Abs(ele->superCluster()->eta()) < 1.479)
    {
      if( TMath::Abs(ele->full5x5_sigmaIetaIeta()) > 0.0101 ) return  false;
      if( TMath::Abs(ele->deltaEtaSuperClusterTrackAtVtx()) > 0.00411) return  false;
      if( TMath::Abs(ele->deltaPhiSuperClusterTrackAtVtx()) > 0.116  ) return  false;
      if( TMath::Abs(ele->hadronicOverEm())  > 0.104  ) return  false;
      if( TMath::Abs(1.0/ele->ecalEnergy() - ele->eSuperClusterOverP()/ele->ecalEnergy() ) > 0.023 ) return  false;
      if( TMath::Abs(gsfTrack->dxy(PV)) > 0.05) return false;
      if( TMath::Abs(gsfTrack->dz(PV)) > 0.10) return false;
      if(gsfTrack->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS)>2) return  false;
    }
  else {
    if( TMath::Abs(ele->full5x5_sigmaIetaIeta()) > 0.027 ) return  false;
    if( TMath::Abs(ele->deltaEtaSuperClusterTrackAtVtx()) > 0.00938 ) return  false;
    if( TMath::Abs(ele->deltaPhiSuperClusterTrackAtVtx()) > 0.164  ) return  false;
    if( TMath::Abs(ele->hadronicOverEm())  > 0.0897  ) return  false;
    if( TMath::Abs(1.0/ele->ecalEnergy() - ele->eSuperClusterOverP()/ele->ecalEnergy()) > 0.018 ) return  false;
    if( TMath::Abs(gsfTrack->dxy(PV)) > 0.10) return false;
    if( TMath::Abs(gsfTrack->dz(PV)) > 0.20) return false;
    if(gsfTrack->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS)>1) return  false;
  }
  double iso = (ele->pfIsolationVariables().sumChargedHadronPt + TMath::Max(0.0, ele->pfIsolationVariables().sumNeutralHadronEt + ele->pfIsolationVariables().sumPhotonEt - 0.5*ele->pfIsolationVariables().sumPUPt))/ele->pt() ; 
  if(iso>0.2) return false; 
  return true;
}
