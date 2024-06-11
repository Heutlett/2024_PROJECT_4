#!/bin/bash

# Ejecutar broker
cd ../broker
kubectl delete deployment obroker
kubectl delete service broker-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../microservices

# Obtener calendario
cd ./obtener_calendario
kubectl delete deployment obtener-calendario
kubectl delete service obtener-calendario-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener usuario
cd ./obtener_usuario
kubectl delete deployment obtener-usuario
kubectl delete service obtener-usuario-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener menú
cd ./obtener_menu
kubectl delete deployment obtener-menu
kubectl delete service obtener-menu-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Cambiar contraseña
cd ./cambiar_contrasena
kubectl delete deployment cambiar-contrasena
kubectl delete service cambiar-contrasena-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Editar reserva
cd ./editar_reserva
kubectl delete deployment editar-reserva
kubectl delete service editar-reserva-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# General
cd ./General
kubectl delete deployment general
kubectl delete service general-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener recomendación
cd ./obtener_recomendacion
kubectl delete deployment obtener-recomendacion
kubectl delete service obtener-recomendacion-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener reservas pasadas
cd ./obtener_reservas_pasadas
kubectl delete deployment obtener-reservas-pasadas
kubectl delete service obtener-reservas-pasadas-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener reserva puntual
cd ./obtener_reserva_puntual
kubectl delete deployment obtener-reserva-puntual
kubectl delete service obtener-reserva-puntual-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener reservas futuras
cd ./obtener_reservas_futuras
kubectl delete deployment obtener-reservas-futuras
kubectl delete service obtener-reservas-futuras-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Obtener reservas todas
cd ./obtener_reservas_todas
kubectl delete deployment obtener-reservas-todas
kubectl delete service obtener-reservas-todas-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Verificar usuario
cd ./verificar_usuario
kubectl delete deployment verificar-usuario
kubectl delete service verificar-usuario-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Crear reserva
cd ./crear_reserva
kubectl delete deployment crear-reserva
kubectl delete service crear-reserva-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Eliminar reserva
cd ./eliminar_reserva
kubectl delete deployment eliminar-reserva
kubectl delete service eliminar-reserva-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Crear usuario
cd ./crear_usuario
kubectl delete deployment crear-usuario
kubectl delete service crear-usuario-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../

# Feedback chatbot
cd ./feedback-chatbot
kubectl delete deployment feedback-chatbot
kubectl delete service feedback-chatbot-service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
cd ../
