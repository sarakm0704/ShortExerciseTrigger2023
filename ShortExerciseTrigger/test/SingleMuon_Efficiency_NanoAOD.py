#!/usr/bin/env python3
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

#importing tools from nanoAOD processing set up to store the ratio histograms in a root file
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

# is_nth_bit_set
def is_nth_bit_set(self, x, n):
    if x & (1 << n): ## & and << -> bitwise operators
        return True
    return False

class TrigMuonAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True
        self.signal_path=signal_path
        
    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
        self.h_passtrig      = ROOT.TH1F("h_passtrig", "; passed trigger", 2, 0. , 2.)
        self.h_mll_allpairs  = ROOT.TH1F("h_mll_allpairs", "; m_{#mu#mu} [GeV]", 75 , 0. , 150.)
        self.h_mll_cut       = ROOT.TH1F("h_mll_cut", "; m_{#mu#mu} [GeV]", 75 , 0. , 150.)
        self.h_pt_probe_all  = ROOT.TH1F("h_pt_probe_all", "; p_{T} [GeV]", 100 , 0. , 100.)
        self.h_pt_probe_pass = ROOT.TH1F("h_pt_probe_pass", "; p_{T} [GeV]", 100 , 0. , 100.)
        self.h_pt_probe_fail = ROOT.TH1F("h_pt_probe_fail", "; p_{T} [GeV]", 100 , 0. , 100.)
        self.h_eta_probe_all = ROOT.TH1F("h_eta_probe_all", "; #eta", 100 , -3. , 3.)
        self.h_eta_probe_pass= ROOT.TH1F("h_eta_probe_pass", "; #eta", 100 , -3. , 3.)
        self.h_eta_probe_fail= ROOT.TH1F("h_eta_probe_fail", "; #eta", 100 , -3. , 3.)
        self.h_phi_probe_all = ROOT.TH1F("h_phi_probe_all", "; #phi", 100 , -3.14 , 3.14)
        self.h_phi_probe_pass= ROOT.TH1F("h_phi_probe_pass", "; #phi", 100 , -3.14 , 3.14)
        self.h_phi_probe_fail= ROOT.TH1F("h_phi_probe_fail", "; #phi", 100 , -3.14 , 3.14)
        self.addObject(self.h_passtrig)
        self.addObject(self.h_mll_allpairs)
        self.addObject(self.h_mll_cut)
        self.addObject(self.h_pt_probe_all)
        self.addObject(self.h_pt_probe_pass)
        self.addObject(self.h_pt_probe_fail)
        self.addObject(self.h_eta_probe_all)
        self.addObject(self.h_eta_probe_pass)
        self.addObject(self.h_eta_probe_fail)
        self.addObject(self.h_phi_probe_all)
        self.addObject(self.h_phi_probe_pass)
        self.addObject(self.h_phi_probe_fail)

        
    def analyze(self, event):

        hlt = Object(event, "HLT")
        
        # Check if event passes the IsoMu24 path
        bit=getattr(hlt, "IsoMu24")
        
        # Save the bit of reference trigger and skim event
        self.h_passtrig.Fill(bit)
        if not bit:
           return False

        def CheckTriggerMatching(offline_mu):
            
            for trgObj in Collection(event, 'TrigObj'):
                trgObj_pt = trgObj.pt
                trgObj_eta = trgObj.eta
                trgObj_phi = trgObj.phi
                trgObj_ID  = trgObj.id
                trgObj_filterBits = trgObj.filterBits
                
                # keep only the trigger objects associated with a muon (13)
                if (trgObj_ID != 13): continue
                
                if (0):
                    print("trigger object ID=", trgObj_ID, "  pt=", trgObj_pt, "  eta=", trgObj_eta, "  phi=", trgObj_phi, " trgObj_filterBits=", trgObj_filterBits)
                
                # Check if trigger filters of HLT_IsoMu24 (index=3) are fired
                if (is_nth_bit_set(self, trgObj.filterBits, 3)):
                    deltaR_mu_trgObj = deltaR(trgObj_eta, trgObj_phi, offline_mu.eta, offline_mu.phi)
                    if (deltaR_mu_trgObj < 0.2):
                        return True
            return False
        
        # Add any offline selection here:
        muons = Collection(event, "Muon")
        
        muons_index   = -1
        tag_mu_index  = -1
        prob_mu_index = -1
    
        if (0): print("\n==========================")
        for tag_mu in muons:
            muons_index += 1
            
            # Tag muon requirements: pT > 28 GeV, |eta|<2.4, tight-ID
            if tag_mu.pt < 28: continue
            if abs(tag_mu.eta) > 2.4: continue
            if not tag_mu.tightId: continue
            if tag_mu.pfRelIso03_all > 0.15: continue
            tag_mu_index = muons_index
            
            if (0):
                print("tag muon pt = %s   eta = %s  phi = %s" % (tag_mu.pt, tag_mu.eta, tag_mu.phi))
            
            tag_mu_isTrgMatched = CheckTriggerMatching(tag_mu)
                        
            # Keep event only if tag muon is matched
            if not tag_mu_isTrgMatched:
                continue
                
            if (0):
                print("Tag muon with index %s passes trigger matching" % (tag_mu_index))
            
            prob_mu_index = -1
            # Look for a probe muon
            for prob_mu in muons:
                
                prob_mu_index += 1
                if (prob_mu_index == tag_mu_index):
                    if (0): print("Skipping muon with index %s as it is the tag muon" % (prob_mu_index))
                    continue
                    
                # Require the same selections for the probe muon
                if prob_mu.pt < 20: continue
                if abs(prob_mu.eta) > 2.4: continue
                if not prob_mu.tightId: continue
                if prob_mu.pfRelIso03_all > 0.15: continue
                if (0):
                    print("Probe muon pT = %s   eta= %s  phi = %s  " % (prob_mu.pt, prob_mu.eta, prob_mu.phi)) 
                
                mll = (prob_mu.p4() + tag_mu.p4()).M()
                if (0): print("Invariant mass = %s" % (mll))
                
                self.h_mll_allpairs.Fill(mll)
                
                if (mll < 81 or mll > 101): continue
                self.h_mll_cut.Fill(mll)
                
                self.h_pt_probe_all.Fill(prob_mu.pt)
                self.h_eta_probe_all.Fill(prob_mu.eta)
                self.h_phi_probe_all.Fill(prob_mu.phi)
                
                # Now check if the probe muons is trigger matched
                probe_mu_isTrgMatched = CheckTriggerMatching(prob_mu)
                if (probe_mu_isTrgMatched):
                    self.h_pt_probe_pass.Fill(prob_mu.pt)
                    self.h_eta_probe_pass.Fill(prob_mu.eta)
                    self.h_phi_probe_pass.Fill(prob_mu.phi)
                else:
                    self.h_pt_probe_fail.Fill(prob_mu.pt)
                    self.h_eta_probe_fail.Fill(prob_mu.eta)
                    self.h_phi_probe_fail.Fill(prob_mu.phi)

        return True

preselection=""
files=["/eos/user/c/cmsdas/2023/short-ex-trg/ex2/Muon2022F_NanoAOD/Muon_Run2022F_PromptNanoAODv11_cd8d1b0c-5ade-4591-beb8-93034cc7ca11.root"]
signal_path = ["IsoMu24"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[TrigMuonAnalysis()],noOut=True,histFileName="histos_SingleMuTrigAnalyzer_NanoAOD.root",histDirName="singleMuTrigAnalyzerNanoAOD")
p.run()
