#  -*- coding: utf-8 -*-

import os
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.plotbase as plotbase
from Artus.HarryPlotter.utility.mplhisto import MplHisto, MplGraph

class HEPData(plotbase.PlotBase):
	"""write histogram to HEPData file."""



	def prepare_args(self, parser, plotData):
		plotData.plotdict['formats'] = ["txt"]
		super(HEPData, self).prepare_args(parser, plotData)

		#plotData.plotdict['filename'] = "hepdata"
		#plotData.plotdict["output_filenames"].append(os.path.join(plotData.plotdict["output_dir"], plotData.plotdict["filename"]+"."+plot_format))

		pass

	def run(self, plotData):
		#super(HEPData, self).run(plotData)
		log.info("Preparing HEP Data...")
		header = ("""*dataset:
*location: F 7
*dscomment: Z->ee fiducial (81 < m(Z) < 101 GeV) cross section for |y(Z)| < 0.4 as a function of p_T(Z).
		""" +  # The (sys) error is the total systematic error, including the luminosity uncertainty of 2.6%
		"""
WARNING contains dummy parameters: 10% systematic uncertainty

*reackey: P P --> Z ee
*obskey: D2SIG/DPT/DYRAP
*qual: ABS(YRAP) : < 0.4
*qual: RE : P P --> Z ee
*qual: SQRT(S) IN GEV : 8000.0
*yheader: D2(SIG)/DPT/DABS(YRAP) IN FB/GEV
*xheader: PT IN GEV
*data: x : y""")
		footer = "*dataend:"
	
	
		data = self.get_values(plotData)

		self.string = header + data + footer
		self.plot_end(plotData)
		
	def get_values(self, plotData):
		data = ""
		if len(plotData.plotdict['nicks']):
			log.warning('HEPData: multiple nicks are written to file! Is this correct?')
		for nick in plotData.plotdict['nicks']:
			root_object = plotData.plotdict["root_objects"][nick]
			hist = MplHisto(root_object)
			for lower, upper, xsec, stat in zip(hist.xl, hist.xu, hist.bincontents, hist.binerr):
				data += " %.0f TO %.0f; %.0f +- %.1f  (DSYS=%.1f);\n" % (lower, upper, xsec, stat, 0.1 * xsec)
		return data
		
	def plot_end(self, plotData):
		f = open(plotData.plotdict["output_filenames"][0], 'w')
		f.write(self.string)
		f.close()
		log.info("HEPData written to %s" % plotData.plotdict["output_filenames"][0])
