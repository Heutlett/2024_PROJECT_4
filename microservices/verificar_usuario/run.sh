# Crear imagen en Dockerhub
eval $(minikube docker-env)
docker build -t verificar-usuario:latest .
docker tag verificar-usuario:latest jusfb18/verificar-usuario:latest
docker login
docker push jusfb18/verificar-usuario:latest

# Borrar el POD anterior
kubectl delete deployment verificar-usuario
kubectl delete service verificar-usuario-service

# Subir el POD nuevo 
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml