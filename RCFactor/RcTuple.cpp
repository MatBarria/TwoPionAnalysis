// g++ -Wall -fPIC -I./include `root-config --cflags` RcTuple.cpp -o ./bin/RcTuple `root-config --glibs` ./include/Binning_Rc.h

#include "Binning_Rc.h"
#include <iostream>
#include "TH1F.h"
#include "TFile.h"
#include "TString.h"
#include "TROOT.h"
#include "TNtuple.h"

int RcTuple(std::string target, TFile* fileRc, TFile* fileRcCorr ,TFile* fileOutput);
const char* VarList = "Q2:Nu:Zh:Pt2:PhiPQ:Rc:RcInter";

int main() {

    TFile *fileRc= new TFile(inputDirectory + "RcFactors.root", "READ");
    TFile *fileRcCorr = new TFile(inputDirectory + "RcFactorsInter.root", "READ");
    TFile* fileOutput = new TFile(outputDirectory + "RcTuple.root", "RECREATE");

    std::cout << "Rc Tuple for C" << std::endl;
    RcTuple("C", fileRc, fileRcCorr, fileOutput);
    std::cout << "Rc Tuple for Fe" << std::endl;
    RcTuple("Fe", fileRc, fileRcCorr, fileOutput);
    std::cout << "Rc Tuple for Pb" << std::endl;
    RcTuple("Pb", fileRc, fileRcCorr, fileOutput);
    std::cout << "Rc Tuple for DC" << std::endl;
    RcTuple("DC", fileRc, fileRcCorr, fileOutput);
    std::cout << "Rc Tuple for DFe" << std::endl;
    RcTuple("DFe", fileRc, fileRcCorr, fileOutput);
    std::cout << "Rc Tuple for DPb" << std::endl;
    RcTuple("DPb", fileRc, fileRcCorr, fileOutput);

    fileRcCorr->Close();
    fileOutput->Close();

    return 0;
}


int RcTuple(std::string target, TFile* fileRc, TFile* fileRcCorr ,TFile* fileOutput) {
    
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

    float Rc, RcInter;

    gROOT->cd();
    for(int nPion = 1; nPion <= N_PION ; nPion++) { // Loops in every number of generated pions

    TNtuple* ntupleSave = new TNtuple(Form("ntuple_%s_%i", targetArr, nPion), "", VarList);

        for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) { // Loops in every Q2 bin
            for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
                for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin
                    for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { 
                        
                        TH1F *PhiHistRc, *PhiHistRcInter; 
                        PhiHistRc = (TH1F*) fileRc->Get(
                                Form("RcFactor_%s_%i%i%i%i_%i",
                                targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion)); 
                        PhiHistRcInter = (TH1F*) fileRcCorr->Get(
                                Form("RcFactor_%s_%i%i%i%i_%i", 
                                targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion)); 
                        if(PhiHistRc == NULL || PhiHistRcInter == NULL) { 
                            delete PhiHistRc;
                            delete PhiHistRcInter;
                            continue; 
                        }

                        for(int PhiCounter = 0; PhiCounter < N_Phi; PhiCounter++) {
                            Rc = PhiHistRc->GetBinContent(PhiCounter+1); 
                            RcInter = PhiHistRcInter->GetBinContent(PhiCounter+1); 
                            ntupleSave->Fill(Q2Counter, NuCounter, ZhCounter, Pt2Counter, 
                                    PhiCounter, Rc, RcInter);

                        } // End Phi loop
                        delete PhiHistRc;
                        delete PhiHistRcInter;
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
