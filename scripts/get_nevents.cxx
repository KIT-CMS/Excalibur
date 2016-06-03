
void nevents(){
	//ROOT macro for calculating the number of events in several ROOT mc files from kappa. Needs a .txt file with paths to the files
	double integral = 0;
	std::vector<std::string> files;
	int n;
	ifstream inf("filelist.txt");
         while (inf){
        // read paths from the file into a vector
        	std::string strInput;
        	inf >> strInput;
		files.push_back(strInput);
    	}
	//get histogram out of the TFiles and calculate the events
	for (int i = 0; i < files.size()-1; i++){
		TFile* f = new TFile(files[i].c_str());
		TTree *tree = (TTree*)f->Get("Lumis");
		tree->Draw("nEventsTotal>>histo","", "goff"); //Creates histogram in gDirectory
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

