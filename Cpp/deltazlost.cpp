void deltazlost() {

  TFile* noCut = new TFile("/home/matias/proyecto/Pt2Broadening_multi-pion/Data/VecSum_Pb2.root", "READ");
  TFile* Cut   = new TFile("/home/matias/proyecto/Pt2Broadening_multi-pion/Data/VecSum_PbdeltaZ.root", "READ");

  TNtuple* tupleNoCut[3];
  TNtuple* tupleCut[3];

  for(int i = 1; i < 4; i++) {
    tupleNoCut[i-1] = (TNtuple*) noCut->Get(Form("ntuple_%i_pion", i));
    tupleCut[i-1]   = (TNtuple*) Cut->Get(Form("ntuple_%i_pion", i));
  }
  float percentaje;

  for(int i = 0; i < 3; i++) {
      percentaje = ((tupleNoCut[i]->GetEntries() - tupleCut[i]->GetEntries())*100.0)/tupleNoCut[i]->GetEntries();
      std::cout << "para " << i +1 << " se perdio el " << percentaje << " Porciento" << std::endl;
  }

}
