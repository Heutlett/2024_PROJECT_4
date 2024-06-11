# Crear docker image en Dockerhub
eval $(minikube docker-env)
docker build -t obtener-calendario:latest .
docker tag obtener-calendario:latest menaleon/obtener-calendario:latest
docker login
docker push menaleon/obtener-calendario:latest

# Borrar el POD anterior
kubectl delete deployment obtener-calendario
kubectl delete service obtener-calendario-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml