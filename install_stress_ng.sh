#!/bin/bash

export http_proxy=http://proxy-chain.intel.com:911
export https_proxy=http://proxy-chain.intel.com:911

chmod +x *
./23ww23_install_centOS_stress-ng.sh
python3 stressng_functions.py