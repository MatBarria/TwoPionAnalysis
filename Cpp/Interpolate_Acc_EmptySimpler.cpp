// g++ -Wall -fPIC -I../include `root-config --cflags` Interpolate_Acc_EmptySimpler.cpp -o
// ../bin/Interpolate_Acc_Empty `root-config --glibs` ../include/Binning.h

#include "Binning.h"
#include "TFile.h"
#include "TH1F.h"
#include "TMath.h"
#include "TROOT.h"
#include "TString.h"
#include <iostream>

int ApplyInterpolateFactors(std::string target, TFile *fileData, TFile *fileInterFactors,
                            TFile *fileDataCorr);

int CallInterpolationFactors(std::string target, TFile *fileData, TFile *fileFactors,
                             TFile *fileInterFactors);

int SetEmptyHistogram(TH1F *hist);

int SetArrayValuesEqualZero(double (&array)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi],
                            double (&errorArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi], int Q2bin,
                            int NuBin, int ZhBin, int Pt2Bin);

int FindEmptyBins(std::string target, int nPion, TFile *fileData, TFile *fileFactors,
                  double (&accArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi],
                  double (&accErrArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi]);

int InterpolateFactors(double (&accArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi],
                       double (&accErrArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi]);

int FindValidNeighbors(int Q2Bin, int NuBin, int ZhBin, int Pt2Bin, int PhiBin,
                       double (&accArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi],
                       double (&accErrArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi],
                       double (&AccNei)[N_VARS][2], double (&AccErrNei)[N_VARS][2]);

int SaveInterporaltedFactors(std::string target, int nPion, TFile *fileInterFactors,
                             double (&accArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi],
                             double (&accErrArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi]);

template <typename Function, typename... Args>
void LoopFunctions4Dimension(Function func, Args &...args) {

    for (int Q2Bin = 0; Q2Bin < N_Q2; Q2Bin++) {                 // Loops Q2 bins
        for (int NuBin = 0; NuBin < N_Nu; NuBin++) {             // Loops Nu bins
            for (int ZhBin = 0; ZhBin < N_Zh; ZhBin++) {         // Loops Zh bins;
                for (int Pt2Bin = 0; Pt2Bin < N_Pt2; Pt2Bin++) { // Pt2 bins;
                    func(args..., Q2Bin, NuBin, ZhBin, Pt2Bin);
                }
            }
        }
    }
}

const double NO_DATA = -1;

int main() {

    TFile *fileData = new TFile(inputDirectory + "corr_data_Phi.root", "READ");
    TFile *fileFactors = new TFile(inputDirectory + "corr_data_Phi.root", "READ");
    TFile *fileInterFactors = new TFile(outputDirectory + "AccInter.root", "RECREATE");
    TFile *fileDataCorr = new TFile(outputDirectory + "corr_data_Phi_Inter.root", "RECREATE");
    gROOT->cd();

    std::cout << inputDirectory + "corr_data_Phi.root" << std::endl;

    const char *Targets[2 * N_STARGETS] = {"C", "Fe", "Pb", "DC", "DFe", "DPb"};

    for (int i = 0; i < 2 * N_STARGETS; i++) {

        std::cout << "Interpolating " << Targets[i] << " ";
        CallInterpolationFactors(Targets[i], fileData, fileFactors, fileInterFactors);
    }

    fileFactors->Close();
    fileInterFactors->Close();
    delete fileInterFactors;

    TFile *fileAccInterRead = new TFile(outputDirectory + "AccInter.root", "READ");

    for (int i = 0; i < 2 * N_STARGETS; i++) {

        std::cout << "Applying Acc Interpolated " << Targets[i] << "\n";
        ApplyInterpolateFactors(Targets[i], fileData, fileAccInterRead, fileDataCorr);
    }

    fileData->Close();
    fileAccInterRead->Close();
    fileDataCorr->Close();
    return 0;
}

