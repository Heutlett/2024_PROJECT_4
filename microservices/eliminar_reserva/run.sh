# Crear docker image en Dockerhub
eval $(minikube docker-env)
docker build -t eliminar-reserva:latest .
docker tag eliminar-reserva:latest jusfb18/eliminar-reserva:latest
docker login
docker push jusfb18/eliminar-reserva:latest

# Borrar el POD anterior
kubectl delete deployment eliminar-reserva
kubectl delete service eliminar-reserva-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml