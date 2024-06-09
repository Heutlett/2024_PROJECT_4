import json
import hashlib
import pyodbc
from flask import Flask, jsonify, request
import datetime

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


def cambiar_contrasena_callback(username, new_password, security_answer,headers):
    try:
        # Verify if the user exists
        user = usar_bd_con_return(f"SELECT * FROM User_ WHERE Username = '{username}'")
        if user == []:
            print(f"Codigo: 400. El usuario {username} no existe.")
            return jsonify({"status": 400, "message": f"El usuario {username} no existe."}), 400, headers
            
        
        # Verify is the user answered correctly the security question
        stored_security_answer = usar_bd_con_return(f"SELECT Security_Answer FROM User_ WHERE Username = '{username}'")
        current_answer_encrypted = encriptar_texto(security_answer)
        
        if stored_security_answer[0][0] != current_answer_encrypted:
            print(f"Codigo: 400. La respuesta de seguridad no es correcta.")
            return jsonify({"status": 400, "message": "La respuesta de seguridad no es correcta."}), 400, headers
        
        # Update the user's password
        result = usar_bd_sin_return(f"UPDATE User_ SET Encrypted_Password = '{encriptar_texto(new_password)}' \
                            WHERE username = '{username}'")
        if result == 400:
            print(f"Codigo: 400. Error al cambiar la contrasena del usuario {username}.")
            return jsonify({"status": 400, "message": f"Error al cambiar la contrasena del usuario {username}."}), 400, headers
        else:
            print(f"Codigo: 200. La contrasena del usuario {username} ha sido cambiada.")
            return jsonify({"status": 200, "message": f"La contrasena del usuario {username} ha sido cambiada."}), 200, headers
        
    except Exception as err:
        print(f"Codigo: 500. Error: {err}")
        return jsonify({"status": 500, "message": f"Error: {err}"}), 500, headers

@app.route('/cambiar-contrasena', methods=['PUT', 'OPTIONS'])
def crear_usuario():
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

    data = request.json
    if path == "/cambiar-contrasena" and request.method == 'PUT':
        try:
            username = data.get('data').get('username', None)
            new_password = data.get('data').get('new_password', None)
            security_answer = data.get('data').get('security_answer', None)
            method = data.get('data').get('method', None)
        except Exception as e:
            print(f"Error al obtener los datos: {e}")
            respuesta["status"] = 400
            respuesta["message"] = "Error al obtener los datos."
            return jsonify(respuesta), 400, headers

        if username and new_password and security_answer and method == "cambiar-contrasena":
            # Assuming obtener_usuario_callback is a function that handles the logic
            return cambiar_contrasena_callback(username, new_password, security_answer, headers)
        else:
            respuesta["status"] = 400
            respuesta["message"] = "Error: Faltan parámetros 'username' o 'password'."
            return jsonify(respuesta), 400, headers
    else:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Método no válido."
        return jsonify(respuesta), 404, headers


    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004,debug=True)