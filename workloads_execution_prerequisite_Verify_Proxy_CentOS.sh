#!/bin/bash
#Verify Proxy is set or not 

echo $http_proxy
echo $https_proxy

#echo "if above commands returns empty results , you need to set proxy on this system. update .bashrc file " 

#curl -fsSL https://get.docker.com -o get-docker.sh
#sh get-docker.sh
#systemctl daemon-reload
#systemctl start docker.service
#systemctl enable docker.service
#systemctl restart docker

#run docker.hello word 
#docker run hello-world