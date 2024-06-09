# Crear imagen en Dockerhub
eval $(minikube docker-env)
docker build -t cambiar-contrasena:latest .
docker tag cambiar-contrasena:latest jusfb18/cambiar-contrasena:latest
docker login
docker push jusfb18/cambiar-contrasena:latest

# Borrar el POD anterior
kubectl delete deployment cambiar-contrasena
kubectl delete service cambiar-contrasena-service

# Subir el POD nuevo 
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml