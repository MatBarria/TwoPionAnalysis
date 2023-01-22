// g++ -Wall -fPIC -I../include `root-config --cflags` PhiHistCorr.cpp -o ../bin/PhiHistCorr `root-config --glibs` ../include/Binning.h

#include <iostream>
#include "Binning.h"
#include "TROOT.h" 
#include "TH1F.h"
#include "TNtuple.h"
#include "TFile.h"
#include "TStopwatch.h"

int PhiHistCorr(std::string target, TFile* fileOutput);

int main() {

  TFile* fileOutput = new TFile(outputDirectory + "corr_data_Phi_Evnt.root", "RECREATE");
  gROOT->cd();

  std::cout << "Acceptance Correction for C" << std::endl;
  PhiHistCorr("C",   fileOutput);
  std::cout << "Acceptance Correction for Fe" << std::endl;
  PhiHistCorr("Fe",  fileOutput);
  std::cout << "Acceptance Correction for Pb" << std::endl;
  PhiHistCorr("Pb",  fileOutput);
  std::cout << "Acceptance Correction for DC" << std::endl;
  PhiHistCorr("DC",  fileOutput);
  std::cout << "Acceptance Correction for DFe" << std::endl;
  PhiHistCorr("DFe", fileOutput);
  std::cout << "Acceptance Correction for DPb" << std::endl;
  PhiHistCorr("DPb", fileOutput);

  fileOutput->Close();
  return 0;

}

int PhiHistCorr(std::string target, TFile* fileOutput) {

  TStopwatch t;

  std::cout << "Start" << std::endl;
  int n = target.length();
  char targetArr[n + 1];
  strcpy(targetArr, target.c_str());	

  float VCCut;
  TString fileDataName;
  // Select the data for the chosen solid target
  if(targetArr[0] == 'D') {
    VCCut = 1.;
    char solidTarget[n];
    for(int i = 0; i < n; i++){
      solidTarget[i] = targetArr[i+1];
    }
    fileDataName = Form(inputDirectory + "VecSum_%s_Acc.root", solidTarget);
  } else{
    VCCut=2;
    fileDataName = Form(inputDirectory + "VecSum_%s_Acc.root", targetArr);
  }
  // Open the input and output files
  TFile* fileData   = new TFile(fileDataName, "READ");
  gROOT->cd();

  float ZhEvnt, Q2Evnt, NuEvnt, Pt2Evnt, PhiEvnt, YCEvnt, Acc, FalPos, Vc, weight;
  
  TH1F *histPhi[N_Q2][N_Nu][N_Zh][N_Pt2]; 
  int Q2Bin, NuBin, ZhBin, Pt2Bin;

  for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) { // Loops in every Q2 bin
    for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
      for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin
        for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Loops in every Pt2 bin
	  delete gROOT->FindObject(Form("histPhi_%i%i%i%i", Q2Counter, NuCounter, ZhCounter,
					Pt2Counter));
	  histPhi[Q2Counter][NuCounter][ZhCounter][Pt2Counter] = new TH1F(Form("histPhi_%i%i%i%i",
		Q2Counter, NuCounter, ZhCounter, Pt2Counter), "", 12, -180, 180); 
	} // End Pt2 loop
      } // End Q2 loop
    } // End Nu loop
  } // End Zh loop
  for(int nPion = 1; nPion <= N_PION; nPion++) {

    TNtuple* ntupleData = (TNtuple*) fileData->Get(Form("ntuple_%i_pion", nPion));
    ntupleData->SetBranchAddress("Q2",     &Q2Evnt);
    ntupleData->SetBranchAddress("Nu",     &NuEvnt);
    ntupleData->SetBranchAddress("Zh",     &ZhEvnt);
    ntupleData->SetBranchAddress("Pt2",    &Pt2Evnt);
    ntupleData->SetBranchAddress("PhiPQ",  &PhiEvnt);
    ntupleData->SetBranchAddress("Acc",    &Acc);
    ntupleData->SetBranchAddress("FalPos", &FalPos);
    ntupleData->SetBranchAddress("VC_TM",  &Vc);
    ntupleData->SetBranchAddress("YC",     &YCEvnt);
  
    for(int i = 0; i < ntupleData->GetEntries() ; i++) { // Loops in every detected paricle

      ntupleData->GetEntry(i);

      if(Vc != VCCut || ZhEvnt > 1 || Q2Evnt < Q2_BINS[0] || Q2Evnt > Q2_BINS[N_Q2] ||
	  NuEvnt < Nu_BINS[0] || NuEvnt > Nu_BINS[N_Nu] || TMath::Abs(YCEvnt) > 1.4) { continue; }

      for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) { // Loops in every Q2 bin
	if(Q2Evnt > Q2_BINS[Q2Counter] && Q2Evnt < Q2_BINS[Q2Counter+ 1]) {
	  Q2Bin = Q2Counter;
	  break;
	}
      } // End Q2 loop

      for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
	if(NuEvnt > Nu_BINS[NuCounter] && NuEvnt < Nu_BINS[NuCounter+ 1]) {
	  NuBin = NuCounter;
	  break;
	}
      } // End Nu loop
      
      for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin
	if(ZhEvnt > Zh_BINS[ZhCounter] && ZhEvnt < Zh_BINS[ZhCounter+ 1]) {
	  ZhBin = ZhCounter;
	  break;
	}
      } // End Zh loop
      
      for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Loops in every Pt2 bin
	if(Pt2Evnt > Pt2_BINS[Pt2Counter] && Pt2Evnt < Pt2_BINS[Pt2Counter+ 1]) {
	  Pt2Bin = Pt2Counter;
	  break;
	}
      } // End Pt2 loop

      if ( Acc != 0 ) { 
	weight = FalPos/Acc;
      } else {
	weight = 0;
      }
      histPhi[Q2Bin][NuBin][ZhBin][Pt2Bin]->Fill(PhiEvnt, weight);
     

    } // End paricle loop

    for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) { // Loops in every Q2 bin
      for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
	for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin
	  for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Loops in every Pt2 bin
	    fileOutput->cd();
	    histPhi[Q2Counter][NuCounter][ZhCounter][Pt2Counter]->Write(Form(
		  "DataCorr2_%s_%i%i%i%i_%i", targetArr, Q2Counter, NuCounter, ZhCounter, 
		   Pt2Counter, nPion));
	    gROOT->cd();
	    histPhi[Q2Counter][NuCounter][ZhCounter][Pt2Counter]->Reset();
	  } // End Pt2 loop
	} // End Q2 loop
      } // End Nu loop
    } // End Zh loop
  
    delete ntupleData;
  }
  fileData->Close();
  return 0;

}
