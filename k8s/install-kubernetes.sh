#!/bin/bash

# Update the system
echo "Updating the system..."
sudo apt update -y && sudo apt upgrade -y

# Install dependencies
echo "Installing required dependencies..."
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Kubernetes' official GPG key
echo "Adding Kubernetes GPG key..."
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# Add Kubernetes APT repository
echo "Adding Kubernetes repository..."
sudo sh -c 'echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list'

# Update apt package list
echo "Updating apt package list..."
sudo apt update -y

# Install kubelet, kubeadm, and kubectl
echo "Installing kubelet, kubeadm, and kubectl..."
sudo apt install -y kubelet kubeadm kubectl

# Hold the packages at their installed versions
echo "Holding Kubernetes packages at their installed versions..."
sudo apt-mark hold kubelet kubeadm kubectl

# Disable swap (required for Kubernetes)
echo "Disabling swap..."
sudo swapoff -a
# To make the change permanent
sudo sed -i '/swap/d' /etc/fstab

# Enable kubelet service
echo "Enabling kubelet service..."
sudo systemctl enable kubelet && sudo systemctl start kubelet

echo "Kubernetes installation completed!"
