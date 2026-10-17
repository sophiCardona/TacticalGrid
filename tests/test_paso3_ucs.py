import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from escenario.cargador import cargar_escenario
from juego.problema_navegacion import ProblemaNavegacion
from algoritmos.base import ejecutar_algoritmo
from verificacion.verificador import verificar_camino

RUTA_CASO2 = os.path.join(os.path.dirname(__file__), "..", "escenarios", "caso2_ruta_corta_vs_economica.json")


class TestUCS(unittest.TestCase):
    def setUp(self):
        self.esc = cargar_escenario(RUTA_CASO2)
        self.problema = ProblemaNavegacion(self.esc.mapa, (2, 2), (2, 8))

    def test_ucs_ejecucion_y_verificacion(self):
        res = ejecutar_algoritmo("UCS", self.problema)
        self.assertTrue(res.exito)
        self.assertIsNotNone(res.costo)
        self.assertGreater(res.estados_expandidos, 0)
        self.assertGreater(res.estados_generados, 0)
        self.assertGreater(res.maximo_frontera, 0)

        checks = verificar_camino(self.esc.mapa, self.problema.inicio, self.problema.objetivo, res)
        self.assertTrue(all(ok for _, ok, _ in checks))

    def test_caso2_bfs_vs_ucs_diferencia(self):
        """Caso 2: Ruta corta vs. ruta económica.
        BFS debe encontrar menos movimientos (camino más corto en saltos pero más caro).
        UCS debe encontrar menor costo acumulado (rodeo más largo en saltos pero más barato)."""
        res_bfs = ejecutar_algoritmo("BFS", self.problema)
        res_ucs = ejecutar_algoritmo("UCS", self.problema)

        self.assertTrue(res_bfs.exito)
        self.assertTrue(res_ucs.exito)

        # Verificar que los caminos son distintos
        self.assertNotEqual(res_bfs.camino, res_ucs.camino)

        # BFS tiene menor número de movimientos
        self.assertLess(res_bfs.longitud, res_ucs.longitud)

        # UCS tiene menor costo total acumulado
        self.assertLess(res_ucs.costo, res_bfs.costo)


if __name__ == "__main__":
    unittest.main(verbosity=2)
