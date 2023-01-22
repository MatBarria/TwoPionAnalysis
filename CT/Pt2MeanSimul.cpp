// It can be compile with
// g++ -Wall -fPIC -I../include `root-config --cflags` Pt2MeanSimul.cpp -o ../bin/Pt2MeanSimul `root-config --glibs` ../include/Broad.h
// For the target name use (C,Fe,Pb) for the solids targets and (DC,DFe,DPb) for the liquid target

#include "Broad.h"
#include "TCut.h"
#include "TFile.h"
#include "TROOT.h"
#include "TVirtualPad.h"
#include <iostream>
#include "TStopwatch.h"
#include "TString.h"
#include "TNtuple.h"
#include "TH1.h"

int MeanPt2Simul(std::string target, TFile* fileOutput);

int main() {

  TString oDirectory = "/home/matias/proyecto/Pt2Broadening_multi-pion/Data/CT/";
  TFile* fileOutput = new TFile(oDirectory + "meanPt2_Zh.root", "RECREATE");
  gROOT->cd();

  std::cout << "Mean Pt2 Simul for C" << std::endl;
  MeanPt2Simul("C",   fileOutput);
  std::cout << "Mean Pt2 Simul for Fe" << std::endl;
  MeanPt2Simul("Fe",  fileOutput);
  std::cout << "Mean Pt2 Simul for Pb" << std::endl;
  MeanPt2Simul("Pb",  fileOutput);
  std::cout << "Mean Pt2 Simul for DC" << std::endl;
  MeanPt2Simul("DC",  fileOutput);
  std::cout << "Mean Pt2 Simul for DFe" << std::endl;
  MeanPt2Simul("DFe", fileOutput);
  std::cout << "Mean Pt2 Simul for DPb" << std::endl;
  MeanPt2Simul("DPb", fileOutput);
 
  fileOutput->Close();

  PtBroadeningZh(oDirectory, oDirectory);

  return 0;
}



int MeanPt2Simul(std::string target, TFile* fileOutput) {

  TStopwatch t;

  std::cout << "Start" << std::endl;
  int n = target.length();
  char targetArr[n + 1];
  strcpy(targetArr, target.c_str());	

  int m;
  // Select the data for the chosen solid target
  if(targetArr[0] == 'D') { m = 2;} else {m = n + 1;}
  char simulTarget[m];
  if(targetArr[0] == 'D') {
    simulTarget[0] = 'D';
    simulTarget[1] = '\0';
  } else{
    for(int i = 0; i < m; i++){
      simulTarget[i] = targetArr[i];
    }
  }

  // Select the data for the chosen solid target
  TFile* fileSimul  = new TFile(Form(dataDirectory + "SimulTuple_%s_2.root", simulTarget), "READ");
  gROOT->cd();
      
  std::cout << "Target: " << simulTarget << std::endl;
  // Create some variables to use inside the for loops
  TString tupleDataName;
  TCut ZhCut, Q2Cut, NuCut, GenCut, cutsSimul;
  // Select liquid or solid target
  Q2Cut   = Form("Q2_gen>%f&&Q2_gen<%f", Q2_BINS[0],   Q2_BINS[N_Q2]);
  NuCut   = Form("Nu_gen>%f&&Nu_gen<%f", Nu_BINS[0],   Nu_BINS[N_Nu]);
  TNtuple* ntupleSimul = (TNtuple*) fileSimul->Get("ntuple_sim_gen_2");
  for(int gen = 1; gen <= N_PION ; gen++) { // Loops in every number of generated pions

    GenCut    = Form("Gen == %f", (float)gen);
    TH1F *histZh = new TH1F("ZhHist","", N_Zh, Zh_BINS);
    for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin

      ZhCut   = Form("Zh_gen>%f&&Zh_gen<%f", Zh_BINS[ZhCounter],   Zh_BINS[ZhCounter+1]);

      cutsSimul = ZhCut&&Q2Cut&&NuCut&&GenCut;
      ntupleSimul->Draw("Pt2_gen>>histPt2(90,0,3)", cutsSimul);
      TH1F *histPt2 = (TH1F*)gPad->GetPrimitive("histPt2");
      std::cout << histPt2->GetMean() << "---" << histPt2->GetMeanError() << std::endl;
      
      fileOutput->cd();
      histPt2->Write(Form("Pt2_%s_%i_%i", targetArr, ZhCounter, gen));
      gROOT->cd();	

      std::cout << "test" << std::endl;
      histZh->SetBinContent(ZhCounter+1, histPt2->GetMean());
      histZh->SetBinError(ZhCounter+1,   histPt2->GetMeanError());

      //gDirectory->rmdir("histPt2");
      delete histPt2;
    } // End Zh loop
      fileOutput->cd();
      histZh->Write(Form("meanPt2_%s_%i", targetArr, gen));
      gROOT->cd();	
      delete histZh;
  } // End pion number loop
  delete ntupleSimul;
  return 0;
}
