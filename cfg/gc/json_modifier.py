#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import imp
import json
import os

def ModifyJSON(jsonConfig, newPath):
	"""
	This workaround is neded since the artus binary does not read the FILE_NAMES
	env variable to get the job specific input files. To solve this we modifiy
	the default json config and copy it to the job specific location.
	"""

	jsonFile = open(jsonConfig, "r")
	conf = json.load(jsonFile)
	jsonFile.close()
	
	conf["InputFiles"] = os.environ['FILE_NAMES'].split()

	with open(newPath + '/' + os.path.basename(jsonConfig), 'w') as newJSON:
		json.dump(conf, newJSON, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":
	ModifyJSON(sys.argv[1], sys.argv[2])
