# Crear docker image en Dockerhub
eval $(minikube docker-env)
docker build -t broker:latest .
docker tag broker:latest jusfb18/broker:latest
docker login
docker push jusfb18/broker:latest

# Borrar el POD anterior
kubectl delete deployment broker
kubectl delete service broker-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml