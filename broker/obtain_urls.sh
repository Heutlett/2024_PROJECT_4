#!/bin/bash

echo "Obteniendo los nombres de los servicios..."
# Obtener los nombres de los servicios
services=$(kubectl get services -o jsonpath='{.items[*].metadata.name}')

# Inicializar un JSON vacío
json_output="{"

# Iterar sobre cada servicio para obtener su URL
for service in $services; do
    echo "Obteniendo la URL para el servicio: $service"
    # Obtener la URL del servicio
    url=$(minikube service $service --url 2>/dev/null)
    
    # Verificar si la URL comienza con "http"
    if [[ $url == http* ]]; then
        echo "URL obtenida: $url"
        json_output+="\"$service\":\"$url\","
        
        echo "Se obtuvo la URL para el servicio: $service. Matando procesos colgados..."
        # Si no se puede obtener la URL, matar cualquier proceso que se haya quedado colgado
        pkill -f "minikube service $service --url"
    fi
done

# Eliminar la última coma y cerrar el JSON
json_output=${json_output%,}
json_output+="}"

echo "Guardando el JSON en el archivo service_urls.json"
# Guardar el JSON en un archivo
echo $json_output > service_urls.json

echo "Las URLs de los servicios se han guardado en service_urls.json"
