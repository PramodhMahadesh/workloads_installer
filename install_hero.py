import subprocess
import os
import functions

functions.init()
functions.read_details(functions.INI_FILE)
functions.check_proxy()
functions.clone_git()
os.chdir(functions.CWD)

subprocess.run([f"./{functions.INSTALL_APPS_SCRIPT}"])
subprocess.run([f"./{functions.INSTALL_CERT_SCRIPT}"]) 

functions.get_docker()

functions.add_ip_username()

functions.install_setup_dev()
functions.install_setup_reg()
functions.install_setup_docker()
functions.install_setup_k8s()
functions.update_build_username()
subprocess.run([f"./{functions.BUILD_SCRIPT}"])
functions.check_build()
functions.update_installation_status()
functions.print_installation_status()