int CallInterpolationFactors(std::string target, TFile *fileData, TFile *fileFactors,
                             TFile *fileInterFactors) {

    std::cout << "Start" << std::endl;

    double accArray[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi];
    double accErrArray[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi];

    for (int nPion = 1; nPion <= N_PION; nPion++) { // Loops number of pions

        std::cout << "Number of pion: " << nPion << std::endl;

        // SetArrayValuesEqualZero(accArray, accErrArray);
        LoopFunctions4Dimension(SetArrayValuesEqualZero, accArray, accErrArray);
        FindEmptyBins(target, nPion, fileData, fileFactors, accArray, accErrArray);
        InterpolateFactors(accArray, accErrArray);
        SaveInterporaltedFactors(target, nPion, fileInterFactors, accArray, accErrArray);

    } // End Number of pions Loop

    return 0;
}

int SetEmptyHistogram(TH1F *hist) {

    for (int i = 1; i <= N_Phi; i++) {
        hist->SetBinContent(i, 0);
        hist->SetBinError(i, 0);
    }

    return 0;
}

int SetArrayValuesEqualZero(double (&array)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi],
                            double (&errorArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi], int Q2Bin,
                            int NuBin, int ZhBin, int Pt2Bin) {
    for (int PhiBin = 0; PhiBin < N_Phi; PhiBin++) {
        array[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin] = NO_DATA;
        errorArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin] = NO_DATA;
    }

    return 0;
}

int FindEmptyBins(std::string target, int nPion, TFile *fileData, TFile *fileFactors,
                  double (&accArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi],
                  double (&accErrArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi]) {

    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());

    for (int Q2Bin = 0; Q2Bin < N_Q2; Q2Bin++) {                 // Loops Q2 bins
        for (int NuBin = 0; NuBin < N_Nu; NuBin++) {             // Loops Nu bins
            for (int ZhBin = 0; ZhBin < N_Zh; ZhBin++) {         // Loops Zh bins;
                for (int Pt2Bin = 0; Pt2Bin < N_Pt2; Pt2Bin++) { // Pt2 bins;

                    TH1F *histData = (TH1F *)fileData->Get(Form(
                        "Data_%s_%i%i%i%i_%i", targetArr, Q2Bin, NuBin, ZhBin, Pt2Bin, nPion));

                    if (histData == NULL) {
                        // histData = new TH1F(Form("Data_%s_%i%i%i%i_%i", targetArr, Q2Bin,
                        // NuBin, ZhBin, Pt2Bin, nPion),
                        //"", N_Phi, -180, 180);
                        // SetEmptyHistogram(histData);
                        delete histData;
                        continue;
                    }

                    TH1F *hist =
                        (TH1F *)fileFactors->Get(Form("FinalFactor_%s_%i%i%i%i_%i", targetArr,
                                                      Q2Bin, NuBin, ZhBin, Pt2Bin, nPion));

                    // TH1F *hist = (TH1F*) fileData->Get(Form("AccFactor_%s_%i%i%i%i_%i",
                    // targetArr, Q2Bin, NuBin, ZhBin, Pt2Bin, nPion));

                    // TH1F *hist = new TH1F("FinalFactor", "", N_Phi, -180, 180);
                    // TH1F *histAcc =
                    //(TH1F *)fileData->Get(Form("AccFactor_%s_%i%i%i%i_%i", targetArr,
                    // Q2Bin, NuBin, ZhBin, Pt2Bin, nPion));
                    // TH1F *histFal =
                    //(TH1F *)fileData->Get(Form("FalPosFactor_%s_%i%i%i%i_%i", targetArr,
                    // Q2Bin, NuBin, ZhBin, Pt2Bin, nPion));

                    // if (histAcc == NULL || histFal == NULL) {
                    // hist = new TH1F(Form("FinalFactor_%s_%i%i%i%i_%i", targetArr, Q2Bin,
                    // NuBin, ZhBin, Pt2Bin, nPion),
                    //"", N_Phi, -180, 180);
                    // SetEmptyHistogram(hist);
                    //} else {
                    // hist->Divide(histAcc, histFal, 1, 1);
                    //}

                    if (hist == NULL) {
                        // std::cout << "Bin: " << Q2Bin << NuBin << ZhBin << Pt2Bin <<
                        // std::endl;
                        hist = new TH1F(Form("FinalFactor_%s_%i%i%i%i_%i", targetArr, Q2Bin,
                                             NuBin, ZhBin, Pt2Bin, nPion),
                                        "", N_Phi, -180, 180);
                        SetEmptyHistogram(hist);
                    }

                    for (int PhiBin = 1; PhiBin <= N_Phi; PhiBin++) {

                        if (histData->GetBinContent(PhiBin) != 0) {

                            if (hist->GetBinContent(PhiBin) <= 1) {
                                accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin - 1] =
                                    hist->GetBinContent(PhiBin);
                                accErrArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin - 1] =
                                    hist->GetBinError(PhiBin);
                                continue;
                            } else {
                                accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin - 1] = 0;
                                accErrArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin - 1] = 0;
                                continue;
                            }
                        } else {
                            accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin - 1] = NO_DATA;
                            accErrArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin - 1] = NO_DATA;
                        }
                    }

                    delete hist;
                    delete histData;

                    // delete histAcc;
                    //  delete histFal;

                } // End Pt2 Loop
            }     // End ZhBin Loop
        }         // End Nu Loop
    }             // End Q2Bin Loop

    return 0;
}

