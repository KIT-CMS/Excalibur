#!/bin/bash
# Usage: test_excalibur.sh [arg=data][-a]   arg can be data or mc

TYPE=${1:-data15}
$EXCALIBURPATH/scripts/artus $EXCALIBURPATH/test/$TYPE.py.json

echo -e "\n\nChecking reference file and new output"
compareRootFiles.py $TYPE.root $EXCALIBURPATH/test/$TYPE.root $2
