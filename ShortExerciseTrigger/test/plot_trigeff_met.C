#include "TFile.h"
#include "TH1.h"
#include "TH2F.h"
#include "TLegend.h"
#include "TString.h"
#include "TCanvas.h"
#include "TEfficiency.h"
#include "TStyle.h"

void plot_trigeff_met (const TString& infile = "histos_METTrigAnalyzer.root") {

  gStyle->SetPadTopMargin(0.08);
  gStyle->SetPadBottomMargin(0.12);
  gStyle->SetPadLeftMargin(0.15);
  gStyle->SetPadRightMargin(0.05);
  gStyle->SetOptStat(0);

  TH1::SetDefaultSumw2();
  
  TFile* f_in = new TFile(infile);

  // ---- efficiency vs met
  
  TH1F* h_met_denom = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_all");
  TH1F* h_met_num_HLT_PFMET120_PFMHT120_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMET120_PFMHT120_IDTight_v22");
  TH1F* h_met_num_HLT_PFMET130_PFMHT130_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMET130_PFMHT130_IDTight_v22");
  TH1F* h_met_num_HLT_PFMET140_PFMHT140_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMET140_PFMHT140_IDTight_v22");
  TH1F* h_met_num_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v22");
  TH1F* h_met_num_HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v21");
  TH1F* h_met_num_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v21");
  TH1F* h_met_num_HLT_PFMETTypeOne140_PFMHT140_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMETTypeOne140_PFMHT140_IDTight_v13");
  TH1F* h_met_num = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig");
  
  TCanvas* c_met = new TCanvas("c_met","c_met");
  c_met->SetGrid(1,1);
  c_met->cd();
  
  auto legend = new TLegend(0.5,0.20,0.90,0.50);
  legend->SetFillColor(0);
  legend->SetFillStyle(0);
  legend->SetBorderSize(0);
  
  TH2F* h_met_axis = new TH2F("h_met_axis",";E_{T}^{miss} [GeV];Efficiency",40,100,500,20,0,1);
  h_met_axis->GetYaxis()->SetTitleOffset(0.98);
  h_met_axis->SetMaximum(1.05);
  h_met_axis->Draw();
  
  // Logical OR of all signal paths
  TEfficiency* h_met_eff = new TEfficiency(*h_met_num, *h_met_denom);
  h_met_eff->SetLineColor(kBlack);
  h_met_eff->SetMarkerColor(kBlack);
  h_met_eff->SetMarkerStyle(20);
  h_met_eff->Draw("pe same");
  legend->AddEntry(h_met_eff, "OR");

  TEfficiency* h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMET120_PFMHT120_IDTight_v, *h_met_denom);
  h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v->SetLineColor(kGreen+1);
  h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v->SetMarkerColor(kGreen+1);
  h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v->SetMarkerStyle(22);
  h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v->Draw("pe same");
  legend->AddEntry(h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v, "HLT_PFMET120_PFMHT120_IDTight_v");
  
  //TEfficiency* h_met_eff_HLT_PFMET130_PFMHT130_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMET130_PFMHT130_IDTight_v, *h_met_denom);
  //h_met_eff_HLT_PFMET130_PFMHT130_IDTight_v->SetLineColor(kMagenta+2);
  //h_met_eff_HLT_PFMET130_PFMHT130_IDTight_v->SetMarkerColor(kMagenta+2);
  //h_met_eff_HLT_PFMET130_PFMHT130_IDTight_v->Draw("pe same");
  
  //TEfficiency* h_met_eff_HLT_PFMET140_PFMHT140_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMET140_PFMHT140_IDTight_v, *h_met_denom);
  //h_met_eff_HLT_PFMET140_PFMHT140_IDTight_v->SetLineColor(kBlue);
  //h_met_eff_HLT_PFMET140_PFMHT140_IDTight_v->SetMarkerColor(kBlue);
  //h_met_eff_HLT_PFMET140_PFMHT140_IDTight_v->Draw("pe same");
  
  TEfficiency* h_met_eff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v, *h_met_denom);
  h_met_eff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v->SetLineColor(kBlue);
  h_met_eff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v->SetMarkerColor(kBlue);
  h_met_eff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v->SetMarkerStyle(34);
  h_met_eff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v->Draw("pe same");
  legend->AddEntry(h_met_eff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v, "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v");
  
  //TEfficiency* h_met_eff_HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v, *h_met_denom);
  //h_met_eff_HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v->SetLineColor(kAzure-4);
  //h_met_eff_HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v->SetMarkerColor(kAzure-4);
  //h_met_eff_HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v->Draw("pe same");
  
  //TEfficiency* h_met_eff_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v, *h_met_denom);
  //h_met_eff_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v->SetLineColor(kRed);
  //h_met_eff_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v->SetMarkerColor(kRed);
  //h_met_eff_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v->Draw("pe same");
  
  TEfficiency* h_met_eff_HLT_PFMETTypeOne140_PFMHT140_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMETTypeOne140_PFMHT140_IDTight_v, *h_met_denom);
  h_met_eff_HLT_PFMETTypeOne140_PFMHT140_IDTight_v->SetLineColor(kRed);
  h_met_eff_HLT_PFMETTypeOne140_PFMHT140_IDTight_v->SetMarkerStyle(29);
  h_met_eff_HLT_PFMETTypeOne140_PFMHT140_IDTight_v->SetMarkerColor(kRed);
  h_met_eff_HLT_PFMETTypeOne140_PFMHT140_IDTight_v->Draw("pe same");
  
  legend->AddEntry(h_met_eff_HLT_PFMETTypeOne140_PFMHT140_IDTight_v, "HLT_PFMETTypeOne140_PFMHT140_IDTight_v");
  legend->Draw("same");
  
  c_met->Modified();
  c_met->Update();
  
  c_met->SaveAs("METEfficiency.pdf");
  return;
}
