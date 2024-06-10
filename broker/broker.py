from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

base_url = "http://192.168.49.2:"

metodos = {}

# GET

metodos["obtener-reserva-puntual"] = {
    "url":f"{base_url}30016/obtener-reserva-puntual",
    "method":"GET"
}
metodos["obtener-usuario"] = {
    "url": f"{base_url}30005/",
    "method": "GET"
}


def hacer_metodo(metodo, data):
    if metodo == "GET":
        response = requests.get(metodos[data["method"]]["url"])
    elif metodo == "POST":
        response = requests.post(metodos[data["method"]]["url"], json=data)
    elif metodo == "PUT":
        response = requests.put(metodos[data["method"]]["url"], json=data)
    elif metodo == "DELETE":
        response = requests.delete(metodos[data["method"]]["url"])
    if response.status_code == 200:
        data = response.json()
        return jsonify(data), 200
    elif response.status_code != 500:
        response_data = response.json()
        return jsonify(response_data), response.status_code
    else:
        error_message = {'error': 'No se pudo obtener los datos de la API'}
        return jsonify(error_message), 500


# entry point de la cloud function
@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def broker():
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
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
    }

    print("Request: ", request)
    request_json = request.get_json(silent=True)
    request_args = request.args
    path = request.path
    respuesta = {}
    print(f"Path: {path}, Method: {request.method}, Request: {request_json}, Args: {request_args}, Headers: {request.headers}")

    if request.method == "GET":
        try:
            if path == "/":
                try:
                    username = request_args.get("username")
                    password = request_args.get("password")
                except Exception as e:
                    respuesta = {
                        "data": "",
                        "status": 400,
                        "message": "Error: Parametro 'username' o 'password' no encontrado."
                    }
                    return jsonify(respuesta), 400, headers
                resultado,status_code = hacer_metodo(metodos["obtener-usuario"]["method"], f"{metodos['obtener-usuario']['url']}?username={username}&password={password}")
                return jsonify(resultado), status_code, headers
            else:
                respuesta = {
                    "data": "",
                    "status": 400,
                    "message": "Bad Request. Método no válido"
                }
                return jsonify(respuesta), 400, headers
        except Exception as e:
            respuesta = {
                "data": "",
                "status": 400,
                "message": "Error: " + str(e)
            }
            return jsonify(respuesta), 400, headers
    elif request.method == "POST":
        try:
            if path == "/broker" and request_json["data"]["method"] == "restablecer-password":
                return jsonify({"response": "Contraseña restablecida"}), 200, headers
            elif path == "/broker" and request_json["data"]["method"] == "crear-usuario":
                return jsonify({"response": "Usuario creado"}), 200, headers
            else:
                respuesta = {
                    "data": "",
                    "status": 400,
                    "message": "Bad Request. Método no válido"
                }
                return jsonify(respuesta), 400, headers
        except Exception as e:
            respuesta = {
                "data": "",
                "status": 400,
                "message": "Error: " + str(e)
            }
            return jsonify(respuesta), 400, headers
    elif request.method == "PUT":
        try:
            if path == "/broker" and request_json["data"]["method"] == "actualizar-usuario":
                return jsonify({"response": "Usuario actualizado"}), 200, headers
            else:
                respuesta = {
                    "data": "",
                    "status": 400,
                    "message": "Bad Request. Método no válido"
                }
                return jsonify(respuesta), 400, headers
        except Exception as e:
            respuesta = {
                "data": "",
                "status": 400,
                "message": "Error: " + str(e)
            }
            return jsonify(respuesta), 400, headers
    elif request.method == "DELETE":
        try:
            if path == "/broker" and request_args.get("method") == "eliminar-usuario":
                return jsonify({"response": "Usuario eliminado"}), 200, headers
            else:
                respuesta = {
                    "data": "",
                    "status": 400,
                    "message": "Bad Request. Método no válido"
                }
                return jsonify(respuesta), 400, headers
        except Exception as e:
            respuesta = {
                "data": "",
                "status": 400,
                "message": "Error: " + str(e)
            }
            return jsonify(respuesta), 400, headers
    else:
        respuesta = {
            "data": "",
            "status": 400,
            "message": "Bad Request. Método no válido"
        }
        return jsonify(respuesta), 400, headers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5016, debug=True)
