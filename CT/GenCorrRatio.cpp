// g++ -Wall -fPIC -I../include `root-config --cflags` GenCorrRatio.cpp -o ../bin/GenCorrRatio `root-config --glibs` ../include/Broad.h

#include "Broad.h"

int main() {

  TString CTDirectory = "/home/matias/proyecto/TwoPionAnalysis/Data/CT/";
  TFile* inputFileAcc  = new TFile(CTDirectory + "Pt_broad_hist_Zh_Corr.root", "READ");
  TFile* inputFileData = new TFile(CTDirectory + "Pt_broad_hist_Zh_Gen.root",  "READ");

  TGraphErrors* g[N_STARGETS][N_PION];

  for(int nPion = 1; nPion <= N_PION; nPion++) { // Loops in every number of pion

    TH1F* histBroadening[N_STARGETS], *histBroadeningData[N_STARGETS], *histRatio[N_STARGETS];

    //C
    histBroadening[0]  = (TH1F*) inputFileAcc->Get(Form("PtBroad_Zh_C_%i", nPion));
    //Fe
    histBroadening[1]  = (TH1F*) inputFileAcc->Get(Form("PtBroad_Zh_Fe_%i", nPion));
    //Pb
    histBroadening[2]  = (TH1F*) inputFileAcc->Get(Form("PtBroad_Zh_Pb_%i", nPion));

    //C
    histBroadeningData[0]  = (TH1F*) inputFileData->Get(Form("PtBroad_Zh_C_%i",  nPion));
    //Fe
    histBroadeningData[1]  = (TH1F*) inputFileData->Get(Form("PtBroad_Zh_Fe_%i", nPion));
    //Pb
    histBroadeningData[2]  = (TH1F*) inputFileData->Get(Form("PtBroad_Zh_Pb_%i", nPion));


    for(int i = 0 ; i < N_STARGETS ; i++) {
      histRatio[i] = new TH1F(Form("histRatio_%i", i), "", N_Zh, Zh_BINS);
      histRatio[i]->Divide(histBroadeningData[i], histBroadening[i],  1, 1);
      g[i][nPion-1] = (TGraphErrors*) TH1TOTGraph(histRatio[i]);
      delete histRatio[i];
    }


  } // End number pion event loop

  TFile* outputFile = new TFile(CTDirectory + "Pt_broad_Zh_RatioGenCorr.root", "RECREATE");

  outputFile->cd();

  for(int i = 0; i < N_STARGETS; i++){
    for(int j = 0; j < N_PION; j++) {
      if(i == 0) { g[i][j]->Write(Form("PtBroad_Zh_C_RatioGenCorr%i",  j)); };
      if(i == 1) { g[i][j]->Write(Form("PtBroad_Zh_Fe_RatioGenCorr%i", j)); };
      if(i == 2) { g[i][j]->Write(Form("PtBroad_Zh_Pb_RatioGenCorr%i", j)); };
    }
  }

  gROOT->cd();
  outputFile->Close();
  inputFileData->Close();
  inputFileAcc->Close();

}
