#!/bin/bash
#Download Intel Certificates
wget --no-proxy http://certificates.intel.com/repository/certificates/Intel%20Root%20Certificate%20Chain%20Base64.zip
wget --no-proxy http://certificates.intel.com/repository/certificates/IntelSHA2RootChain-Base64.zip
wget --no-proxy http://certificates.intel.com/repository/certificates/PublicSHA2RootChain-Base64-crosssigned.zip


#Setup CentOS
sudo yum install ca-certificates -y
sudo update-ca-trust enable -y
sudo unzip -o "Intel Root Certificate Chain Base64.zip" -d /etc/pki/ca-trust/source/anchors
sudo unzip -o IntelSHA2RootChain-Base64.zip -d /etc/pki/ca-trust/source/anchors
sudo update-ca-trust extract -y

