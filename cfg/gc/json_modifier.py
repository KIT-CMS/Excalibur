#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import os
from socket import gethostname


def ModifyJSON(jsonConfig, newPath, cachePercentage, oldexcaliburpath=None):
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
                
                
        if "srm:" in os.environ['FILE_NAMES']: ## srm files will be downloaded
                conf["InputFiles"] = [ f.split('//')[-1].strip().strip('"') for f in os.environ['FILE_NAMES'].replace(',','').split(' ')]
        else:
                conf["InputFiles"] = [ f.strip('"') for f in os.environ['FILE_NAMES'].replace(',','').split(' ')]
   
    try:
        # check if files should be cached, if true set prefix for caching
        # if str(cache-percentage) != "0":
        XROOTD_PROXY = ""
        if str(cachePercentage) != "0":
            if int(cachePercentage) > 100:
                cachePercentage = 100
            elif int(cachePercentage) < 0:
                cachePercentage = 0
            print("@msauter@")
            try:
                with open("/etc/xrootd/client.plugins.d/client-plugin-proxy.conf", "r") as proxyFile:
                    proxyFile = proxyFile.read()
                    print(" - [OK] Client proxy plugin available")
                    XROOTD_PROXY = (proxyFile.split("XROOT_PROXY=")[1]).split("\n")[0]
                    print("- [OK] proxy is set to:" + str(XROOTD_PROXY))
            except:
                print(" - [FAILED] Client proxy plugin missing, using backup-config")
            if XROOTD_PROXY == "":
                try:
                    with open("/etc/xrootd/client.plugins.d/client-plugin-proxy.conf.bak", "r") as proxyFile:
                        proxyFile = proxyFile.read()
                        print(" - [OK] Client proxy-backup plugin available")
                        XROOTD_PROXY = (proxyFile.split("XROOT_PROXY=")[1]).split("\n")[0]
                        print("- [OK] proxy is set to:" + str(XROOTD_PROXY))
                except:
                    print(" - [FAILED] Client proxy plugin missing, using backup-config")
            if XROOTD_PROXY == "":
                print(" - [FAILED] Client proxy plugin missing, using hostname")
                hostname = gethostname()
                XROOTD_PROXY = "root://" + hostname + ":1094//"
                print(" - [OK] proxy is set to:" + str(XROOTD_PROXY))

            proxy_prefix_list = []
            for index, filename in enumerate(conf["InputFiles"]):
                if index < round((int(cachePercentage) * len(conf["InputFiles"]))/100.0):
                    proxy_prefix_list.append(str(XROOTD_PROXY) + filename)
                else:
                    proxy_prefix_list.append(filename)
            shuffle(proxy_prefix_list)
            conf["InputFiles"] = proxy_prefix_list
    except:
        print("ERROR: setting caching prefix failed!")
        raise
     
   # check if files should be cached, if true set prefix for caching
   # if str(cache-percentage) != "0":
   #     print(conf["InputFiles"])
   # for index, filename in conf["InputFiles"]:
   #    if index < round(int(cachePercentage)/100 * len(conf["InputFiles"])):



    with open(newPath + '/' + os.path.basename(jsonConfig), 'w') as newJSON:
        json.dump(conf, newJSON, sort_keys=True, indent=1, separators=(',', ':'))
        print conf["InputFiles"]

if __name__ == "__main__":
        if len(sys.argv) < 4:
          ModifyJSON(sys.argv[1], sys.argv[2])
        elif len(sys.argv) < 5:
          ModifyJSON(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
          ModifyJSON(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
