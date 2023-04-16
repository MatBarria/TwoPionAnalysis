// It can be compile with
// g++ -Wall -fPIC -I../include `root-config --cflags` ApplyACFactors.cpp -o ../bin/ApplyACFactors `root-config --glibs` ../include/Binning.h
// For the target name use (C,Fe,Pb) for the solids targets and (DC,DFe,DPb) for the liquid target

#include "Binning.h"
#include "TCut.h"
#include "TFile.h"
#include "TROOT.h"
#include <iostream>
#include "TStopwatch.h"
#include "TString.h"
#include "TNtuple.h"
#include "TH1.h"
#include "TEventList.h"
#include "TMath.h"
#include "TCanvas.h"

int ApplyAccFactors(std::string target, TFile* fileOutput);
int EmptyHist(TH1F* h);

int main() {

    TFile* fileOutput = new TFile(outputDirectory + "corr_data_Phi_Evnt.root", "RECREATE");
    gROOT->cd();

    std::cout << "Apply AC Factor for C" << std::endl;
    ApplyAccFactors("C",   fileOutput);
    std::cout << "Apply AC Factor for Fe" << std::endl;
    ApplyAccFactors("Fe",  fileOutput);
    std::cout << "Apply AC Factor for Pb" << std::endl;
    ApplyAccFactors("Pb",  fileOutput);
    std::cout << "Apply AC Factor for DC" << std::endl;
    ApplyAccFactors("DC",   fileOutput);
    std::cout << "Apply AC Factor for DFe" << std::endl;
    ApplyAccFactors("DFe",  fileOutput);
    std::cout << "Apply AC Factor for DPb" << std::endl;
    ApplyAccFactors("DPb",  fileOutput);

    fileOutput->Close();
    return 0;
}



int ApplyAccFactors(std::string target,TFile* fileOutput) {

    Pt2_BINS[0] = 0.;
    for(int i = 1; i <= N_Pt2; i++) {
        Pt2_BINS[i] = Pt2_BINS[i-1] + Delta_Pt2;
        //std::cout << "Pt Bin " << i << ": " << Pt2_BINS[i] << std::endl;
    }

    TStopwatch t;

    std::cout << "Start" << std::endl;
    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());	

    TString fileDataName;
    // Select the data for the chosen solid target
    if(targetArr[0] == 'D') {
        char solidTarget[n];
        for(int i = 0; i < n; i++){
            solidTarget[i] = targetArr[i+1];
        }
        fileDataName = Form(dataDirectory + "VecSum_%s_Acc.root", solidTarget);
    } else{
        fileDataName = Form(dataDirectory + "VecSum_%s_Acc.root", targetArr);
    }

    float VCData;
    if(targetArr[0] == 'D') { VCData  = 1.;}
    else {VCData  = 2.;}

    TFile *fileData = new TFile(Form(fileDataName, targetArr), "READ");

    int Q2Bin, NuBin, ZhBin, Pt2Bin;
    float Q2, Nu, Zh, Pt2, PhiPQ, Yc, Vc, Acc, FalPos;
    gROOT->cd();

    for(int nPion = 1; nPion <= N_PION ; nPion++) { // Loops in every number of generated pions
        TH1F *PhiHistograms[N_Q2][N_Nu][N_Zh][N_Pt2];

        for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++ ) {
            for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++ ) {
                for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++ ) {
                    for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++ ) {
                        PhiHistograms[Q2Counter][NuCounter][ZhCounter][Pt2Counter] = new TH1F(
                            Form("DataCorr2_%s_%i%i%i%i_%i",  targetArr, Q2Counter, NuCounter,
                                ZhCounter, Pt2Counter, nPion), "", N_Phi, -180, 180);
                    }
                }
            }
        }
        TNtuple* ntupleData  = (TNtuple*) fileData->Get(Form("ntuple_%i_pion", nPion));

        ntupleData->SetBranchAddress("Q2",&Q2);
        ntupleData->SetBranchAddress("Nu",&Nu);
        ntupleData->SetBranchAddress("Zh",&Zh);
        ntupleData->SetBranchAddress("Pt2",&Pt2);
        ntupleData->SetBranchAddress("PhiPQ",&PhiPQ);
        ntupleData->SetBranchAddress("YC",&Yc);
        ntupleData->SetBranchAddress("VC_TM",&Vc);
        ntupleData->SetBranchAddress("Acc",&Acc);
        ntupleData->SetBranchAddress("FalPos",&FalPos);


        for(int i = 0; i < ntupleData->GetEntries() ; i++) { // Loops in every detected paricle

            ntupleData->GetEntry(i);
            Q2Bin = -99; NuBin = -99; ZhBin = -99; Pt2Bin = -99;

            if(Vc != VCData || TMath::Abs(Yc) > 1.4 || Acc == 0 || FalPos == 0) { 
                continue; }
            // Search in which Q2 bin is the event
            for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) { // Loops in every Q2 bin
                if(Q2 > Q2_BINS[Q2Counter] && Q2 < Q2_BINS[Q2Counter+ 1]) {
                    Q2Bin = Q2Counter;
                    break;
                }

            } // End Q2 loop

            // Search in which Nu bin is the event
            for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin

                if(Nu > Nu_BINS[NuCounter] && Nu < Nu_BINS[NuCounter+ 1]) {
                    NuBin = NuCounter;
                    break;
                }

            } // End Nu loop

            // Search in which Zh bin is the event
            for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin

                if(Zh > Zh_BINS[ZhCounter] && Zh < Zh_BINS[ZhCounter+ 1]) {
                    ZhBin = ZhCounter;
                    break;
                }

            } // End Zh loop

            // Search in which Pt2 bin is the event
            for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Loops in every Pt2 bin

                if(Pt2 > Pt2_BINS[Pt2Counter] && Pt2 < Pt2_BINS[Pt2Counter+ 1]) {
                    Pt2Bin = Pt2Counter;
                    break;
                }

            } // End Pt2 loop

            //std::cout << Q2Bin << NuBin << ZhBin << Pt2Bin << std::endl;
            //std::cout << Pt2Bin << std::endl;
            //std::cout << "Filling" << std::endl;
            PhiHistograms[Q2Bin][NuBin][ZhBin][Pt2Bin]->Fill(PhiPQ, FalPos/Acc);
            //std::cout << "Post Filling" << std::endl;

        } // End paricle loop

        for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++ ) {
            for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++ ) {
                for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++ ) {
                    for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++ ) {
                        fileOutput->cd();
                        if(EmptyHist(PhiHistograms[Q2Counter][NuCounter][ZhCounter][Pt2Counter])
                                == 1){ continue; }
                        PhiHistograms[Q2Counter][NuCounter][ZhCounter][Pt2Counter]->Write();
                        gROOT->cd();
                        delete PhiHistograms[Q2Counter][NuCounter][ZhCounter][Pt2Counter];        
                    }
                }
            }
        }

        //for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++ ) {
            //for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++ ) {
                //for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++ ) {
                    //for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++ ) {
                    //}
                //}
            //}
        //}
    } // End number of pions loop


    fileData->Close();
    return 0;

}

int EmptyHist(TH1F* h) {

    int empty = 0;
    for(int i = 1 ; i <= h->GetNbinsX() ; i++) {
        if(h->GetBinContent(i) == 0){ empty++; } 
    }
    if(empty == h->GetNbinsX()) { return 1; }
    else { return 0; }

}
