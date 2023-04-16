// g++ -Wall -fPIC -I../include `root-config --cflags` AccFactorsTuple.cpp -o ../bin/AccFactorsTuple  `root-config --glibs` ../include/Binning.h

#include "Binning.h"
#include <iostream>
#include "TH1F.h"
#include "TFile.h"
#include "TString.h"
#include "TROOT.h"
#include "TNtuple.h"

int AccTuple(std::string target, TFile* fileDataCorr ,TFile* fileOutput);
const char* VarList = "Q2:Nu:Zh:Pt2:PhiPQ:Acc:FalPos:FinalFactor";

int main() {

    TFile *fileDataCorr = new TFile(inputDirectory + "corr_data_Phi.root", "READ");
    TFile* fileOutput = new TFile(outputDirectory + "AccTuple.root", "RECREATE");

    std::cout << "Acceptance Tuple for C" << std::endl;
    AccTuple("C", fileDataCorr, fileOutput);
    std::cout << "Acceptance Tuple for Fe" << std::endl;
    AccTuple("Fe", fileDataCorr, fileOutput);
    std::cout << "Acceptance Tuple for Pb" << std::endl;
    AccTuple("Pb", fileDataCorr, fileOutput);
    std::cout << "Acceptance Tuple for DC" << std::endl;
    AccTuple("DC", fileDataCorr, fileOutput);
    std::cout << "Acceptance Tuple for DFe" << std::endl;
    AccTuple("DFe", fileDataCorr, fileOutput);
    std::cout << "Acceptance Tuple for DPb" << std::endl;
    AccTuple("DPb", fileDataCorr, fileOutput);

    fileDataCorr->Close();
    fileOutput->Close();

    return 0;
}


int AccTuple(std::string target, TFile* fileDataCorr ,TFile* fileOutput) {
    
    Pt2_BINS[0] = 0.;
    Phi_BINS[0] = -180;
    for(int i = 1; i <= N_Pt2; i++) {
        Pt2_BINS[i] = Pt2_BINS[i-1] + Delta_Pt2;
    }
    for(int i = 1; i <= N_Phi; i++) {
        Phi_BINS[i] = Phi_BINS[i-1] + Delta_Phi;
    }

    std::cout << "Start" << std::endl;
    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());	

    float Acc, FalPos, FinalFactor;

    gROOT->cd();
    for(int nPion = 1; nPion <= N_PION ; nPion++) { // Loops in every number of generated pions

    TNtuple* ntupleSave = new TNtuple(Form("ntuple_%s_%i", targetArr, nPion), "", VarList);

        for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) { // Loops in every Q2 bin
            for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
                for(int ZhCounter = ZH_SUM; ZhCounter < N_Zh-1; ZhCounter++) { // Loops in every Zh bin
                    for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { 
                        
                        TH1F *PhiHistAccFac, *PhiHistAccFalPos; 
                        PhiHistAccFac = (TH1F*) fileDataCorr->Get(
                                Form("AccFactor_%s_%i%i%i%i_%i",
                                targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion)); 
                        PhiHistAccFalPos = (TH1F*) fileDataCorr->Get(
                                Form("FalPosFactor_%s_%i%i%i%i_%i", 
                                targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion)); 
                        if(PhiHistAccFac == NULL || PhiHistAccFalPos == NULL) { 
                            delete PhiHistAccFac;
                            delete PhiHistAccFalPos;
                            continue; 
                        }

                        for(int PhiCounter = 0; PhiCounter < N_Phi; PhiCounter++) {
                            Acc = PhiHistAccFac->GetBinContent(PhiCounter+1); 
                            FalPos = PhiHistAccFalPos->GetBinContent(PhiCounter+1); 
                            if(FalPos!=0) { FinalFactor = Acc/FalPos; }
                            else {FinalFactor = 0;}
                            ntupleSave->Fill(Q2Counter, NuCounter, ZhCounter, Pt2Counter, 
                                    PhiCounter, Acc, FalPos, FinalFactor);

                        } // End Phi loop
                        delete PhiHistAccFac;
                        delete PhiHistAccFalPos;
                    } // End Phi loop
                } // End Phi loop
            } // End Phi loop
        } // End Phi loop
                


    fileOutput->cd();
    ntupleSave->Write();
    gROOT->cd();
    delete ntupleSave;

    } // End number of pions loop

    return 0;

}

