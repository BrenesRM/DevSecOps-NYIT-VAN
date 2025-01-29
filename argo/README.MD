Argo CD Guide

Overview

Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes. It listens to the OPS repository, which contains Kubernetes YAML files, and applies any detected configuration changes to the cluster.

1. Installing ArgoCD

Installation Guide

kubectl create namespace argocd

# Non-HA installation
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl config set-context --current --namespace=argocd
watch kubectl get pods

Optional: High Availability (HA) Setup

HA Installation Guide

2. UI Access

2.1. Option 1: NodePort

Create a NodePort service:

File: nodeport.yaml

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

Apply the configuration:

kubectl apply -f nodeport.yaml
kubectl get svc
kubectl describe svc argo-nodeport

2.2. Option 2: Port-forward (Local Cluster)

kubectl -n argocd port-forward $(kubectl -n argocd get pod -l app.kubernetes.io/name=argocd-server -o jsonpath='{.items[0].metadata.name}') 8080:8080

3. Generate Admin Password

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo

3.1. Install ArgoCD CLI

sudo curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo chmod +x /usr/local/bin/argocd

Alternatively, use Homebrew:

brew install argocd

3.2. CLI Login

argocd login <DOMAIN>:30080 --insecure --grpc-web --username admin --password <ADMIN_PASSWORD>

For port-forwarding:

argocd login --port-forward

3.2.1. Test CLI

argocd app list

4. Set New Repository (UI)

Navigate to Settings → Repositories

Connect Repo Using SSH (Git "OPS" repo)

Name: ops

Project: default

GitHub SSH URL: git@github.com:<user>/<project>.git

Private Key: cat ~/.ssh/id_rsa

5. Create Application

Sync Options

5.1. Option 1: UI

Applications → Create Application

Name: stage-public-api

Sync Automated

Prune: true

SelfHeal: true

Auto-create Namespace

Repository URL: git@github.com:<user>/<project>.git

Path: public-api/overlays/stage/

Cluster URL: https://kubernetes.default.svc

Namespace: public-stage

5.2. View YAML and Copy

Paste into: ops/argo-apps/public-api-stage.yaml

5.3. Create Application

Check App Status, App Diagram, App Details, Pod Details, and Sync Status

Sync Forced

Ingress Progressing Issues

5.4. Manual Scaling

kubectl scale --replicas 1 deploy public-api -n public-stage

5.5. Edit Replicas in GitHub

git add .
git commit -m "update deployment replicas"
git push origin main

5.6. Check ArgoCD UI Applications

5.7. Sync Git Repository

argocd app sync --project default
argocd app sync stage-public-api

5.8. Check Pods Running 2 Replicas

Wait 3 minutes for auto-sync.

argocd app sync <APP_NAME>

5.9. Useful Commands

kubectl get application -A
argocd app list
argocd app get <APP_NAME>
argocd app history <APP_NAME>
argocd app delete <APP_NAME>

6. Optional: App of Apps Pattern

New Folder in OPS Repo: /argo-apps

Add stage-public-api.yaml to /argo-apps

Commit & Push to GitHub

Delete stage-public-api Argo Application

Create a New Application: argo-apps

Name: argo-apps

Project: default

Sync: auto

Prune: true

Self Heal: true

Path: argo-apps

Namespace: argocd

Copy and paste the YAML configuration to /argo-apps/app-of-apps.yaml.

7. Optional: Expose Argo via Ingress

YAML Configuration
GKE Load Balancer

8. Optional: Administration

8.1. User Management

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

8.4. Disable Admin User

Modify cm-users.yaml:

admin.enabled: "false"

8.5. Logout & Login as New User