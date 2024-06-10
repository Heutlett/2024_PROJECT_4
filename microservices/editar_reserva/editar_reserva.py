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
    status_code = 200
    message = ""
    try:
        cursor.execute(query)
        cnxn.commit()
        message = "Query ejecutada con exito"
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        status_code = 500
        message = f"Error al ejecutar la consulta: {e}"
        return jsonify(message), status_code
    cursor.close()
    cnxn.close()
    return jsonify(message), status_code

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

def editar_reserva_callback(token, reservation_id, restaurant_id, number_of_people, reservation_date, start_time, selected_tables, headers):
    # Validar token con el microservicio: verificar_usuario
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

    # El metodo como tal
    try: 
        # Obtener hora y fecha actual en formato "HH:MM:SS" y "YYYY-MM-DD"
        us_central_tz = pytz.timezone('US/Central')
        hora_actual = datetime.datetime.now(us_central_tz)
        fecha_actual = hora_actual.strftime('%Y-%m-%d')
        hora_actual = hora_actual.strftime('%H:%M:%S')
        
        # Verificar que la reserva exista
        reserva_verification = usar_bd_con_return(f"SELECT * FROM Reservations WHERE Reservation_ID = {reservation_id}")
        old_data = reserva_verification[0]
        if reserva_verification == []:
            mensaje = {
                "data": "",
                "status": 400,
                "message": "La reserva no existe"
            }
            return jsonify(mensaje), 400, headers
        
        
        # TODO: verificar que haya disponibilidad de las mesas en la fecha y hora solicitada
        
        # Validar datos del usuario
        username = token_decoded['username']

        # Fecha y hora de la reserva a editar
        old_date = reserva_verification[0][4].strftime('%Y-%m-%d')
        old_start_time = reserva_verification[0][5].strftime('%H:%M:%S')
        # Verificar si la reserva es futura
        if fecha_actual > old_date:
            mensaje = {
                "data": "",
                "status": 400,
                "message": "No se puede editar una reserva pasada"
            }
            return jsonify(mensaje), 400, headers

        # Validar que la cantidad de personas de la reserva sea menor o igual a la capacidad de las mesas seleccionadas
        total_chairs = []
        for table in selected_tables:
            sillas = usar_bd_con_return(f"SELECT Chairs FROM Tables WHERE Table_Number = {table} AND Restaurant_ID = {restaurant_id}")
            total_chairs.append(sillas[0][0])

        if sum(total_chairs) < int(number_of_people):            
            mensaje = {
                "data": "",
                "status": 400,
                "message": "Reserva no creada, eligio mal las mesas ya que le faltarian sillas."
            }
            return jsonify(mensaje),400, headers
        
        # Verificar que las horas de la reserva esten dentro del horario de atencion del restaurante
        hora_apertura_restaurante = usar_bd_con_return(f"SELECT Opening_Time FROM Restaurants WHERE Restaurant_ID = {restaurant_id}")
        hora_cierre_restaurante = usar_bd_con_return(f"SELECT Closing_Time FROM Restaurants WHERE Restaurant_ID = {restaurant_id}")
        end_reservation_time = sumar_hora(start_time)
        after_aperture_time = hora1_menor_hora2(str(hora_apertura_restaurante[0][0]), start_time)
        before_closing_time = hora1_menor_hora2(end_reservation_time, str(hora_cierre_restaurante[0][0]))

        if after_aperture_time == False or before_closing_time == False:            
            mensaje = {
                "data": "",
                "status": 400,
                "message": "Las horas de la potencial reserva no estan dentro del horario de atencion del restaurante"
            }
            return jsonify(mensaje),400, headers
        
        #return f"RD {str(reservation_date)} NP {str(number_of_people)} ST {str(start_time)} ET {str(end_reservation_time)} RI {str(reservation_id)}", 200, headers

        # Actualizar la reserva
        usar_bd_sin_return(f"UPDATE Reservations SET \
                                    Restaurant_ID = {restaurant_id}, \
                                    Number_Of_People = {number_of_people}, \
                                    Date_Reserved = '{reservation_date}', \
                                    Start_Time = '{start_time}', \
                                    End_Time = '{end_reservation_time}' \
                                WHERE Reservation_ID = {reservation_id}")
        reservation_id = usar_bd_con_return(f"SELECT Reservation_ID FROM Reservations \
                                WHERE User_ID = '{username}' \
                                AND Restaurant_ID = {restaurant_id} \
                                AND Date_Reserved = '{reservation_date}' \
                                AND Start_Time = '{start_time}' \
                                AND End_Time = '{end_reservation_time}'")
        # Actualizar las mesas   
        for table in selected_tables:
            usar_bd_sin_return(f"DELETE FROM Table_Availability \
                        WHERE Table_ID = {table} \
                        AND Date_Reserved = '{old_date}' \
                        AND Start_Time = '{old_start_time}' \
                        AND End_Time = '{sumar_hora(old_start_time)}'")
                
            usar_bd_sin_return(f"INSERT INTO Table_Availability (Table_ID, Date_Reserved, Start_Time, End_Time) \
                    VALUES ({table}, '{reservation_date}', '{start_time}', '{end_reservation_time}')")
            
            # actualizar la tabla de asociacion de mesas con reservas
            usar_bd_sin_return(f"DELETE FROM Reservation_Tables_Association \
                                WHERE Reservation_ID = {reservation_id} \
                                AND Table_ID = {table}")
            
            usar_bd_sin_return(f"INSERT INTO Reservation_Tables_Association (Reservation_ID, Table_ID) \
                                VALUES ({reservation_id}, {table})")
            
            return jsonify({"message": "Reserva editada con éxito"}), 200, headers
            
    except Exception as e:
        print(f"Codigo: 500. Error al editar la reserva: {str(e)}")
        mensaje = {
            "data": "",
            "status": 500,
            "message": f"Error al editar reserva: {str(e)}"
        } 
        return jsonify(mensaje), 500, headers
        
@app.route("/editar-reserva", methods=["PUT", "OPTIONS"])
def editar_reserva(): # EDITA RESERVAS FUTURAS
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
    if path == "/editar-reserva" and request.method == 'PUT':
        try:
            token = data.get('data').get('token', None)
            reservation_id = data.get('data').get('reservation_id', None)
            restaurant_id = data.get('data').get('restaurant_id', None)
            number_of_people = data.get('data').get('number_of_people', None)
            reservation_date = data.get('data').get('reservation_date', None)
            start_time = data.get('data').get('start_time', None)
            selected_tables = data.get('data').get('selected_tables', None)
            method = data.get('data').get('method', None)
        except Exception as e:
            print(f"Error al obtener los datos: {e}")
            respuesta["status"] = 400
            respuesta["message"] = "Error al obtener los datos."
            return jsonify(respuesta), 400, headers

        if reservation_id and token and restaurant_id and number_of_people and reservation_date and start_time and selected_tables and method == "editar-reserva":
            return editar_reserva_callback(token, reservation_id, restaurant_id, number_of_people, reservation_date, start_time, selected_tables, headers)
        else:
            respuesta["status"] = 400
            respuesta["message"] = "Error: ."
            return jsonify(respuesta), 400, headers
    else:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Método no válido."
        return jsonify(respuesta), 404, headers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009,debug=True)
