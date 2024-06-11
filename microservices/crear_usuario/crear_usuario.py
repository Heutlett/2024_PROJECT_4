import json
import hashlib
import pyodbc
from flask import Flask, jsonify, request
from flask_cors import CORS

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


@app.route('/crear-usuario', methods=['POST'])
def crear_usuario():
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
    data = request.json

    # data = {"data":{ "username": "usuario_prueba", "password": "password_prueba", "first_name": "nombre_prueba", "last_name1": "apellido1_prueba", "last_name2": "apellido2_prueba", "security_question": "pregunta_prueba", "security_answer": "respuesta_prueba", "method": "crear-usuario"}}
    # como sería el .get si data es un diccionario y dentro de data hay otro diccionario llamado data
    try:
        username = data.get('data').get('username', None)
        password = data.get('data').get('password', None)
        first_name = data.get('data').get('first_name', None)
        last_name1 = data.get('data').get('last_name1', None)
        last_name2 = data.get('data').get('last_name2', None)
        security_question = data.get('data').get('security_question', None)
        security_answer = data.get('data').get('security_answer', None)
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return (jsonify({f"mensaje": "Error al obtener los datos"}), 400, headers)

    if not username or not password or not first_name or not last_name1 or not last_name2 or not security_question or not security_answer:
        return (jsonify({'mensaje': 'Faltan datos en la solicitud de creacion de usuario'}), 400, headers)


    # Verificar que el metodo sea correcto
    if data.get('data').get('method') != "crear-usuario":
        print("Codigo: 400. Metodo incorrecto.")
        return (jsonify({'mensaje': 'Metodo incorrecto'}), 400, headers)

    try:
        # Encriptar la contraseña
        encrypted_password = encriptar_texto(password)
        encrypted_security_question = encriptar_texto(security_question)
        encrypted_security_answer = encriptar_texto(security_answer)

        # Crear la solicitud SQL
        status = usar_bd_sin_return(f"INSERT INTO User_ (Username, Encrypted_Password, First_Name, Last_Name1, Last_Name2, Security_Question, Security_Answer) \
                        VALUES ('{username}', '{encrypted_password}', '{first_name}', '{last_name1}', \
                        '{last_name2}', '{encrypted_security_question}', '{encrypted_security_answer}')")
        
        # Asociar el usuario con el tipo de usuario "Cliente"
        status = usar_bd_sin_return(f"INSERT INTO User_Type_Association (Username, Type_ID) \
                           VALUES ('{username}', 2)")

        if status == 400:
            print("Codigo: 500. Error al crear el usuario.")
            return (jsonify({'mensaje': 'Ya existe el usuario'}), 400, headers)
        else:
            return (jsonify({'mensaje': 'Usuario creado exitosamente'}), 201, headers)
    except Exception as e:
        print(f"Codigo: 500. Error al crear el usuario: {e}")
        return (jsonify({'mensaje': 'Error al crear el usuario'}), 500, headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True)