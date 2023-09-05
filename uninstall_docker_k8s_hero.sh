#!/bin/bash

sudo yum install -y pip
pip install pexpect

cd /root
rm -rf applications.benchmarking.benchmark.platform-hero-features
cd -
./remove_docker_k8s.sh

echo "Please reboot the SUT and run the hero installation script"