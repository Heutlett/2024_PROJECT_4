eval $(minikube docker-env)
docker build -t test-api:latest .
docker tag test-api:latest menaleon/test-api:latest
docker login
docker push menaleon/test-api:latest
kubectl apply -f test-api-deployment.yaml
kubectl apply -f test-api-service.yaml