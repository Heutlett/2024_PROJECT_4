# Crear docker image en Dockerhub
eval $(minikube docker-env)
#docker build -t editar-reserva:latest .
#docker tag editar-reserva:latest jusfb18/editar-reserva:latest
#docker login
#docker push jusfb18/editar-reserva:latest

# Borrar el POD anterior
kubectl delete deployment editar-reserva
kubectl delete service editar-reserva-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
