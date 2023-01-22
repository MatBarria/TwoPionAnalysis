// g++ -Wall -fPIC -I./include `root-config --cflags` Percentaje_Rc.cpp -o ./bin/Percentaje_Rc  `root-config --glibs` ./include/Broad_Rc.h 


#include <iostream>
#include "TFile.h"
#include "TNtuple.h"
#include "Broad_Rc.h"
#include "TH1F.h"


int main() {

    TFile* fileStandar = new TFile(inputDirectory + "Pt_broad_hist_Zh.root", "READ");
    TFile* fileCompare = new TFile(inputDirectory + "Pt_broad_hist_Zh_Rc.root",   "READ");


    TH1F *standarHist[3][3], *compareHist[3][3], *sustracHist[3][3], *divideHist[3][3];
    for(int i = 0; i < 2 ; i++) {
        standarHist[0][i] = (TH1F*) fileStandar->Get(Form("PtBroad_Zh_C_%i",  i+1));
        standarHist[1][i] = (TH1F*) fileStandar->Get(Form("PtBroad_Zh_Fe_%i", i+1));
        standarHist[2][i] = (TH1F*) fileStandar->Get(Form("PtBroad_Zh_Pb_%i", i+1));
        compareHist[0][i] = (TH1F*) fileCompare->Get(Form("PtBroad_Zh_C_%i",  i+1));
        compareHist[1][i] = (TH1F*) fileCompare->Get(Form("PtBroad_Zh_Fe_%i", i+1));
        compareHist[2][i] = (TH1F*) fileCompare->Get(Form("PtBroad_Zh_Pb_%i", i+1));
    }

    TGraphErrors* graphs[3][3];

    float binValue;
    TFile* outputFile = new TFile(outputDirectory + "Percentaje_Rc.root", "RECREATE"); 
    gROOT->cd();
    for(int i = 0; i < N_STARGETS; i++) {
        for(int j = 0; j < N_PION; j++) {
            sustracHist[i][j] = new TH1F(Form("Sustrac%i%i", i, j), "", N_Zh, Zh_BINS);
            sustracHist[i][j]->Add(standarHist[i][j], compareHist[i][j], 1, -1);

            for(int ZhCounter = 1; ZhCounter <= N_Zh; ZhCounter++) {
                binValue = sustracHist[i][j]->GetBinContent(ZhCounter);
                sustracHist[i][j]->SetBinContent(ZhCounter, TMath::Abs(binValue));
            }

            divideHist[i][j] = new TH1F(Form("Divide%i%i", i, j), "", N_Zh, Zh_BINS);
            divideHist[i][j]->Divide(sustracHist[i][j], standarHist[i][j]);

            std::cout << "The percentaje of different is " << std::endl;
            std::cout << "For " << i << " target and " << j + 1 << "number of pion" << std::endl;
            for(int ZhCounter = 1; ZhCounter <= N_Zh; ZhCounter++) {
                std::cout << "Zh Bin" << ZhCounter << ": " << 
                    divideHist[i][j]->GetBinContent(ZhCounter)*100 << "%, " ;
                std::cout << std::endl;
            }

            graphs[i][j] = TH1TOTGraph(divideHist[i][j]);
            outputFile->cd();
            if(i == 0) { graphs[i][j]->Write(Form("Percentaje_C_%i",  j+1)); }
            if(i == 1) { graphs[i][j]->Write(Form("Percentaje_Fe_%i", j+1)); }
            if(i == 2) { graphs[i][j]->Write(Form("Percentaje_Pb_%i", j+1)); }
            gROOT->cd();
        }
    }

    outputFile->Close();
    fileStandar->Close();
    fileCompare->Close();

    return 0;
}
