Remember to modiffied:

In Settings in the project change:

1.Action.
2.Workflow permissions
a.Read and write permissions
b.Allow GitHub Actions to create and approve pull requests

To fix. resource in use. in the building the pipeline. Error in fork used.

Fix ArgosCD

kubectl get pods
kubectl delete pod argocd-server-74b5b78785-nlhvb (Name pods down)
kubectl get deployment argocd-server -o yaml (in the directory of the yml location)
kubectl get pods
argocd login 127.0.0.1:30080  --insecure --grpc-web --username admin --password mvYfugFrz5z1NGGC
kubectl logs argocd-server-74b5b78785-xc79p

SSH status

sudo service ssh status
sudo systemctl start ssh


-----------------------------------------------------------------------------------------

week 1 - 20-01-2025.

Introduction of the course and sylabus.

week 2 - 27-01-2025.

Feedback from professor:

Review and research pass work academics to find chalanges they already have done.
chalanges, tools, what people have done, from the research perspective.

test