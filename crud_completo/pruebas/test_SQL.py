import unittest
from sql import Sql
import settings

class Articulos():
    def __init__(self,id='', codigo = '', descripcion = '', precio = 0) -> None:
        self.codigo = codigo
        self.descripcion = descripcion
        self.precio = precio

class TestSql(unittest.TestCase):
    def test_existencia(self):
        s = Sql(settings.BD)
        self.assertIsNotNone(s)

    def test_prepara_insert(self):
        s = Sql(settings.BD)
        consulta = s.prepara_insert(Articulos('art','dscrp',99))
    
    def test_insert_correcto(self):
        s = Sql(settings.BD)
        nuevo_id = s.insert(Articulos('art','dscrp',99))
        self.assertIsNotNone(nuevo_id)

    def test_select_recien_insertado(self):
        s = Sql(settings.BD)
        nuevo_id = s.insert(Articulos('art_xx','dscrp',909))
        resp = s.select(f'select * from articulos where id ={nuevo_id}')
        self.assertIsNotNone(resp)

    def test_prepara_update(self):
        s = Sql(settings.BD)
        art = Articulos('art_xx','dscrp',909)
        art.id = 3
        consulta = s.prepara_update(art)
        self.assertEqual(consulta,
                "update articulos set codigo='art_xx',descripcion='dscrp',precio='909' where id = '3';")