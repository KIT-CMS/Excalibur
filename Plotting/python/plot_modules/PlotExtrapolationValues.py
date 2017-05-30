# -*- coding: utf-8 -*-

"""
	plot fit labels to extrapolation plot
"""

import Artus.HarryPlotter.plotbase as plotbase
from matplotlib import transforms, pyplot

import ROOT
from array import array
import Artus.HarryPlotter.analysisbase as analysisbase

class PlotExtrapolationValues(plotbase.PlotBase):

	def run(self, plotData):
		
		#print 'this is going to be the values function'
		#ETA=plotData.plotdict['histogram_from_fit_eta_values']
		#ZPT=plotData.plotdict['histogram_from_fit_zpt_values']
		#nicks = plotData.plotdict['extrapolation_values_nicks']
		#print nicks
        #
		#for index, nick in enumerate(nicks):
		#	for eta1,eta2 in zip(ETA[:-1],ETA[1:]):
		#		for zpt1,zpt2 in zip(ZPT[:-1],ZPT[1:]):
		#			plotData.plotdict['weights']=['abs(jet1eta)>%s'%eta1+'&&abs(jet1eta)<%s'%eta2+'&&zpt>%s'%zpt1+'&&zpt<%s'%zpt2]
		#			x_values = map(float,[eta1 eta2])
		#			print x_values
		#			hist = ROOT.TH1D(self.__class__.__name__, self.__class__.__name__, len(nicks), array('d',x_values))
		#			fit_function = plotData.plotdict["root_objects"][nick]
		#			fit_result = plotData.fit_results[nick]
		#			hist.SetBinContent(index+1,  fit_function.GetParameter(0))
		#			hist.SetBinError(index+1,  fit_function.GetParError(0))
		
		
		#for hist_id in xrange(len(plotData.plotdict['extrapolation_values_nicks'])):
		nicks = plotData.plotdict['extrapolation_values_nicks']
		print nicks
		#x_values = map(float,plotData.plotdict['histogram_from_fit_eta_values'])
		x_values = map(float,plotData.plotdict['etavalues'])
		print x_values
		hist = ROOT.TH1D(self.__class__.__name__, self.__class__.__name__, len(nicks), array('d',x_values))
		print 'this is going to be the values function'
		for index, nick in enumerate(nicks):
			fit_function = plotData.plotdict["root_objects"][nick]
			fit_result = plotData.fit_results[nick]
			hist.SetBinContent(index+1,  fit_function.GetParameter(0))
			hist.SetBinError(index+1,  fit_function.GetParError(0))
		#	#print "%.4f, %.4f" % (fit_function.GetParameter(0), fit_function.GetParError(0))
		#	#print "%.2f / %d" % (fit_result.Chi2(), fit_result.Ndf())
			print  nick+' - set Bin: %s'%x_values[0]+'-%s'%x_values[1]+' '+str(fit_function.GetParameter(0))+'+/-'+str(fit_function.GetParError(0))
			plotData.plotdict['nicks'].append(nick)
			plotData.plotdict['root_objects'][nick] = hist
		#		
		#for index, nick in enumerate(map(str,nicks)):
		#	fit_function = plotData.plotdict["root_objects"][nick]
		#	hist.SetBinContent(index+1,  fit_function.GetParameter(0))
		#	hist.SetBinError(index+1,  fit_function.GetParError(0))
		#	print  nick+' - set Bin: '+str(index)+' '+str(fit_function.GetParameter(0))+'+/-'+str(fit_function.GetParError(0))
		#nick = plotData.plotdict['histogram_from_fit_newnick'][hist_id]
		
