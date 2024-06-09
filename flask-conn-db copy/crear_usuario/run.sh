eval $(minikube docker-env)
docker build -t crear-usuario:latest .
docker tag crear-usuario:latest jusfb18/crear-usuario:latest
docker login
docker push jusfb18/crear-usuario:latest

#kubectl scale deployment test-api --replicas=0
#kubectl delete deployment test-api
#kubectl apply -f multicontainer-deployment.yaml
#kubectl delete service test-api
#kubectl apply -f multicontainer-service.yaml