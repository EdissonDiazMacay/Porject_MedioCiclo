## Impotar modulos requeridos
from flask import Flask, jsonify as res, request as req, render_template as render
from flask import json
from flask.json import JSONDecoder, JSONEncoder, jsonify
from flask_mysqldb import MySQL as db

## Crear instancia de la aplicación
app = Flask(__name__)

## Configuración de la conexión a la base de datos
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'py_programacionavanzada'

## Crear instancia de MySQL
MySQL = db(app)

"""INICIO - RUTAS DE LA APLICACIÓN"""
@app.route('/')
def welcome():
    return listarClientes()

####################################################################
## Listar clientes
####################################################################
@app.route('/clientes', methods=['GET'])
def listarClientes():
    ## Consulta SQL para extraer todos los clientes
    sql = "SELECT cliente.id, cedula, nombres, apellidos, COALESCE((SELECT sum(monto) FROM deuda WHERE deuda.id_cliente = cliente.id),0) - COALESCE((SELECT sum(monto) FROM pago WHERE pago.id_cliente = cliente.id),0) as adeuda FROM cliente"

    ## Ejecutar consulta
    cursor = MySQL.connection.cursor()
    cursor.execute(sql)

    return render('listadoclientes.html', clientes = cursor.fetchall())

####################################################################
## Ver información del cliente seleccionado
####################################################################
@app.route('/clientes/<id>', methods=['GET'])
def verCliente(id):
    ## Obtener cursor
    cursor = MySQL.connection.cursor()

    ## Consulta SQL para extraer todos los clientes (1)
    sql = f"SELECT id, cedula, nombres, apellidos, COALESCE((SELECT sum(monto) FROM deuda WHERE deuda.id_cliente = cliente.id),0) - COALESCE((SELECT sum(monto) FROM pago WHERE pago.id_cliente = cliente.id),0) as adeuda FROM cliente WHERE cliente.id = {id}"

    ## Ejecutar consulta  (1)
    cursor.execute(sql)
    cliente = cursor.fetchone()

    ## Consulta SQL para extraer el historial de deudas (2)
    sql = f"SELECT id_cliente, monto, descripcion, id FROM deuda WHERE id_cliente = {id}"

    ## Ejecutar consulta  (2)
    cursor.execute(sql)
    historialDeudas = cursor.fetchall()

    ## Consulta SQL para extraer el historial de pagos (3)
    sql = f"SELECT id_cliente, monto, id FROM pago WHERE id_cliente = {id}"

    ## Ejecutar consulta  (3)
    cursor.execute(sql)
    historialPagos = cursor.fetchall()

    return render('clientes.html', data = {
        "cliente": cliente,
        "historialDeudas": historialDeudas,
        "historialPagos": historialPagos,
    })

####################################################################
## Crear cliente
####################################################################
@app.route('/clientes', methods=['POST'])
def crearCliente():
    ## Recuperar información recibida del formulario
    cedula    = req.json['cedula']
    nombres   = req.json['nombres']
    apellidos = req.json['apellidos']

    ## Consulta SQL para guardar el cliente
    sql = f"INSERT INTO cliente(cedula, nombres, apellidos) VALUES('{cedula}', '{nombres}', '{apellidos}')"

    ## Ejecutar consulta
    cursor = MySQL.connection.cursor()
    cursor.execute(sql)

    ## Aplicar cambios en la base de datos
    MySQL.connection.commit()

    ## Recuperar información almacenada
    sql = f"SELECT id, cedula, nombres, apellidos FROM cliente WHERE cedula = '{cedula}'"
    cursor.execute(sql)
    nuevoCliente = cursor.fetchone()

    return res({
        "data": {
            "id"        : nuevoCliente[0],
            "cedula"    : nuevoCliente[1],
            "nombres"   : nuevoCliente[2],
            "apellidos" : nuevoCliente[3]
        }
    })

####################################################################
## Actualizar cliente
####################################################################
@app.route('/clientes2/<id>', methods=['POST'])
def actualizarCliente(id):
    ## Recuperar información recibida del formulario
    cedula    = req.json['cedula']
    nombres   = req.json['nombres']
    apellidos = req.json['apellidos']

    ## Consulta SQL para actualizar el cliente
    sql = f"UPDATE cliente SET cedula = '{cedula}', nombres = '{nombres}', apellidos = '{apellidos}' WHERE id = {id}"

    ## Ejecutar consulta
    cursor = MySQL.connection.cursor()
    cursor.execute(sql)

    ## Aplicar cambios en la base de datos
    MySQL.connection.commit()

    ## Recuperar información almacenada
    sql = f"SELECT id, cedula, nombres, apellidos FROM cliente WHERE cedula = '{cedula}'"
    cursor.execute(sql)
    nuevoCliente = cursor.fetchone()

    return res({
        "status": "ok"
    })

