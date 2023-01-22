// This code apply the two acceptance factors to the half the of the simulation to do a closure test
// generate a PhiPq histogram for each bin of Q2, Nu, Zh, Pt2
// The hadrons variables used were calculate taking the vectorial
// sum of the hadrons momentum and using it as hadron momentum for the event
// For simultion use the tuple generate by the code VecSumSimul.cpp
// The simulation are splited in two by groups by the program SlipHalf.cpp
// It can be compile with
// g++ -Wall -fPIC -I../include `root-config --cflags` AccSimul.cpp -o ../bin/AccSimul `root-config --glibs` ../include/Acc.h
// For the target name use (C, Fe, Pb, D)

#include "Acc.h"

int AccSimul(std::string target, TFile* fileOutput);

int main() {

  TFile* fileOutput = new TFile(outputDirectory + "corr_data_Phi.root", "RECREATE");
  gROOT->cd();

  std::cout << "Acceptance Correction for C" << std::endl;
  AccSimul("C",   fileOutput);
  std::cout << "Acceptance Correction for Fe" << std::endl;
  AccSimul("Fe",  fileOutput);
  std::cout << "Acceptance Correction for Pb" << std::endl;
  AccSimul("Pb",  fileOutput);
  std::cout << "Acceptance Correction for D" << std::endl;
  AccSimul("D",  fileOutput);
 
  fileOutput->Close();
  return 0;
}


