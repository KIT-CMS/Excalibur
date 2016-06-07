#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, os

filelist = open('filelist.txt','w')
os.chdir("/storage/a/cheidecker/cmssw807_calo_noPUJetID/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7/")
for f in glob.glob("*.root"):
	filelist.write("/storage/a/cheidecker/cmssw807_calo_noPUJetID/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7/"+f+'\n')

