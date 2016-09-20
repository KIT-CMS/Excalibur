#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import os


def ModifyJSON(jsonConfig, newPath, oldexcaliburpath=None):
	"""
	This workaround is neded since the artus binary does not read the FILE_NAMES
	env variable to get the job specific input files. To solve this we modifiy
	the default json config and copy it to the job specific location.
	"""
	if oldexcaliburpath:
	  with open(jsonConfig, "r") as jsonFile:
		temp = jsonFile.read().replace(oldexcaliburpath,os.environ['CMSSW_BASE']+'/src/Excalibur')                                                                                                                                                                                                                                                                                                                          
                conf = json.loads(temp)
        else:
          with open(jsonConfig, "r") as jsonFile:
                conf = json.load(jsonFile)
                
	conf["InputFiles"] = [ f.split('//')[-1].strip().strip('"') for f in os.environ['FILE_NAMES'].replace(',',' ').split(' ')]
	with open(newPath + '/' + os.path.basename(jsonConfig), 'w') as newJSON:
		json.dump(conf, newJSON, sort_keys=True, indent=1, separators=(',', ':'))
	print conf["InputFiles"]
if __name__ == "__main__":
	if len(sys.argv) < 4:
	  ModifyJSON(sys.argv[1], sys.argv[2])
	else:
	  ModifyJSON(sys.argv[1], sys.argv[2], sys.argv[3])
