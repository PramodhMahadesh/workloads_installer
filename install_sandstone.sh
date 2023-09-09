#!/bin/bash

export http_proxy=http://proxy-chain.intel.com:911
export https_proxy=http://proxy-chain.intel.com:911


# To remove old sandstone versions, uncomment the below four lines

# cd /root
# rm -rf sandstone-*-linux-fullstatic
# rm -rf sandstone-*-linux-fullstatic.tar.xz
# cd -

chmod +x *

sudo yum install -y pip
pip install requests
pip install beautifulsoup4
python3 sandstone_functions.py

