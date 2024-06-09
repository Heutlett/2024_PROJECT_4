eval $(minikube docker-env)
docker build -t verificar-usuario:latest .
docker tag verificar-usuario:latest jusfb18/verificar-usuario:latest
docker login
docker push jusfb18/verificar-usuario:latest