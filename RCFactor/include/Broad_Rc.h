#include "Binning_Rc.h"
#include "TStopwatch.h"
#include <iostream>
#include "TMath.h"
#include "TString.h"
#include "TFile.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TGraphErrors.h"
#include "TMultiGraph.h"

TGraphErrors* TH1TOTGraph(TH1 *h1) {

    TGraphErrors* g1= new TGraphErrors();

    if(!h1) {
        std::cout << "TH1TOTGraph: histogram not found !" << std::endl;
        return g1;
    }

    Double_t x, y, ex, ey;
    for (Int_t i = 1; i <= h1->GetNbinsX(); i++) {
        y = h1->GetBinContent(i);
        ey = h1->GetBinError(i);
        x = h1->GetBinCenter(i);
        // ex=h1->GetBinWidth(i);
        ex = 0.5*h1->GetBinWidth(i);
        g1->SetPoint(i-1, x, y);
        g1->SetPointError(i-1, ex, ey);
    }
    return g1;

}


// Calculate the Pt broadening and plot in funcion of the size of the target
void PtBroadeningFullIntegrated(TString inputDirectory, TString plotDirectory) {

    TFile* inputFile = new TFile(inputDirectory + "meanPt2_Rc.root", "READ");

    TGraphErrors* g[N_STARGETS][N_PION];

    for(int nPion = 1; nPion <= N_PION; nPion++) {

        TH1F* histSolid[N_STARGETS]; TH1F* histLiquid[N_STARGETS]; 
        TH1F* histBroadening[N_STARGETS];

        histSolid[0]  = (TH1F*) inputFile->Get(Form("meanPt2_C_%i",   nPion));
        histSolid[1]  = (TH1F*) inputFile->Get(Form("meanPt2_Fe_%i",  nPion));
        histSolid[2]  = (TH1F*) inputFile->Get(Form("meanPt2_Pb_%i",  nPion));

        histLiquid[0] = (TH1F*) inputFile->Get(Form("meanPt2_DC_%i",  nPion));
        histLiquid[1] = (TH1F*) inputFile->Get(Form("meanPt2_DFe_%i", nPion));
        histLiquid[2] = (TH1F*) inputFile->Get(Form("meanPt2_DPb_%i", nPion));

        for(int i = 0 ; i < N_STARGETS ; i++) {
            //Calculate the Broadening (subtract of the means)
            histBroadening[i] = new TH1F(Form("histBroadening_%i", i), "", 1, Zh_MIN, Zh_MAX);
            histBroadening[i]->Add(histSolid[i], histLiquid[i], 1, -1);
        }

        // Set the points in TGraphErrors
        g[0][nPion-1] = new TGraphErrors();
        g[0][nPion-1]->SetPoint(1, TMath::Power(12.01,1./3.), histBroadening[0]->GetBinContent(1));
        g[0][nPion-1]->SetPointError(1, 0, histBroadening[0]->GetBinError(1));

        g[1][nPion-1] = new TGraphErrors();
        g[1][nPion-1]->SetPoint(1, TMath::Power(55.845,1./3.), histBroadening[1]->GetBinContent(1));
        g[1][nPion-1]->SetPointError(1, 0,histBroadening[1]->GetBinError(1));

        g[2][nPion-1] = new TGraphErrors();
        g[2][nPion-1]->SetPoint(1, TMath::Power(207.2,1./3.), histBroadening[2]->GetBinContent(1));
        g[2][nPion-1]->SetPointError(1, 0, histBroadening[2]->GetBinError(1));

        for(int i = 0; i < N_STARGETS; i++) {
            delete histSolid[i];
            delete histLiquid[i];
            delete histBroadening[i];
        }
    } // End number pion event loop
    inputFile->Close();

    TFile* outputFile = new TFile(inputDirectory + "Pt_broad_FullIntegrated_Rc.root", "RECREATE");

    outputFile->cd();

    for(int i = 0; i < N_STARGETS; i++){
        for(int j = 0; j < N_PION; j++) {
            if(i == 0) { g[i][j]->Write(Form("PtBroad_FullIntegrated_C_%i" , j+1)); };
            if(i == 1) { g[i][j]->Write(Form("PtBroad_FullIntegrated_Fe_%i", j+1)); };
            if(i == 2) { g[i][j]->Write(Form("PtBroad_FullIntegrated_Pb_%i", j+1)); };
        }
    }

    outputFile->Close();

}

