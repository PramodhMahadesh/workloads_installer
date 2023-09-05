import subprocess
import os
import datetime


STRESSNG_INSTALLATION_STATUS = "N/A"
STRESSNG_INSTALLED_VERSION = "N/A"
STRESSNG_SANITY_STATUS = "N/A"
CWD = os.path.dirname(__file__)
INSTALLATION_STATUS_LOG = f"{CWD}/Installations.log"


def check_stressng():
    if not os.path.isdir("/root/stress-ng"):
        print("Stress-ng folder not found.")
        return False
    else:
        os.chdir("/root/stress-ng")
        out = subprocess.run(["./stress-ng","--version"],stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.decode()
        if "version" not in out:
            print("Stress-ng not installed properly")
            return False
        else:
            version = out.split(" ")[out.split(" ").index("version") + 1]
            print(f"Current stress-ng version: {version}")
            global STRESSNG_INSTALLATION_STATUS, STRESSNG_INSTALLED_VERSION
            STRESSNG_INSTALLATION_STATUS = "INSTALLED"
            STRESSNG_INSTALLED_VERSION = version
            return True
        
def run_sanity():
    logfile = "sanity.txt"
    os.system("rm -rf sanity.txt")
    test_command = f"./stress-ng --ioport 40 --ioport-opts inout --iomix 40 --lockbus-nosplit --oom-avoid -v --iostat 120 --times --tz --vmstat 120 --thermalstat 120 --metrics --klog-check --timestamp -t 1m --log-file {logfile}"
    os.chdir("/root/stress-ng")
    os.system(test_command)
    with open(logfile,'r') as f:
        lines = f.readlines()
        if "unsuccessful" in lines[-1].strip() or "unsuccessful" in lines[-2].strip():
            print("Sanity test failed")
            return False
        elif "successful" in lines[-1].strip() or "successful" in lines[-2].strip():
            print("Sanity test passed")
            os.system("rm -rf sanity.txt")
            global STRESSNG_SANITY_STATUS
            STRESSNG_SANITY_STATUS = "PASS"
            return True
        else:
            print("Test status could not be determined")
            return False

def update_installation_status():
   global timestamp, INSTALLATION_STATUS_LOG
   timestamp = datetime.datetime.now().strftime("%d/%m/%Y -- %H:%M:%S")
   with open(INSTALLATION_STATUS_LOG,'a') as f:
      f.write("\n************************************************************************")
      f.write(f"\nRecent install on {timestamp}")
      f.write("\n{:<10} {:<20} {:<20} {:<15}".format("WORKLOAD","INSTALLATION STATUS","INSTALLED VERSION","SANITY TEST"))
      f.write("\n{:<10} {:<20} {:<20} {:<15}".format("STRESS-NG",STRESSNG_INSTALLATION_STATUS,STRESSNG_INSTALLED_VERSION,STRESSNG_SANITY_STATUS))
      f.write("\n")

def print_installation_status():
    print("\n************************************************************************")
    print(f"\nRecent install on {timestamp}")
    print("\n{:<10} {:<20} {:<20} {:<15}".format("WORKLOAD","INSTALLATION STATUS","INSTALLED VERSION","SANITY TEST"))
    print("\n{:<10} {:<20} {:<20} {:<15}".format("STRESS-NG",STRESSNG_INSTALLATION_STATUS,STRESSNG_INSTALLED_VERSION,STRESSNG_SANITY_STATUS))
    print("\n") 


if check_stressng():
    run_sanity()
    update_installation_status()
    print_installation_status()
else:
    print("Error with stress-ng installation")
    update_installation_status()
    print_installation_status()
