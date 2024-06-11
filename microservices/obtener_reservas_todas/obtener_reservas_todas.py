import json
import jwt
import hashlib
import pyodbc
from flask import Flask, jsonify, request
import requests
import datetime
import pytz

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
    cursor.execute(query)
    cnxn.commit()
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

    
def sumar_hora(start_time_request):
    decena = start_time_request[0]
    unidad = start_time_request[1]
    end_time = ""
    # sumar 2 horas a la hora de inicio para obtener la hora de fin
    if decena == "0":  
        suma = int(unidad) + 2

        if suma < 10:
            end_time = "0" + str(suma) + start_time_request[2:]
        else:
            end_time = str(suma) + start_time_request[2:]

    elif decena == "1":
        suma = int(decena)*10 + int(unidad) + 2
        end_time = str(suma) + start_time_request[2:]
    
    elif decena == "2":
        suma = int(decena)*20 + int(unidad) + 2

        if suma < 25:
            end_time = str(suma) + start_time_request[2:]
        else: # si la suma es mayor a 24
            end_time = "00" + start_time_request[2:]
    
    return end_time

# Funcion que compara dos horas en formato "HH:MM:SS"
def hora1_menor_hora2(hora1, hora2):
    if hora1 < hora2:
        return True
    else:
        return False

# Secret key to validate token
secret_key="6af00dfe63f6495195a3341ef6406c2c"

# 
def obtener_reservas_todas(fecha,hora, headers):
    query = f"SELECT * FROM Reservations WHERE Date_Reserved = '{fecha}' AND Start_Time > '{hora}' OR Date_Reserved > '{fecha}';"
    result = usar_bd_con_return(query)
    mensaje = {}
    mensaje["data"] = []

    if len(result) == 0:
        mensaje["data"] = "No hay reservas futuras"
        return jsonify(mensaje), 200, headers
    
    for elem in result:
        mensaje["data"].append({
            "Reservation_ID": elem[0],
            "User_ID": elem[1],
            "Restaurant_ID": elem[2],
            "Number_Of_People": elem[3],
            "Date_Reserved": elem[4].strftime('%Y-%m-%d'),  # Convertir a cadena de texto en formato 'YYYY-MM-DD'
            "Start_Time": elem[5].strftime('%H:%M:%S'),    # Convertir a cadena de texto en formato 'HH:MM:SS'
            "End_Time": elem[6].strftime('%H:%M:%S')       # Convertir a cadena de texto en formato 'HH:MM:SS'
        })
    return jsonify(mensaje), 200, headers

# Obtiene todas las reservas FUTURAS de TODOS los usuarios
@app.route("/obtener-reserva/", methods=["GET", "OPTIONS"])
def obtener_reservas():
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return jsonify({"message": "Preflight successful"}), 204, headers

    headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": "true",
    }

    request_args = request.args
    path = request.path
    respuesta = {}

    # Definir la zona horaria US-Central
    us_central_tz = pytz.timezone('US/Central')
    # Obtener la hora actual en la zona horaria US-Central
    hora_actual_us_central = datetime.datetime.now(us_central_tz)
    fecha_actual = hora_actual_us_central.strftime('%Y-%m-%d')
    hora_actual = hora_actual_us_central.strftime('%H:%M:%S')

    if path == "/obtener-reserva/" and request.method == 'GET':
        try:
            time = request_args.get("time")
        except Exception as e:
            respuesta["message"] = "Error: Parametro 'time' no encontrado."
            return jsonify(respuesta), 400, headers

        if time != "all":
            respuesta["message"] = "Error: Parametro 'time' no encontrado."
            return jsonify(respuesta), 400, headers
        
        return obtener_reservas_todas(fecha_actual, hora_actual, headers)
    else:
        respuesta["message"] = "Error: Metodo no valido."
        return jsonify(respuesta), 400, headers
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011,debug=True)
