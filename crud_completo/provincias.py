from sql2 import Sqlite
from settings import BD


class Provincia():
    tabla = 'T_provincias'
    def __init__(self, codigo, descripcion,id = None) -> None:
        self.__id = id
        self.__codigo = codigo
        self.__descripcion = descripcion
    
    def insertar(self):
        #TODO: Poner try
        # Obsoleto
        manejador = Sqlite(BD)
        campos = 'codigo,descripcion'
        valores = f'{self.__codigo},{self.__descripcion}'
        nuevo_id = manejador.insertar(Provincia.tabla,campos,valores)
        return nuevo_id

    def actualizar(self):
        #TODO: Poner try
        # Obsoleto
        manejador = Sqlite(BD)
        campos = 'codigo,descripcion'
        valores = f'{self.__codigo},{self.__descripcion}'
        nuevo_id = manejador.actualizar(Provincia.tabla,campos,valores, self.__id)
        return nuevo_id  
          
    def guardar(self):
        #TODO: Poner try
        manejador = Sqlite(BD)
        campos = 'codigo,descripcion'
        valores = f'{self.__codigo},{self.__descripcion}'
        if self.__id:
            nuevo_id = manejador.actualizar(Provincia.tabla,campos,valores, self.__id)
            return nuevo_id
        else:
            nuevo_id = manejador.insertar(Provincia.tabla,campos,valores)
            return  self.leer_por_id(nuevo_id)
             
    def leer_por_id(self,id_provincia):
        """
        Buscar en la bd un registro con el id pasado como parámetro.
        Si existe devuelve un objeto con esas propiedades.
        Si no existe devuelve None
        """
        
        #TODO: Poner try
        manejador = Sqlite(BD)
        lista = manejador.seleccionar(f'select * from T_provincias where id ={id_provincia}')
        if lista:
            #return Provincia(lista[0][1],lista[0][2],lista[0][0])
            return Provincia(   id          =lista[0][0],
                                codigo      =lista[0][1],
                                descripcion =lista[0][2])
        else:
            return None

    def borrar(self):
        """
        Borra de la bd un registro con el id pasado como parámetro.
        Si existe devuelve el número de filas borradas (1).
        Si no existe devuelve None
        """
        id_provincia = self.__id
        manejador = Sqlite(BD)
        resp = manejador.borrar(Provincia.tabla,'id',id_provincia)
        return resp

    @property
    def id(self):
        return self.__id

    @property
    def codigo(self):
        return self.__codigo

    @property
    def descripcion(self):
        return self.__descripcion