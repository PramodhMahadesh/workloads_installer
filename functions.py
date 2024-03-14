import os
import subprocess
import sys
import re
import socket
import configparser
import datetime
import pexpect

INSTALL_APPS_SCRIPT = "workloads_execution_prerequisite_installApps_CentOS.sh"
INSTALL_CERT_SCRIPT = "workloads_execution_prerequisite_InstallCert_RHEL_CentOS.sh"
INSTALL_DOCKER_PATH = "workloads_execution_prerequisite_installDocker-CentOS.sh"
VERIFY_PROXY_SCRIPT = "workloads_execution_prerequisite_Verify_Proxy_CentOS.sh"
INI_FILE = "test_details.ini"
AUTOMATION_PRE_REQUISITE_FILE = "install_pre_requisite_automation.sh"
GIT_PATH = 'https://github.com/intel-innersource/applications.benchmarking.benchmark.platform-hero-features.git'
HERO_DIR = "/root/applications.benchmarking.benchmark.platform-hero-features"
CONFIG_FILE_PATH = f"{HERO_DIR}/script/terraform/terraform-config.static.tf"
SETUP_DIR = f"{HERO_DIR}/script/setup"
SETUP_DEV_FILE = "setup-dev.sh"
SETUP_REG_FILE = "setup-reg.sh"
SETUP_DOCKER_FILE = "setup-sut-docker.sh"
SETUP_K8S_FILE = "setup-sut-k8s.sh"
BUILD_SCRIPT = "BuildWorkload_needtoupdate.sh"
WORKLOAD_DIR = f"{HERO_DIR}/build/workload"

HERO_INSTALLATION_STATUS = "N/A"
HERO_INSTALLED_VERSION = "N/A"
HERO_SANITY_STATUS = "N/A"
CWD = os.path.dirname(__file__)
INSTALLATION_STATUS_LOG = f"{CWD}/Installations.log"



def init():
  os.chdir(CWD)
  os.system("chmod +x *")

  # try:
  #   import pexpect
  # except Exception as e:
  #   print(f"pexpect not installed. {e}")
  #   os.chdir(CWD)
  #   subprocess.run([f"./{AUTOMATION_PRE_REQUISITE_FILE}"])
  #   import pexpect
   

def read_details(filename):
    parser = configparser.ConfigParser()
    parser.read(filename)
    global SUT_USERNAME, SUT_PASSWORD, USER, PLATFORM, TEST_WORKLOAD, GITHUB_TOKEN
    try:
        SUT_USERNAME = parser.get('DETAILS','SUT_USERNAME')
        SUT_PASSWORD = parser.get('DETAILS','SUT_PASSWORD')
        USER = parser.get('DETAILS','USER')
        PLATFORM = parser.get('DETAILS','PLATFORM')
        TEST_WORKLOAD = parser.get('DETAILS','TEST_WORKLOAD')
        GITHUB_TOKEN = parser.get('DETAILS','GITHUB_TOKEN')
    except configparser.NoOptionError as e:
        print(e)
        print(f"Please check {INI_FILE} and ensure option names are correct according to the example in the file")
        sys.exit()

