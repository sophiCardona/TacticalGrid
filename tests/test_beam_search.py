"""Pruebas de regresión de Beam Search y sus tamaños de haz."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import algoritmos  # registra todos los algoritmos
from escenario.cargador import cargar_escenario
from juego.problema_navegacion import ProblemaNavegacion
from algoritmos.base import ejecutar_algoritmo
from verificacion.verificador import verificar_camino

CASOS = os.path.join(os.path.dirname(__file__), "..", "escenarios", "casos minimos")


class TestBeamSearch(unittest.TestCase):
    def test_k_1_2_4_8_devuelven_camino_valido_en_caso5(self):
        esc = cargar_escenario(os.path.join(CASOS, "caso05_beam_search.json"))
        inicio = next(u for u in esc.unidades if u.id == "A1")
        prueba = esc.prueba
        problema = ProblemaNavegacion(
            esc.mapa, (inicio.fila, inicio.columna),
            (prueba["objetivo"]["fila"], prueba["objetivo"]["columna"]))
        for k in (1, 2, 4, 8):
            with self.subTest(k=k):
                res = ejecutar_algoritmo("BEAM_SEARCH", problema, k=k,
                                         heuristica=prueba.get("heuristica", "manhattan"))
                # En este escenario adversarial, k=1 queda atrapado en la copa;
                # k mayores conservan alternativas y sí encuentran una ruta.
                if k == 1:
                    self.assertFalse(res.exito)
                else:
                    self.assertTrue(res.exito, f"Beam Search no encontró ruta con k={k}")
                    checks = verificar_camino(esc.mapa, problema.inicio, problema.objetivo, res)
                    self.assertTrue(all(ok for _, ok, _ in checks), checks)

    def test_sin_solucion_termina_sin_camino(self):
        esc = cargar_escenario(os.path.join(CASOS, "caso05_beam_search.json"))
        # El escenario real de caso 5 se prueba arriba; aquí el inicio y meta
        # quedan separados por una barrera creada en un mapa mínimo de prueba.
        from escenario.mapa import Mapa
        mapa = Mapa(3, 3,
                    (("pasto", "muro", "pasto"),
                     ("pasto", "muro", "pasto"),
                     ("pasto", "muro", "pasto")),
                    {"pasto": {"transitable": True, "costo": 1},
                     "muro": {"transitable": False, "costo": None}})
        problema = ProblemaNavegacion(mapa, (1, 0), (1, 2))
        res = ejecutar_algoritmo("BEAM_SEARCH", problema, k=2)
        self.assertFalse(res.exito)
        self.assertEqual(res.camino, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
