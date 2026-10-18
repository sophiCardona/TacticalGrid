"""Demuestra el caso 6: misma posición física, estados distintos. Uso: python3 experimentos/caso06_estado_compuesto.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from escenario.cargador import cargar_escenario
from juego.reglas import Reglas

D = os.path.join(os.path.dirname(__file__), "..", "escenarios", "casos_minimos")
a = cargar_escenario(os.path.join(D, "caso06a_sin_recurso.json"))
b = cargar_escenario(os.path.join(D, "caso06b_con_recurso.json"))
sa, sb = a.estado_inicial(), b.estado_inicial()
print("Posición de A1 en 6a:", (sa.unidad("A1").fila, sa.unidad("A1").columna),
      "| en 6b:", (sb.unidad("A1").fila, sb.unidad("A1").columna))
print("Unidades idénticas:", sa.unidades == sb.unidades)
print("Estados iguales:", sa == sb, "| mismo hash:", hash(sa) == hash(sb))
print("Portador 6a:", sa.portador, "| 6b:", sb.portador, "| recurso en el suelo 6a:", sa.recurso_pos, "| 6b:", sb.recurso_pos)
for nombre, esc, s in (("6a", a, sa), ("6b", b, sb)):
    acc = Reglas(esc).acciones_legales(s)
    b1 = [x.destino for x in acc if x.unidad_id == "B1" and x.tipo == "MOVER"]
    print(f"{nombre}: turno {s.turno}, acciones legales = {len(acc)}, movimientos de B1 = {b1}")
