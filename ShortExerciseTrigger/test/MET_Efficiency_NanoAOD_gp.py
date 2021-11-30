#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

#importing tools from nanoAOD processing set up to store the ratio histograms in a root file
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TrigMETAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
        self.h_passreftrig  = ROOT.TH1F("h_passreftrig" , "; passed ref trigger" , 2 , 0. , 2. )
        self.h_met_all      = ROOT.TH1F("h_met_all" , "; E_{T}^{miss} [GeV]" , 20, 100., 500 )
        self.h_met_passtrig = ROOT.TH1F("h_met_passtrig" , "; E_{T}^{miss} [GeV]" , 20, 100., 500)
        self.addObject(self.h_passreftrig )
        self.addObject(self.h_met_all )
        self.addObject(self.h_met_passtrig )

    def analyze(self, event):
        met       = Object(event, "MET")
        hlt       = Object(event, "HLT")

        refAccept = hlt.Ele27_eta2p1_WPTight_Gsf
        sigAccept = hlt.PFMET170_HBHECleaned
        self.h_passreftrig.Fill(refAccept)
        if not refAccept:
           return False

        self.h_met_all.Fill(met.pt)
        if sigAccept:
            self.h_met_passtrig.Fill(met.pt)

        return True


preselection=""
files=["./New_NanoAOD_M1000.root"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[TrigMETAnalysis()],noOut=True,histFileName="histos_METTrigNanoAOD.root",histDirName="metTrigAnalyzerNanoAOD")
p.run()
