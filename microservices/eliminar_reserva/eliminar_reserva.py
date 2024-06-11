import json
import jwt
import pytz
import hashlib
import pyodbc
from flask import Flask, jsonify, request
import requests
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

def eliminar_reserva_callback(token, username, reservation_id, reservation_date, start_time, headers):
    # json de respuesta
    mensaje = {}

    respuesta = {}
    #verificar el token
    url = f"http://192.168.49.2:30006/verificar-usuario?token={token}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            token_decoded  = jwt.decode(jwt=token, key=secret_key, algorithms=["HS256"])
        except Exception as e:
            mensaje = {
                "data": "",
                "status": 400,
                "message": "Token invalido"
            }
            return jsonify(mensaje),400, headers
    else:        
        mensaje = {
            "data": "",
            "status": 400,
            "message": "Token invalido"
        }
        return jsonify(mensaje),400, headers
    
    # Definir la zona horaria US-Central
    us_central_tz = pytz.timezone('US/Central')

    # Obtener la hora actual en la zona horaria US-Central
    hora_actual_us_central = datetime.datetime.now(us_central_tz)

    # Convertir a la zona horaria de Arizona
    zona_horaria_arizona = pytz.timezone('US/Arizona')
    hora_actual_arizona = hora_actual_us_central.astimezone(zona_horaria_arizona)

    hora_actual = hora_actual_us_central.strftime('%H:%M:%S')
    fecha_actual = hora_actual_us_central.strftime('%Y-%m-%d')

    print("Hora actual en Arizona:", hora_actual_arizona)
    print("Hora normal en Arizona:", hora_actual)
    
    try:
        # verificar si la reserva es futura
        if fecha_actual > reservation_date:
            print("No se puede eliminar una reserva pasada")
            mensaje['status'] = '400'
            mensaje['message'] = 'No se puede eliminar una reserva pasada'
            return jsonify(mensaje), 400, headers
        
        # verificar que la reserva exista
        reserva_verification = usar_bd_con_return(f"SELECT * FROM Reservations WHERE Reservation_ID = {reservation_id}")
        if reserva_verification == []:
            print("La reserva no existe")
            mensaje['status'] = '404'
            mensaje['message'] = 'La reserva no existe'
            return jsonify(mensaje), 404, headers
        print(f"reservaporborrar = {reserva_verification[0][0]}")

        # obtener las mesas asociadas a la reserva
        mesasporliberar = usar_bd_con_return(f"SELECT Table_ID FROM Reservation_Tables_Association WHERE Reservation_ID = {reservation_id}")
        print(f"mesasporliberar = {mesasporliberar}")
        print(f"mesasporliberar = {mesasporliberar[0][0]}")  # [#row][#column]
        
        # verificar si la reserva tiene mesas asociadas
        if mesasporliberar == []:
            print("La reserva no tiene mesas asociadas")
            mensaje['status'] = '404'
            mensaje['message'] = 'La reserva no tiene mesas asociadas'
            return jsonify(mensaje), 404, headers

        usar_bd_sin_return(f"DELETE FROM Reservation_Tables_Association WHERE Reservation_ID = {reservation_id}")
        print("Mesas desasociadas de la reserva")

        # liberar las mesas ocupadas
        for row in mesasporliberar:
            usar_bd_sin_return(f"DELETE FROM Table_Availability WHERE Table_ID = {str(row[0])} \
                        AND Date_Reserved = '{reservation_date}' \
                        AND Start_Time = '{start_time}'")
            
        print("Mesas liberadas")

        usar_bd_sin_return(f"DELETE FROM Reservations WHERE Reservation_ID = {reservation_id}")
        print("Reserva eliminada")

        mensaje['status'] = '200'
        mensaje['message'] = 'Reserva eliminada'
        
        return jsonify(mensaje), 200, headers
    except Exception as e:
        mensaje['status'] = '500'
        mensaje['message'] = f'Error al eliminar la reserva: {str(e)}'
        return jsonify(mensaje), 500, headers

@app.route("/eliminar-reserva", methods=['DELETE', 'OPTIONS'])
def eliminar_reserva():
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
   # Set CORS headers for main requests
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }

    request_args = request.args
    path = request.path
    respuesta = {}
    print(request_args)

    data = request.json
    if path == "/eliminar-reserva" and request.method == 'DELETE':
        try:
            token = data.get('data').get('token', None)
            reservation_date = data.get('data').get('reservation_date', None)
            reservation_id = data.get('data').get('reservation_id', None)
            restaurant_id = data.get('data').get('restaurant_id', None)
            start_time = data.get('data').get('start_time', None)
            method = data.get('data').get('method', None)
        except Exception as e:
            print(f"Error al obtener los datos: {e}")
            respuesta["status"] = 400
            respuesta["message"] = "Error al obtener los datos."
            return jsonify(respuesta), 400, headers

        if token and reservation_date and reservation_id and restaurant_id and start_time and method:
            return eliminar_reserva_callback(token, reservation_id, reservation_date, start_time, headers)
        else:
            respuesta["status"] = 400
            respuesta["message"] = "Error: Faltan parámetros 'username' o 'password'."
            return jsonify(respuesta), 400, headers
    else:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Método no válido."
        return jsonify(respuesta), 404, headers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010,debug=True)