int AccSimul(std::string target, TFile* fileOutput) {

  TStopwatch t;

  std::cout << "Start" << std::endl;
  int n = target.length();
  char targetArr[n + 1];
  strcpy(targetArr, target.c_str());	

  TFile* fileData   = new TFile(Form(dataDirectory + "SimulTuple_%s_2.root", targetArr), "READ");
  TFile* fileSimul  = new TFile(Form(dataDirectory + "SimulTuple_%s_1.root", targetArr), "READ");
  gROOT->cd();

  // Create some variables to use inside the for loops
  TString tupleDataName;
  TCut Q2CutGen, NuCutGen, ZhCutGen, Pt2CutGen, cutsGen, GenCut, RecCut, GenDecCut;
  TCut Q2CutRec, NuCutRec, ZhCutRec, Pt2CutRec, cutsRec;
  // Do not take in count of 0 generated pion in the simultion beacause the is not hadrons variables to select a bin
  // Select liquid or solid target
  // Create all the necessary histograms
  TH1F* histDetected    = new TH1F("Detected",      "", N_Phi, -180, 180);
  TH1F* histTotDetected = new TH1F("TotDetected",   "", N_Phi, -180, 180);
  TH1F* histThrown      = new TH1F("Thrown",        "", N_Phi, -180, 180);
  TH1F* histData        = new TH1F("Data",          "", N_Phi, -180, 180);
  TH1F* histFalPos      = new TH1F("FalPosFactor",  "", N_Phi, -180, 180);
  TH1F* histAccFactors  = new TH1F("AccFactor",     "", N_Phi, -180, 180);
  TH1F* histDataCorr    = new TH1F("DataCorr",      "", N_Phi, -180, 180);
  TH1F* histDataCorr2   = new TH1F("DataCorr2",     "", N_Phi, -180, 180);

  // Store the sum of the weights A.K.A the erros (in the other histograms if save it by other methods)
  histData->Sumw2();
  histThrown->Sumw2();
  histTotDetected->Sumw2();
  histDetected->Sumw2();

  for(int gen = 1; gen <= N_PION ; gen++) { // Loops in every number of generated pions

    GenCut    = Form("Gen == %f", (float)gen);
    RecCut    = Form("Rec == %f", (float)gen);
    GenDecCut = GenCut||RecCut;

    for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) { // Loops in every Q2 bin
      for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
        for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin

          std::cout << "Bin selected: " << gen << Q2Counter << NuCounter << ZhCounter << std::endl;

          // Select the cuts for each bin
          Q2CutGen   = Form("Q2_gen>%f&&Q2_gen<%f", Q2_BINS[Q2Counter],   Q2_BINS[Q2Counter+1]);
          NuCutGen   = Form("Nu_gen>%f&&Nu_gen<%f", Nu_BINS[NuCounter],   Nu_BINS[NuCounter+1]);
          ZhCutGen   = Form("Zh_gen>%f&&Zh_gen<%f", Zh_BINS[ZhCounter],   Zh_BINS[ZhCounter+1]);
          Q2CutRec   = Form("Q2_rec>%f&&Q2_rec<%f", Q2_BINS[Q2Counter],   Q2_BINS[Q2Counter+1]);
          NuCutRec   = Form("Nu_rec>%f&&Nu_rec<%f", Nu_BINS[NuCounter],   Nu_BINS[NuCounter+1]);
          ZhCutRec   = Form("Zh_rec>%f&&Zh_rec<%f", Zh_BINS[ZhCounter],   Zh_BINS[ZhCounter+1]);

          cutsGen  = Q2CutGen&&NuCutGen&&ZhCutGen&&GenCut;
          cutsRec  = Q2CutRec&&NuCutRec&&ZhCutRec&&RecCut;


          TNtuple* ntupleData  = (TNtuple*) fileData->Get("ntuple_sim_rec_2");
          TNtuple* ntupleSimulGen = (TNtuple*) fileSimul->Get("ntuple_sim_gen_1");
          TNtuple* ntupleSimulRec = (TNtuple*) fileSimul->Get("ntuple_sim_rec_1");

          // Apply the cuts to the ntuples to increces the efficiency
          ntupleData->Draw(">>listData", cutsRec);
          ntupleSimulGen->Draw(">>listSimulGen", cutsGen);
          ntupleSimulRec->Draw(">>listSimulRec", cutsRec);
          TEventList* evntData= (TEventList*) gDirectory->Get("listData");
          TEventList* evntSimulRec = (TEventList*) gDirectory->Get("listSimulRec");
          TEventList* evntSimulGen= (TEventList*) gDirectory->Get("listSimulGen");
          ntupleData->SetEventList(evntData);
          ntupleSimulRec->SetEventList(evntSimulRec);
          ntupleSimulGen->SetEventList(evntSimulGen);

          for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Loops in every Pt2 bin

            // Select the Pt2 bin
            Pt2CutGen = Form("Pt2_gen>%f&&Pt2_gen<%f", Pt2_BINS[Pt2Counter], Pt2_BINS[Pt2Counter+1]);
            Pt2CutRec = Form("Pt2_rec>%f&&Pt2_rec<%f", Pt2_BINS[Pt2Counter], Pt2_BINS[Pt2Counter+1]);

            ntupleData->Project("Data", "PhiPQ_rec", Pt2CutRec);
            if(EmptyHist(histData) == 1){ continue; } // If there isn't any event in data skip this bin
            ntupleSimulRec->Project("Detected",    "PhiPQ_rec", Pt2CutRec&&GenCut);
            ntupleSimulGen->Project("Thrown",      "PhiPQ_gen", Pt2CutGen);
            ntupleSimulRec->Project("TotDetected", "PhiPQ_rec", Pt2CutRec);

            // Calculate the Acceptance factor
            histAccFactors->Divide(histDetected, histThrown, 1, 1, "B");
            histFalPos->Divide(histDetected, histTotDetected, 1, 1, "B");
            // Check that the acceptance factors are smaller than one
            // Apply the correction factors
            histDataCorr->Divide(histData, histAccFactors, 1, 1);
            histDataCorr2->Multiply(histDataCorr, histFalPos, 1, 1);

            // Save the histograms in the output file

            fileOutput->cd();
	
	    if(targetArr[0] != 'D') { 
	      histDataCorr2->Write(Form("DataCorr2_%s_%i%i%i%i_%i",    targetArr, Q2Counter, 
					NuCounter, ZhCounter, Pt2Counter, gen));
	      histDataCorr->Write(Form("DataCorr_%s_%i%i%i%i_%i",      targetArr, Q2Counter,
					NuCounter, ZhCounter, Pt2Counter, gen));
	    } else {
	      histDataCorr2->Write(Form("DataCorr2_%sC_%i%i%i%i_%i",   targetArr, Q2Counter,
					NuCounter, ZhCounter, Pt2Counter, gen));
	      histDataCorr->Write(Form("DataCorr_%sC_%i%i%i%i_%i",     targetArr, Q2Counter,
					NuCounter, ZhCounter, Pt2Counter, gen));
	      histDataCorr2->Write(Form("DataCorr2_%sFe_%i%i%i%i_%i",  targetArr, Q2Counter,
					NuCounter, ZhCounter, Pt2Counter, gen));
	      histDataCorr->Write(Form("DataCorr_%sFe_%i%i%i%i_%i",    targetArr, Q2Counter,
					NuCounter, ZhCounter, Pt2Counter, gen));
	      histDataCorr2->Write(Form("DataCorr2_%sPb_%i%i%i%i_%i",  targetArr, Q2Counter,
					NuCounter, ZhCounter, Pt2Counter, gen));
	      histDataCorr->Write(Form("DataCorr_%sPb_%i%i%i%i_%i",    targetArr, Q2Counter,
					NuCounter, ZhCounter, Pt2Counter, gen));
	    }

            gROOT->cd();

            // Set the histograms values to 0
            histData->Reset();
            histDataCorr2->Reset();
            histDataCorr->Reset();
            histFalPos->Reset();
            histAccFactors->Reset();
            histThrown->Reset();
            histDetected->Reset();
            histTotDetected->Reset();

          } // End Pt2 loop
	    //
          delete ntupleData;
          delete ntupleSimulRec;
	  delete ntupleSimulGen;
          delete evntData;
          delete evntSimulRec;
          delete evntSimulGen;
        } // End Q2 loop
      } // End Nu loop
    } // End Zh loop
  } // End pion number loop
  fileData->Close();
  fileSimul->Close();
  t.Print();
  delete histDetected    ;
  delete histTotDetected ;
  delete histThrown      ;
  delete histData        ;
  delete histFalPos      ;
  delete histAccFactors  ;
  delete histDataCorr    ;
  delete histDataCorr2   ;
  return 0;
}
