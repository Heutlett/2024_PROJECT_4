eval $(minikube docker-env)

# Ejecutar el run.sh de cada microservicio. Agregar una linea por cada microservicio
cd crear_usuario/ && ./run_docker_image.sh && cd ../
cd obtener_usuario/ && ./run_docker_image.sh && cd ../
cd cambiar_contrasena/ && ./run_docker_image.sh && cd ../
cd verificar_usuario/ && ./run_docker_image.sh && cd ../

# Borrar los PODS anteriores
#kubectl scale deployment microrestaurant-service --replicas=0
kubectl delete deployment microrestaurant
kubectl delete service microrestaurant-service

# Subir el POD nuevo con todos los microservicios incluidos
kubectl apply -f multicontainer-deployment.yaml
kubectl apply -f multicontainer-service.yaml