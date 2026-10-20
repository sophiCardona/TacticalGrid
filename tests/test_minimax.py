import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from escenario.cargador import cargar_escenario
from juego.reglas import Reglas
from algoritmos.minimax import minimax, alfa_beta

CASOS = os.path.join(os.path.dirname(__file__), "..", "escenarios", "casos minimos")


class TestBusquedaAdversarial(unittest.TestCase):
    def cargar(self, nombre):
        esc = cargar_escenario(os.path.join(CASOS, nombre))
        return esc, Reglas(esc), esc.estado_inicial()

    def test_caso7_intercepta_portador_adyacente(self):
        esc, reglas, estado = self.cargar("caso07_decision_adversarial.json")
        resultado = alfa_beta(estado, reglas, esc, profundidad_maxima=3)
        self.assertEqual(estado.portador, "B1")
        self.assertEqual(resultado.accion.unidad_id, "A1")
        self.assertEqual(resultado.accion.destino, (8, 9))
        sucesor = reglas.aplicar(estado, resultado.accion)
        self.assertIsNone(sucesor.unidad("B1"))
        self.assertEqual(sucesor.portador, "A1")

    def test_caso8_minimax_y_alfa_beta_equivalentes(self):
        esc, reglas, estado = self.cargar("caso08_minimax_vs_alfa_beta.json")
        mm = minimax(estado, reglas, esc, 3, "estandar")
        ab = alfa_beta(estado, reglas, esc, 3, "estandar")
        self.assertEqual(mm.accion, ab.accion)
        self.assertAlmostEqual(mm.valor, ab.valor)
        self.assertLess(ab.nodos_evaluados, mm.nodos_evaluados)

    def test_rechaza_profundidad_invalida(self):
        esc, reglas, estado = self.cargar("caso08_minimax_vs_alfa_beta.json")
        for profundidad in (0, -1, 1.5):
            with self.assertRaises(ValueError):
                alfa_beta(estado, reglas, esc, profundidad)


if __name__ == "__main__":
    unittest.main(verbosity=2)