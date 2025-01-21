#!/bin/bash

# Ensure the script is run as root or with sudo
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root or with sudo" 
    exit 1
fi

# Update and install required dependencies
echo "Updating system packages..."
apt-get update -y
apt-get upgrade -y

# Install curl, apt-transport-https, and other utilities
echo "Installing curl and required dependencies..."
apt-get install -y curl apt-transport-https ca-certificates gnupg lsb-release

# Install Docker (required for Kubernetes nodes)
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl enable docker
systemctl start docker

# Install kubeadm, kubelet, and kubectl
echo "Adding Kubernetes repository..."
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list

echo "Updating package lists..."
apt-get update -y

# Install Kubernetes components
echo "Installing Kubernetes components (kubeadm, kubelet, kubectl)..."
apt-get install -y kubelet kubeadm kubectl

# Hold back versions to prevent auto-upgrade
echo "Holding Kubernetes package versions..."
apt-mark hold kubelet kubeadm kubectl

# Disable swap (required by Kubernetes)
echo "Disabling swap..."
swapoff -a
sed -i '/ swap / s/^/#/' /etc/fstab

# Enable and start kubelet service
echo "Starting kubelet..."
systemctl enable kubelet
systemctl start kubelet

# Output versions of installed tools
echo "Docker version:"
docker --version
echo "Kubeadm version:"
kubeadm version
echo "Kubelet version:"
kubelet --version
echo "Kubectl version:"
kubectl version --client

echo "Kubernetes installation is complete!"
