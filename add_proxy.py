import os
import subprocess
import sys

VERIFY_PROXY_SCRIPT = "workloads_execution_prerequisite_Verify_Proxy_CentOS.sh"
http_proxy1 = "http://proxy-chain.intel.com:911"
http_proxy2 = "http://proxy-chain.intel.com:911"
https_proxy1 = "http://proxy-chain.intel.com:911"
https_proxy2 = "http://proxy-chain.intel.com:912"

def check_proxy():
    
    
    out = subprocess.run([f"./{VERIFY_PROXY_SCRIPT}"],stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.decode()
    k = out.splitlines()
    if (k[0] == http_proxy1 or k[0] == http_proxy2) and (k[1] == https_proxy1 or k[1] == https_proxy2):
      print("Proxies present")
    else:
        if (k[0] != http_proxy1 and k[0] != http_proxy2) or (k[1] != https_proxy1 and k[1] != https_proxy2):
            print("Proxies not present...")
            add_proxy()
            print("Proxies have been added to the bashrc file. Please run the below command and re-run the script again\n`source /root/.bashrc`")
            sys.exit()
    
def add_proxy():
    
    bashrc_path = os.path.expanduser("/root/.bashrc")
    with open(bashrc_path, "r") as bashrc_file:
        bashrc_contents = bashrc_file.read()

    
    if http_proxy1 not in bashrc_contents and http_proxy2 not in bashrc_contents:
        
        with open(bashrc_path, "a") as bashrc_file:
            bashrc_file.write(f"\nexport http_proxy={http_proxy1}")
            bashrc_file.write(f"\nexport HTTP_PROXY={http_proxy1}")

    
    if https_proxy1 not in bashrc_contents and https_proxy2 not in bashrc_contents:
        
        with open(bashrc_path, "a") as bashrc_file:
            bashrc_file.write(f"\nexport https_proxy={https_proxy2}")
            bashrc_file.write(f"\nexport HTTPS_PROXY={https_proxy2}")

    print("Proxy settings added to .bashrc if not already present.")

check_proxy()