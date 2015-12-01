#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface
from Excalibur.Plotting.utility.colors import histo_colors

#colors for z-->ee, z-->mumu comparison plots
color = {
	"mu": 'blue',
	"e": 'red',
	"jet": 'black',
	"z": histo_colors['green'],
	"undef": histo_colors['yellow'],
	"undef2": histo_colors['grey'],
}
#Latex
latex = {
	"jet1" : ['$Jet1$'],
	"muminus" : r'$\\mu^-$',
	"eminus" : "$e^-$",
	"pt" : "$p_{{T}}$",
	"phi" : r"$\\phi$",
	"eta" : r"$\\eta$",
	"z" : "$Z$",
	"y" : "$y$",
	"mass" : "$mass$",
	#weightinglabels
	"0_pt_noweight" : '$gen p_{{T}}$',
	"1_pt_lower50" : '$gen p_{{T}}$ $<$ $50$ $GeV$',
	"2_pt_50to100" : '$50$ $GeV$ $<$ $gen p_{{T}}$ $<$ $100$ $GeV$',
	"3_pt_higher100" : '$gen p_{{T}}$ $>$ $100$ $GeV$',
}

#weightings for pt, used in jet_muon_z_comparison and jet_muon_ee_comparison
weighting_z = {
		"0_pt_noweight" : ["1", "1", "1"],
		"1_pt_lower50" : ["(genjet1pt<50)", "(genmuminuspt<50)", "(genzpt<50)"],
		"2_pt_50to100" : ["(genjet1pt>50&&genjet1pt<100)", "(genmuminuspt>50&&genmuminuspt<100)", "(genzpt>50&&genzpt<100)"],
		"3_pt_higher100" : ["(genjet1pt>100)", "(genmuminuspt>100)", "(genzpt>100)"],
}
weighting_e = {
		"0_pt_noweight" : ["1", "1", "1"],
		"1_pt_lower50" : [ "(geneminuspt<50)", "(genjet1pt<50)", "(genmuminuspt<50)"],
		"2_pt_50to100" :["(geneminuspt>50&&geneminuspt<100)","(genjet1pt>50&&genjet1pt<100)","(genmuminuspt>50&&genmuminuspt<100)"],
		"3_pt_higher100" : [ "(geneminuspt>100)", "(genjet1pt>100)", "(genmuminuspt>100)"],
}


#expressions, labels, bins, used in jet_muon_z_comparison and jet_muon_z_comparison_tree
jmzexpress = {
	#relative reco gen for pT
		'jetpt':'jet1pt/genjet1pt',
		'mupt':'muminuspt/genmuminuspt',
		'zpt':'zpt/genzpt',
	#Delta reco gen for eta
		'jeteta':'(abs(jet1eta-genjet1eta))',
		'mueta':'(abs(muminuseta-genmuminuseta))',
		'zeta':'(abs(zeta-genzeta))',
	#Delta reco gen for phi, different formulas because of -pi < phi < pi
		'jetphi':'(abs(abs(abs(jet1phi-genjet1phi)-TMath::Pi())-TMath::Pi()))',
		'muphi':'(abs(abs(abs(muminusphi-genmuminusphi)-TMath::Pi())-TMath::Pi()))',
		'zphi':'(abs(abs(abs(zphi-genzphi)-TMath::Pi())-TMath::Pi()))',
}
jmzlabel = {
	#relative reco gen for pT
		'pt':'{}$_{{reco}}/${}$_{{gen}}$'.format(latex['pt'],latex['pt'],),
		'eta':r'|$ \\eta_{{reco}} - \\eta_{{gen}}$|',
		'phi':r'|$ \\phi_{{reco}} - \\phi_{{gen}}$|',
}
jmzbin = {
	'pt':'50,0.8,1.2',
	'eta':'50,0,0.06',
	'phi':'50,0,0.06',
}

#expressions, labels, bins, used in jet_muon_ee_comparison and jet_muon_ee_comparison_tree and jet_muon_ee_comp_npv_tree
ejmexpress = {
	#relative reco gen for pT
		'jetpt':'jet1pt/genjet1pt',
		'mupt':'muminuspt/genmuminuspt',
		'ept':'eminuspt/geneminuspt',
	#Delta reco gen for eta
		'jeteta':'(abs(jet1eta-genjet1eta))',
		'mueta':'(abs(muminuseta-genmuminuseta))',
		'eeta':'(abs(eminuseta-geneminuseta))',
	#Delta reco gen for phi, different formulas because of -pi < phi < pi (abs(abs(abs(jet1phi-jet2phi)-TMath::Pi())-TMath::Pi()))
		'jetphi':'(abs(abs(abs(jet1phi-genjet1phi)-TMath::Pi())-TMath::Pi()))',
		'muphi':'(abs(abs(abs(muminusphi-genmuminusphi)-TMath::Pi())-TMath::Pi()))',
		'ephi':'(abs(abs(abs(eminusphi-geneminusphi)-TMath::Pi())-TMath::Pi()))',
}
ejmlabel = {
	#relative reco gen for pT
		'pt':'{}$_{{reco}}/${}$_{{gen}}$'.format(latex['pt'],latex['pt'],),
		'eta':r'|$ \\eta_{{reco}} - \\eta_{{gen}}$|',
		'phi':r'|$ \\phi_{{reco}} - \\phi_{{gen}}$|',
}
ejmbin = {
	'pt':'50,0.8,1.2',
	'eta':'50,0,0.06',
	'phi':'50,0,0.06',
}





if __name__ == '__main__':
	muoniso_aod()
