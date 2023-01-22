// This code apply the Rc Factors generate by genRC.cpp to the data with acceptance correction
// It can be compiled using
// g++ -Wall -fPIC -I./include `root-config --cflags` ApplyRcFactor.cpp -o ./bin/ApplyRcFactor  `root-config --glibs` ./include/Integration_Rc.h
#include "Integration_Rc.h"

int ApplyRC(std::string target, TFile* fileData, TFile* fileRcFactors, TFile* fileOutput);

int main() {

    TFile* fileData      = new TFile(inputDirectory  + "corr_data_Phi.root"    , "READ");
    TFile* fileRcFactors = new TFile(inputDirectory  + "RcFactorsInter.root"   , "READ");
    //TFile* fileRcFactors = new TFile(inputDirectory  + "RcFactors.root"   , "READ");
    TFile* fileOutput    = new TFile(outputDirectory + "corr_data_Phi_Rc.root" , "RECREATE");
    gROOT->cd();

    std::cout << "Appling Rc on C" << std::endl;
    ApplyRC("C",   fileData, fileRcFactors, fileOutput);
    std::cout << "Appling Rc on Fe" << std::endl;
    ApplyRC("Fe",  fileData, fileRcFactors, fileOutput);
    std::cout << "Appling Rc on Pb" << std::endl;
    ApplyRC("Pb",  fileData, fileRcFactors, fileOutput);
    std::cout << "Appling Rc on DC" << std::endl;
    ApplyRC("DC",  fileData, fileRcFactors, fileOutput);
    std::cout << "Appling Rc on DFe" << std::endl;
    ApplyRC("DFe", fileData, fileRcFactors, fileOutput);
    std::cout << "Appling Rc on DPb" << std::endl;
    ApplyRC("DPb", fileData, fileRcFactors, fileOutput);

    fileData->Close();
    fileRcFactors->Close();
    fileOutput->Close();
    return 0;

}

int ApplyRC(std::string target, TFile* fileData, TFile* fileRcFactors, TFile* fileOutput) {

    std::cout << "Start" << std::endl;
    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());

    TH1F* histDataCorr  = new TH1F("DataCorrRc", "", N_Phi, -180, 180);

    for(int nPion = 1; nPion <= N_PION ; nPion++) { // Loops in every number of generated pions
        for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) { // Loops Q2 bins
            for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops Nu bins
                for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops Zh bins
                    for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Loops Pt2 bin

                        TH1F *histData = (TH1F*) fileData->Get(Form("DataCorr2_%s_%i%i%i%i_%i", 
                                targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion));
                        TH1F *histRc = (TH1F*) fileRcFactors->Get(Form("RcFactor_%s_%i%i%i%i_%i",
                                targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion));

                        if(histRc == NULL || histData == NULL ||
                            EmptyHist(histRc) == 1 || EmptyHist(histData) == 1) {
                            delete histData;
                            delete histRc;
                            continue; }

                        histDataCorr->Divide(histData, histRc, 1, 1);

                        // Save the histograms in the output file
                        fileOutput->cd();
                        histDataCorr->Write(Form("DataCorrRc_%s_%i%i%i%i_%i",targetArr, 
                                    Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion));
                        gROOT->cd();

                        delete histData;
                        delete histRc;
                        histDataCorr->Reset();
                    } // End Pt2 loop
                } // End Zh loop
            } // End Nu loop
        } // End Q2 loop
    } // End pion number loop

    delete histDataCorr;
    return 0;

}
