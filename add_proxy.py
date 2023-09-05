import os
import subprocess
import sys

VERIFY_PROXY_SCRIPT = "workloads_execution_prerequisite_Verify_Proxy_CentOS.sh"

def check_proxy():
    http_proxy1 = "http://proxy-dmz.intel.com:911"
    http_proxy2 = "http://proxy-dmz.intel.com:911"
    https_proxy1 = "http://proxy-dmz.intel.com:911"
    https_proxy2 = "http://proxy-dmz.intel.com:912"
    
    out = subprocess.run([f"./{VERIFY_PROXY_SCRIPT}"],stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.decode()
    k = out.splitlines()
    if (k[0] == http_proxy1 or k[0] == http_proxy2) and (k[1] == https_proxy1 or k[1] == https_proxy2):
      print("Proxies present")
    if (k[0] != http_proxy1 and k[0] != http_proxy2) or (k[1] != https_proxy1 and k[1] != https_proxy2):
      print("Proxies not present...")
      add_proxy()
      print("Proxies have been added to the bashrc file. Please run the below command and re-run the script again\n`source /root/.bashrc`")
      sys.exit()
    
def add_proxy():
    # Define the proxy settings
    http_proxy1 = "http://proxy-dmz.intel.com:911"
    http_proxy2 = "http://proxy-dmz.intel.com:912"
    https_proxy1 = "http://proxy-dmz.intel.com:911"
    https_proxy2 = "http://proxy-dmz.intel.com:912"
   
    # Read the contents of the .bashrc file
    bashrc_path = os.path.expanduser("/root/.bashrc")
    with open(bashrc_path, "r") as bashrc_file:
        bashrc_contents = bashrc_file.read()

    # Check if the HTTP proxy is already present
    if http_proxy1 not in bashrc_contents and http_proxy2 not in bashrc_contents:
        # Add HTTP proxy to .bashrc
        with open(bashrc_path, "a") as bashrc_file:
            bashrc_file.write(f"\nexport http_proxy={http_proxy1}")
            bashrc_file.write(f"\nexport HTTP_PROXY={http_proxy1}")

    # Check if the HTTPS proxy is already present
    if https_proxy1 not in bashrc_contents and https_proxy2 not in bashrc_contents:
        # Add HTTPS proxy to .bashrc
        with open(bashrc_path, "a") as bashrc_file:
            bashrc_file.write(f"\nexport https_proxy={https_proxy2}")
            bashrc_file.write(f"\nexport HTTPS_PROXY={https_proxy2}")

    print("Proxy settings added to .bashrc if not already present.")

check_proxy()