#!/bin/bash

export http_proxy=http://proxy-dmz.intel.com:911
export https_proxy=http://proxy-dmz.intel.com:911

chmod +x *
python3 add_proxy.py
source /root/.bashrc
sudo yum install -y pip
pip install pexpect
python3 install_hero.py