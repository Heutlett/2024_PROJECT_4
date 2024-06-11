# Crear docker image en Dockerhub
eval $(minikube docker-env)
docker build -t obtener-recomendacion:latest .
docker tag obtener-recomendacion:latest jusfb18/obtener-recomendacion:latest
docker login
docker push jusfb18/obtener-recomendacion:latest

# Borrar el POD anterior
kubectl delete deployment obtener-recomendacion
kubectl delete service obtener-recomendacion-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml