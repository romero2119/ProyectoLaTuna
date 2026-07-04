from django.test import TestCase
from apl.models import Categoria

class PruebaBasica(TestCase):
    def test_verificar_entorno(self):
        """Una prueba simple para validar que CI/CD funciona"""
        self.assertEqual(1 + 1, 2)