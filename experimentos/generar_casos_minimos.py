"""Genera los escenarios de los casos mínimos 1, 5 y 6 (mapas de 20x20).
Uso: python3 experimentos/generar_casos_minimos.py
Los mapas se construyen por código para que sean reproducibles y fáciles de modificar."""
import json
import os
import random

SALIDA = os.path.join(os.path.dirname(__file__), "..", "escenarios", "casos_minimos")
N = 20
TIPOS = {
    "camino":  {"costo": 1, "transitable": True},
    "pasto":   {"costo": 2, "transitable": True},
    "bosque":  {"costo": 4, "transitable": True},
    "pantano": {"costo": 7, "transitable": True},
    "muro":    {"transitable": False},
}


def matriz(base="camino"):
    return [[base] * N for _ in range(N)]


def poner(m, celdas, tipo):
    for f, c in celdas:
        m[f][c] = tipo


def rect(f0, f1, c0, c1):
    return [(f, c) for f in range(f0, f1 + 1) for c in range(c0, c1 + 1)]


def unidad(i, b, f, c):
    return {"id": i, "bando": b, "tipo": "estandar", "fila": f, "columna": c}


def escenario(meta, terreno, bases, recurso, unidades, turno, portador, prueba, profundidad=3):
    return {**meta, "version": "1.0", "mapa": {"filas": N, "columnas": N}, "tipos_terreno": TIPOS,
            "terreno": terreno,
            "bases": {"A": {"fila": bases[0][0], "columna": bases[0][1]},
                      "B": {"fila": bases[1][0], "columna": bases[1][1]}},
            "recurso": {"fila": recurso[0], "columna": recurso[1]}, "unidades": unidades, "turno": turno,
            "juego": {"portador_recurso": portador, "profundidad_maxima_minimax": profundidad},
            "prueba": prueba}


def guardar(nombre, datos):
    ruta = os.path.join(SALIDA, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    print("generado:", os.path.normpath(ruta))


# ---------------------------------------------------------------- CASO 1: BFS frente a DFS
def caso1():
    m = matriz()
    for r in (rect(5, 7, 8, 9), rect(11, 13, 4, 5), rect(9, 10, 12, 14)):
        poner(m, r, "muro")
    unidades = [unidad("A1", "A", 2, 2), unidad("A2", "A", 2, 4), unidad("A3", "A", 4, 2),
                unidad("B1", "B", 17, 17), unidad("B2", "B", 17, 15), unidad("B3", "B", 15, 18)]
    guardar("caso01_bfs_vs_dfs.json", escenario(
        {"caso": 1, "descripcion": "Zona abierta con pocos obstáculos. BFS y DFS hallan solución; BFS el camino más corto, "
                                   "DFS uno largo y sinuoso. Usar «Comparar todos»."},
        m, ((0, 0), (19, 19)), (15, 16), unidades, "A", None,
        {"modo": "busqueda", "unidad_inicio": "A1", "objetivo": {"fila": 15, "columna": 16}}))


# ---------------------------------------------------------------- CASO 5: Beam Search y k
def caso5():
    m = matriz()
    muros = rect(0, 15, 12, 12)                                   # muro largo: hueco abajo (filas 16-19)
    muros += rect(6, 6, 7, 10) + rect(10, 10, 7, 10) + rect(6, 10, 10, 10)   # copa sin salida abierta a la izquierda
    poner(m, muros, "muro")
    unidades = [unidad("A1", "A", 8, 2), unidad("A2", "A", 2, 2), unidad("A3", "A", 14, 2),
                unidad("B1", "B", 3, 17), unidad("B2", "B", 14, 17), unidad("B3", "B", 17, 15)]
    guardar("caso05_beam_search.json", escenario(
        {"caso": 5, "descripcion": "Muro largo con hueco al fondo y una copa sin salida frente a él. La heurística (Manhattan) "
                                   "atrae a la búsqueda hacia la copa. Probar k = 1, 2, 4, 8 en modo exploración."},
        m, ((1, 1), (18, 18)), (8, 17), unidades, "A", None,
        {"modo": "busqueda", "algoritmo": "BEAM_SEARCH", "heuristica": "manhattan", "k": 1,
         "unidad_inicio": "A1", "objetivo": {"fila": 8, "columna": 17}}))


# ---------------------------------------------------------------- CASO 6: estado compuesto
def caso6():
    rng = random.Random(6)
    m = matriz()
    for f in range(N):
        for c in range(N):
            x = rng.random()
            m[f][c] = "pasto" if x < 0.18 else "bosque" if x < 0.26 else "pantano" if x < 0.30 else "camino"
    poner(m, [(5, 14), (14, 5), (7, 3), (12, 16)], "muro")
    unidades = [unidad("A1", "A", 10, 10), unidad("A2", "A", 3, 3), unidad("A3", "A", 3, 6),
                unidad("B1", "B", 10, 11), unidad("B2", "B", 16, 16), unidad("B3", "B", 16, 13)]
    for u in unidades:                                            # que ninguna unidad ni base quede sobre un muro
        assert m[u["fila"]][u["columna"]] != "muro"
    for pos in ((0, 0), (19, 19), (10, 15)):
        m[pos[0]][pos[1]] = "camino"
    comun = dict(terreno=m, bases=((0, 0), (19, 19)), recurso=(10, 15), unidades=unidades, turno="B",
                 prueba={"modo": "adversarial"})
    guardar("caso06a_sin_recurso.json", escenario(
        {"caso": "6a", "descripcion": "A1 en (10,10) SIN el recurso. B1, adyacente, no puede entrar a esa celda."},
        portador=None, **comun))
    guardar("caso06b_con_recurso.json", escenario(
        {"caso": "6b", "descripcion": "IDÉNTICO a 6a salvo juego.portador_recurso = A1. B1 puede interceptar a A1."},
        portador="A1", **comun))


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    caso1()
    caso5()
    caso6()
