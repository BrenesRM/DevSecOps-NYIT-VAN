Argo CD Setup and Configuration

Overview

Core Concepts

Argo CD listens to the OPS repository, which contains Kubernetes YAML files. When it detects changes in the configuration, it applies those changes to the cluster.

1. Install ArgoCD

Installation Guide

kubectl create namespace argocd

# Non-HA Installation
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl config set-context --current --namespace=argocd
watch kubectl get pods

Optional: High Availability (Production)

HA Installation

2. UI Access

2.1. Option 1: NodePort

Create nodeport.yaml:

apiVersion: v1
kind: Service
metadata:
    name: argo-nodeport
    namespace: argocd
spec:
  ports:
  - protocol: TCP
    port: 8080
    nodePort: 30080
    targetPort: 8080
  selector:
    app.kubernetes.io/name: argocd-server
  type: NodePort

Apply and verify:

kubectl apply -f nodeport.yaml
kubectl get svc
kubectl describe svc argo-nodeport

2.2. Option 2: Port-Forward (Local Cluster)

kubectl -n argocd port-forward $(kubectl -n argocd get pod -l app.kubernetes.io/name=argocd-server -o jsonpath='{.items[0].metadata.name}') 8080:8080

3. Generate Admin Password

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo

3.1. Install ArgoCD CLI

sudo curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo chmod +x /usr/local/bin/argocd

Or using Homebrew:

brew install argocd

3.2. CLI Login

argocd login <DOMAIN>:30080 --insecure --grpc-web --username admin --password <ADMIN_PASSWORD>

Or using port-forward:

argocd login --port-forward

3.2.1. Test CLI

argocd app list

4. Set New Repository (UI)

Navigate to Settings → Repositories

Connect the OPS repository using SSH

Name: ops

Project: default

GitHub SSH URL: git@github.com:<user>/<project>.git

Private Key: cat ~/.ssh/id_rsa

5. Create Application

Sync Options

5.1. Option 1: UI

Navigate to Applications → Create Application

Name: stage-public-api

Sync: Automated

Prune: True

SelfHeal: True

Auto-create namespace

Repository URL: git@github.com:<user>/ops.git

Path: public-api/overlays/stage/

Cluster URL: https://kubernetes.default.svc

Namespace: public-stage

5.2. View YAML and Copy

Paste into ops/argo-apps/public-api-stage.yaml

5.3. Create Application

Check App Status, Diagram, and Details

Check Pod Details and Sync Status

Force Sync if necessary

Ingress Progressing Troubleshooting

5.4. Manual Scaling

kubectl scale --replicas 1 deploy public-api -n public-stage

5.5. Edit Replicas in GitHub

git add .
git commit -m "Update deployment replicas"
git push origin main

5.6. Check ArgoCD UI Applications

5.7. Sync Git Repo

argocd app sync --project default
# OR
argocd app sync stage-public-api

5.8. Check Running Pods

Wait ~3 minutes for auto-sync.

argocd app sync <APP_NAME>

5.9. Useful Commands

kubectl get application -A
argocd app list
argocd app get <APP_NAME>
argocd app history <APP_NAME>
argocd app delete <APP_NAME>

6. Optional: App of Apps Pattern

Create a new folder in the OPS repo: /argo-apps

Add stage-public-api.yaml to /argo-apps

Commit & Push changes to GitHub

Delete stage-public-api Argo application

Create a new application named argo-apps

Repository Path: argo-apps

Namespace: argocd

Sync Auto, Prune, Self-Heal enabled

7. Optional: Expose Argo via Ingress

Ingress YAML

8. Optional: Administration

8.1. Users

User Management
RBAC

kubectl get cm argocd-cm
argocd login --port-forward
argocd account list --port-forward

8.2. Login UI

URL: localhost:8080

Username: admin

8.3. Create Users & Roles

kubectl apply -f assets/argo/cm-users.yaml
argocd account update-password --account <name> --current-password <admin-password> --new-password <new-user-password> --port-forward

kubectl get cm argocd-rbac-cm
kubectl apply -f assets/argo/argocd-rbac-cm.yaml

8.4. Disable Admin User

Edit cm-users.yaml:

admin.enabled: "false"

8.5. Logout and Login with New User