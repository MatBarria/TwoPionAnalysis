// g++ -Wall -fPIC -I../include `root-config --cflags` AccEvnt.cpp -o ../bin/AccEvnt  `root-config --glibs` ../include/Binning.h

#include "Binning.h"
#include <iostream>
#include "TH1F.h"
#include "TFile.h"
#include "TString.h"
#include "TROOT.h"
#include "TNtuple.h"

int AccEvnt(std::string target);

const char* VarList = "Q2:Nu:Zh:Pt2:PhiPQ:YC:VC_TM:Zh_1:Zh_2:Zh_3:Acc:FalPos:AccE:FalPosE";

int main() {


  std::cout << "Acceptance Correction for C" << std::endl;
  AccEvnt("C");
  std::cout << "Acceptance Correction for Fe" << std::endl;
  AccEvnt("Fe");
  std::cout << "Acceptance Correction for Pb" << std::endl;
  AccEvnt("Pb");
 
  return 0;
}



int AccEvnt(std::string target) {

  std::cout << "Start" << std::endl;
  int n = target.length();
  char targetArr[n + 1];
  strcpy(targetArr, target.c_str());	
  
  TFile *fileData = new TFile(Form(dataDirectory  + "VecSum_%s.root", targetArr), "READ");
  TFile *fileDataCorr = new TFile(inputDirectory +  "corr_data_Phi.root", "READ");

  float *vars         = new Float_t[14];
  
  int Q2Bin, NuBin, ZhBin, Pt2Bin, PhiBin;
  //bool InPS; // True if the event is in the phase space

  TFile* fileOutput = new TFile(Form(outputDirectory + "VecSum_%s_Acc.root", targetArr),"RECREATE");
  gROOT->cd();
  for(int nPion = 1; nPion <= N_PION ; nPion++) { // Loops in every number of generated pions
  
    TNtuple* ntupleData  = (TNtuple*) fileData->Get(Form("ntuple_%i_pion", nPion));
  
    ntupleData->SetBranchAddress("Q2",&vars[0]);
    ntupleData->SetBranchAddress("Nu",&vars[1]);
    ntupleData->SetBranchAddress("Zh",&vars[2]);
    ntupleData->SetBranchAddress("Pt2",&vars[3]);
    ntupleData->SetBranchAddress("PhiPQ",&vars[4]);
    ntupleData->SetBranchAddress("YC",&vars[5]);
    ntupleData->SetBranchAddress("VC_TM",&vars[6]);
    ntupleData->SetBranchAddress("Zh_1",&vars[7]);
    ntupleData->SetBranchAddress("Zh_2",&vars[8]);
    ntupleData->SetBranchAddress("Zh_3",&vars[9]);
  
    TNtuple* ntupleSafe  = new TNtuple("SafeTuple", "", VarList);

    for(int i = 0; i < ntupleData->GetEntries() ; i++) { // Loops in every detected paricle

      //std::cout << "here 1" << std::endl;
      ntupleData->GetEntry(i);
      //InPS= true;
      Q2Bin = -99; NuBin = -99; ZhBin = -99; PhiBin = -99; Pt2Bin = -99;

      // Search in which Q2 bin is the event
      for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) { // Loops in every Q2 bin
	
  	if(vars[0] > Q2_BINS[Q2Counter] && vars[0] < Q2_BINS[Q2Counter+ 1]) {
	  Q2Bin = Q2Counter;
	  break;
	}

      } // End Q2 loop
      
      // Search in which Nu bin is the event
      for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
      
  	if(vars[1] > Nu_BINS[NuCounter] && vars[1] < Nu_BINS[NuCounter+ 1]) {
	  NuBin = NuCounter;
	  break;
	}

      } // End Nu loop

      // Search in which Zh bin is the event
      for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin
	
  	if(vars[2] > Zh_BINS[ZhCounter] && vars[2] < Zh_BINS[ZhCounter+ 1]) {
	  ZhBin = ZhCounter;
	  break;
	}

      } // End Zh loop

      // Search in which Pt2 bin is the event
      for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Loops in every Pt2 bin

  	if(vars[3] > Pt2_BINS[Pt2Counter] && vars[3] < Pt2_BINS[Pt2Counter+ 1]) {
	  Pt2Bin = Pt2Counter;
	  break;
	}

      } // End Pt2 loop
 
      // Search in which Phi bin is the event
      for(int PhiCounter = 0; PhiCounter < N_Phi; PhiCounter++) { // Loops in every Phi bin

  	if(vars[4] > Phi_BINS[PhiCounter] && vars[4] < Phi_BINS[PhiCounter+ 1]) {
	  PhiBin = PhiCounter;
	  break;
	}

      } // End Phi loop
   
      // Look for the Acc Factors
      TH1F *PhiHistAccFac, *PhiHistAccFalPos; 
      if (vars[6] == 1) {
	PhiHistAccFac = (TH1F*) fileDataCorr->Get(Form("AccFactor_D%s_%i%i%i%i_%i", targetArr, 
							Q2Bin, NuBin, ZhBin, Pt2Bin, nPion)); 
	PhiHistAccFalPos = (TH1F*) fileDataCorr->Get(Form("FalPosFactor_D%s_%i%i%i%i_%i", targetArr, 
							    Q2Bin, NuBin, ZhBin, Pt2Bin, nPion)); 
      }
      if (vars[6] == 2) {
	PhiHistAccFac = (TH1F*) fileDataCorr->Get(Form("AccFactor_%s_%i%i%i%i_%i", targetArr, Q2Bin,
							NuBin, ZhBin, Pt2Bin, nPion)); 
	PhiHistAccFalPos = (TH1F*) fileDataCorr->Get(Form("FalPosFactor_%s_%i%i%i%i_%i", targetArr, 
							   Q2Bin, NuBin, ZhBin, Pt2Bin, nPion)); 
      }
      
      if (vars[6] == 0) {
	PhiHistAccFac = NULL;
	PhiHistAccFalPos = NULL;
      }
      //std::cout << "here 3" << std::endl;
      if(PhiHistAccFac != NULL) {

       vars[10] = PhiHistAccFac->GetBinContent(PhiBin+1); 
       vars[11] = PhiHistAccFalPos->GetBinContent(PhiBin+1); 
       vars[12] = PhiHistAccFac->GetBinError(PhiBin+1); 
       vars[13] = PhiHistAccFalPos->GetBinError(PhiBin+1); 
      
      } else {
	
	vars[10] = 0;
	vars[11] = 0;
	vars[12] = 0;
	vars[13] = 0;
      
      }
      ntupleSafe->Fill(vars);

      delete PhiHistAccFac;
      delete PhiHistAccFalPos;

    } // End paricle loop

    fileOutput->cd();
    ntupleSafe->Write(Form("ntuple_%i_pion", nPion));
    gROOT->cd();

    delete ntupleData;
    delete ntupleSafe;
  } // End number of pions loop

  fileData->Close();
  fileDataCorr->Close();
  fileOutput->Close();
  return 0;

}