####################################################################
## Eliminar cliente
####################################################################
@app.route('/clientes/<id>', methods=['DELETE'])
def eliminarCliente(id):
    ## Ejecutar consulta
    cursor = MySQL.connection.cursor()
    cursor.execute(f"DELETE FROM pago WHERE id_cliente = {id}")
    cursor.execute(f"DELETE FROM deuda WHERE id_cliente = {id}")
    cursor.execute(f"DELETE FROM cliente WHERE id = {id}")

    ## Aplicar cambios en la base de datos
    MySQL.connection.commit()

    return res({
        "status": "201",
        "msg": f"El cliente <{id}> fue eliminado."
    })

####################################################################
## Crear deuda
####################################################################
@app.route('/deuda', methods = ['POST'])
def crearDeuda():
    monto = req.json['monto']
    desc = req.json['desc']
    id_cliente = req.json['id_cliente']

    ## Consulta SQL para registrar la deuda
    sql = f"INSERT INTO deuda(id_cliente, monto, descripcion) VALUES('{id_cliente}', '{monto}', '{desc}')"

    ## Ejecutar la consulta
    cursor = MySQL.connection.cursor()
    cursor.execute(sql)
    MySQL.connection.commit()

    return res({
        "status": "ok"
    })

####################################################################
## Eliminar deuda
####################################################################
@app.route('/eliminar-deuda/<id>', methods = ['POST'])
def eliminarDeuda(id):
    ## Consulta SQL para eliminar la deuda
    sql = f"DELETE FROM deuda WHERE id = {id}"

    ## Ejecutar la consulta
    cursor = MySQL.connection.cursor()
    cursor.execute(sql)
    MySQL.connection.commit()

    return res({
        "status": "ok"
    })

@app.route('/modificar-deuda/<id>', methods = ['POST'])
def modificarDeuda(id):
    monto = req.json['monto']
    desc = req.json['desc']

    ## Consulta SQL para eliminar la deuda
    sql = f"UPDATE deuda SET monto = {monto}, descripcion = '{desc}' WHERE id = {id}"

    ## Ejecutar la consulta
    cursor = MySQL.connection.cursor()
    cursor.execute(sql)
    MySQL.connection.commit()

    return res({
        "status": "ok"
    })
####################################################################
## Crear pago
####################################################################
@app.route('/pago', methods = ['POST'])
def crearPago():
    monto = req.json['monto']
    id_cliente = req.json['id_cliente']

    ## Consulta SQL para registrar la deuda
    sql = f"INSERT INTO pago(id_cliente, monto) VALUES('{id_cliente}', '{monto}')"

    ## Ejecutar la consulta
    cursor = MySQL.connection.cursor()
    cursor.execute(sql)
    MySQL.connection.commit()

    return res({
        "status": "ok"
    })


####################################################################
## Eliminar pago
####################################################################
@app.route('/eliminar-pago/<id>', methods = ['POST'])
def eliminarPago(id):
    ## Consulta SQL para eliminar la deuda
    sql = f"DELETE FROM pago WHERE id = {id}"

    ## Ejecutar la consulta
    cursor = MySQL.connection.cursor()
    cursor.execute(sql)
    MySQL.connection.commit()

    return res({
        "status": "ok"
    })

####################################################################
## Eliminar pago
####################################################################
@app.route('/modificar-pago/<id>', methods = ['POST'])
def modificarPago(id):
    monto = req.json['monto']

    ## Consulta SQL para eliminar la deuda
    sql = f"UPDATE pago SET monto = {monto} WHERE id = {id}"

    ## Ejecutar la consulta
    cursor = MySQL.connection.cursor()
    cursor.execute(sql)
    MySQL.connection.commit()

    return res({
        "status": "ok"
    })
"""FIN - RUTAS DE LA APLICACIÓN"""

## Iniciar la aplicación
if __name__=='__main__':
    app.run(port=4000, debug=True)
