eval $(minikube docker-env)
docker build -t obtener-menu:latest .
docker tag obtener-menu:latest jusfb18/obtener-menu:latest
docker login
docker push jusfb18/obtener-menu:latest