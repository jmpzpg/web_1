import unittest
from provincias import Provincia

class TestProvincia(unittest.TestCase):
    def test_existencia(self):
        p = Provincia('','')
        self.assertIsNotNone(p)
    
    def test_insert_provincia(self):
        p = Provincia(111,'primera')
        resp = p.insertar()
        self.assertIsNotNone(resp)

    def test_actualizar_provincia(self):
        p = Provincia(777,'Modificado',10)
        resp = p.actualizar()
        self.assertEqual(resp,1)

    def test_guardar_provincia_nueva(self):
        p = Provincia(1313,'Murcia')
        resp = p.guardar()
        self.assertIsNotNone(resp)

    def test_guardar_provincia_existente(self):
        p = Provincia(999,'Ahora si',26)
        resp = p.guardar()
        self.assertEqual(resp,1)    

    def test_leer_no_existente(self):
        p = Provincia('','')
        resp = p.leer_por_id(199)
        self.assertIsNone(resp)

    def test_leer_existente(self):
        p = Provincia('','')
        resp = p.leer_por_id(1) #Huelva
        self.assertIsNotNone(resp)

    def test_borrar_existente(self):
        p = Provincia('','',id=25)
        resp = p.borrar() 
        self.assertEqual(resp,1)

    def test_borrar_no_existente(self):
        p = Provincia('','',id=991)
        resp = p.borrar() 
        self.assertEqual(resp,0)         