# Crear docker image en Dockerhub
eval $(minikube docker-env)
docker build -t obtener-reservas-pasadas:latest .
docker tag obtener-reservas-pasadas:latest jusfb18/obtener-reservas-pasadas:latest
docker login
docker push jusfb18/obtener-reservas-pasadas:latest

# Borrar el POD anterior
kubectl delete deployment obtener-reservas-pasadas
kubectl delete service obtener-reservas-pasadas-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml