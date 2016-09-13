#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os

import Artus.KappaAnalysis.kappaanalysiswrapper as kappaanalysiswrapper
import Artus.Utility.jsonTools as jsonTools

import sys

class ExcaliburAnalysisWrapper(kappaanalysiswrapper.KappaAnalysisWrapper):

	def __init__(self):
		super(ExcaliburAnalysisWrapper, self).__init__("HiggsToTauTauAnalysis")

	def _initArgumentParser(self, userArgParsers=None):
		super(ExcaliburAnalysisWrapper, self)._initArgumentParser(userArgParsers)	  
	  
        def run(self):
	  return super(HiggsToTauTauAnalysisWrapper, self).run()
	
	
if __name__ == "__main__":
	excaliburAnalysisWrapper =  ExcaliburAnalysisWrapper()
        sys.exit(excaliburAnalysisWrapper.run())