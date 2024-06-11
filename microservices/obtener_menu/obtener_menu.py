import pyodbc
import json
from flask import Flask, request

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

def obtener_menu_callback(message):
    mensaje = {}
    mensaje["data"] = {}
    mensaje["data"]["types"] = []
    mensaje["data"]["MainCourses"] = []
    mensaje["data"]["Drinks"] = []
    mensaje["data"]["Desserts"] = []

    
    food_types = usar_bd_con_return("SELECT * FROM Food_Type;")

    for row in food_types:
        food_type_id = row[0]
        food_type_name = row[1]
        mensaje["data"]["types"].append({"id": food_type_id, "name": food_type_name})
    
    main_courses = usar_bd_con_return("SELECT ID, Name\
                FROM Food\
                WHERE ID IN (\
                SELECT Food_ID\
                FROM Food_Type_Association\
                WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'MainCourse'));")
    for row in main_courses:
        main_course_id = row[0]
        main_course_name = row[1]
        mensaje["data"]["MainCourses"].append({"id": main_course_id, "name": main_course_name})

    drinks = usar_bd_con_return("SELECT ID, Name\
                FROM Food\
                WHERE ID IN (\
                SELECT Food_ID\
                FROM Food_Type_Association\
                WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'Drink'));")
    for row in drinks:
        drink_id = row[0]
        drink_name = row[1]
        mensaje["data"]["Drinks"].append({"id": drink_id, "name": drink_name})

    desserts = usar_bd_con_return("SELECT ID, Name\
                FROM Food\
                WHERE ID IN (\
                SELECT Food_ID\
                FROM Food_Type_Association\
                WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'Dessert'));")
    for row in desserts:
        dessert_id = row[0]
        dessert_name = row[1]
        mensaje["data"]["Desserts"].append({"id": dessert_id, "name": dessert_name})

    mensaje["status"] = 200
    mensaje["message"] = "Menu obtenido correctamente"
    
    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)

    return mensaje_json

@app.route('/obtener-menu', methods=['GET', 'OPTIONS'])
def obtener_menu():
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

    request_args = request.args
    path = (request.path)
    respuesta = {}
    # Set CORS headers for main requests
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }
    if path == "/obtener-menu" and request.method == 'GET':
        return (obtener_menu_callback(request),200,headers)
    else:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Método no válido."
        return (f"{json.dumps(respuesta, ensure_ascii=False)}",404,headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5017,debug=True)