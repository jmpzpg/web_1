import os
from bottle import route, run, TEMPLATE_PATH, jinja2_view, static_file

# para que bottle sepa donde buscar nuestras plantillas:
TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))

# hace falta otro route para la devolucion de los ficheros static desde el servidor, que seran los css:
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')

@route('/')
@jinja2_view('home2.html')
def hola():
    return {'datos':[('Teo', 1, 'lunes'),('Jose', 2,'Martes'),('Pau',3 , 'Jueves')]}

# =============

run(host='localhost', port=8080, debug=True)
