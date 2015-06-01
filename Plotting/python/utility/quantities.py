#  -*- coding: utf-8 -*-

"""
	Aliases for quantities
"""

quantities_dict = {
	'alpha': '(jet2pt/zpt)',
	'ptbalance': '(jet1pt/zpt)',
	'deltaphizjet1' : '(abs(abs(abs(zphi-jet1phi)-TMath::Pi())-TMath::Pi()))',
	'deltaphijet1jet2' : '(abs(abs(abs(jet1phi-jet2phi)-TMath::Pi())-TMath::Pi()))',
	'deltaphizmet' : '(abs(abs(abs(zphi-metphi)-TMath::Pi())-TMath::Pi()))',
	'sortedflavour' : (
		'matchedgenparton1flavour*(matchedgenparton1flavour<20 && matchedgenparton1flavour>(-20))'  # quarks: ok
		+'+6*(matchedgenparton1flavour==21)'  # gluons: 21 -> 6
		+'+7*(matchedgenparton1flavour==-999)'  # undef ->7
	),
	'sortedabsflavour' : (
		'abs(matchedgenparton1flavour)*(abs(matchedgenparton1flavour)<20)'  # quarks: ok
		+'+6*(abs(matchedgenparton1flavour)==21)'  # gluons: 21 -> 6
		+'+7*(abs(matchedgenparton1flavour)==999)'  # undef ->7
	),
}
