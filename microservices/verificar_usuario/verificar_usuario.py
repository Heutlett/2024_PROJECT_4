import json
import hashlib
import pyodbc
from flask import Flask, jsonify, request
from datetime import datetime, timedelta, timezone
import jwt

app = Flask(__name__)

def getconn():
    server = 'sqlserver-service'
    database = 'master'
    username = 'sa'
    password = 'Admin1234!'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';TrustServerCertificate=yes')
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

def verificar_usuario_callback(token, headers):
    try:
        # Validar token
        try:
            token_decoded  = jwt.decode(jwt=token, key=secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as e:
            print("Error 1: ", e)
            return jsonify({"status": 401, "message": "El token esta expirado!"}), 401, headers
        
        except jwt.exceptions.InvalidTokenError as e:
            print(f"Error 2: {e}")
            return jsonify({"status": 401, "message": "El token es invalido!"}), 401, headers
        
        except Exception as e:
            print(f"Error 3 : {e}")
            return jsonify({"status": 401, "message": e}), 401, headers
        
        # Validar datos del usuario
        username = token_decoded['username']
        password = encriptar_texto(token_decoded['password'])
        if username == "" or password == "":
            return jsonify({"status": 400, "message": "No se ha ingresado un username o password"}), 400, headers
        print(f"username: {username}, password: {password}")

        # Validar contrasena del usuario
        user = usar_bd_con_return(F"SELECT * FROM User_ WHERE Username = '{username}' AND Encrypted_Password = '{password}'")
        if user == []:
            return jsonify({"status": 404, "message": "Usuario no existe o la contrasena es incorrecta"}), 404, headers
        
        # Devolver exitoso
        return jsonify({"status": 200, "message": f"Usuario {user} encontrado"}), 200, headers

    except Exception as e:
        return jsonify({"status": 500, "message": e}), 500, headers

@app.route('/verificar-usuario', methods=['GET', 'OPTIONS'])
def verificar_usuario():
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
        return ("", 204, headers)
    # Set CORS headers for main requests
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }

    # Validaciones del path, body y method
    respuesta = {}
    request_args = request.args
    path = request.path
    if path == "/verificar-usuario" and request.method == 'GET':
        try:
            token = request_args.get('token', None)
        except Exception as e:
            print(f"Error al obtener los datos: {e}")
            respuesta["status"] = 400
            respuesta["message"] = "Error al obtener los datos."
            return jsonify(respuesta), 400, headers

        if token:
            return verificar_usuario_callback(token, headers)
        else:
            respuesta["status"] = 400
            respuesta["message"] = "Error: Faltan parametros 'username' o 'password'."
            return jsonify(respuesta), 400, headers
    else:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Metodo no valido."
        return jsonify(respuesta), 404, headers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003,debug=True)