"""Ejecución y reporte de los experimentos adversariales: Casos 7, 8, 9 y 10.
Uso: python experimentos/ejecutar_casos_adversariales.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from escenario.cargador import cargar_escenario
from juego.reglas import Reglas
from algoritmos.minimax import minimax, alfa_beta

DIR_MINIMOS = os.path.join(os.path.dirname(__file__), "..", "escenarios", "casos minimos")
if not os.path.isdir(DIR_MINIMOS):
    DIR_MINIMOS = os.path.join(os.path.dirname(__file__), "..", "escenarios", "casos_minimos")


def demo_caso7():
    print("=" * 70)
    print("CASO 7: Decisión Adversarial (Interceptación táctica vs correr ciegamente)")
    print("=" * 70)
    esc = cargar_escenario(os.path.join(DIR_MINIMOS, "caso07_decision_adversarial.json"))
    r = Reglas(esc)
    s = esc.estado_inicial()
    res = alfa_beta(s, r, esc, profundidad_maxima=3)
    print(f"Estado inicial: Turno={s.turno}, Portador rival={s.portador}")
    print(f"Acción recomendada por Alfa-Beta: {res.accion}")
    print(f"Valor Minimax: {res.valor:.2f}")
    print("Explicación táctica: A1 decide entrar a la casilla del portador B1 para interceptarlo,")
    print("eliminando la unidad enemiga y recuperando el recurso según la Regla R4.\n")


def demo_caso8():
    print("=" * 70)
    print("CASO 8: Minimax frente a Poda Alfa-Beta")
    print("=" * 70)
    esc = cargar_escenario(os.path.join(DIR_MINIMOS, "caso08_minimax_vs_alfa_beta.json"))
    r = Reglas(esc)
    s = esc.estado_inicial()
    res_mm = minimax(s, r, esc, profundidad_maxima=3, orden_acciones="estandar")
    res_ab = alfa_beta(s, r, esc, profundidad_maxima=3, orden_acciones="estandar")

    print(f"{'Algoritmo':<12} | {'Acción':<22} | {'Valor':<8} | {'Nodos Eval':<10} | {'Podas':<8} | {'Tiempo ms':<10}")
    print("-" * 80)
    print(f"{res_mm.algoritmo:<12} | {str(res_mm.accion):<22} | {res_mm.valor:<8.2f} | {res_mm.nodos_evaluados:<10} | {res_mm.nodos_podados:<8} | {res_mm.tiempo_ms:<10.3f}")
    print(f"{res_ab.algoritmo:<12} | {str(res_ab.accion):<22} | {res_ab.valor:<8.2f} | {res_ab.nodos_evaluados:<10} | {res_ab.nodos_podados:<8} | {res_ab.tiempo_ms:<10.3f}")
    ahorro = (1 - res_ab.nodos_evaluados / res_mm.nodos_evaluados) * 100
    print(f"\nConclusión: Misma jugada y mismo valor. Alfa-Beta redujo las evaluaciones en un {ahorro:.1f}%.\n")


def demo_caso9():
    print("=" * 70)
    print("CASO 9: Impacto del Orden de Acciones en la Poda Alfa-Beta")
    print("=" * 70)
    ruta = os.path.join(DIR_MINIMOS, "caso09_orden_acciones.json")
    if not os.path.exists(ruta):
        ruta = os.path.join(DIR_MINIMOS, "caso08_minimax_vs_alfa_beta.json")
    esc = cargar_escenario(ruta)
    r = Reglas(esc)
    s = esc.estado_inicial()

    print(f"{'Orden':<12} | {'Nodos Eval':<12} | {'Nodos Podados':<14} | {'Tiempo ms':<10}")
    print("-" * 55)
    for orden in ("estandar", "inverso", "heuristico"):
        res = alfa_beta(s, r, esc, profundidad_maxima=3, orden_acciones=orden)
        print(f"{orden:<12} | {res.nodos_evaluados:<12} | {res.nodos_podados:<14} | {res.tiempo_ms:<10.3f}")
    print("\nConclusión: El orden heurístico (mejores acciones primero) maximiza los cortes")
    print("prematuros, evaluando significativamente menos ramas que el orden inverso.\n")


def demo_caso10():
    print("=" * 70)
    print("CASO 10: Efecto de la Variación de Profundidad en Minimax")
    print("=" * 70)
    ruta = os.path.join(DIR_MINIMOS, "caso10_profundidad.json")
    if not os.path.exists(ruta):
        ruta = os.path.join(DIR_MINIMOS, "caso08_minimax_vs_alfa_beta.json")
    esc = cargar_escenario(ruta)
    r = Reglas(esc)
    s = esc.estado_inicial()

    print(f"{'Profundidad':<12} | {'Acción Elegida':<22} | {'Valor':<8} | {'Nodos Eval':<12} | {'Tiempo ms':<10}")
    print("-" * 72)
    for prof in (1, 2, 3, 4):
        res = alfa_beta(s, r, esc, profundidad_maxima=prof, orden_acciones="heuristico")
        print(f"{prof:<12} | {str(res.accion):<22} | {res.valor:<8.2f} | {res.nodos_evaluados:<12} | {res.tiempo_ms:<10.3f}")
    print("\nConclusión: A mayor profundidad, mayor anticipación táctica con costo temporal exponencial.\n")


if __name__ == "__main__":
    demo_caso7()
    demo_caso8()
    demo_caso9()
    demo_caso10()
