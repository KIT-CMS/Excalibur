// use as root -l -q max_bin.C
void max_bin() {
    //TFile *f = TFile::Open("mc16_mm_BCDEFGH_DYtoLLamcatnlo.root");
    TFile *f = TFile::Open("/storage/c/tberger/excalibur_results_xsec/2017-12-11/data16_mm_BCDEFGH_SiMuLegacy.root");
    //TFile *f = TFile::Open("/storage/c/tberger/excalibur_results_xsec/2017-12-11/data16_mm_EF_SiMuLegacy.root");
    TNtuple *ntuple = (TNtuple*)f->Get("leptoncuts/ntuple");
    double_t binstar[] =  {2.0,2.5};//{0.0,0.5,1.0,1.5,2.0,2.5};
    double_t binboost[] = {0.0,0.5};//{0.0,0.5,1.0,1.5,2.0,2.5};
    //double_t binz[] = {30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 225, 250, 275, 300, 350, 400, 1000};
    double_t binz[] = {20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 200};//double minz = 30;//
    /*float binstar[6] =  {2.5,2.0,1.5,1.0,0.5,0.0};
    float binboost[6] = {2.5,2.0,1.5,1.0,0.5,0.0};*/
    unsigned allentries = 0;
    for (unsigned int istar=1; istar<sizeof(binstar)/sizeof(binstar[0]); istar++){
      for (unsigned int iboost=1; iboost<sizeof(binboost)/sizeof(binboost[0]); iboost++){
        for (unsigned int iz=1; iz<sizeof(binz)/sizeof(binz[0]); iz++){
            std::string cut = "abs(zy-jet1y)/2>"+ std::to_string(binstar[istar-1])  +"&&abs(zy-jet1y)/2<"+ std::to_string(binstar[istar])+"&&"
                            + "abs(zy+jet1y)/2>"+ std::to_string(binboost[iboost-1])+"&&abs(zy+jet1y)/2<"+ std::to_string(binboost[iboost])+"&&"
                            + "zpt>"+ std::to_string(binz[iz-1])+"&&zpt<"+ std::to_string(binz[iz]);
            //std:cout << cut << std::endl;
            if (binstar[istar]+binboost[iboost]<=3){
                const unsigned nentries = ntuple->Draw("zpt",("abs(jet1eta)<2.5&&"+cut).c_str(),"goff");
                allentries = allentries+nentries;
                //if (nentries){
                    std::cout << fixed << setprecision(1)
                            << "ystar in [" <<binstar[istar-1]<<   ","<<binstar[istar]  <<"], " 
                            << "yboost in ["<<binboost[iboost-1]<< ","<<binboost[iboost]<<"], " 
                            << "zpt in ["<<   binz[iz-1]<<         ","<<binz[iz]<<        "]: "
                            << "number of entries: "<<std::to_string(nentries)<<", "
                                //+"overall number of entries: "+std::to_string(allentries)+", "
                            << "zptmax=" << *std::max_element(ntuple->GetV1(),ntuple->GetV1()+nentries) << std::endl;
                //}
                
                /*const unsigned lastbinentries = ntuple->Draw("zpt",("zpt>"+std::to_string(minz)+"&&abs(jet1eta)<2.5&&"+cut).c_str(),"goff");
                if (nentries && lastbinentries){
                    std::cout << fixed << setprecision(1)
                              << "ystar in ["<<binstar[istar]<<  ","<<binstar[istar+1]<<"]," 
                              <<"yboost in ["<<binboost[iboost]<<","<<binboost[iboost+1]<<"]: " 
                              <<"number of entries with zpt>"<<minz<<": "<<std::to_string(lastbinentries)<<", "
                                //+"overall number of entries: "+std::to_string(allentries)+", "
                              <<"zptmax=" << *std::max_element(ntuple->GetV1(),ntuple->GetV1()+nentries) << std::endl;
                }*/
            }
            /*else {
                std::cout << "ystar in ["+std::to_string(binstar[istar])+   ","+std::to_string(binstar[istar+1])+"],"
                            +"yboost in ["+std::to_string(binboost[iboost])+","+std::to_string(binboost[iboost+1])+"]:"
                            +"no zpt entries" << std::endl;
            }*/
        }
      }
    }
    
    
}

