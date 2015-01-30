#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import sys

import ZJet.Plotting.harryZJet as harryZJet


if __name__ == "__main__":
	"""This script executes all steps necessary to create a plot."""
	if len(sys.argv) == 1:
		sys.argv.append("-h")
		
	harryZJet.HarryPlotterZJet()

