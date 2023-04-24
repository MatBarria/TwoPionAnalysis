// g++ -Wall -fPIC -I../include `root-config --cflags` WeightTuple.cpp -o ../bin/WeightTuple `root-config --glibs` ../include/Binning.h

#include "Binning.h"
#include <iostream>
#include "TH1F.h"
#include "TFile.h"
#include "TString.h"
#include "TROOT.h"
#include "TNtuple.h"

int WeightsTuple(std::string target, TFile* fileWeights ,TFile* fileOutput);
const char* VarList = "Q2:Nu:Zh:Pt2:PhiPQ:weight";

int main() {



    TString CTDirectory = "/home/matias/proyecto/TwoPionAnalysis/Data/60Systematic/CT/";
    TFile* fileWeights = new TFile(CTDirectory + "Weights.root"       , "READ");
    TFile* fileOutput = new TFile(outputDirectory + "WeightTuple.root", "RECREATE");

    std::cout << "Acceptance Tuple for C" << std::endl;
    WeightsTuple("C", fileWeights, fileOutput);
    std::cout << "Acceptance Tuple for Fe" << std::endl;
    WeightsTuple("Fe", fileWeights, fileOutput);
    std::cout << "Acceptance Tuple for Pb" << std::endl;
    WeightsTuple("Pb", fileWeights, fileOutput);
    std::cout << "Acceptance Tuple for DC" << std::endl;
    WeightsTuple("DC", fileWeights, fileOutput);
    std::cout << "Acceptance Tuple for DFe" << std::endl;
    WeightsTuple("DFe", fileWeights, fileOutput);
    std::cout << "Acceptance Tuple for DPb" << std::endl;
    WeightsTuple("DPb", fileWeights, fileOutput);

    fileWeights->Close();
    fileOutput->Close();

    return 0;
}


int WeightsTuple(std::string target, TFile* fileWeights ,TFile* fileOutput) {
    
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

    float weight;

    gROOT->cd();
    for(int nPion = 1; nPion <= N_PION ; nPion++) { // Loops in every number of generated pions

    TNtuple* ntupleSave = new TNtuple(Form("ntuple_%s_%i", targetArr, nPion), "", VarList);

        for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) { // Loops in every Q2 bin
            for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
                for(int ZhCounter = 1; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin
                    for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { 
                        
                        TH1F *histWeight = (TH1F*) fileWeights->Get(Form("Weight_%s_%i%i%i%i_%i",
                                targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion));

                        if(histWeight == NULL) { 
                            delete histWeight;
                            continue; 
                        }

                        for(int PhiCounter = 0; PhiCounter < N_Phi; PhiCounter++) {
                            weight = histWeight->GetBinContent(PhiCounter+1); 
                            if(weight != 0) {
                                ntupleSave->Fill(Q2Counter, NuCounter, ZhCounter, Pt2Counter, 
                                    PhiCounter, weight);
                            }

                        } // End Phi loop
                        delete histWeight;
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

