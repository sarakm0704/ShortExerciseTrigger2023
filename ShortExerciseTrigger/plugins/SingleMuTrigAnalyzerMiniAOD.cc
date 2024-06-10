#include "FWCore/ServiceRegistry/interface/ServiceMaker.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"

#include "FWCore/Utilities/interface/InputTag.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "DataFormats/Common/interface/ValueMap.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

// ROOT includes
#include "Math/VectorUtil.h"
#include <TLorentzVector.h>

#include <cassert>

using namespace reco;
using namespace edm;
using namespace std;
using namespace trigger;

//
// class declaration
//
class SingleMuTrigAnalyzerMiniAOD : public edm::one::EDAnalyzer <edm::one::SharedResources> {

  typedef math::XYZTLorentzVectorF LorentzVector;

 public:
  explicit SingleMuTrigAnalyzerMiniAOD(const edm::ParameterSet&);
  ~SingleMuTrigAnalyzerMiniAOD();
  // Create Trigger Units before starting event processing
  //virtual void beginRun(edm::Run const &, edm::EventSetup const&);
  // but for now it is not working. leave it but commented out
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  bool analyzeTrigger(const edm::Event&, const edm::EventSetup&, const std::string& triggerName);

 private:

  void bookHists(edm::Service<TFileService>& fs, const std::string& suffix);
  void fillHists(const LorentzVector& lv, const std::string& suffix);
  float muonPFiso(const pat::Muon& mu);

  /// module config parameters
  std::string   processName_;
  std::string   triggerName_;
  edm::EDGetTokenT<edm::TriggerResults> triggerResultsToken_;
  edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjectStandAloneToken_;
  edm::EDGetTokenT<edm::View<pat::Muon> > muonsToken_;
  edm::EDGetTokenT<reco::VertexCollection> vtxToken_;
  double tagPt_;
  double tagEta_;
  double probePt_;
  double probeEta_;
  bool verbose_;

  /// additional class data memebers
  edm::Handle<edm::TriggerResults>           triggerResultsHandle_;
  HLTConfigProvider hltConfig_;

  std::map<std::string,TH1F*> hists_1d_;

};