int InterpolateFactors(double (&accArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi],
                       double (&accErrArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi]) {

    int nInterpolatedBins = 0;
    double Acc, AccErr, AccSum, AccErrSum;
    double AccNei[N_VARS][2];
    double AccErrNei[N_VARS][2];
    int counter;
    Acc = 0;
    AccErr = 0;

    for (int Q2Bin = 0; Q2Bin < N_Q2; Q2Bin++) {                 // Loops Q2 bins
        for (int NuBin = 0; NuBin < N_Nu; NuBin++) {             // Loops Nu bins
            for (int ZhBin = 0; ZhBin < N_Zh; ZhBin++) {         // Loops Zh bins;
                for (int Pt2Bin = 0; Pt2Bin < N_Pt2; Pt2Bin++) { // Pt2 bins;
                    for (int PhiBin = 0; PhiBin < N_Phi; PhiBin++) {

                        for (int i = 0; i < N_VARS; i++) {
                            AccNei[i][0] = 0;
                            AccErrNei[i][0] = 0;
                            AccNei[i][1] = 0;
                            AccErrNei[i][1] = 0;
                        }

                        if (accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin] == NO_DATA ||
                            accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin] != 0)
                            continue;

                        nInterpolatedBins++;

                        FindValidNeighbors(Q2Bin, NuBin, ZhBin, Pt2Bin, PhiBin, accArray,
                                           accErrArray, AccNei, AccErrNei);
                        // for (int i = 0; i < N_VARS; i++) {
                        // std::cout << AccNei[i][0] << " & " << AccNei[i][1] << " & ";
                        //}
                        // std::cout << std::endl;

                        counter = 0;
                        AccSum = 0;
                        AccErrSum = 0;

                        for (int var = 0; var < N_VARS; var++) {
                            for (int nei = 0; nei < 2; nei++) {

                                if (AccNei[var][nei] != 0 && AccNei[var][nei] != NO_DATA) {
                                    AccSum += AccNei[var][nei];
                                    AccErrSum += AccErrNei[var][nei];
                                    counter++;
                                }
                            }
                        }

                        if (counter == 0) {
                            accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin] = Acc;
                            accErrArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin] = AccErr;
                        } else {
                            Acc = AccSum / counter;
                            AccErr = AccErrSum / counter;
                            accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin] = Acc;
                            accErrArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin] = AccErr;
                            if (!TMath::Finite(Acc))
                                std::cout << "Acc Is Inf for Bin: "
                                          << " - " << Q2Bin << NuBin << ZhBin << Pt2Bin
                                          << PhiBin << " Value: " << Acc << std::endl;
                        }
                    }
                }
            }
        }
    }

    std::cout << "Interpolated Bins: " << nInterpolatedBins << std::endl;
    return 0;
}

