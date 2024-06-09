eval $(minikube docker-env)
docker build -t crear-usuario:latest .
docker tag crear-usuario:latest jusfb18/crear-usuario:latest
docker login
docker push jusfb18/crear-usuario:latest