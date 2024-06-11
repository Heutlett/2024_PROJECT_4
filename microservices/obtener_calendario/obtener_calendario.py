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

def obtener_calendario_callback(date_request, start_time_request, restaurant_id, headers):
    # json de respuesta
    mensaje = {}
    mensaje['data'] = {}
    mensaje['data']['available_tables'] = []

    # Obtener todas las mesas disponibles para una fecha y hora especifica

    try:
        print("Date request: " + date_request)
        print("Start time request: " + start_time_request)

        # obtener todas las mesas
        mesas = usar_bd_con_return(f"SELECT * FROM Tables WHERE Restaurant_ID = '{restaurant_id}'")
        #return str(mesas), 200, headers             

        # obtener las mesas ocupadas para esa fecha y hora
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

        print("End time  " + end_time)

        mesas_ocupadas = usar_bd_con_return(f"SELECT * FROM Table_Availability WHERE Date_Reserved = '{date_request}' AND Start_Time >= '{start_time_request}' AND End_Time <= '{end_time}'")
        
        # cuando todas las mesas estan ocupadas, no hay mesas disponibles
        # esto puede pasar en eventos especiales
        if len(mesas_ocupadas) == len(mesas):
            print("No hay mesas disponibles para la fecha y hora solicitada.")
            mensaje['data']['available_tables'] = []
            mensaje['status'] = 404
            mensaje['message'] = "No hay mesas disponibles para la fecha y hora solicitada."
            return jsonify(mensaje), 404, headers

        # cuando no hay mesas ocupadas
        if len(mesas_ocupadas) == 0:
            for mesa in mesas:
                mensaje['data']['available_tables'].append({"Table_ID": mesa[0], "Chairs" : mesa[1]})
        else:
            print("Hay algunas mesas ocupadas para la fecha y hora solicitada")
            # cuando si hay mesas ocupadas
            for mesa in mesas:
                busy_table = True
                for mesa_ocupada in mesas_ocupadas:
                    if mesa[0] == mesa_ocupada[0]:
                        busy_table = False
                        break

                if busy_table:
                    mensaje['data']['available_tables'].append({"Table_ID": mesa[0], "Chairs" : mesa[1]})

 
        mensaje['status'] = 200
        mensaje['message'] = "Mesas disponibles obtenidas correctamente."
        
        
        return jsonify(mensaje), 200, headers
    except Exception as e:
        mensaje['status'] = 500
        mensaje['message'] = f"Error al obtener el calendario: {str(e)}"
        return jsonify(mensaje), 500, headers


# Obtiene una reserva puntual
@app.route("/obtener-calendario", methods=["GET", "OPTIONS"])
def obtener_calendario():
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

    if path == "/obtener-calendario" and request.method == 'GET':
        try:
            date = request_args.get("date")
            start_time = request_args.get("start_time")
            restaurant_id = request_args.get("restaurant_id")
        except Exception as e:
            respuesta["message"] = "Error: Parametro 'reservation_id' no encontrado."
            return jsonify(respuesta), 400, headers
    
        return obtener_calendario_callback(date, start_time, restaurant_id, headers)
    else:
        respuesta["message"] = "Error: Metodo no valido."
        return jsonify(respuesta), 400, headers
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5019,debug=True)
