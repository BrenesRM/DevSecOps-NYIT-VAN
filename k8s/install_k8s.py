import subprocess

def run_command(command):
    """Run a system command and return the output."""
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"Command succeeded: {command}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}")
        print(e.stderr)

def install_kubernetes():
    """Install Kubernetes and its dependencies on Ubuntu."""
    
    # Update the system
    print("Updating the system...")
    run_command(["sudo", "apt", "update", "-y"])
    run_command(["sudo", "apt", "upgrade", "-y"])

    # Install required dependencies
    print("Installing required dependencies...")
    run_command(["sudo", "apt", "install", "-y", "apt-transport-https", "ca-certificates", "curl", "software-properties-common"])

    # Add Kubernetes GPG key
    print("Adding Kubernetes GPG key...")
    run_command(["curl", "-s", "https://packages.cloud.google.com/apt/doc/apt-key.gpg", "|", "sudo", "apt-key", "add", "-"])

    # Add Kubernetes APT repository
    print("Adding Kubernetes repository...")
    run_command(["sudo", "sh", "-c", 'echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list'])

    # Update apt package list
    print("Updating apt package list...")
    run_command(["sudo", "apt", "update", "-y"])

    # Install kubelet, kubeadm, and kubectl
    print("Installing kubelet, kubeadm, and kubectl...")
    run_command(["sudo", "apt", "install", "-y", "kubelet", "kubeadm", "kubectl"])

    # Hold the packages at their installed versions
    print("Holding Kubernetes packages at their installed versions...")
    run_command(["sudo", "apt-mark", "hold", "kubelet", "kubeadm", "kubectl"])

    # Disable swap (required for Kubernetes)
    print("Disabling swap...")
    run_command(["sudo", "swapoff", "-a"])
    # Make the change permanent
    run_command(["sudo", "sed", "-i", "/swap/d", "/etc/fstab"])

    # Enable and start kubelet service
    print("Enabling and starting kubelet service...")
    run_command(["sudo", "systemctl", "enable", "kubelet"])
    run_command(["sudo", "systemctl", "start", "kubelet"])

    print("Kubernetes installation completed!")

if __name__ == "__main__":
    install_kubernetes()