int FindValidNeighbors(int Q2Bin, int NuBin, int ZhBin, int Pt2Bin, int PhiBin,
                       double (&accArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi],
                       double (&accErrArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi],
                       double (&AccNei)[N_VARS][2], double (&AccErrNei)[N_VARS][2]) {

    // Skip the factor in the border bins
    if (Q2Bin != 0) {
        AccNei[0][0] = accArray[Q2Bin - 1][NuBin][ZhBin][Pt2Bin][PhiBin];
        AccErrNei[0][0] = accErrArray[Q2Bin - 1][NuBin][ZhBin][Pt2Bin][PhiBin];
    }

    if (Q2Bin != N_Q2 - 1) {
        AccNei[0][1] = accArray[Q2Bin + 1][NuBin][ZhBin][Pt2Bin][PhiBin];
        AccErrNei[0][1] = accErrArray[Q2Bin + 1][NuBin][ZhBin][Pt2Bin][PhiBin];
    }

    if (NuBin != 0) {
        AccNei[1][0] = accArray[Q2Bin][NuBin - 1][ZhBin][Pt2Bin][PhiBin];
        AccErrNei[1][0] = accErrArray[Q2Bin][NuBin - 1][ZhBin][Pt2Bin][PhiBin];
    }

    if (NuBin != N_Nu - 1) {
        AccNei[1][1] = accArray[Q2Bin][NuBin + 1][ZhBin][Pt2Bin][PhiBin];
        AccErrNei[1][1] = accErrArray[Q2Bin][NuBin + 1][ZhBin][Pt2Bin][PhiBin];
    }

    if (ZhBin != 0) {
        AccNei[2][0] = accArray[Q2Bin][NuBin][ZhBin - 1][Pt2Bin][PhiBin];
        AccErrNei[2][0] = accErrArray[Q2Bin][NuBin][ZhBin - 1][Pt2Bin][PhiBin];
    }

    if (ZhBin != N_Zh - 1) {
        AccNei[2][1] = accArray[Q2Bin][NuBin][ZhBin + 1][Pt2Bin][PhiBin];
        AccErrNei[2][1] = accErrArray[Q2Bin][NuBin][ZhBin + 1][Pt2Bin][PhiBin];
    }

    if (Pt2Bin != 0) {
        AccNei[3][0] = accArray[Q2Bin][NuBin][ZhBin][Pt2Bin - 1][PhiBin];
        AccErrNei[3][0] = accErrArray[Q2Bin][NuBin][ZhBin][Pt2Bin - 1][PhiBin];
    }

    if (Pt2Bin != N_Pt2 - 1) {
        AccNei[3][1] = accArray[Q2Bin][NuBin][ZhBin][Pt2Bin + 1][PhiBin];
        AccErrNei[3][1] = accErrArray[Q2Bin][NuBin][ZhBin][Pt2Bin + 1][PhiBin];
    }

    if (PhiBin != 0) {
        AccNei[4][0] = accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin - 1];
        AccNei[4][0] = accErrArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin - 1];
    }

    if (PhiBin != N_Phi - 1) {
        AccNei[4][1] = accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin + 1];
        AccErrNei[4][1] = accErrArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin + 1];
    }

    return 0;
}

