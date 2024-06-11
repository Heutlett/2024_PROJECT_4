# Crear docker image en Dockerhub
eval $(minikube docker-env)
docker build -t obtener-reservas-todas:latest .
docker tag obtener-reservas-todas:latest jusfb18/obtener-reservas-todas:latest
docker login
docker push jusfb18/obtener-reservas-todas:latest

# Borrar el POD anterior
kubectl delete deployment obtener-reservas-todas
kubectl delete service obtener-reservas-todas-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml