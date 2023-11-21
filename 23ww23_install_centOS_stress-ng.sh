#!/bin/bash

yum install -y https://rpmfind.net/linux/centos/8-stream/PowerTools/x86_64/os/Packages/Judy-devel-1.0.5-18.module_el8.3.0+757+d382997d.x86_64.rpm

cd /root
rm -rf stress-ng
git clone https://github.com/ColinIanKing/stress-ng
cd stress-ng/
git pull
make clean
make -j 50
#./stress-ng 
sudo yum install -y keyutils-libs-devel kmod-devel libaio-devel libatomic libattr-devel libbsd-devel libcap-devel libgbm-devel libgcrypt-devel libglvnd-core-devel libglvnd-devel libjpeg-devel libmd-devel mpfr-devel libX11-devel libXau-devel libxcb-devel lksctp-tools-devel xorg-x11-proto-devel xxhash-devel zlib-devel
sudo yum makecache --refresh
sudo yum update
sudo yum -y install stress-ng
make clean
make -j 50

# Install Judy-devel before running this script
#
# Give the below command to install the rpm file
# yum install -y https://rpmfind.net/linux/centos/8-stream/PowerTools/x86_64/os/Packages/Judy-devel-1.0.5-18.module_el8.3.0+757+d382997d.x86_64.rpm



