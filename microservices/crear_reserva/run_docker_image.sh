eval $(minikube docker-env)
docker build -t crear-reserva:latest .
docker tag crear-reserva:latest jusfb18/crear-reserva:latest
docker login
docker push jusfb18/crear-reserva:latest