int SaveInterporaltedFactors(std::string target, int nPion, TFile *fileInterFactors,
                             double (&accArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi],
                             double (&accErrArray)[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi]) {

    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());

    TH1F *histSave = new TH1F("histSave", "", N_Phi, -180, 180);

    for (int Q2Bin = 0; Q2Bin < N_Q2; Q2Bin++) {                 // Loops Q2 bins
        for (int NuBin = 0; NuBin < N_Nu; NuBin++) {             // Loops Nu bins
            for (int ZhBin = 0; ZhBin < N_Zh; ZhBin++) {         // Loops Zh bins;
                for (int Pt2Bin = 0; Pt2Bin < N_Pt2; Pt2Bin++) { // Pt2 bins;

                    int counterNoData = 0;
                    for (int PhiBin = 0; PhiBin < N_Phi; PhiBin++) {

                        if (accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin] == NO_DATA) {
                            counterNoData++;
                        }
                    }
                    if (counterNoData == N_Phi) {
                        continue;
                    }

                    for (int PhiBin = 0; PhiBin < N_Phi; PhiBin++) {

                        if (accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin] == NO_DATA ||
                            accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin] == 0) {

                            histSave->SetBinContent(PhiBin + 1, 0);
                            histSave->SetBinError(PhiBin + 1, 0);

                        } else {

                            histSave->SetBinContent(
                                PhiBin + 1, accArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin]);
                            histSave->SetBinError(
                                PhiBin + 1, accErrArray[Q2Bin][NuBin][ZhBin][Pt2Bin][PhiBin]);
                        }
                    }

                    fileInterFactors->cd();
                    histSave->Write(Form("FinalFactor_%s_%i%i%i%i_%i", targetArr, Q2Bin, NuBin,
                                         ZhBin, Pt2Bin, nPion));
                    gROOT->cd();
                    histSave->Reset();
                }
            }
        }
    }

    delete histSave;
    return 0;
}

int ApplyInterpolateFactors(std::string target, TFile *fileData, TFile *fileInterFactors,
                            TFile *fileDataCorr) {

    std::cout << "Start" << std::endl;

    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());
    TH1F *histDataCorr = new TH1F("DataCorr2", "", N_Phi, -180, 180);

    for (int nPion = 1; nPion <= N_PION; nPion++) { // Loops number of pions

        for (int Q2Bin = 0; Q2Bin < N_Q2; Q2Bin++) {                 // Loops Q2 bins
            for (int NuBin = 0; NuBin < N_Nu; NuBin++) {             // Loops Nu bins
                for (int ZhBin = 0; ZhBin < N_Zh; ZhBin++) {         // Loops Zh bins;
                    for (int Pt2Bin = 0; Pt2Bin < N_Pt2; Pt2Bin++) { // Pt2 bins;

                        TH1F *histData =
                            (TH1F *)fileData->Get(Form("Data_%s_%i%i%i%i_%i", targetArr, Q2Bin,
                                                       NuBin, ZhBin, Pt2Bin, nPion));

                        if (histData == NULL) {
                            delete histData;
                            continue;
                        }

                        TH1F *hist = (TH1F *)fileInterFactors->Get(
                            Form("FinalFactor_%s_%i%i%i%i_%i", targetArr, Q2Bin, NuBin, ZhBin,
                                 Pt2Bin, nPion));

                        histDataCorr->Divide(histData, hist, 1, 1);
                        fileDataCorr->cd();

                        histData->Write(Form("Data_%s_%i%i%i%i_%i", targetArr, Q2Bin, NuBin,
                                             ZhBin, Pt2Bin, nPion));
                        histDataCorr->Write(Form("DataCorr2_%s_%i%i%i%i_%i", targetArr, Q2Bin,
                                                 NuBin, ZhBin, Pt2Bin, nPion));
                        hist->Write(Form("FinalFactor_%s_%i%i%i%i_%i", targetArr, Q2Bin, NuBin,
                                         ZhBin, Pt2Bin, nPion));

                        gROOT->cd();

                        histDataCorr->Reset();
                        delete hist;
                        delete histData;
                    }
                }
            }
        }
    }

    delete histDataCorr;
    return 0;
}
