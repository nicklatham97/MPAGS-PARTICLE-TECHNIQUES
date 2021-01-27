#define MyClass_cxx
#include "MyClass.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

// To run:
// root -l                   # Load ROOT
// .L MyClass2.C              # Load MyClass.C
// MyClass a; a.Loop()       # Define MyClass to a and run loop

double ECEnergy;
double HCEnergy;
vector<double>  *vx1 = 0;
vector<double>  *vy1 = 0;
vector<double>  *vz1 = 0;
vector<double>  *vx2 = 0;
vector<double>  *vy2 = 0;
vector<double>  *vz2 = 0;

void MyClass::Loop()
{
TFile *myfile= TFile::Open("B5_mu+.root");
TTree *tree= (TTree*) myfile->Get("B5");
tree->SetBranchAddress("ECEnergy", &ECEnergy);
tree->SetBranchAddress("HCEnergy", &HCEnergy);
tree->SetBranchAddress("Dc1HitsVector_x", &vx1);
tree->SetBranchAddress("Dc1HitsVector_y", &vy1);
tree->SetBranchAddress("Dc1HitsVector_z", &vz1);
tree->SetBranchAddress("Dc2HitsVector_x", &vx2);
tree->SetBranchAddress("Dc2HitsVector_y", &vy2);
tree->SetBranchAddress("Dc2HitsVector_z", &vz2);

   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();
   TH1F *h1 = new TH1F("h1","ECEnergy;Energy Deposited (MeV);Frequency",100,0,1000);
   TGraphErrors* tg1 = new TGraphErrors();
   TGraphErrors* tg2 = new TGraphErrors();
   TCanvas* c = new TCanvas();

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      h1->Fill(ECEnergy);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      GetEntry(jentry);
   }
   for (int i = 0; i < tree->GetEntries(); ++i){
      tree->GetEntry(i);
   }
   for (int j = 0; j < vx1->size(); ++j){
      tg1->SetPoint(j, vz1->at(j), vx1->at(j));
      tg2->SetPoint(j, vz2->at(j), vx2->at(j));
   }

  h1->Draw();
  c->Update();
  c->Modified();
  c->Print("ECEnergyHist.pdf");

  TMultiGraph* m1 = new TMultiGraph();
  tg1->SetLineColor(kBlue);
  tg2->SetLineColor(kRed);
  m1->SetTitle("Trajectory in xz-plane;z;x");
  m1->Add(tg1);
  m1->Add(tg2); 
  m1->Draw("a fb l3d");

  c->Update();
  c->Modified();
  c->Print("Trajectory1.pdf");
}
