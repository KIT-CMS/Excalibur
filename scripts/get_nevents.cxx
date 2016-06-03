
void nevents(){
	double integral = 0;
	std::vector<std::string> files;
	int n;
	ifstream inf("filelist.txt");
         while (inf){
        // read stuff from the file into a string and print it
        	std::string strInput;
        	inf >> strInput;
		files.push_back(strInput);
    	}
	for (int i = 0; i < files.size()-1; i++){
		TFile* f = new TFile(files[i].c_str());
		//TFile* f = new TFile("/storage/a/cheidecker/cmssw807_calo_noPUJetID/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7_job_995_skim80.root");
		//std::cout << files[i] << std::endl;
		TTree *tree = (TTree*)f->Get("Lumis");
		tree->Draw("nEventsTotal>>histo","", "goff");
		TH1F *histo = (TH1F*)gDirectory->Get("histo");
		n = histo->GetNbinsX();
		for (int j = 0; j < n; j++)
			integral += histo->GetBinContent(j)*histo->GetBinCenter(j);
		f->Close();
		delete f;
	}
	std::cout.setf(ios::fixed);
	std::cout << setprecision(0) << integral << std::endl;
}
//"/storage/a/cheidecker/cmssw807_calo_noPUJetID/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7_job_995_skim80.root"