//
// constructors and destructor
//
//____________________________________________________________________________
SingleMuTrigAnalyzerMiniAOD::SingleMuTrigAnalyzerMiniAOD(const edm::ParameterSet& iConfig)
  :
  processName_(iConfig.getUntrackedParameter<std::string>("processName","HLT")),
  triggerName_(iConfig.getUntrackedParameter<std::string>("triggerName","HLT_IsoMu24_v15")),
  triggerResultsToken_(consumes<edm::TriggerResults> (iConfig.getUntrackedParameter<edm::InputTag>("triggerResultsTag", edm::InputTag("TriggerResults", "", "HLT")))),
  triggerObjectStandAloneToken_(consumes<pat::TriggerObjectStandAloneCollection> (iConfig.getUntrackedParameter<edm::InputTag>("triggerObjectsStandAloneTag", edm::InputTag("slimmedPatTrigger")))),
  muonsToken_(consumes<View<pat::Muon> > (iConfig.getUntrackedParameter<edm::InputTag>("muonsInputTag",edm::InputTag("slimmedMuons")))),
  vtxToken_(consumes<reco::VertexCollection> (iConfig.getUntrackedParameter<edm::InputTag>("vtxInputTag",edm::InputTag("offlineSlimmedPrimaryVertices")))),
  tagPt_(iConfig.getUntrackedParameter<double>("tagPt",25.)),
  tagEta_(iConfig.getUntrackedParameter<double>("tagEta",2.4)),
  probePt_(iConfig.getUntrackedParameter<double>("probePt",20.)),
  probeEta_(iConfig.getUntrackedParameter<double>("probeEta",2.4)),
  verbose_(iConfig.getUntrackedParameter<bool>("verbose",false))
{    
  // histogram setup
  usesResource(TFileService::kSharedResource);
  edm::Service<TFileService> fs;

  if (not fs) {
      throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  hists_1d_["h_passtrig"] = fs->make<TH1F>("h_passtrig" , "; passed trigger" , 2 , 0. , 2. );
  hists_1d_["h_mll_allpairs"] = fs->make<TH1F>("h_mll_allpairs" , "; m_{ll} [GeV]" , 75 , 0. , 150. );
  hists_1d_["h_mll_cut"] = fs->make<TH1F>("h_mll_cut" , "; m_{ll} [GeV]" , 75 , 0. , 150. );
  bookHists(fs,"probe_all");
  bookHists(fs,"probe_pass");
  bookHists(fs,"probe_fail");

}

//____________________________________________________________________________
SingleMuTrigAnalyzerMiniAOD::~SingleMuTrigAnalyzerMiniAOD()
{
}

//
// member functions
//
// currently beginRun is not working, temporal disable
// initialize HLTConfigProvider inside of analyze instead
/*
//____________________________________________________________________________
void
SingleMuTrigAnalyzerMiniAOD::beginRun(edm::Run const & iRun, edm::EventSetup const& iSetup)
{
  using namespace std;
  using namespace edm;

  bool changed(true);
  if (hltConfig_.init(iRun,iSetup,processName_,changed)) {
    if (changed) {
      const unsigned int n(hltConfig_.size());
      // check if trigger names in (new) config
      unsigned int triggerIndex(hltConfig_.triggerIndex(triggerName_));
      if (triggerIndex>=n) {
	cout << "SingleMuTrigAnalyzerMiniAOD::analyze:"
	     << " TriggerName " << triggerName_ 
	     << " not available in config!" << endl;
      }
    } // if changed
  } else {
    cout << "SingleMuTrigAnalyzerMiniAOD::analyze:"
	 << " config extraction failure with process name "
	 << processName_ << endl;
  }

}
*/

//____________________________________________________________________________
// ------------ method called to produce the data  ------------
void
SingleMuTrigAnalyzerMiniAOD::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  if (verbose_) cout << endl;

  // get event products
  iEvent.getByToken(triggerResultsToken_,triggerResultsHandle_);
  if (!triggerResultsHandle_.isValid()) {
    cout << "SingleMuTrigAnalyzerMiniAOD::analyze: Error in getting TriggerResults product from Event!" << endl;
    return;
  }
  edm::Handle<pat::TriggerObjectStandAloneCollection> triggerOSA_;
  iEvent.getByToken(triggerObjectStandAloneToken_,triggerOSA_);
  if (!triggerOSA_.isValid()) {
    cout << "Error in getting TriggerObjectStandAlone product from Event!" << endl;
    return;
  }

  bool changed = true;
  if (!hltConfig_.init(iEvent.getRun(), iSetup, processName_, changed)) {
      edm::LogWarning("HLTAnalyzer") << "Initialization of HLTConfigProvider failed!";
      return;
  }

  // Now you can access HLT paths, prescales, etc.
  //const std::vector<std::string>& triggerNames = hltConfig_.triggerNames();
  //for (size_t i = 0; i < triggerNames.size(); ++i) {
  //    const std::string& triggerName = triggerNames[i];
  //    //cout << triggerName << endl;
  //    //bool triggerFired = TriggerResults->accept(i);
  //    //int prescale = hltConfig_.prescaleValue(iEvent, iSetup, triggerName);
  //    // Do something with the trigger information...
  //}

  // sanity check
  assert(triggerResultsHandle_->size()==hltConfig_.size());

  // retrieve necessary containers
  Handle<reco::VertexCollection> vertexHandle_;
  iEvent.getByToken(vtxToken_, vertexHandle_);
  Handle<View<pat::Muon> > musHandle_;
  iEvent.getByToken( muonsToken_ , musHandle_ );

  if (verbose_) cout << endl;

  const unsigned int ntrigs(hltConfig_.size());
  const unsigned int triggerIndex(hltConfig_.triggerIndex(triggerName_));
  assert(triggerIndex==iEvent.triggerNames(*triggerResultsHandle_).triggerIndex(triggerName_));

  // abort on invalid trigger name
  if (triggerIndex>=ntrigs) {
    cout << "SingleMuTrigAnalyzerMiniAOD::analyzeTrigger: path "
	 << triggerName_ << " - not found!" << endl;
    return;
  }

  if (verbose_) {
    cout << "SingleMuTrigAnalyzerMiniAOD::analyzeTrigger: path "
	 << triggerName_ << " [" << triggerIndex << "]" << endl;
  }
  // modules on this trigger path
  const unsigned int m(hltConfig_.size(triggerIndex));
  const vector<string>& moduleLabels(hltConfig_.moduleLabels(triggerIndex));

  bool wasRun = triggerResultsHandle_->wasrun(triggerIndex);
  bool accept = triggerResultsHandle_->accept(triggerIndex);
  bool error = triggerResultsHandle_->error(triggerIndex);
  const unsigned int moduleIndex(triggerResultsHandle_->index(triggerIndex));
  // Results from TriggerResults product
  if (verbose_) {
    cout << " Trigger path status:"
	 << " WasRun=" << wasRun
	 << " Accept=" << accept
	 << " Error =" << error
	 << endl;
    cout << " Last active module - label/type: "
	 << moduleLabels[moduleIndex] << "/" << hltConfig_.moduleType(moduleLabels[moduleIndex])
	 << " [" << moduleIndex << " out of 0-" << (m-1) << " on this path]"
	 << endl;
  }
  assert (moduleIndex<m);

  if (accept) hists_1d_["h_passtrig"]->Fill(1);
  else {  
    // don't consider event if trigger didn't fire
    hists_1d_["h_passtrig"]->Fill(0);
    return;
  }

  // loop over trigger then reco objects, match, make plots

  // first, get trigger objects from last filter

  //------------------------------------
  //  hlt objects
  //------------------------------------

  std::vector<LorentzVector> trigMuons;

  if (verbose_) cout << "found trigger muons:" << endl;
  const edm::TriggerNames &names = iEvent.triggerNames(*triggerResultsHandle_);
  for (pat::TriggerObjectStandAlone obj : *triggerOSA_) {
    obj.unpackPathNames(names);
    if ( !obj.id(83) ) continue; // muon type id
    if ( !obj.hasPathName( triggerName_, true, true ) ) continue; // checks if object is associated to last filter (true) and L3 filter (true)
    trigMuons.push_back(LorentzVector(obj.p4()));
    if (verbose_) cout << "  - pt: " << obj.pt() << ", eta: " << obj.eta() << ", phi: " << obj.phi() << endl;
  } // loop on trigger objects

  if (verbose_) cout << endl;
  if (accept && trigMuons.size() == 0) {
    cout << "SingleMuTrigAnalyzerMiniAOD::analyzeTrigger: ERROR!! no valid trigger leptons!" << endl;
  }

  //-------------------------------------
  //   reco vertices -- need for muon ID
  //-------------------------------------

  // find vertex 0 in vertex container
  const VertexCollection* vertexCollection = vertexHandle_.product();
  VertexCollection::const_iterator firstGoodVertex = vertexCollection->end();
  for ( VertexCollection::const_iterator vtx = vertexCollection->begin(); vtx != vertexCollection->end(); ++vtx ) {
    if (  !vtx->isFake() && vtx->ndof()>=4. && vtx->position().Rho()<=2.0 && fabs(vtx->position().Z())<=24.0 ) {
      if (firstGoodVertex == vertexCollection->end()) {
	firstGoodVertex = vtx;
	break;
      }
    }
  } // loop on vertices

  if (firstGoodVertex == vertexCollection->end()) {
    cout << "SingleMuTrigAnalyzerMiniAOD::analyze: didn't find any good offline vertices!! size: " 
	 << vertexCollection->size() << std::endl;
    return;
  }

  //-------------------------------------
  //   reco muons 
  //-------------------------------------

  const float dr_trigmatch = 0.2;
  
  std::vector<LorentzVector> offTagMuons;
  std::vector<LorentzVector> offProbeMuons;
  std::vector<LorentzVector> offProbeMatchedMuons;

  if (verbose_) cout << "found offline muons:" << endl;
  View<pat::Muon>::const_iterator muons_end = musHandle_->end();  // Iterator
  for ( View<pat::Muon>::const_iterator muon_tag = musHandle_->begin(); muon_tag != muons_end; ++muon_tag ) {

    if (verbose_) cout << " - tag cand: pt: " << muon_tag->pt() << ", eta: " << muon_tag->eta()
		       << ", phi: " << muon_tag->phi() << ", iso: " << muonPFiso(*muon_tag) << endl;
    
    // check if muon passes tag cuts
    if (muon_tag->pt() < tagPt_) continue;
    if (fabs(muon_tag->eta()) > tagEta_) continue;
    if (!muon_tag->isTightMuon(*firstGoodVertex)) continue;
    if (verbose_) cout << "   - passes tight" << endl;
    if (muonPFiso(*muon_tag) > 0.15) continue;
    if (verbose_) cout << "   - passes iso" << endl;
    
    // check if muon matches trigger
    bool trigmatch_tag = false;
    for (unsigned int itrig=0; itrig < trigMuons.size(); ++itrig) {
      if (ROOT::Math::VectorUtil::DeltaR(muon_tag->p4(),trigMuons.at(itrig)) < dr_trigmatch) trigmatch_tag = true;
    }
    if (!trigmatch_tag) continue;
    if (verbose_) cout << "   - matched to trigger" << endl;

    // good tag muon: look for any probe muons in the event
    for ( View<pat::Muon>::const_iterator muon_probe = musHandle_->begin(); muon_probe != muons_end; ++muon_probe ) {
      
      // make sure probe isn't the same as the tag
      if (ROOT::Math::VectorUtil::DeltaR(muon_tag->p4(),muon_probe->p4()) < 0.01) continue;

      // check probe cuts
      if (muon_probe->pt() < probePt_) continue;
      if (fabs(muon_probe->eta()) > probeEta_) continue;
      if (!muon_probe->isTightMuon(*firstGoodVertex)) continue;
      if (muonPFiso(*muon_probe) > 0.15) continue;

      if (verbose_) cout << " - probe cand: pt: " << muon_probe->pt() << ", eta: " << muon_probe->eta()
			 << ", phi: " << muon_probe->phi() << ", iso: " << muonPFiso(*muon_probe) << endl;
    
      // check dimuon mass: must be in range 81-101
      LorentzVector dimuon = LorentzVector(muon_tag->p4() + muon_probe->p4());
      hists_1d_["h_mll_allpairs"]->Fill(dimuon.M());
      if (verbose_) cout << " - probe dimuon mass: " << dimuon.M()  << endl;
      if (dimuon.M() < 81. || dimuon.M() > 101.) continue;
      hists_1d_["h_mll_cut"]->Fill(dimuon.M());

      fillHists(LorentzVector(muon_probe->p4()),"probe_all");

      // check if probe muon matches trigger
      bool trigmatch_probe = false;
      for (unsigned int itrig=0; itrig < trigMuons.size(); ++itrig) {
	if (ROOT::Math::VectorUtil::DeltaR(muon_probe->p4(),trigMuons.at(itrig)) < dr_trigmatch) trigmatch_probe = true;
      }

      if (trigmatch_probe) fillHists(LorentzVector(muon_probe->p4()),"probe_pass");
      else fillHists(LorentzVector(muon_probe->p4()),"probe_fail");

    } // loop over probes
  } // loop over tags (offline muons)

  if (verbose_) cout << endl;
  return;
}

