# Crear docker image en Dockerhub
eval $(minikube docker-env)
docker build -t obtener-reserva:latest .
docker tag obtener-reserva:latest jusfb18/obtener-reserva:latest
docker login
docker push jusfb18/obtener-reserva:latest

# Borrar el POD anterior
kubectl delete deployment obtener-reserva
kubectl delete service obtener-reserva-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml