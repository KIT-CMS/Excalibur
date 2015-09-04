#!/usr/bin/env sh

BASE=$(cd .. && echo $PWD)
cd $BASE

# Install Kappa
git clone --depth=10 https://github.com/KappaAnalysis/Kappa.git || exit 1
make -C Kappa/DataFormats/test || exit 1

# Install KappaTools
git clone --depth=10 https://github.com/KappaAnalysis/KappaTools.git || exit 1
make -C KappaTools || exit 1

# Install CondFormats
wget http://www-ekp.physik.uni-karlsruhe.de/~sieber/CondFormats.tar.gz || exit 1
tar xzf CondFormats.tar.gz || exit 1

#Install Artus
git clone --depth=10 https://github.com/artus-analysis/Artus.git
cd Artus
cmake .
make
cd $BASE
