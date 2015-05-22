#  -*- coding: utf-8 -*-

"""
	some default binnings
"""

absetabins = "0 0.783 1.305 1.93 2.5 2.964 3.139 5.191"

binnings = {
	'zpt': "30 40 50 60 75 95 125 180 300 1000",
	'npv':"-0.5 4.5 8.5 15.5 21.5 45.5",
	'eta':" ".join([str(y) for y in [-i for i in [float(x) for x in absetabins.split(" ")][7:0:-1]]+[float(x) for x in absetabins.split(" ")]]),
	'abseta': absetabins,
}
