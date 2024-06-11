# Crear docker image en Dockerhub
eval $(minikube docker-env)
docker build -t crear-reserva:latest .
docker tag crear-reserva:latest jusfb18/crear-reserva:latest
docker login
docker push jusfb18/crear-reserva:latest

# Borrar el POD anterior
kubectl delete deployment crear-reserva
kubectl delete service crear-reserva-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml