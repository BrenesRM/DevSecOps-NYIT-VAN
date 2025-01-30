Option B: Using the Web UI
Go to the Argo CD web UI (usually at https://<ARGO_CD_SERVER>:8080).
Log in using your admin credentials.
In the left-hand menu, click on Settings (the gear icon).
Click Repositories under the Settings menu.
Click the Connect Repo button.
Choose Git as the repository type.
Enter your GitHub repository URL, and provide your GitHub username and token for authentication.
Click Connect to add the repository.


kubectl get apps -n argocd

argocd app sync --project default

kubectl get svc
kubectl describe svc argo-nodeport
argocd app list
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo

argocd app get devsecops-nyit-van
argocd app resources devsecops-nyit-van
argocd app history devsecops-nyit-van

kubectl get namespaces

