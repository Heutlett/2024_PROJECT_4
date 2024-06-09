eval $(minikube docker-env)
docker build -t cambiar-contrasena:latest .
docker tag cambiar-contrasena:latest jusfb18/cambiar-contrasena:latest
docker login
docker push jusfb18/cambiar-contrasena:latest