#!/bin/bash

# script to get delivered and recorded lumi in run2 (from https://twiki.cern.ch/twiki/bin/view/CMS/Lcr2)
# Usage: lcr2.sh data/json/json_DCSONLY_Run2015B.txt

cd /afs/cern.ch/user/m/marlow/public/lcr2/
python lcr2.py -i $EXCALIBURPATH/$1
