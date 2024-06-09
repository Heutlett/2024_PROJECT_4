eval $(minikube docker-env)
cd crear_usuario/ && ./run.sh && cd ../

kubectl scale deployment api-crear-usuario-service --replicas=0
kubectl delete deployment api-crear-usuario-service
kubectl apply -f multicontainer-deployment.yaml
kubectl delete service api-crear-usuario-service
kubectl apply -f multicontainer-service.yaml