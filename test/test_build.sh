#!/bin/sh

/etc/cvmfs/run-cvmfs.sh

# export SCRAM_ARCH=slc6_amd64_gcc481
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch

mkdir -p /home/build && cd /home/build


. $VO_CMS_SW_DIR/cmsset_default.sh
scram project ${TEST_CMSSW_VERSION}

cd ${TEST_CMSSW_VERSION}

cmsenv

cd src/

## Required packages ##

git cms-init
git cms-addpkg CondFormats/JetMETObjects
git clone https://github.com/KIT-CMS/Kappa.git -b master

# we don't need all of Kappa, just a few subdirectories -> sparse checkout
cd Kappa
echo docs/ >> .git/info/sparse-checkout
echo DataFormats/ >> .git/info/sparse-checkout
echo Skimming/data/ >> .git/info/sparse-checkout
echo Skimming/python/ >> .git/info/sparse-checkout
git config core.sparsecheckout true
git read-tree -mu HEAD
cd ..

git clone https://github.com/KIT-CMS/KappaTools.git -b master
git clone https://github.com/KIT-CMS/Artus.git -b master
#git clone https://github.com/KIT-CMS/TauRefit.git VertexRefit/TauRefit -b master
#git clone https://github.com/cms-jet/JECDatabase.git --depth=1 -b master

#######################

mkdir Excalibur
cp -r /home/travis/* Excalibur/

echo "# ================= #"
echo "# Building in CMSSW #"
echo "# ================= #"

scram b -v -j 2 || exit 1
