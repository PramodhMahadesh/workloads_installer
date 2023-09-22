#!/bin/bash
cd /root/applications.benchmarking.benchmark.platform-hero-features
rm -rf build
mkdir build
cd build


#cmake -DREGISTRY=amr-registry.caas.intel.com/sf-cwr -DRELEASE=v23.17.6 -DPLATFORM=GNR -DBENCHMARK= -DTERRAFORM_OPTIONS="--docker --svrinfo --intel_publish --owner=mahadesx" ..

cmake -DREGISTRY=amr-registry.caas.intel.com/sf-cwr -DRELEASE=v23.17.6 -DPLATFORM=GNR -DTERRAFORM_SUT='static' -DBENCHMARK= -DTERRAFORM_OPTIONS="--native --docker --svrinfo --owner=mahadesx" ..

ls -l 


