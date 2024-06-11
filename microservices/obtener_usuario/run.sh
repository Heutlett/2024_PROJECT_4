# Crear imagen en Dockerhub
eval $(minikube docker-env)
#docker build -t obtener-usuario:latest .
#docker tag obtener-usuario:latest jusfb18/obtener-usuario:latest
#docker login
#docker push jusfb18/obtener-usuario:latest

# Borrar el POD anterior
kubectl delete deployment obtener-usuario
kubectl delete service obtener-usuario-service

# Subir el POD nuevo 
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
