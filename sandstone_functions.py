import requests
import re
from bs4 import BeautifulSoup
import os
import sys
import datetime


SANDSTONE_INSTALLATION_STATUS = "N/A"
SANDSTONE_INSTALLED_VERSION = "N/A"
SANDSTONE_SANITY_STATUS = "N/A"
CWD = os.path.dirname(__file__)
INSTALLATION_STATUS_LOG = f"{CWD}/Installations.log"

url = "https://ubit-artifactory-or.intel.com/artifactory/sandstone-or-local/release-binaries/"



def extract_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    return -1  # Return a default value if no number is found


def download_tar_file():

    response = requests.get(url)
    #print(response)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=re.compile(r'.*linux-fullstatic.*\.xz$'))
        filenames = [v['href'] for v in links]
        #print(filenames)
        
        if filenames:
            # latest_link = links[-1]['href']
            max_number = -1
            max_filename = None
            for filename in filenames:
                number = extract_number(filename)
                if number > max_number:
                    max_number = number
                    max_filename = filename
            file_url = url + max_filename
            
            # Download the file
            filename = max_filename.split('/')[-1]
            response = requests.get(file_url)
            
            if response.status_code == 200:
                with open(filename, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded {filename} successfully!")
                return filename
            else:
                print(f"Failed to download the file {max_filename}.")
                return None
        else:
            print("No .xz files found on the page.")
            return None
    else:
        print("Failed to fetch the webpage.")
        return None

def sanity_check():
    # sandstone_folder = "sandstone-150-linux-fullstatic"
    logfile = "sanity_test.txt"
    t = "0m"
    T = "2m"
    test_command = f"./sandstone -vv  -e vex* -e vpc* -e tmul* -e vmo* -e tsx* -e mul* -e gather* -t {t} -T {T} -o {logfile}"
    os.chdir(f"/root/{sandstone_folder}/bin")
    os.system(test_command)
    with open(logfile,'r') as f:
        output = f.read()
        if "exit: pass" in output:
            print("\nSanity test completed and passed.")
            os.system(f"rm -rf {logfile}")
            global SANDSTONE_SANITY_STATUS
            SANDSTONE_SANITY_STATUS = "PASS"
            return True
        else:
            print("\nSanity test failed. Please check manually.")
            return False

def update_installation_status():
   global timestamp, INSTALLATION_STATUS_LOG
   timestamp = datetime.datetime.now().strftime("%d/%m/%Y -- %H:%M:%S")
   with open(INSTALLATION_STATUS_LOG,'a') as f:
      f.write("\n************************************************************************")
      f.write(f"\nRecent install on {timestamp}")
      f.write("\n{:<10} {:<20} {:<40} {:<15}".format("WORKLOAD","INSTALLATION STATUS","INSTALLED VERSION","SANITY TEST"))
      f.write("\n{:<10} {:<20} {:<40} {:<15}".format("SANDSTONE",SANDSTONE_INSTALLATION_STATUS,SANDSTONE_INSTALLED_VERSION,SANDSTONE_SANITY_STATUS))
      f.write("\n")

def print_installation_status():
    print("\n************************************************************************")
    print(f"\nRecent install on {timestamp}")
    print("\n{:<10} {:<20} {:<40} {:<15}".format("WORKLOAD","INSTALLATION STATUS","INSTALLED VERSION","SANITY TEST"))
    print("\n{:<10} {:<20} {:<40} {:<15}".format("SANDSTONE",SANDSTONE_INSTALLATION_STATUS,SANDSTONE_INSTALLED_VERSION,SANDSTONE_SANITY_STATUS))
    print("\n") 

sandstone_tar_filename = download_tar_file()


if sandstone_tar_filename:
    SANDSTONE_INSTALLATION_STATUS = "INSTALLED"
    os.system(f"mv {sandstone_tar_filename} /root/")
    os.chdir("/root")
    os.system(f"tar -xvf {sandstone_tar_filename}")
    global sandstone_folder
    sandstone_folder = sandstone_tar_filename.split(".")[0:-2][0]
    SANDSTONE_INSTALLED_VERSION = sandstone_folder
    sanity_check()
    update_installation_status()
    print_installation_status()
else:
    print("Error while downloading tar file")
    update_installation_status()
    print_installation_status()
    sys.exit()