def get_ip_address2():
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Connect to a remote server (doesn't matter which)
        sock.connect(('8.8.8.8', 80))
        
        # Get the socket's IP address
        ip_address = sock.getsockname()[0]
        return ip_address
    except socket.error:
        print("Unable to get ip")
        sys.exit()
    finally:
        # Close the socket
        sock.close()
        
        
IP = get_ip_address2()



def install_apps():
  child = pexpect.spawn(f"./{INSTALL_APPS_SCRIPT}")
  if child.expect(["\[y/N\]:","y/n","yes/n",pexpect.EOF,pexpect.TIMEOUT]) in [0,1,2]:
    child.sendline("y")
    print(child.before.decode())
    #print(child.after.decode())
    child.interact()
  else:
    print(child.before.decode())

  

def get_docker():
  try:
    output = subprocess.run(["docker", "--version"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #print(output.stdout.decode())
    #print("Updating docker...")
    #os.system("sudo yum update docker")
    out1 = subprocess.run(["systemctl", "status", "docker.service"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if "Active: inactive" in out1.stdout.decode() or "Active: failed" in out1.stdout.decode():
      print("Starting docker service")
      os.system("systemctl start docker.service")
    out2 = subprocess.run(["systemctl", "status", "docker.service"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if "Active: active (running)" in out2.stdout.decode():
      print("Docker is running")
    else:
      print("Unable to start docker. Please check manually")
      sys.exit()
  except FileNotFoundError:
    print("Installing docker from script")
    subprocess.run([f"./{INSTALL_DOCKER_PATH}"])
    out1 = subprocess.run(["systemctl", "status", "docker.service"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if "Active: inactive" in out1.stdout.decode() or "Active: failed" in out1.stdout.decode():
      print("Starting docker service")
      os.system("systemctl start docker.service")
    out2 = subprocess.run(["systemctl", "status", "docker.service"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if "Active: active (running)" in out2.stdout.decode():
      print("Docker is running")
    else:
      print("Unable to start docker. Please check manually")
      sys.exit()
      
def check_proxy():
    http_proxy1 = "http://proxy-chain.intel.com:911"
    http_proxy2 = "http://proxy-chain.intel.com:912"
    https_proxy1 = "http://proxy-chain.intel.com:911"
    https_proxy2 = "http://proxy-chain.intel.com:912"
    
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
    http_proxy1 = "http://proxy-chain.intel.com:911"
    http_proxy2 = "http://proxy-chain.intel.com:912"
    https_proxy1 = "http://proxy-chain.intel.com:911"
    https_proxy2 = "http://proxy-chain.intel.com:912"
   
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

     
def clone_git():
  os.chdir("/root")
  GIT_USERNAME = SUT_USERNAME
  GIT_TOKEN = GITHUB_TOKEN
  try:
    child = pexpect.spawn(f'git clone {GIT_PATH}')
    output_file = f'{CWD}/output_git.txt'
    fout = open(output_file,'wb')
    child.logfile = fout
    child.expect("Username for 'https://github.com': ")
    child.sendline(GIT_USERNAME)
    child.expect("Password for 'https://*")
    child.sendline(GIT_TOKEN)
    print(child.before.decode())
    child.interact()
    child.close()
    exit_code = child.exitstatus
    
    with open(output_file,'r') as f:
      out = f.read()
      if "Authentication failed" in out:
        print("\nPlease provide correct username and TOKEN.")
        sys.exit()
      if "To access\nremote: this repository, visit" in out:
        print("\nPlease authenticate your token by visiting the link shown above.")
        sys.exit()
      if exit_code == 0:
        print("\nRepo cloned successfully")
        
  except pexpect.exceptions.EOF:
    with open(output_file,'r') as f:
      out = f.read()
      if 'already exists' in out:
        print("\nRepo already exists.")
      else:
        print("\nError occured while cloning repo")
        sys.exit() 
        
  except Exception as e:
    print(f"Unknown error occured\n{e}")
    sys.exit()

def update_git():
  os.chdir(HERO_DIR)
  GIT_USERNAME = SUT_USERNAME
  GIT_TOKEN = GITHUB_TOKEN
  try:
    child = pexpect.spawn('git pull')
    output_file = f'{CWD}/output_git_pull.txt'
    fout = open(output_file,'wb')
    child.logfile = fout
    child.expect("Username for 'https://github.com': ")
    child.sendline(GIT_USERNAME)
    child.expect("Password for 'https://*")
    child.sendline(GIT_TOKEN)
    print(child.before.decode())
    child.interact()
    child.close()
    exit_code = child.exitstatus
    
    with open(output_file,'r') as f:
      out = f.read()
      if "Authentication failed" in out:
        print("\nPlease provide correct username and TOKEN.")
        sys.exit()
      if "To access\nremote: this repository, visit" in out:
        print("\nPlease authenticate your token by visiting the link shown above.")
        sys.exit()
      if exit_code == 0:
        print("\nRepo pulled to latest version successfully")
        
  except pexpect.exceptions.EOF:
    with open(output_file,'r') as f:
      out = f.read()
      if 'already exists' in out:
        print("\nRepo already exists.")
      else:
        print("\nError occured while pulling repo")
        sys.exit() 
        
  except Exception as e:
    print(f"Unknown error occured while puuling repo\n{e}")
    sys.exit()

  
def add_ip_username():  
  with open(CONFIG_FILE_PATH,'r') as f:
    k = f.readlines()
    for i in range(len(k)):
      if 'user_name":' in k[i]:
        k[i] = k[i].replace("# ","")
        v = k[i].split(":")
        v[1] = f' "{SUT_USERNAME}",\n'
        k[i] = ":".join(v)
      if '"public_ip"' in k[i]:
        v = k[i].split(":")
        v[1] = f' "{IP}",\n'
        k[i] = ":".join(v)
      if '"private_ip"' in k[i]:
        v = k[i].split(":")
        v[1] = f' "{IP}",\n'
        k[i] = ":".join(v)
    #print(k)
  with open(CONFIG_FILE_PATH,'w') as f:
    f.writelines(k)

def get_ip_address():
    try:
        output = subprocess.check_output(['ifconfig']).decode('utf-8')
        ip_pattern = r'inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        matches = re.findall(ip_pattern, output)
        if matches:
            return matches[0]
        else:
            print("Trouble in getting IP address")
            sys.exit()
    except subprocess.CalledProcessError as e:
        print("Trouble while getting IP")
        print(f'Error: {e}')
        sys.exit()




def install_setup_dev():
  #os.chdir(SETUP_DIR)
  child = pexpect.spawn(f"{SETUP_DIR}/{SETUP_DEV_FILE}")
  
  output_file = 'output1.txt'
  fout = open(output_file,'wb')
  child.logfile = fout
  
  child.expect(["password:",pexpect.EOF,pexpect.TIMEOUT])
  child.sendline(SUT_PASSWORD)
  print(child.before.decode())
  child.interact()
  k = check_setup_output(output_file)
  if k:
    print(f"Done executing {SETUP_DEV_FILE}")
  else:
    print(f"Error while executing {SETUP_DEV_FILE}")
    sys.exit()

def install_setup_reg():
  #os.chdir(SETUP_DIR)
  child = pexpect.spawn(f"{SETUP_DIR}/{SETUP_REG_FILE} {IP}")
  
  output_file = 'output2.txt'
  fout = open(output_file,'wb')
  child.logfile = fout
  
  child.expect(["password:",pexpect.EOF,pexpect.TIMEOUT])
  child.sendline(SUT_PASSWORD)
  print(child.before.decode())
  child.interact()
  k = check_setup_output(output_file)
  if k:
    print(f"Done executing {SETUP_REG_FILE}")
  else:
    print(f"Error while executing {SETUP_REG_FILE}")
    # print("If this system has ww23(new) BKC, please run the below commands,reboot the SUT and restart the installation\n`sudo yum remove docker-ce-cli docker-ce docker-compose-plugin`\n`rm -rf /root/applications.benchmarking.benchmark.platform-hero-features/`\n`sudo grubby --update-kernel=ALL --args=\"systemd.unified_cgroup_hierarchy=0\"`")
    sys.exit()


def install_setup_docker():
  child = pexpect.spawn(f"{SETUP_DIR}/{SETUP_DOCKER_FILE} {SUT_USERNAME}@{IP} {SUT_USERNAME}@{IP}")
  
  output_file = 'output3.txt'
  fout = open(output_file,'wb')
  child.logfile = fout
  
  flag = 0
  if child.expect(["yes/no",pexpect.EOF,pexpect.TIMEOUT],timeout=7) == 0:
    flag=1
    child.sendline("yes")
    print(child.before.decode())
  if child.expect(["password:",pexpect.EOF,pexpect.TIMEOUT],timeout=10) == 0:
    flag=2
    child.sendline(SUT_PASSWORD)
    print(child.before.decode())
  if flag==1:
    print(child.before.decode())
  child.interact()
  #if flag==0:
    #with open(output_file,'r') as f:
      #print(f.read())
      
  k = check_setup_output(output_file)
  if k:
    print(f"Done executing {SETUP_DOCKER_FILE}")
  else:
    print(f"Error while executing {SETUP_DOCKER_FILE}")
    sys.exit()
    


def install_setup_k8s():
  child = pexpect.spawn(f"{SETUP_DIR}/{SETUP_K8S_FILE} {SUT_USERNAME}@{IP} {SUT_USERNAME}@{IP}")
  
  output_file = 'output4.txt'
  fout = open(output_file,'wb')
  child.logfile = fout
  
  flag = 0
  if child.expect(["yes/no",pexpect.EOF,pexpect.TIMEOUT],timeout=7) == 0:
    flag=1
    child.sendline("yes")
    print(child.before.decode())
  if child.expect(["password:",pexpect.EOF,pexpect.TIMEOUT],timeout=10) == 0:
    flag=2
    child.sendline(SUT_PASSWORD)
    print(child.before.decode())
  if flag==1:
    print(child.before.decode())
  child.interact()
  #if flag==0:
    #with open(output_file,'r') as f:
      #print(f.read())
      
  k = check_setup_output(output_file)
  if k:
    print(f"Done executing {SETUP_K8S_FILE}")
  else:
    print(f"Error while executing {SETUP_K8S_FILE}")
    # sys.exit()  
    
    

def check_output(filename):
  with open(filename,'r') as f:
    output_line = f.readlines()[-2]
    #print(output_line)
    
    match1 = re.search(r'failed=(\d+)', output_line)
    match2 = re.search(r'unreachable=(\d+)', output_line)

    if match1 and match2:
        failed_value = int(match1.group(1))
        unreachable_value = int(match2.group(1))
        if failed_value > 0:
            print(f"{failed_value} failed installations detected. Please check...")
            return False
        if unreachable_value > 0:
            print(f"{unreachable_value} unreachable installations detected. Please check...")
            return False
        else:
            return True
    else:
        print("No 'failed'/'unreachable' value found in the line.")
        return False

def check_k8s_output(filename):
  with open(filename,'r') as f:
    output_lines = f.readlines()[-4:-1]
    flag=0
    for output_line in output_lines:
      #print(output_line)
      match1 = re.search(r'failed=(\d+)', output_line)
      match2 = re.search(r'unreachable=(\d+)', output_line)
      if match1 and match2:
        failed_value = int(match1.group(1))
        unreachable_value = int(match2.group(1))
        if failed_value > 0:
          flag+=1
          print("Failed installations detected. Please check...")
          print(output_line)
        if unreachable_value > 0:
          flag+=1
          print("Unreachable installations detected. Please check...")
          print(output_line)
      else:
          print("No 'failed'/'unreachable' value found in the line.")
          print(output_line)
          return False
    
    return True if flag==0 else False

def check_setup_output(filename):
  with open(filename,'r') as f:
    output_lines = f.readlines()[-7:-1]
    flag=0
    result_line_flag = 0
    for output_line in output_lines:
      #print(output_line)
      match1 = re.search(r'failed=(\d+)', output_line)
      match2 = re.search(r'unreachable=(\d+)', output_line)
      if match1 and match2:
        result_line_flag += 1
        failed_value = int(match1.group(1))
        unreachable_value = int(match2.group(1))
        if failed_value > 0:
          flag+=1
          print("Failed installations detected. Please check...")
          print(output_line)
        if unreachable_value > 0:
          flag+=1
          print("Unreachable installations detected. Please check...")
          print(output_line)
    
    if result_line_flag == 0: 
      print("No failed/unreachable lines seen in the last six lines")
      return False

    return True if flag==0 else False

def update_build_username():
  version = get_git_version()
  sut_type = get_sut_type()
  os.chdir(CWD)
  with open(BUILD_SCRIPT,'r') as f:
    k = f.readlines()
  
  for i in range(len(k)):
    if '--owner' in k[i]:
      k[i] = re.sub(r'--owner=[a-zA-Z0-9]*',f'--owner={USER}',k[i])
    if '-DPLATFORM' in k[i]:
      k[i] = re.sub(r'-DPLATFORM=[a-zA-Z]*',f'-DPLATFORM={sut_type}',k[i])
    if "-DRELEASE" in k[i]:
      k[i] = re.sub(r'-DRELEASE=[a-zA-Z0-9.-]*',f'-DRELEASE={version}',k[i])
      
  with open(BUILD_SCRIPT,'w') as f:
    f.writelines(k)      

def get_git_version():
  os.chdir(HERO_DIR)
  k = subprocess.run(["git","describe","--tags"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  version = k.stdout.decode().strip()
  #print(version)
  global HERO_INSTALLED_VERSION
  if "-" in version:
    HERO_INSTALLED_VERSION =  version.split("-")[0]
    return version.split("-")[0]
  else:
    HERO_INSTALLED_VERSION = version
    return version

def get_sut_type():
  gnr_model = "173"
  srf_model = "175"
  number = 0
  k = subprocess.run(["lscpu"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  lines = k.stdout.decode().splitlines()
  for line in lines:
    if "model:" in line.lower():
      number = line.split(":")[-1].strip()
      break
  if number == 0:
    print(f"No model number to determine SUT type.\nUsing the default value in script-->{PLATFORM}")
    return PLATFORM
  elif number == gnr_model:
    return "GNR"
  elif number == srf_model:
    return "SRF"
  else:
    print(f"Error while getting SUT type.\nUsing the default value in script-->{PLATFORM}")
    return PLATFORM
    
  
def check_build():
  global HERO_INSTALLATION_STATUS
  os.chdir(f"{WORKLOAD_DIR}/{TEST_WORKLOAD}")
  k = subprocess.run(["./ctest.sh", "-N"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  output = k.stdout.decode()
  print(output)
  lines = output.splitlines()
  sanity_test_name = ""
  for line in lines:
    match = re.search(r'Total Tests: (\d+)', line)

    if match:
        value = int(match.group(1))
        if value > 0:
            for v in lines:
               if "Test #" in v and not any(ele in v for ele in ["gated","pkm"]):
                  sanity_test_name = v.split(":")[-1].strip()
                  break
            if sanity_test_name:
               os.chdir(f"{HERO_DIR}/build/workload/{TEST_WORKLOAD}")
               os.system("rm -rf nohup.out")
               run_sanity_test(sanity_test_name)
               res = parse_test("nohup.out")
            else:
               print("No valid test names found for sanity. Exiting..")
               HERO_INSTALLATION_STATUS = "CORRUPT INSTALL"
               return False

            if res:
              print(f"Sanity test for {sanity_test_name} completed. Build Successful")
              HERO_INSTALLATION_STATUS = "INSTALLED"
              return True
            else:
               print(f"Sanity test for {sanity_test_name} failed. Please check")
               return False
        else:
            print("Build Unsuccessful. Please check..")
            return False
  if not match:
    print("No 'Total Tests:' detected. Please check build..")
    return False  
      
def run_sanity_test(test_name):
    os.chdir(f"{HERO_DIR}/build/workload/{TEST_WORKLOAD}")
    command_for_one_loop = f"nohup ./ctest.sh -R {test_name} -V --loop 1"
    #k = subprocess.run([command_for_one_loop],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    os.system(command_for_one_loop)

def parse_test(filename):
    global HERO_SANITY_STATUS
    with open(filename,'r') as f:
        lines = f.readlines()
        loops = 0
        passed = 0
        failed = 0
        for line in lines:
            if "Loop: " in line:
                match = re.search(r'Loop: (\d+)',line)
                loops = max(int(match.group(1)),loops)
            if not loops:
                loops = "Could not find Loops value from file"
                return False
            if "100% tests passed" in line:
                passed += 1
            if "tests passed," in line:
                match = re.search(r'(\d+)% tests passed',line)
                if match:
                    percent = int(match.group(1))
                    if percent<100:
                        failed +=1
        print(f"No. of loops = {loops}\nNo. of loops passed = {passed}\nNo. of loop failed = {failed}")
        if failed > 0:
          HERO_SANITY_STATUS = "FAIL"
          return False
        else:
          HERO_SANITY_STATUS = "PASS"
          return True

def update_installation_status():
   global timestamp
   timestamp = datetime.datetime.now().strftime("%d/%m/%Y -- %H:%M:%S")
   with open(INSTALLATION_STATUS_LOG,'a') as f:
      f.write("\n************************************************************************")
      f.write(f"\nRecent install on {timestamp}")
      f.write("\n{:<10} {:<20} {:<20} {:<15}".format("WORKLOAD","INSTALLATION STATUS","INSTALLED VERSION","SANITY TEST"))
      f.write("\n{:<10} {:<20} {:<20} {:<15}".format("HERO",HERO_INSTALLATION_STATUS,HERO_INSTALLED_VERSION,HERO_SANITY_STATUS))
      f.write("\n")

def print_installation_status():
    print("\n************************************************************************")
    print(f"\nRecent install on {timestamp}")
    print("\n{:<10} {:<20} {:<20} {:<15}".format("WORKLOAD","INSTALLATION STATUS","INSTALLED VERSION","SANITY TEST"))
    print("\n{:<10} {:<20} {:<20} {:<15}".format("HERO",HERO_INSTALLATION_STATUS,HERO_INSTALLED_VERSION,HERO_SANITY_STATUS))
    print("\n")      
      



# init()
# read_details()
# check_proxy()
# clone_git()
# os.chdir(CWD)

# subprocess.run([f"./{INSTALL_APPS_SCRIPT}"])
# subprocess.run([f"./{INSTALL_CERT_SCRIPT}"]) 

# get_docker()


# add_ip_username()

# install_setup_dev()
# install_setup_reg()
# install_setup_docker()
# install_setup_k8s()
# update_build_username()
# subprocess.run([f"./{BUILD_SCRIPT}"])
# check_build()