void PtBroadeningZh(TString inputDirectory, TString outputDirectory) {

    TFile* inputFile  = new TFile(inputDirectory + "meanPt2_Zh_processed_Rc.root", "READ");
    TFile* outputFileHist = new TFile(outputDirectory + "Pt_broad_hist_Zh_Rc.root", "RECREATE");
    gROOT->cd();
    TGraphErrors* g[N_STARGETS][N_PION];

    TString meanPt2;
    for(int nPion = 1; nPion <= N_PION; nPion++) { // Loops in every number of pion
        TH1F* histSolid[N_STARGETS];   TH1F* histLiquid[N_STARGETS]; 
        TH1F* histBroadening[N_STARGETS];

        if(UseCutOff == 1) { meanPt2 = "meanPt2_%s_%i_interpolated"; }
        if(UseCutOff == 2) { meanPt2 = "meanPt2_%s_%i_clean"; }
        if(UseCutOff == 3) { meanPt2 = "meanPt2_%s_%i"; }

        //C
        histSolid[0]  = (TH1F*) inputFile->Get(Form(meanPt2, C,   nPion));
        histLiquid[0] = (TH1F*) inputFile->Get(Form(meanPt2, DC,  nPion));
        //Fe
        histSolid[1]  = (TH1F*) inputFile->Get(Form(meanPt2, Fe,  nPion));
        histLiquid[1] = (TH1F*) inputFile->Get(Form(meanPt2, DFe, nPion));
        //Pb
        histSolid[2]  = (TH1F*) inputFile->Get(Form(meanPt2, Pb,  nPion));
        histLiquid[2] = (TH1F*) inputFile->Get(Form(meanPt2, DPb, nPion));


        for(int i = 0 ; i < N_STARGETS ; i++){
            histBroadening[i] = new TH1F(Form("histBroadening_%i",i), "", N_Zh, Zh_BINS);
            histBroadening[i]->Add(histSolid[i], histLiquid[i], 1, -1);

            outputFileHist->cd();
            if(i == 0) { histBroadening[i]->Write(Form("PtBroad_Zh_C_%i",  nPion)); };
            if(i == 1) { histBroadening[i]->Write(Form("PtBroad_Zh_Fe_%i", nPion)); };
            if(i == 2) { histBroadening[i]->Write(Form("PtBroad_Zh_Pb_%i", nPion)); };
            gROOT->cd();

            g[i][nPion-1] = (TGraphErrors*) TH1TOTGraph(histBroadening[i]);
            //SetErrorXNull(g[i][nPion-1], nBins);

            delete histSolid[i];
            delete histLiquid[i];
            delete histBroadening[i];
        }
    } // End number pion event loop

    inputFile->Close();
    outputFileHist->Close();

    TFile* outputFile = new TFile(outputDirectory + "Pt_broad_Zh_Rc.root", "RECREATE");

    outputFile->cd();

    for(int i = 0; i < N_STARGETS; i++){
        for(int j = 0; j < N_PION; j++) {
            if(i == 0) { g[i][j]->Write(Form("PtBroad_Zh_C_%i", j)); };
            if(i == 1) { g[i][j]->Write(Form("PtBroad_Zh_Fe_%i", j)); };
            if(i == 2) { g[i][j]->Write(Form("PtBroad_Zh_Pb_%i", j)); };
        }
    }

    outputFile->Close();

}
