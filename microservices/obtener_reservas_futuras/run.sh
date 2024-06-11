# Crear docker image en Dockerhub
eval $(minikube docker-env)
docker build -t obtener-reservas-futuras:latest .
docker tag obtener-reservas-futuras:latest jusfb18/obtener-reservas-futuras:latest
docker login
docker push jusfb18/obtener-reservas-futuras:latest

# Borrar el POD anterior
kubectl delete deployment obtener-reservas-futuras
kubectl delete service obtener-reservas-futuras-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml