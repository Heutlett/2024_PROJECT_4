from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)


baseurl = "http://192.168.49.2:"

services = {
    "cambiar-contrasena": f"{baseurl}30007/cambiar-contrasena", # funciona
    "crear-reserva": f"{baseurl}30010/crear-reserva", # funciona
    "crear-usuario": f"{baseurl}30004/crear-usuario", # funciona
    "editar-reserva": f"{baseurl}30012/editar-reserva", # funciona
    "eliminar-reserva":f"{baseurl}30013/eliminar-reserva", # CORREGIR QUE SOLO PARA TOKEN DE ADMIN
    "obtener-reserva-puntual": f"{baseurl}30016/obtener-reserva/", # funciona
    "obtener-reservas-futuras": f"{baseurl}30017/obtener-reserva/", # funciona
    "obtener-reservas-pasadas": f"{baseurl}30015/obtener-reserva/", # REDEPLOY
    "obtener-reservas-todas": f"{baseurl}30014/obtener-reserva/", # REDEPLOY
    "obtener-usuario":f"{baseurl}30005/obtener-usuario", # funciona
    "obtener-calendario": f"{baseurl}puerto/obtener-calendario",
}

# entry point de la cloud function
@app.route('/<service_name>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def broker(service_name):
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)
    
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
        "Content-Type": "application/json"
    }
    

    if service_name in services:
        service_url = services[service_name]

        if request.method == 'GET':
            args = request.args if request.args else {}
            
            # Realizar solicitud GET con parámetros
            if service_name=="obtener-usuario":
                username = args.get('username')
                password = args.get('password')
                service_url += f"?username={username}&password={password}"
            
            if service_name == "obtener-reserva-puntual":
                reservation_id = args.get('reservation_id')
                service_url += f"?reservation_id={reservation_id}"

            if service_name == "obtener-reservas-futuras":
                time = args.get('time')
                token = args.get('token')
                service_url += f"?time={time}&token={token}"
            
            if service_name == "obtener-reservas-pasadas": # CORREGIR USER LOGICA
                time = args.get('time')
                token = args.get('token')
                service_url += f"?time={time}&token={token}"
            
            if service_name == "obtener-reservas-todas": # CORREGIR LOGICA
                time = args.get('time')
                service_url += f"?time={time}"
            
            
            response = requests.get(service_url)

        elif request.method == 'POST':
            try:
                body = request.json if request.json else {}
                response = requests.post(service_url, json=body, headers=headers)
            except:
                return jsonify("Error con los datos"),400,headers
        elif request.method == 'PUT':
            try:
                body = request.json if request.json else {}
                response = requests.put(service_url, json=body, headers=headers)
            except:
                return jsonify("Error con los datos"),400,headers
            
        elif request.method == 'DELETE':
            args = request.args if request.args else {}
            
            # Realizar solicitud DELETE con parámetros
            if service_name=="eliminar-reserva": 
                reservation_id = args.get('reservation_id')
                password = args.get('password')
        
        return response.content, response.status_code,headers
    else:
        # Si el servicio no es encontrado, retornar error 404
        return 'Service not found', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5016, debug=True)