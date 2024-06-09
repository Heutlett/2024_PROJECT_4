@echo off
REM Build the Docker image
docker build -t test-app:latest .


REM Apply the Kubernetes deployment
kubectl apply -f flask-deployment.yaml