from settings import TEMPLATES,BD,STATIC_FILES
from bottle import run, route, jinja2_view, TEMPLATE_PATH, request, redirect, static_file
from sql2 import Sqlite
from provincias import Provincia

bdatos = Sqlite(BD)
TEMPLATE_PATH.append(TEMPLATES)

@route('/static/<filename:path>')
def server_static(filename):
    archivo = static_file(filename, root=STATIC_FILES)
    return archivo

@route('/')
@jinja2_view('prov_home.html')
def lista():
    registros = bdatos.seleccionar('Select * from T_provincias')
    return {'rows':registros}

@route('/ins')
@jinja2_view('formulario.html')
def nuevo():
    return {}

@route('/edit/<id:int>')
@jinja2_view('prov_formulario.html')
def editar(id):
    p = Provincia('','')
    provincia = p.leer_por_id(id)
    if provincia:
        return {'row':provincia}
    else:
        return {}

# @route('/del/<el_id:int>')
# def borrar(el_id):
#     art = Articulos(id=el_id)
#     bdatos.delete(art)
#     redirect('/')

# @route('/save', method='POST')
# def guardar():
#     art = Articulos()
#     art.id = request.POST.id.strip()
#     art.codigo = request.POST.codigo.strip()
#     art.descripcion = request.POST.descripcion.strip()
#     art.precio = request.POST.precio.strip()
#     if request.POST.id.strip(): #Actualizar
#         bdatos.update(art)
#     else:
#         bdatos.insert(art)
#     redirect('/')


run(host='localhost', port=8000,debug=True,reloader=True)