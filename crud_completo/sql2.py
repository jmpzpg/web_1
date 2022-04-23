import sqlite3


class Sqlite():
    """
    Clase para gestionar el trabajo con la base de datos sqlite.
    - Conectarse a la BD
    - Insertar
    - Actualizar
    - Borrar
    - Seleccionar

    """
    #TODO: Eliminar la bd a piñón

    def __init__(self, bd) -> None:
        """
        Inicializa la clase con la propiedad nombre de la bd
        """
        self.__base_datos = bd

    def conectar(self):
        """
        Conecta/desconecta el código con la base de datos
        """
        cnx = sqlite3.connect(self.__base_datos)
        return cnx

    def seleccionar(self,consulta):
        """
        Ejecuta la consulta de selección de datos y devuelve el resultado
        """
        cnx = self.conectar()
        #TODO: Ejecutar dentro de un try
        cursor = cnx.cursor()
        cursor.execute(consulta)
        salida = cursor.fetchall()
        cnx.close()

        return salida
        
    def borrar(self,tabla, campo_id, valor_id):
        """
        Ejecuta la consulta de borrado de datos y devuelve el resultado
        """
        consulta = f'delete from {tabla} where {campo_id} = {valor_id};'
        cnx = self.conectar()
        #TODO: Ejecutar dentro de un try
        salida = cnx.execute(consulta)
        cnx.commit()
        cnx.close()
        return salida.rowcount

    def insertar(self,tabla, lista_campos, lista_valores):
        """ Añade un nuevo registro a la tabla pasada como parámetro.
            La lista de campos debe tener el mismo número de elementos que la de valores.
            La lista de campos y la de valores son una cadena de campos separados por comas.
        """
        cnx = self.conectar()
        #TODO: Ejecutar dentro de un try
        lista_comillas = [] 
        for val in lista_valores.split(','):
            lista_comillas.append("'" + val + "'")
        
        tmp = ','.join(lista_comillas)

        consulta = f'insert into {tabla}({lista_campos}) values({tmp});'
        cursor = cnx.cursor()
        cursor.execute(consulta)
        cnx.commit()
        salida = cursor.lastrowid
        cnx.close()

        return salida

    def actualizar(self,tabla, lista_campos, lista_valores,valor_id):
        """
        Actualiza un registro de la tabla pasada como parámetro.
        La lista de campos debe tener el mismo número de elementos que la de valores.
        La lista de campos y la de valores son una cadena de campos separados por comas.
        """
        cnx = self.conectar()
        #TODO: Ejecutar dentro de un try
        consulta = f'update {tabla} set '
        tmp = ''
        campos = lista_campos.split(',')
        valores = lista_valores.split(',')
        for i in range(len(valores)):
            tmp += f"{campos[i]}='{valores[i]}',"

        consulta += tmp[:-1]
        consulta += f' where id={valor_id};'

        cursor = cnx.cursor()
        cursor.execute(consulta)
        cnx.commit()
        salida = cursor.rowcount
        cnx.close()

        return salida
