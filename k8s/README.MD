# Kubernetes Environment Setup

## Table of Contents
- [1. Create and Configure the VM](#1-create-and-configure-the-vm)
- [2. Install Kubernetes](#2-install-kubernetes)
  - [2.1. Install Kind](#21-install-kind)
  - [2.2. Install Kubectl](#22-install-kubectl)
- [3. Create Cluster](#3-create-cluster)
  - [3.1. Create the `kind-cluster.yaml` file](#31-create-the-kind-clusteryaml-file)
  - [3.2. Create the cluster](#32-create-the-cluster)
- [4. Check Cluster Status](#4-check-cluster-status)

## 1. Create and Configure the VM

Before proceeding, ensure your virtual machine (VM) is set up and running.

## 2. Install Kubernetes

### 2.1. Install Docker
Run the following commands to install Docker:
```sh
sudo apt update
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo usermod -aG docker $USER
newgrp docker
```

### Verify the Installation
```sh
docker info
```

### 2.1. Install Kind
```sh
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

kind version
```

### 2.2. Install Kubectl
```sh
sudo snap install kubectl --classic
```

## 3. Create Cluster

### 3.1. Create the `kind-cluster.yaml` file
Create a new file `kind-cluster.yaml` with the following configuration:

```yaml
apiVersion: kind.x-k8s.io/v1alpha4
kind: Cluster
name: demo
nodes:
  - role: control-plane
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:
      - containerPort: 80
        hostPort: 80
        protocol: TCP
      - containerPort: 443
        hostPort: 443
        protocol: TCP
      - containerPort: 30080
        hostPort: 30080
        protocol: TCP
      - containerPort: 30081
        hostPort: 30081
        protocol: TCP
      - containerPort: 8080  # Jenkins Web UI
        hostPort: 8080
        protocol: TCP
      - containerPort: 5000  # ArgoCD UI
        hostPort: 5000
        protocol: TCP
  - role: worker
  - role: worker
  - role: worker
```

### 3.2. Create the Cluster
Run the following command to create the cluster:
```sh
kind create cluster --config kind-cluster.yaml
```

Verify the cluster information:
```sh
kubectl cluster-info --context kind-demo
```
Expected output:
```
Kubernetes control plane is running at https://127.0.0.1:41513
CoreDNS is running at https://127.0.0.1:41513/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

## 4. Check Cluster Status
Run the following command to check node status:
```sh
kubectl get nodes
```
Expected output:
```
NAME                 STATUS   ROLES           AGE     VERSION
kind-control-plane   Ready    control-plane   6m40s   v1.27.3
kind-worker          Ready    <none>          6m12s   v1.27.3
kind-worker2         Ready    <none>          6m12s   v1.27.3
kind-worker3         Ready    <none>          6m13s   v1.27.3
```

Your Kubernetes environment is now set up and ready for use!


Install MetalLB (LoadBalancer for Kind)

kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.7/config/manifests/metallb-native.yaml

Wait for MetalLB to be ready:

kubectl get pods -n metallb-system

Create a MetalLB IP Pool

nano metallb-config.yaml

apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
    - 192.168.1.100-192.168.1.200
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: first-advertisement
  namespace: metallb-system
cat: cat: No such file or directory
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
    - 192.168.1.100-192.168.1.200
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: first-advertisement
  namespace: metallb-system


Deploy Web Test App.

kubectl apply -f web-test.yaml

kubectl get svc web-test-service

kubectl run test --rm -it --image=alpine -- sh
apk add curl
curl web-test-service

kubectl get pods -n metallb-system


Test Localy.

http://10.0.0.10:30080/


another test:

kubectl run -it --rm debug --image=busybox --restart=Never -- sh
wget -O- http://10.96.129.181  # Test ClusterIP
wget -O- http://192.168.1.100  # Test LoadBalancer
