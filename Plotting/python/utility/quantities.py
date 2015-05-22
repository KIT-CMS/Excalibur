#  -*- coding: utf-8 -*-

"""
	Aliases for quantities
"""

quantities_dict = {
	'ptbalance': '(jet1pt/zpt)',
	'deltaphizjet1' : '(abs(abs(abs(zphi-jet1phi)-TMath::Pi())-TMath::Pi()))',
	'deltaphizmet' : '(abs(abs(abs(zphi-metphi)-TMath::Pi())-TMath::Pi()))',
	'sortedflavour' : (
		'matchedgenparton1flavour*(matchedgenparton1flavour<20 && matchedgenparton1flavour>(-20))'  # quarks: ok
		+'+6*(matchedgenparton1flavour==21)'  # gluons: 21 -> 6
		+'+0*(matchedgenparton1flavour==-999)'  # undef ->0
	),
	'abssortedflavour' : (
		'abs(matchedgenparton1flavour)*(abs(matchedgenparton1flavour)<20)'  # quarks: ok
		+'+6*(abs(matchedgenparton1flavour)==21)'  # gluons: 21 -> 6
		+'+0*(abs(matchedgenparton1flavour)==-999)'  # undef ->0
	),
}
