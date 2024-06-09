eval $(minikube docker-env)


kubectl scale deployment microrestaurant-service --replicas=0
kubectl delete deployment sqlserver
kubectl delete service sqlserver-service-service

kubectl apply -f sqlserver-deployment.yaml
kubectl apply -f sqlserver-service.yaml