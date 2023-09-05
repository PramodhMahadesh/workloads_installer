#!/bin/bash
#Download Intel Certificates


sudo systemctl stop docker-ce
sudo systemctl stop containerd
sudo yum remove docker-ce docker-ce-cli docker-compose-plugin containerd runc -y
yum erase podman buildah -y
# rm -f /etc/yum.repos.d/docker-ce.repo
# rm -f /etc/yum.repos.d/k8s.repo

curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl daemon-reload
systemctl start docker.service
#systemctl status docker.service


#systemctl restart docker
docker info 



#Method 2 
#sudo yum install -y yum-utils
#sudo yum-config-manager \
#    --add-repo \
#    https://download.docker.com/linux/centos/docker-ce.repo
	
#sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin '--allowerasing' '--skip-broken' '--nobest'
	
#run docker.hello word 
#docker run hello-world
