## Workloads_Installer

#### This repo aims to automate the installation of different workloads like stress-ng, sandstone, hero-feature for the execution of eSST test-plan.

### Pre Setup
1. For Hero Setup, please edit the "test_details.ini" file with necessary info such as SUT username, password etc. (example shown in the file).
2. For Sandstone installation, if you want to remove the older versions of sandstone directories, uncomment the commented lines in "install_sandstone.sh" (instruction given in script).
3. Give execute permissions to the scripts.  
` chmod +x * `

### Installation
#### These are some of the scripts/options available with this installer.
1. install_all_workloads.sh -> Installs all 3 workloads (Hero, Sandstone, Stress-ng).
2. install_latest_hero.sh -> Installs the latest Hero feature setup.
3. update_latest_hero.sh -> Updates to the latest version Hero feature.
4. install_sandstone.sh -> Installs the latest version sandstone workload.
5. install_stress_ng.sh -> Installs the latest stress-ng workload.

After the installation, it will also perform a sanity test and print out the result with info like installation status, version, sanity status. This info is also logged and will be stored in "Installations.log" file in the same folder.

Note: 
1. Before sandstone installation, please make sure to copy the test log files in the sandstone folder if those are required.
