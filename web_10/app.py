import os
from bottle import route, run, TEMPLATE_PATH, jinja2_view, static_file, request, redirect
import sqlite3

BASE_DATOS = os.path.join(os.path.dirname(__file__),'personas.db')

# para que bottle sepa donde buscar nuestras plantillas:
TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))

# hace falta otro route para la devolucion de los ficheros static desde el servidor. Los css:
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')

# -----------------------------------------------------------------------------------------
# --------------------------------- HOME de la web ----------------------------------------
# ------------------------------------------------------------------------------------------

@route('/')
@jinja2_view('home2.html')
def hola():
    # return {'datos':[('Teo', 1, 'lunes'),('Jose', 2,'Martes'),('Pau',3 , 'Jueves')]}

    # consulta para recoger de la tabla persona (de la BD) todos los campos para pintar la tabla del HOME
    cons_vista_datos_servidor = '''select p.id, p.nombre, p.apellidos, p.dni, t.descripcion, n.descripcion 
                                    from persona p left join T_ocupacion t on p.id_ocupacion = t.id 
                                    left join T_numero n on n.id =p.id_numero '''
    
    cnx = sqlite3.connect(BASE_DATOS)
    cursor = cnx.execute(cons_vista_datos_servidor)
    filas = cursor.fetchall()
    
    cnx.close()
    return {'datos':filas}  # la variable FILAS contiene todos los campos para pintar la tabla del HOME

# ------------------------------------------------------------------------------------------
# --------------------------------- EDITAR registro ----------------------------------------
# ------------------------------------------------------------------------------------------

@route('/editar')
@route('/editar/<id:int>')
@jinja2_view('formulario.html')
def mi_form(id=None):
    cnx = sqlite3.connect(BASE_DATOS)

    # Bloque de ocupaciones para pintar:
    consulta_ocupaciones = "select * from T_ocupacion"
    cursor = cnx.execute(consulta_ocupaciones)
    t_ocupaciones = cursor.fetchall()

    # Bloque de números para pintar:
    consulta_numeros = "select * from T_numero"
    cursor = cnx.execute(consulta_numeros)
    t_numeros = cursor.fetchall()

    # Bloque de vehículos para pintar:
    consulta_vehiculos = "select * from T_vehiculo"
    cursor = cnx.execute(consulta_vehiculos)
    t_vehiculos = cursor.fetchall()


    if id is None: # es un ALTA
        # solo hay que facilitar los datos de las tablas T, para que estén disponibles en el alta de persona
        return {'ocupaciones':t_ocupaciones, 'numeros':t_numeros, 'vehiculos':t_vehiculos}

    else:   # es una ACTUALIZACIÓN del registro marcdo por "id"
        # Consulta para PINTAR los datos del registro indicado por el "id". Solo los Datos Personales + la Ocupación. SIN número y SIN vehículo
        cons_datos_Personales_y_Ocupacion_al_servidor = 'select id, nombre, apellidos, dni, id_ocupacion, id_numero from persona where id=?'
        
        cursor = cnx.execute(cons_datos_Personales_y_Ocupacion_al_servidor, (id,))
        filas = cursor.fetchone()
        
        # Bloque de vehículos para una persona dada:
        consulta_vehiculos_almacenados_para_persona_dada = f"select id_vehiculo from persona_vh where id_persona = {id}"
        cursor = cnx.execute(consulta_vehiculos_almacenados_para_persona_dada)
        tmp = cursor.fetchall()
        listado_vehiculos_persona = []
        for t in tmp:
            listado_vehiculos_persona.append(t[0])  # cada persona puede tener 0-n vehículos. Se añaden a esta lista
        
    cnx.close()
    # filas = los datos personales + la ocupación de la persona 
    # ocupaciones, numeros y vehiculos = los campos de las tablas T que recogen todos esos valores disponibles
    return {'datos':filas, 'ocupaciones':t_ocupaciones, 'numeros':t_numeros, 'vehiculos':t_vehiculos, 'listado_vehiculos':listado_vehiculos_persona}

# -------------------------------------------------------------------------------------------
# --------------------------------- GUARDAR registro ----------------------------------------
# -------------------------------------------------------------------------------------------    

@route('/guardar', method='POST')
def guardar():
    """ vehiculos = []
    nombre = request.POST.fname
    apellidos = request.POST.lname
    coche = request.POST.cars
    numero = request.POST.daigual
    if 'vehicle' in request.POST:
        vehiculos = list(request.POST.dict['vehicle']) """
    
    # ------------------------------- recogemos los campos del formulario en variables locales ------------------------
    nombre = request.POST.f_nombre
    apellidos = request.POST.f_apellidos
    dni = request.POST.f_dni
    id = request.POST.f_id
    ocupacion = request.POST.f_ocupacion
    numero = request.POST.f_numero
    vehiculos = request.POST.dict['f_vehiculo']    # es una lista de vehiculos
    # ------------------------------------------------------------------------------------------------------------------
    cnx = sqlite3.connect(BASE_DATOS)
    
    if id == '': # Alta
        cons_insercion_datos_servidor = ''' insert into persona (nombre, apellidos, dni, id_ocupacion, id_numero) 
                                                    values (?,?,?,?,?)'''
        tmp = cnx.execute(cons_insercion_datos_servidor, (nombre,apellidos,dni,ocupacion,numero)) 
        nuevo_id_persona = tmp.lastrowid
        # -----------------------insertamos en la tabla persona-vehiculo los marcados en el formulario -------------------
        for v in vehiculos:
            consulta_insert_persona_veh = f'insert into persona_vh(id_persona, id_vehiculo) values({nuevo_id_persona},{v})'
            cnx.execute(consulta_insert_persona_veh)

    else:   # Actualizacion
        consulta = "update persona set nombre=?, apellidos=?, dni=? , id_ocupacion=? , id_numero=? where id=?"
        cnx.execute(consulta, (nombre,apellidos,dni,ocupacion,numero,id))

    cnx.commit()
    cnx.close()

    redirect('/')

# -------------------------------------------------------------------------------------------
# --------------------------------- ELIMINAR registro ---------------------------------------
# ------------------------------------------------------------------------------------------- 

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
