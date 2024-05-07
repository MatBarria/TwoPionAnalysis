// This code apply the  Factors generate by genRC.cpp to the data with acceptance correction
// It can be compiled using
// g++ -Wall -fPIC -I../include `root-config --cflags` ApplyCTWeights.cpp -o
// ../bin/ApplyCTWeights  `root-config --glibs` ../include/Integration2.h

#include "Integration2.h"

int ApplyWeights(std::string target, TFile *fileData, TFile *fileWeights, TFile *fileOutput);

int main() {

    // const TString inputDirectory  =
    // "/home/matias/proyecto/TwoPionAnalysis/Data/60Systematic/LimitHigh/";

    TFile *fileData = new TFile(inputDirectory + "corr_data_Phi_Inter.root", "READ");
    TFile *fileWeights = new TFile(sysDirectory + "CT/Weights.root", "READ");
    TFile *fileOutput = new TFile(sysDirectory + "CT/corr_data_Phi.root", "RECREATE");
    gROOT->cd();

    std::cout << "Appling Weights on C" << std::endl;
    ApplyWeights("C", fileData, fileWeights, fileOutput);
    std::cout << "Appling Weights on Fe" << std::endl;
    ApplyWeights("Fe", fileData, fileWeights, fileOutput);
    std::cout << "Appling Weights on Pb" << std::endl;
    ApplyWeights("Pb", fileData, fileWeights, fileOutput);
    std::cout << "Appling Weights on DC" << std::endl;
    ApplyWeights("DC", fileData, fileWeights, fileOutput);
    std::cout << "Appling Weights on DFe" << std::endl;
    ApplyWeights("DFe", fileData, fileWeights, fileOutput);
    std::cout << "Appling Weights on DPb" << std::endl;
    ApplyWeights("DPb", fileData, fileWeights, fileOutput);

    fileData->Close();
    fileWeights->Close();
    fileOutput->Close();
    return 0;
}

int ApplyWeights(std::string target, TFile *fileData, TFile *fileWeights, TFile *fileOutput) {

    std::cout << "Start" << std::endl;
    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());

    TH1F *histAccCorr = new TH1F("histAccCorr", "", N_Phi, -180, 180);

    for (int nPion = 1; nPion <= N_PION; nPion++) { // Loops in every number of generated pions
        for (int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) {         // Loops Q2 bins
            for (int NuCounter = 0; NuCounter < N_Nu; NuCounter++) {     // Loops Nu bins
                for (int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops Zh bins
                    for (int Pt2Counter = 0; Pt2Counter < N_Pt2;
                         Pt2Counter++) { // Loops Pt2 bin

                        // TH1F *histAcc = (TH1F*)
                        // fileData->Get(Form("FinalFactor_%s_%i%i%i%i_%i", targetArr,
                        // Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion));
                        TH1F *histAcc = (TH1F *)fileData->Get(
                            Form("DataCorr2_%s_%i%i%i%i_%i", targetArr, Q2Counter, NuCounter,
                                 ZhCounter, Pt2Counter, nPion));
                        TH1F *histWeight = (TH1F *)fileWeights->Get(
                            Form("Weight_%s_%i%i%i%i_%i", targetArr, Q2Counter, NuCounter,
                                 ZhCounter, Pt2Counter, nPion));

                        if (histWeight == NULL || histAcc == NULL ||
                            EmptyHist(histWeight) == 1 || EmptyHist(histAcc) == 1) {
                            delete histAcc;
                            delete histWeight;
                            continue;
                        }

                        // histAccCorr->Multiply(histAcc, histWeight, 1, 1);
                        histAccCorr->Divide(histAcc, histWeight, 1, 1);

                        // Save the histograms in the output file
                        fileOutput->cd();
                        histAccCorr->Write(Form("DataCorr2_%s_%i%i%i%i_%i", targetArr,
                                                Q2Counter, NuCounter, ZhCounter, Pt2Counter,
                                                nPion));
                        gROOT->cd();

                        delete histAcc;
                        delete histWeight;
                        histAccCorr->Reset();
                    } // End Pt2 loop
                }     // End Zh loop
            }         // End Nu loop
        }             // End Q2 loop
    }                 // End pion number loop

    delete histAccCorr;
    return 0;
}
