#!/bin/python3

import subprocess

def install_docker():
  """Installs Docker on the system."""
  print("Updating apt package list...")
  subprocess.run(["apt", "update"])  # No sudo needed for apt update

  print("Downloading Docker installation script...")
  subprocess.run(["curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"])

  print("Installing Docker...")
  # Explicitly check for presence of sudo before running the command
  if subprocess.run(["which", "sudo"], capture_output=True).returncode == 0:
    subprocess.run(["sudo", "sh", "get-docker.sh"])
  else:
    print("Warning: 'sudo' not found. You may need to run this script with sudo privileges to install Docker.")

  print("Adding user to docker group...")
  # Check for sudo and run accordingly
  if subprocess.run(["which", "sudo"], capture_output=True).returncode == 0:
    subprocess.run(["sudo", "usermod", "-aG", "docker", "$USER"])
    subprocess.run(["sudo", "newgrp", "docker"])
  else:
    print("Warning: 'sudo' not found. You may need to manually add your user to the docker group after installation.")

def install_kind():
  """Installs Kind if the architecture is x86_64."""
  if subprocess.run(["uname", "-m"], capture_output=True).stdout.decode().strip() == "x86_64":
    print("Downloading Kind...")
    subprocess.run(["curl", "-Lo", "./kind", "https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64"])

    print("Making Kind executable...")
    subprocess.run(["chmod", "+x", "./kind"])

    print("Moving Kind to /usr/local/bin...")
    subprocess.run(["sudo", "mv", "./kind", "/usr/local/bin/kind"])

def install_kubectl():
  """Installs kubectl using snap."""
  print("Installing kubectl using snap...")
  subprocess.run(["sudo", "snap", "install", "kubectl", "--classic"])

def main():
  """Installs Kubernetes and its dependencies."""
  install_docker()
  install_kind()
  install_kubectl()

if __name__ == "__main__":
  main()