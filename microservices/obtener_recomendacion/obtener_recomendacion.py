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

def obtener_recomendacion_callback(recomendacion, quantity):
    mensaje = {}
    mensaje["data"] = {}

    if quantity == 1:
        print("One dish")

        name_dish = usar_bd_con_return(f"SELECT Name FROM Food WHERE ID='{recomendacion[0]}';")
        print("Name_dish: ", name_dish)

        if len(name_dish) == 0:
            mensaje["data"] = "No existe esa comida"

        row_recommendation = usar_bd_con_return(f"SELECT * FROM Recommendation \
                                     WHERE Main_Dish_ID = {recomendacion[0]} \
                                     OR Drink_ID = {recomendacion[0]} \
                                     OR Dessert_ID = {recomendacion[0]};")
        print("row_recommendation", row_recommendation)

        main_dish_name = usar_bd_con_return(f"SELECT Name FROM Food WHERE ID= {row_recommendation[0][1]}")
        print("main_dish_name", main_dish_name[0][0])

        drink_name = usar_bd_con_return(f"SELECT Name FROM Food WHERE ID= {row_recommendation[0][2]}")

        print("drink_name: ", drink_name[0][0])

        dessert = usar_bd_con_return(f"SELECT Name FROM Food WHERE ID= {row_recommendation[0][3]}")

        print("dessert_name:", dessert[0][0])


        mensaje["data"]["Main_Dish"] = main_dish_name[0][0]
        mensaje["data"]["Drink"] = drink_name[0][0]
        mensaje["data"]["Dessert"] = dessert[0][0]
        mensaje["status"] = 200
        mensaje["message"] = "Recomendacion encontrada"

    else:
        print("Two dishes")
        
        name_dish1 = usar_bd_con_return(f"SELECT Name FROM Food WHERE ID='{recomendacion[0]}';")
        name_dish2 = usar_bd_con_return(f"SELECT Name FROM Food WHERE ID= {recomendacion[1]}")
        print("Name_dish1: ", name_dish1[0][0])
        print("Name_dish2: ", name_dish2[0][0])

        if name_dish1 == "" or name_dish2 == "":
            mensaje["status"] = 404
            mensaje['message'] = "No existe alguno de los dos platillos"
            return json.dumps(mensaje)


        row1 = usar_bd_con_return(f"SELECT * FROM Recommendation \
                                     WHERE Main_Dish_ID = {recomendacion[0]} \
                                     OR Drink_ID = {recomendacion[0]} \
                                     OR Dessert_ID = {recomendacion[0]};")
        
        row2 = usar_bd_con_return(f"SELECT * FROM Recommendation \
                                     WHERE Main_Dish_ID = {recomendacion[1]} \
                                     OR Drink_ID = {recomendacion[1]} \
                                     OR Dessert_ID = {recomendacion[1]};")
        
        print("row1", row1)
        print("row2: ", row2)

        if row1 != row2:
            print("No hay recomendacion para esa combinacion de comidas")
            mensaje["status"] = 404
            mensaje["message"] = "No hay recomendacion para esa combinacion de comidas"
            # Convertir el mensaje a JSON
            mensaje_json = json.dumps(mensaje)
            return mensaje_json

        main_dish_name = usar_bd_con_return(f"SELECT Name FROM Food WHERE ID= {row1[0][1]}")
        print("main_dish_name", main_dish_name[0][0])

        drink_name = usar_bd_con_return(f"SELECT Name FROM Food WHERE ID= {row1[0][2]}")

        print("drink_name: ", drink_name[0][0])

        dessert = usar_bd_con_return(f"SELECT Name FROM Food WHERE ID= {row1[0][3]}")

        print("dessert_name:", dessert[0][0])


        mensaje["data"]["Main_Dish"] = main_dish_name[0][0]
        mensaje["data"]["Drink"] = drink_name[0][0]
        mensaje["data"]["Dessert"] = dessert[0][0]
        mensaje["status"] = 200
        mensaje["message"] = "Recomendacion encontrada"
    
    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)
    
    return mensaje_json

@app.route('/obtener-recomendacion', methods=['GET', 'OPTIONS'])
def obtener_recomendacion():

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
    path = request.path
    respuesta = {}
    # Set CORS headers for main requests
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }   

    validate = ('dish1' in request_args and request_args["dish1"] != 0 and request_args["dish1"] is not None and request_args.get("dish1") != "")

    if not validate:
        respuesta["message"] = "Error: Peticion incorrecta"
        return (json.dumps(respuesta), 400, headers)

    
    if path == "/obtener-recomendacion" and request.method == 'GET' and "dish1" in request_args:
        dish1_id = request_args.get("dish1")
        
        if "dish2" not in request_args:
            dishes = (dish1_id)
            return (obtener_recomendacion_callback(dishes, 1), 200,headers)
        else:
            validate2 = (request_args["dish2"] != 0 and request_args["dish2"] is not None and request_args.get("dish2") != "")
            if not validate2:
                respuesta["message"] = "Error: Peticion incorrecta"
                return (json.dumps(respuesta), 400,headers)
            dish2_id = request_args.get("dish2")
            if dish2_id is None or dish2_id == "0":
                respuesta["message"] = "Error: Peticion incorrecta"
                return (json.dumps(respuesta), 400,headers)
            dishes = (dish1_id, dish2_id)
            return (obtener_recomendacion_callback(dishes, 2), 200,headers)
    else:
        respuesta["message"] = "Error: Método no válido."
        return (json.dumps(respuesta), 404,headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True)