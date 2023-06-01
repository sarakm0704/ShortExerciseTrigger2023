import ROOT
import math 
import time
from plot_dict import *

def getCanvas():
    d = ROOT.TCanvas("", "", 800, 700)
    d.SetLeftMargin(0.12)
    d.SetRightMargin(0.15)
    d.SetLeftMargin(0.13)
    return d

def AddPrivateWorkText(setx=0.21, sety=0.905):
    tex = ROOT.TLatex(0.,0., 'Private Work');
    tex.SetNDC();
    tex.SetX(setx);
    tex.SetY(sety);
    tex.SetTextFont(53);
    tex.SetTextSize(28);
    tex.SetLineWidth(2)
    return tex

def AddCMSText(setx=0.205, sety=0.905):
    texcms = ROOT.TLatex(0.,0., 'CMS');
    texcms.SetNDC();
    texcms.SetTextAlign(31);
    texcms.SetX(setx);
    texcms.SetY(sety);
    texcms.SetTextFont(63);
    texcms.SetLineWidth(2);
    texcms.SetTextSize(30);
    return texcms

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTextFont(42)

file = ROOT.TFile("histos_METTrigNanoAOD.root")
workdir =file.GetDirectory("metTrigAnalyzerNanoAOD")

# Create the canvas
canvas=getCanvas()

legend = ROOT.TLegend(0.4412607,0.1932773,0.8223496,0.4453782)
legend.SetFillColor(0)
legend.SetFillStyle(0);
legend.SetBorderSize(0);

Denominator = workdir.Get("h_met_all")

# OR of all MET triggers
Numerator   = workdir.Get("h_met_passtrig")
Efficiency = ROOT.TGraphAsymmErrors(Numerator,Denominator,'MET')
Efficiency.SetLineColor(ROOT.kBlack)
Efficiency.SetMarkerStyle(20)
Efficiency.SetMarkerColor(ROOT.kBlack)
Efficiency.GetXaxis().SetTitle("E_{T}^{miss} [GeV]")
Efficiency.GetYaxis().SetTitle("Efficiency")
Efficiency.GetYaxis().SetRange(0, 2) 
Efficiency.Draw("ap")
legend.AddEntry(Efficiency,"OR", "ep")

# HLT_PFMET120_PFMHT120_IDTight
hNum_HLT_PFMET120_PFMHT120_IDTight = workdir.Get("h_met_passtrig_HLT_PFMET120_PFMHT120_IDTight")
hEff_HLT_PFMET120_PFMHT120_IDTight = ROOT.TGraphAsymmErrors(hNum_HLT_PFMET120_PFMHT120_IDTight, Denominator)
hEff_HLT_PFMET120_PFMHT120_IDTight.SetLineColor(ROOT.kGreen+1)
hEff_HLT_PFMET120_PFMHT120_IDTight.SetMarkerColor(ROOT.kGreen+1)
hEff_HLT_PFMET120_PFMHT120_IDTight.SetMarkerStyle(22)
hEff_HLT_PFMET120_PFMHT120_IDTight.Draw("pe same")
legend.AddEntry(hEff_HLT_PFMET120_PFMHT120_IDTight, "HLT_PFMET120_PFMHT120_IDTight_v")

# HLT_PFMETNoMu120_PFMHTNoMu120_IDTight
hNum_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight = workdir.Get("h_met_passtrig_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight")
hEff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight = ROOT.TGraphAsymmErrors(hNum_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight, Denominator)
hEff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight.SetLineColor(ROOT.kBlue)
hEff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight.SetMarkerColor(ROOT.kBlue)
hEff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight.SetMarkerStyle(34)
hEff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight.Draw("pe same")
legend.AddEntry(hEff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight, "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v")

# HLT_PFMETTypeOne140_PFMHT140_IDTight_v
hNum_HLT_PFMETTypeOne140_PFMHT140_IDTight = workdir.Get("h_met_passtrig_HLT_PFMETTypeOne140_PFMHT140_IDTight")
hEff_HLT_PFMETTypeOne140_PFMHT140_IDTight = ROOT.TGraphAsymmErrors(hNum_HLT_PFMETTypeOne140_PFMHT140_IDTight, Denominator)
hEff_HLT_PFMETTypeOne140_PFMHT140_IDTight.SetLineColor(ROOT.kRed)
hEff_HLT_PFMETTypeOne140_PFMHT140_IDTight.SetMarkerColor(ROOT.kRed)
hEff_HLT_PFMETTypeOne140_PFMHT140_IDTight.SetMarkerStyle(29)
hEff_HLT_PFMETTypeOne140_PFMHT140_IDTight.Draw("pe same")
legend.AddEntry(hEff_HLT_PFMETTypeOne140_PFMHT140_IDTight, "HLT_PFMETTypeOne140_PFMHT140_IDTight_v")

# Additional text
tex_cms = AddCMSText()
tex_cms.Draw("same")

private = AddPrivateWorkText()
private.Draw("same")

header = ROOT.TLatex()
header.SetTextSize(0.04)
header.DrawLatexNDC(0.57, 0.905, "2022, #sqrt{s} = 13.6 TeV")

legend.Draw("same")
canvas.Update()
canvas.Modified()
canvas.SaveAs("METEfficiency_NanoAOD.pdf")
