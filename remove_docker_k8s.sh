#!/bin/bash
#remove docker and kubernetes

sudo yum remove -y docker-engine docker docker.io docker-ce docker-ce-cli docker-compose-plugin
sudo rm -f /etc/yum.repos.d/docker-ce.repo

#kubeadm reset 
sudo yum remove -y kubeadm kubectl kubelet kubernetes-cni kube*
sudo rm -f /etc/yum.repos.d/k8s.repo

sudo rm -rf /var/lib/docker /etc/docker
sudo rm -rf /etc/apparmor.d/docker
sudo groupdel docker
sudo rm -rf /var/run/docker.sock
sudo rm -rf /var/run/containerd/containerd.sock
sudo rm -rf ~/.kube