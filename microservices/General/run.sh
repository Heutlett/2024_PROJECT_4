# Ejecutar el run.sh de cada microservicio. Agregar una linea por cada microservicio
cd ../crear_usuario/ && ./run_docker_image.sh && cd ../
cd ../obtener_usuario/ && ./run_docker_image.sh && cd ../
cd ../cambiar_contrasena/ && ./run_docker_image.sh && cd ../
cd ../verificar_usuario/ && ./run_docker_image.sh && cd ../
cd ../crear_reserva/ && ./run_docker_image.sh && cd ../
