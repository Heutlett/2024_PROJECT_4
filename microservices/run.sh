#!/bin/bash

# Ejecutar broker
cd ../broker
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../microservices

# Obtener calendario
cd ./obtener_calendario
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener usuario
cd ./obtener_usuario
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener menú
cd ./obtener_menu
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Cambiar contraseña
cd ./cambiar_contrasena
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Editar reserva
cd ./editar_reserva
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# General
cd ./General
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener recomendación
cd ./obtener_recomendacion
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener reservas pasadas
cd ./obtener_reservas_pasadas
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener reserva puntual
cd ./obtener_reserva_puntual
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener reservas futuras
cd ./obtener_reservas_futuras
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener reservas todas
cd ./obtener_reservas_todas
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Verificar usuario
cd ./verificar_usuario
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Crear reserva
cd ./crear_reserva
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Eliminar reserva
cd ./eliminar_reserva
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Crear usuario
cd ./crear_usuario
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Feedback chatbot
cd ./feedback-chatbot
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../
