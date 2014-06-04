#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ZJet.ZJetAnalysis.zjetConfigBase as cb

from Artus.Configuration.artusWrapper import ArtusWrapper


def run(baseconfig=None):
	#Additional ZJet parser arguments
	zjetParser = argparse.ArgumentParser(add_help=False)
	zjetGroup = zjetParser.add_argument_group("ZJet options")
	zjetGroup.add_argument('-y', '--year', type=int,
        default=2012,
        help="data taking period. Default ist %(default)s")
	zjetGroup.add_argument('-z', '--zjet', type=bool,
        default=None,
        help="python config")

	dummydict = {'InputFiles':['dummy']}
	artusWrapper = ArtusWrapper("ZJet", [zjetParser], basedict=dummydict)

	conf = artusWrapper.getConfig()

	#Get additional Zjet settings from config base

	#print dir(artusWrapper._args.zjet)

	artusWrapper.setConfig(conf)
	# Run the wrapper
	sys.exit(artusWrapper.run())

if __name__ == "__main__":
	run()
