# Crear docker image en Dockerhub
eval $(minikube docker-env)
#docker build -t obtener-reserva-puntual:latest .
#docker tag obtener-reserva-puntual:latest jusfb18/obtener-reserva-puntual:latest
#docker login
#docker push jusfb18/obtener-reserva-puntual:latest

# Borrar el POD anterior
kubectl delete deployment obtener-reserva-puntual
kubectl delete service obtener-reserva-puntual-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
