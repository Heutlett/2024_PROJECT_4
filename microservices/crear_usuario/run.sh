# Crear imagen en Dockerhub
#eval $(minikube docker-env)
#docker build -t crear-usuario:latest .
#docker tag crear-usuario:latest jusfb18/crear-usuario:latest
#docker login
#docker push jusfb18/crear-usuario:latest

# Borrar el POD anterior
kubectl delete deployment crear-usuario
kubectl delete service crear-usuario-service

# Subir el POD nuevo 
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml