#!/bin/bash

export http_proxy=http://proxy-chain.intel.com:911
export https_proxy=http://proxy-chain.intel.com:911

chmod +x *

./install_latest_hero.sh
./install_sandstone.sh
./install_stress_ng.sh

echo -e "\n\n############################################# INSTALLATION SUMMARY #############################################\n\n"
tail -n 14 Installations.log
