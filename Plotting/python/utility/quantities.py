#  -*- coding: utf-8 -*-

"""
	Aliases for quantities
"""

quantities_dict = {
	'ptbalance': '(jet1pt/zpt)',
	'deltaphizjet1' : '(abs(abs(abs(zphi-jet1phi)-TMath::Pi())-TMath::Pi()))',
	'deltaphizmet' : '(abs(abs(abs(zphi-metphi)-TMath::Pi())-TMath::Pi()))',
}
