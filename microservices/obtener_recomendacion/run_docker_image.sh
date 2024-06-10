eval $(minikube docker-env)
docker build -t obtener-recomendacion:latest .
docker tag obtener-recomendacion:latest jusfb18/obtener-recomendacion:latest
docker login
docker push jusfb18/obtener-recomendacion:latest