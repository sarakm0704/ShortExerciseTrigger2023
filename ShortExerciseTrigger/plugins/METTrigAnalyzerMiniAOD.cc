/** \class METTrigAnalyzerMiniAOD
 *
 * See header file for documentation
 *
 *  \author Dominick Olivito
 *
 */

#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"
#include "ShortExerciseTrigger2022/ShortExerciseTrigger/interface/METTrigAnalyzerMiniAOD.h"

#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

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
  
  float met = ( pfMetHandle_->front() ).pt();;
  if (verbose_) cout << "met: " << met << endl;
  hists_1d_["h_met_all"]->Fill(met);
  
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

