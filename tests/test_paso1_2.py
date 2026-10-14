import json, os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from escenario.cargador import cargar_escenario, construir_escenario, ErrorEscenario
from juego.estado import Accion
from juego.reglas import Reglas

RUTA = os.path.join(os.path.dirname(__file__), "..", "escenarios", "ejemplo.json")
def datos():
    with open(RUTA, encoding="utf-8") as f:
        return json.load(f)

class TestCarga(unittest.TestCase):
    def test_valido(self):
        esc = cargar_escenario(RUTA)
        self.assertEqual(esc.mapa.filas, 4)
        self.assertEqual(esc.mapa.costo(2, 2), 7)
        self.assertEqual(esc.mapa.costo_minimo(), 1)
        self.assertEqual(esc.profundidad_minimax, 4)
    def test_errores_multiples(self):
        d = datos()
        d["terreno"][0][0] = "lava"
        d["unidades"][1]["id"] = "A1"
        d["unidades"][2]["fila"] = 99
        d["turno"] = "C"
        d["juego"]["portador_recurso"] = "Z9"
        self.assertGreaterEqual(len(self._errs(d)), 5)
    def test_unidad_sobre_muro(self):
        d = datos(); d["unidades"][0].update(fila=1, columna=1)
        self.assertTrue(any("no transitable" in x for x in self._errs(d)))
    def test_costo_no_positivo(self):
        d = datos(); d["tipos_terreno"]["pasto"]["costo"] = 0
        self.assertTrue(any("costo positivo" in x for x in self._errs(d)))
    def test_dimensiones_inconsistentes(self):
        d = datos(); d["mapa"]["filas"] = 5
        self.assertTrue(any("filas" in x for x in self._errs(d)))
    def _errs(self, d):
        with self.assertRaises(ErrorEscenario) as cm:
            construir_escenario(d)
        return cm.exception.errores

class TestJuego(unittest.TestCase):
    def setUp(self):
        self.esc = cargar_escenario(RUTA)
        self.r = Reglas(self.esc)
        self.s0 = self.esc.estado_inicial()
    def test_hashable_e_inmutable(self):
        self.assertEqual(self.s0, self.esc.estado_inicial())
        self.assertEqual(len({self.s0, self.esc.estado_inicial()}), 1)
    def test_acciones_y_sucesor(self):
        acs = self.r.acciones_legales(self.s0)
        self.assertTrue(all(self.s0.unidad(a.unidad_id).bando == "A" for a in acs))
        s1 = self.r.aplicar(self.s0, acs[0])
        self.assertEqual(s1.turno, "B")
        self.assertEqual(self.s0.turno, "A")
    def test_estado_compuesto(self):
        d = datos(); d["unidades"][0].update(fila=2, columna=2)
        sin = construir_escenario(d)
        d["juego"]["portador_recurso"] = "A1"
        con = construir_escenario(d)
        a, b = sin.estado_inicial(), con.estado_inicial()
        self.assertEqual(a.unidad("A1"), b.unidad("A1"))
        self.assertNotEqual(a, b)
    def test_recoger_recurso(self):
        d = datos(); d["unidades"][0].update(fila=2, columna=1)
        esc = construir_escenario(d); r = Reglas(esc)
        s = r.aplicar(esc.estado_inicial(), Accion("A1", "MOVER", (2, 2)))
        self.assertEqual(s.portador, "A1"); self.assertIsNone(s.recurso_pos)
    def test_victoria(self):
        d = datos(); d["juego"]["portador_recurso"] = "A1"
        esc = construir_escenario(d); r = Reglas(esc)
        s = r.aplicar(esc.estado_inicial(), Accion("A1", "MOVER", (0, 0)))
        self.assertEqual(r.ganador(s), "A"); self.assertTrue(r.es_terminal(s))
    def test_interceptar(self):
        d = datos(); d["juego"]["portador_recurso"] = "B1"
        d["unidades"][0].update(fila=3, columna=1)
        esc = construir_escenario(d); r = Reglas(esc)
        s = r.aplicar(esc.estado_inicial(), Accion("A1", "MOVER", (3, 2)))
        self.assertIsNone(s.unidad("B1")); self.assertEqual(s.portador, "A1")
    def test_no_atraviesa_muro_ni_ocupadas(self):
        for a in self.r.acciones_legales(self.s0):
            if a.tipo == "MOVER":
                self.assertTrue(self.esc.mapa.es_transitable(*a.destino))
                self.assertNotIn(a.destino, {(u.fila, u.columna) for u in self.s0.unidades})

if __name__ == "__main__":
    unittest.main(verbosity=2)
