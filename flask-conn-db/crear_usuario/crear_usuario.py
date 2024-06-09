import json
import hashlib
import pyodbc
from flask import Flask, jsonify, request

app = Flask(__name__)

def getconn():
    server = 'api-crear-usuario-service' # ESTO DEBE SER EL IP Y PUERTO DE TU SERVIDOR SQL
    database = 'master'
    username = 'sa'
    password = 'Admin1234!'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';TrustServerCertificate=yes')
    #cursor = cnxn.cursor()
    return cnxn


def usar_bd_sin_return(query):
    cnxn = getconn()
    cursor = cnxn.cursor()
    try:
        cursor.execute(query)
        cnxn.commit()
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
    finally:
        cursor.close()
        cnxn.close()

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
    # Set CORS headers for main requests
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }
    data = request.json

    username = data.get('username', None)
    password = data.get('password', None)
    first_name = data.get('first_name', None)
    last_name1 = data.get('last_name1', None)
    last_name2 = data.get('last_name2', None)
    security_question = data.get('security_question', None)
    security_answer = data.get('security_answer', None)

    if not username or not password or not first_name or not last_name1 or not last_name2 or not security_question or not security_answer:
        return jsonify({'mensaje': 'Faltan datos en la solicitud de creacion de usuario'}), 400, headers


    # Verificar que el metodo sea correcto
    if data.get('method') != "crear-usuario":
        print("Codigo: 400. Metodo incorrecto.")
        return jsonify({'mensaje': 'Metodo incorrecto'}), 400, headers

    try:
        # Encriptar la contraseña
        encrypted_password = encriptar_texto(password)
        encrypted_security_question = encriptar_texto(security_question)
        encrypted_security_answer = encriptar_texto(security_answer)

        # Crear la solicitud SQL
        usar_bd_sin_return(f"INSERT INTO User_ (Username, Encrypted_Password, First_Name, Last_Name1, Last_Name2, Security_Question, Security_Answer) \
                        VALUES ('{username}', '{encrypted_password}', '{first_name}', '{last_name1}', \
                        '{last_name2}', '{encrypted_security_question}', '{encrypted_security_answer}')")
        
        # Asociar el usuario con el tipo de usuario "Cliente"
        usar_bd_sin_return(f"INSERT INTO User_Type_Association (Username, Type_ID) \
                           VALUES ('{username}', 2)")

        
        return jsonify({'mensaje': 'Usuario creado exitosamente'}), 201, headers
    except Exception as e:
        print(f"Codigo: 500. Error al crear el usuario: {e}")
        return jsonify({'mensaje': 'Error al crear el usuario'}), 500, headers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True)