//____________________________________________________________________________
void SingleMuTrigAnalyzerMiniAOD::bookHists(edm::Service<TFileService>& fs, const std::string& suffix) {

  std::string suf(suffix);
  if (suffix.size()) suf = "_"+suffix;

  hists_1d_["h_pt"+suf] = fs->make<TH1F>(Form("h_pt%s",suf.c_str()) , "; p_{T} [GeV]" , 100 , 0. , 100. );
  hists_1d_["h_eta"+suf] = fs->make<TH1F>(Form("h_eta%s",suf.c_str()) , "; #eta" , 100 , -3. , 3. );
  hists_1d_["h_phi"+suf] = fs->make<TH1F>(Form("h_phi%s",suf.c_str()) , "; #phi" , 100 , -3.14 , 3.14 );

  return;
}

//____________________________________________________________________________
void SingleMuTrigAnalyzerMiniAOD::fillHists(const LorentzVector& lv, const std::string& suffix) {

  std::string suf(suffix);
  if (suffix.size()) suf = "_"+suffix;

  hists_1d_["h_pt"+suf]->Fill(lv.pt());
  hists_1d_["h_eta"+suf]->Fill(lv.eta());
  hists_1d_["h_phi"+suf]->Fill(lv.phi());

  return;
}

//____________________________________________________________________________
float SingleMuTrigAnalyzerMiniAOD::muonPFiso(const pat::Muon& mu) {
  return (mu.pfIsolationR03().sumChargedHadronPt + std::max(0., mu.pfIsolationR03().sumNeutralHadronEt + mu.pfIsolationR03().sumPhotonEt - 0.5*mu.pfIsolationR03().sumPUPt))/mu.pt();
}

DEFINE_FWK_MODULE(SingleMuTrigAnalyzerMiniAOD);
