// This code generate a TGraphErrors of the Pt2 distribution in the Zh nBins
// for the diferents steps of the processing
// It can be compiled using
// g++g++ -Wall -fPIC -I../include `root-config --cflags` Pt2Distributions.cpp -o
// ../bin/Pt2Distributions `root-config --glibs` ../include/Broad.h -Wall -fPIC -I../include
// `root-config --cflags` Pt2Distributions.cpp -o ../bin/Pt2Distributions `root-config --glibs`
// ../include/Broad.h

#include "Broad.h"

int Pt2_Distribution(std::string target, TFile *inputFile, TFile *outputFile);

int main() {

    TFile *inputFile = new TFile(inputDirectory + "corr_data_Pt2_processed.root", "READ");
    TFile *outputFile = new TFile(outputDirectory + "Pt2_Distribution.root", "RECREATE");
    gROOT->cd();

    Pt2_Distribution("C", inputFile, outputFile);
    Pt2_Distribution("Fe", inputFile, outputFile);
    Pt2_Distribution("Pb", inputFile, outputFile);
    Pt2_Distribution("DC", inputFile, outputFile);
    Pt2_Distribution("DFe", inputFile, outputFile);
    Pt2_Distribution("DPb", inputFile, outputFile);

    inputFile->Close();
    outputFile->Close();
}

int Pt2_Distribution(std::string target, TFile *inputFile, TFile *outputFile) {

    TStopwatch t;

    std::cout << "Start" << std::endl;
    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());

    for (int nPion = 1; nPion <= N_PION; nPion++) { // Loops in every number of pion
        // Generate a histogram to save Zh for every number of pion in the final event
        for (int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) {     // Loops in every Zh bin
            for (int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Zh bin
                for (int ZhCounter = 0; ZhCounter < N_Zh;
                     ZhCounter++) { // Loops in every Zh bin
                    // Generate a Pt2 histogram for every bin of Zh and kind of processind
                    TH1F *histPt2 =
                        (TH1F *)inputFile->Get(Form("corr_data_Pt2_%s_%i%i%i_%i", targetArr,
                                                    Q2Counter, NuCounter, ZhCounter, nPion));
                    TH1F *histPt2Clean = (TH1F *)inputFile->Get(
                        Form("corr_data_Pt2_%s_%i%i%i_%i_clean", targetArr, Q2Counter,
                             NuCounter, ZhCounter, nPion));
                    TH1F *histPt2Inter = (TH1F *)inputFile->Get(
                        Form("corr_data_Pt2_%s_%i%i%i_%i_interpolated", targetArr, Q2Counter,
                             NuCounter, ZhCounter, nPion));
                    TGraphErrors *Pt2Distribution, *Pt2DistributionClean,
                        *Pt2DistributionInter;

                    // Transform the histogram into TGraphs
                    std::cout << "-----" << std::endl;
                    Pt2Distribution = (TGraphErrors *)TH1TOTGraph(histPt2);
                    Pt2DistributionClean = (TGraphErrors *)TH1TOTGraph(histPt2Clean);
                    Pt2DistributionInter = (TGraphErrors *)TH1TOTGraph(histPt2Inter);
                    outputFile->cd();
                    // Save the TGraphs
                    Pt2Distribution->Write(Form("Pt2_Distribution_%s_%i%i%i_%i", targetArr,
                                                Q2Counter, NuCounter, ZhCounter, nPion));
                    Pt2DistributionClean->Write(Form("Pt2_Distribution_Clean_%s_%i%i%i_%i",
                                                     targetArr, Q2Counter, NuCounter,
                                                     ZhCounter, nPion));
                    Pt2DistributionInter->Write(Form("Pt2_Distribution_Inter_%s_%i%i%i_%i",
                                                     targetArr, Q2Counter, NuCounter,
                                                     ZhCounter, nPion));
                    gROOT->cd();

                    delete histPt2;
                    delete histPt2Clean;
                    delete histPt2Inter;
                }
            }
        } // End Zh loop
    }     // End number pion event loop

    t.Print();
    return 0;
}
