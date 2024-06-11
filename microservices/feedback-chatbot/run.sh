# Crear docker image en Dockerhub
eval $(minikube docker-env)
docker build -t feedback-chatbot:latest .
docker tag feedback-chatbot:latest jusfb18/feedback-chatbot:latest
docker login
docker push jusfb18/feedback-chatbot:latest

# Borrar el POD anterior
kubectl delete deployment feedback-chatbot
kubectl delete service feedback-chatbot-service

# Subir el POD nuevo
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml