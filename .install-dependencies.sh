#!/usr/bin/env sh

BASE=$(cd .. && echo $PWD)
cd $BASE

# Install Root
#wget http://www-ekp.physik.uni-karlsruhe.de/~sieber/root_5.34.07-1_amd64.deb || exit 1
#sudo dpkg -i root_5.34.07-1_amd64.deb || exit 1
echo "/usr/local/lib" | sudo tee -a /etc/ld.so.conf
echo "/usr/local/lib/root" | sudo tee -a /etc/ld.so.conf
sudo ldconfig || exit 1

# Install Kappa
git clone https://github.com/KappaAnalysis/Kappa.git || exit 1
#make -C Kappa/DataFormats/test || exit 1

# Install KappaTools
git clone https://github.com/KappaAnalysis/KappaTools.git || exit 1
#make -C KappaTools || exit 1

# Install CondFormats
wget http://www-ekp.physik.uni-karlsruhe.de/~sieber/CondFormats.tar.gz || exit 1
tar xzf CondFormats.tar.gz || exit 1

#Install Artus
git clone https://github.com/artus-analysis/Artus.git
cd Artus
#cmake .
#make
cd $BASE
