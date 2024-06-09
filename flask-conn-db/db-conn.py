from flask import Flask, jsonify, request
import pyodbc

app = Flask(__name__)

# Configuración de la conexión a la base de datos
server = 'sqlserver-service' # ESTO DEBE SER EL IP Y PUERTO DE TU SERVIDOR SQL
database = 'master'
username = 'sa'
password = 'Admin1234!'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';TrustServerCertificate=yes')
cursor = cnxn.cursor()

#OBTENER COMIDAS
@app.route('/foods', methods=['GET'])
def obtener_alimentos():
    cursor.execute("SELECT * FROM Food")
    alimentos = []
    for row in cursor.fetchall():
        alimento = {
            'id': row[0],
            'name': row[1]
        }
        alimentos.append(alimento)
    return jsonify({'alimentos': alimentos})

#AGREGAR COMIDAS
@app.route('/foods', methods=['POST'])
def crear_alimento():
    nombre = request.json.get('nombre', None)
    if not nombre:
        return jsonify({'mensaje': 'El nombre del alimento es requerido'}), 400
    
    cursor.execute("INSERT INTO Food (Name) VALUES (?)", (nombre,))
    cnxn.commit()
    return jsonify({'mensaje': 'Alimento creado correctamente'}), 201

#ACTUALIZAR 1 COMIDA
@app.route('/foods', methods=['PUT'])
def actualizar_alimento():
    data = request.json
    alimento_id = data.get('id', None)
    nombre = data.get('nombre', None)
    
    if alimento_id is None or nombre is None:
        return jsonify({'mensaje': 'Se requiere el ID del alimento y el nuevo nombre'}), 400
    
    cursor.execute("UPDATE Food SET Name=? WHERE Id=?", (nombre, alimento_id))
    cnxn.commit()
    return jsonify({'mensaje': 'Alimento actualizado correctamente'})

#ELIMINAR 1 COMIDA
@app.route('/foods', methods=['DELETE'])
def eliminar_alimento():
    data = request.json
    alimento_id = data.get('id', None)
    if alimento_id is None:
        return jsonify({'mensaje': 'Se requiere el ID del alimento'}), 400

    cursor.execute("DELETE FROM Food WHERE Id=?", (alimento_id,))
    cnxn.commit()
    return jsonify({'mensaje': 'Alimento eliminado correctamente'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
