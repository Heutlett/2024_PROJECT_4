# Crear docker image en Dockerhub
eval $(minikube docker-env)
docker build -t obtener-menu:latest .
docker tag obtener-menu:latest jusfb18/obtener-menu:latest
docker login
docker push jusfb18/obtener-menu:latest

# Borrar el POD anterior
kubectl delete deployment obtener-menu
kubectl delete service obtener-menu-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml