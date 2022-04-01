import os
from bottle import route, run, TEMPLATE_PATH, jinja2_view, static_file, request, redirect
import sqlite3

BASE_DATOS = os.path.join(os.path.dirname(__file__),'personas.db')

# para que bottle sepa donde buscar nuestras plantillas:
TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))

# hace falta otro route para la devolucion de los ficheros static desde el servidor, que seran los css:
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')
 
@route('/')
@jinja2_view('home2.html')
def hola():
    # return {'datos':[('Teo', 1, 'lunes'),('Jose', 2,'Martes'),('Pau',3 , 'Jueves')]}

    cons_vista_datos_servidor = 'select p.id, p.nombre, p.apellidos, p.dni, t.descripcion, n.descripcion from persona p left join T_ocupacion t on p.id_ocupacion = t.id left join T_numero n on n.id =p.id_numero '
    # consulta_ver_descripcio_ocupacion = f'select descripcion from T_ocupacion where id = {id_ocu}'
    cnx = sqlite3.connect(BASE_DATOS)
    cursor = cnx.execute(cons_vista_datos_servidor)
    filas = cursor.fetchall()
    
    cnx.close()
    return {'datos':filas}

@route('/editar')
@route('/editar/<id:int>')
@jinja2_view('formulario.html')
def mi_form(id=None):
    cnx = sqlite3.connect(BASE_DATOS)
    consulta_ocupaciones = "select * from T_ocupacion"
    
    cursor = cnx.execute(consulta_ocupaciones)
    lista_ocupaciones = cursor.fetchall()

    # Bloque de números para pintar:
    consulta_numeros = "select * from T_numero"
    cursor = cnx.execute(consulta_numeros)
    lista_numeros = cursor.fetchall()

    # Bloque de vehículos para pintar:
    consulta_vehiculos = "select * from T_vehiculo"
    cursor = cnx.execute(consulta_vehiculos)
    lista_vehiculos = cursor.fetchall()


    if id is None: # es un ALTA
        return {'ocupaciones':lista_ocupaciones, 'numeros':lista_numeros, 'vehiculos':lista_vehiculos}
    else: 
        cons_update_datos_servidor = 'select id, nombre, apellidos, dni, id_ocupacion from persona where id=?'
        
        cursor = cnx.execute(cons_update_datos_servidor, (id,))
        filas = cursor.fetchone()
        
        # Bloque de vehículos para una persona dada:
        consulta_vehiculos_almacenados_para_persona_dada = f"select id_vehiculo from persona_vh where id_persona = {id}"
        cursor = cnx.execute(consulta_vehiculos_almacenados_para_persona_dada)
        tmp = cursor.fetchall()
        listado_vehiculos_persona = []
        for t in tmp:
            listado_vehiculos_persona.append(t[0])
        
    cnx.close()
       
    return {'datos':filas, 'ocupaciones':lista_ocupaciones, 'numeros':lista_numeros, 'vehiculos':lista_vehiculos, 'listado_vehiculos':listado_vehiculos_persona}
    

@route('/guardar', method='POST')
def guardar():
    """ vehiculos = []
    nombre = request.POST.fname
    apellidos = request.POST.lname
    coche = request.POST.cars
    numero = request.POST.daigual
    if 'vehicle' in request.POST:
        vehiculos = list(request.POST.dict['vehicle']) """
    
    nombre = request.POST.nombre
    apellidos = request.POST.apellidos
    dni = request.POST.dni
    id = request.POST.id
    ocupacion = request.POST.ocupacion
    numero = request.POST.daigual
    vehiculos = request.POST.dict['vehiculo']    # es una lista de vehiculos

    cnx = sqlite3.connect(BASE_DATOS)
    
    
    if id == '': # Alta
        cons_insercion_datos_servidor = 'insert into persona (nombre, apellidos, dni, id_ocupacion, id_numero) values (?,?,?,?,?)'
        tmp = cnx.execute(cons_insercion_datos_servidor, (nombre,apellidos,dni,ocupacion,numero)) 
        # consulta_alta_persona_con_vehiculo = 'select max(id) from persona'
        nuevo_id_persona = tmp.lastrowid
        # -------------------------------
        for v in vehiculos:
            consulta_insert_persona_veh = f'insert into persona_vh(id_persona, id_vehiculo) values({nuevo_id_persona},{v})'
            cnx.execute(consulta_insert_persona_veh)

    else:   # Actualizacion
        consulta = "update persona set nombre=?, apellidos=?, dni=? , id_ocupacion=? , id_numero=? where id=?"
        cnx.execute(consulta, (nombre,apellidos,dni,ocupacion,numero))
    cnx.commit()
    cnx.close()

    redirect('/')

@route('/borrar/<id:int>')
def borrar(id):
    cnx = sqlite3.connect(BASE_DATOS)
    consulta = f'delete from persona where id = "{id}"'
    cnx.execute(consulta)
    cnx.commit()
    cnx.close()
    redirect('/')


    print('Hecho')


# ==============================================================================

run(host='localhost', port=8080, debug=True)
