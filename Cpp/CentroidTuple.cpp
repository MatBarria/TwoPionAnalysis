// This program take the histogram generated by AccCorrection.cpp and apply a fit funcion to it
// It can be compile with
// g++ -Wall -fPIC -I./include `root-config --cflags` CentroidTuple.cpp -o ./bin/CentroidTuple `root-config --glibs` ./include/Acc.h
// For the target name use (C,Fe,Pb) for the solids targets and (DC,DFe,DPb) for the liquid target

#include <fstream>
#include <iostream>
#include <string>
#include "Acc.h"
#include "TString.h"
#include "TNtuple.h"
#include "TFile.h"
#include "TH1.h"
#include "TF1.h"
#include "TCanvas.h"


int PhiPQ(std::string target);

int main(){

  std::cout << "PhiPQ C" << std::endl;
  PhiPQ("C");
  std::cout << "PhiPQ Fe" << std::endl;
  PhiPQ("Fe");
  std::cout << "PhiPQ Pb" << std::endl;
  PhiPQ("Pb");
  std::cout << "PhiPQ DC" << std::endl;
  PhiPQ("DC");
  std::cout << "PhiPQ DFe" << std::endl;
  PhiPQ("DFe");
  std::cout << "PhiPQ DPb" << std::endl;
  PhiPQ("DPb");

  return 0;
}


int PhiPQ(std::string target) {

  TStopwatch t;

  std::cout << "Start" << std::endl;
  int n = target.length();
  char targetArr[n + 1];
  strcpy(targetArr, target.c_str());

  float VC;
  TString fileDataName;
  if(targetArr[0] == 'D') {
    VC = 1.;
    char solidTarget[n];
    for(int i = 0; i < n; i++){
      solidTarget[i] = targetArr[i+1];
    }
    fileDataName = Form(dataDirectory + "VecSum_%s.root", solidTarget);
  } else{
    VC = 2.;
    fileDataName = Form(dataDirectory + "VecSum_%s.root", targetArr);
  }
  //float Masa = 0.938; // Nucleon Mass (Proton)
  TFile* fileData  = new TFile(fileDataName, "READ");
  float Xb_MIN = 0.1;
  float Xb_MAX = 0.6;
  float Pt_MIN = TMath::Sqrt(Pt2_MIN);
  float Pt_MAX = TMath::Sqrt(Pt2_MAX);
  gROOT->cd();
  TH1F *histQ2 = new TH1F("histQ2", "", 200, Q2_MIN, Q2_MAX);
  TH1F *histXb = new TH1F("histXb", "", 200, Xb_MIN, Xb_MAX);
  TH1F *histZh = new TH1F("histZh", "", 200, Zh_MIN, Zh_MAX);
  TH1F *histPt = new TH1F("histPt", "", 200, Pt_MIN, Pt_MAX);
  TCut Q2Cut, NuCut, ZhCut, Pt2Cut, VCData, cutsData;
  TCut YCCut = "TMath::Abs(YC)<1.4";
  float Q2, Xb, Zh, Pt;
  VCData = Form("VC_TM == %f", VC);

  TFile* outputFile = new TFile(outputDirectory + Form("Centroid_%s.root", targetArr), "RECREATE");
  gROOT->cd();
  for(int nPion = 1; nPion <= N_PION; nPion++) { // Loops in every number of pion
    TNtuple* centroidTuple = new TNtuple(Form("Centroid_%i", nPion), "", 
				     "Q2:Xb:Zh:Pt:Q2Bin:NuBin:ZhBin:Pt2Bin");
    for(int Q2Counter = 0 ; Q2Counter < N_Q2; Q2Counter++) { // Loops in every Q2 bin
      for(int NuCounter = 0 ; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
	for(int ZhCounter = 0 ; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin;

          std::cout << "Bin selected: " << nPion << Q2Counter << NuCounter << ZhCounter << std::endl;
	  Q2Cut  = Form("Q2>%f&&Q2<%f", Q2_BINS[Q2Counter], Q2_BINS[Q2Counter+1]);
	  NuCut  = Form("Nu>%f&&Nu<%f", Nu_BINS[NuCounter], Nu_BINS[NuCounter+1]);
	  ZhCut  = Form("Zh>%f&&Zh<%f", Zh_BINS[ZhCounter], Zh_BINS[ZhCounter+1]);
	  cutsData  = Q2Cut&&NuCut&&ZhCut&&YCCut&&VCData;
	  TNtuple* ntupleData = (TNtuple*) fileData->Get(Form("ntuple_%i_pion", nPion));
	  ntupleData->Draw(">>listData", cutsData, "goff");
	  TEventList* evntData = (TEventList*) gDirectory->Get("listData");
	  ntupleData->SetEventList(evntData);

	  //std::cout << "cuts: "<< cutsData << std::endl;
	  for(int Pt2Counter = 0 ; Pt2Counter < N_Pt2 ; Pt2Counter++) { // Loops in every Pt2 bin

	    Pt2Cut = Form("Pt2>%f&&Pt2<%f", Pt2_BINS[Pt2Counter], Pt2_BINS[Pt2Counter+1]);
	    ntupleData->Draw("Q2>>histQ2", Pt2Cut);
	    ntupleData->Draw("Xb>>histXb", Pt2Cut);
	    ntupleData->Draw("Zh>>histZh", Pt2Cut);
	    ntupleData->Draw("TMath::Sqrt(Pt2)>>histPt", Pt2Cut);
	    // Set the centroid points of the bin
	    Q2 = histQ2->GetMean(); 
	    Xb = histXb->GetMean();
	    Zh = histZh->GetMean();
	    Pt = histPt->GetMean();
	    if(Q2 == 0) { continue; }

	  //std::cout << "Q2: " << Q2 << " Xb: " << Xb << " Zh: " << Zh << " Pt: " << Pt << std::endl;
          centroidTuple->Fill(Q2, Xb, Zh, Pt, Q2Counter, NuCounter, ZhCounter, Pt2Counter);
	  histQ2->Reset();
	  histXb->Reset();
	  histZh->Reset();
	  histPt->Reset();
  	  } // End Pt2 loop
	delete ntupleData;
	delete evntData;
        } // End Zh loop
      } // End Nu loop
    } // End Q2 loop

    outputFile->cd();
    centroidTuple->Write();
    gROOT->cd();
    delete centroidTuple;
  }// End number pion event loop


  outputFile->Close();
  delete histQ2;
  delete histXb;
  delete histZh;
  delete histPt;
  fileData->Close();
  t.Print();
  return 0;

}