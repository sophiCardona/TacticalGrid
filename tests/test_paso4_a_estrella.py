import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from escenario.cargador import cargar_escenario
from juego.problema_navegacion import ProblemaNavegacion
from algoritmos.base import ejecutar_algoritmo
from algoritmos.a_estrella import h_manhattan, h_propia, h_euclidiana
from verificacion.verificador import verificar_camino

RUTA_CASO3 = os.path.join(os.path.dirname(__file__), "..", "escenarios", "casos minimos",
                          "caso3_obstaculo_y_heuristica.json")
RUTA_CASO4 = os.path.join(os.path.dirname(__file__), "..", "escenarios", "casos minimos",
                          "caso4_comparacion_heuristicas.json")


class TestAEstrella(unittest.TestCase):
    def test_admisibilidad_heuristicas(self):
        esc = cargar_escenario(RUTA_CASO4)
        p = ProblemaNavegacion(esc.mapa, (10, 4), (10, 16))

        # En la meta, todas deben ser exactamente 0
        self.assertEqual(h_manhattan(p.objetivo, p), 0)
        self.assertEqual(h_propia(p.objetivo, p), 0)
        self.assertEqual(h_euclidiana(p.objetivo, p), 0)

        # En el inicio, h_propia >= h_manhattan >= h_euclidiana
        hm = h_manhattan(p.inicio, p)
        hp = h_propia(p.inicio, p)
        he = h_euclidiana(p.inicio, p)

        self.assertGreaterEqual(hp, hm)
        self.assertGreaterEqual(hm, he)

    def test_caso3_obstaculo_y_heuristica(self):
        """Caso 3: La heurística intenta avanzar en línea recta, pero un muro
        obliga al algoritmo a rodear el obstáculo."""
        esc = cargar_escenario(RUTA_CASO3)
        p = ProblemaNavegacion(esc.mapa, (10, 4), (10, 12))

        res = ejecutar_algoritmo("A_ESTRELLA", p, heuristica="manhattan")
        self.assertTrue(res.exito)
        checks = verificar_camino(esc.mapa, p.inicio, p.objetivo, res)
        self.assertTrue(all(ok for _, ok, _ in checks))

        # Verificar que el camino rodea el muro (pasa por fila <= 5 o fila >= 15)
        filas_camino = [f for f, c in res.camino]
        self.assertTrue(any(f <= 5 or f >= 15 for f in filas_camino))

    def test_caso4_comparacion_heuristicas(self):
        """Caso 4: Comparar A* con Manhattan vs Propia en el mismo escenario.
        Ambas deben encontrar un camino de costo óptimo idéntico,
        pero la heurística propia debe expandir menos estados al ser más ajustada."""
        esc = cargar_escenario(RUTA_CASO4)
        p = ProblemaNavegacion(esc.mapa, (10, 4), (10, 16))

        res_manhattan = ejecutar_algoritmo("A_ESTRELLA", p, heuristica="manhattan")
        res_propia = ejecutar_algoritmo("A_ESTRELLA", p, heuristica="propia")

        self.assertTrue(res_manhattan.exito)
        self.assertTrue(res_propia.exito)

        # Ambos encuentran el costo óptimo idéntico
        self.assertEqual(res_manhattan.costo, res_propia.costo)

        # La heurística propia es más informada y expande menos nodos
        self.assertLess(res_propia.estados_expandidos, res_manhattan.estados_expandidos)


if __name__ == "__main__":
    unittest.main(verbosity=2)
