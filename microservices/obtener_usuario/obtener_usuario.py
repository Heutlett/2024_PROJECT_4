import json
import hashlib
import pyodbc
from flask import Flask, jsonify, request
from datetime import datetime, timedelta, timezone
import jwt

app = Flask(__name__)

def getconn():
    server = 'sqlserver-service' # ESTO DEBE SER EL IP Y PUERTO DE TU SERVIDOR SQL
    database = 'master'
    username = 'sa'
    password = 'Admin1234!'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';TrustServerCertificate=yes')
    #cursor = cnxn.cursor()
    return cnxn


def usar_bd_sin_return(query):
    cnxn = getconn()
    cursor = cnxn.cursor()
    status_code = 0
    try:
        cursor.execute(query)
        cnxn.commit()
        status_code = 201
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        status_code = 400
    finally:
        cursor.close()
        cnxn.close()
        return status_code

def usar_bd_con_return(query):
    cnxn = getconn()
    cursor = cnxn.cursor()
    try:
        cursor.execute(query)
        row = cursor.fetchall()
        datos = []
        for r in row:
            datos.append(r)
        cursor.close()
        cnxn.close()
        return datos
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None

#Secret key to validate tokens
secret_key="6af00dfe63f6495195a3341ef6406c2c" 

def encriptar_texto(texto):
    # Codifica el texto en UTF-8 antes de encriptar
    texto_codificado = texto.encode('utf-8')
    # Crea un objeto hash utilizando el algoritmo SHA-256
    hash_obj = hashlib.sha256()
    # Actualiza el hash con el texto codificado
    hash_obj.update(texto_codificado)
    # Obtiene el hash en formato hexadecimal
    hash_str_hexadecimal = str(hash_obj.hexdigest())
    return hash_str_hexadecimal


def obtener_usuario_callback(username, password, headers):
    """
    Verifies the request and retrieves the user information.

    Args:
        username (str): The username provided in the request.
        password (str): The password provided in the request.
        headers (dict): The headers of the request.

    Returns:
        tuple: A tuple containing the JSON response, status code, and headers.
    """

    print("Verificando request")

    respuesta = {}
    if username == "":
        respuesta["status"] = 400
        respuesta["message"] = "Error: No se ha ingresado un username."
        return jsonify(respuesta), respuesta["status"], headers
    
    print("Username ingresado correctamente")

    encrypted_password = encriptar_texto(password)

    # Obtener datos del usuario
    user = usar_bd_con_return(F"SELECT * FROM User_ WHERE Username = '{username}' and Encrypted_Password = '{encrypted_password}'")

    if user == []:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Usuario no encontrado."
        
        return jsonify(respuesta), respuesta["status"], headers

    print("El usuario si existe. Se procedera a generar el token del usuario: ", username)

    type = usar_bd_con_return(f"SELECT Type_ID FROM User_Type_Association WHERE Username='{username}'")

    if type[0] == 1:
        type = "admin"
    else:
        type = "client"

    print("El tipo de usuario es: ", type)

    # Calcular la fecha de expiración como un entero de tiempo Unix en segundos
    exp_timestamp = int((datetime.now(timezone.utc) + timedelta(seconds=1800)).timestamp()) # 1800 segundos = 30 minutos

    token = jwt.encode(
        payload={   
            "username": username,
            "password": password,
            "exp": exp_timestamp
        },
        key=secret_key,
    )

    print("Token generado correctamente")

    respuesta["token"] = token
    respuesta["type"] = type
    respuesta["status"] = 200
    respuesta["message"] = "Usuario encontrado y token generado."

    return jsonify(respuesta), respuesta["status"], headers


@app.route('/obtener-usuario', methods=['GET', 'OPTIONS'])
def obtener_usuario():
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return "", 204, headers

    request_args = request.args
    path = request.path
    respuesta = {}
    print(request_args)

    # Set CORS headers for main requests
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }

    if path == "/obtener-usuario" and request.method == 'GET':
        username = request_args.get('username')
        password = request_args.get('password')

        if username and password:
            # Assuming obtener_usuario_callback is a function that handles the logic
            return obtener_usuario_callback(username, password, headers)
        else:
            respuesta["status"] = 400
            respuesta["message"] = "Error: Faltan parámetros 'username' o 'password'."
            return jsonify(respuesta), 400, headers
    else:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Método no válido."
        return jsonify(respuesta), 404, headers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002,debug=True)