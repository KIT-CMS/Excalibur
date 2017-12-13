void wristehist(){
    /*h->GetYaxis()->GetBinCenter(j)
    2016B: [-2.250 <eta< -1.930, 2.200<phi<2.500]
    2016C: [-3.489 <eta< -3.139, 2.237<phi<2.475]
    2016D: [-3.600 <eta< -3.139, 2.237<phi<2.475] */

    double binx[4]={-5.2,-2.25,-1.93,5.2};
    double biny[4]={-3.141,2.2,2.5,3.141};
    TFile* f = new TFile("hcal-legacy-runB.root","RECREATE");
    
    /*double binx[4]={-5.2,-3.489,-3.139,5.2};
    double biny[4]={-3.141,2.237,2.475,3.141};
    TFile* f = new TFile("hcal-legacy-runC.root","RECREATE");*/
    
    /*double binx[4]={-5.2,-3.6,-3.139,5.2};
    double biny[4]={-3.141,2.237,2.475,3.141};
    TFile* f = new TFile("hcal-legacy-runD.root","RECREATE");*/
    
    TH2D *h = new TH2D("h2jet","cleaninghist",3,binx,3,biny);
    //TH2D *h = new TH2D("h2jet","cleaninghist",100,-5.2,5.2,100,-3.141,3.141);
    for (int i=0; i<=h->GetNbinsX(); i++){
        for (int j=0; j<=h->GetNbinsY(); j++){
            (i==2 && j==2)
            ? h->SetBinContent(i,j,10)
            : h->SetBinContent(i,j,-10);
        }
    }
    h->Write();
    f->Close();
    
}
