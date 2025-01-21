#!/bin/bash

# Update apt package list
sudo apt update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install kind if architecture is x86_64
if [ $(uname -m) = x86_64 ]; then
  curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
  chmod +x ./kind
  sudo mv ./kind /usr/local/bin/kind
fi

# Verify kind installation
kind version

# Install kubectl using snap
sudo snap install kubectl --classic
