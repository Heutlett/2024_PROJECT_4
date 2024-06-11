eval $(minikube docker-env)
docker build -t feedback-chatbot:latest .
docker tag obtener-menu:latest jusfb18/obtener-menu:latest
docker login
docker push jusfb18/obtener-menu:latest