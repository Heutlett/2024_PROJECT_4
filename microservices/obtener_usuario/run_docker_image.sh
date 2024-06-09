eval $(minikube docker-env)
docker build -t obtener-usuario:latest .
docker tag obtener-usuario:latest jusfb18/obtener-usuario:latest
docker login
docker push jusfb18/obtener-usuario:latest