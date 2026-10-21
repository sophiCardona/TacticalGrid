"""BFS y DFS"""
from collections import deque

from algoritmos.base import ResultadoBusqueda, reconstruir_camino, registrar


def _exito(nombre, padre, meta, gen, exp, mf, explorados):
    camino, costo = reconstruir_camino(padre, meta)
    return ResultadoBusqueda(nombre, True, camino, costo, gen, exp, mf, explorados=explorados)


@registrar("BFS")
def bfs(problema, **params):
    """Purpose: hallar el camino con MENOS movimientos (ignora costos de terreno).
    Preconditions: problema expone estado_inicial(), es_objetivo(s), sucesores(s).
    Postconditions: camino óptimo en número de pasos si existe; contadores coherentes:
      generados = estados metidos a la frontera; expandidos = estados cuyos sucesores se analizaron
      (la meta no cuenta como expandida porque se detecta antes de analizarla).
    Complexity: tiempo O(V+E), espacio O(V).
    AI usage: Yes. AI intervention: generó la implementación base.
    Student validation: Se ha validado la función con varios escenarios de prueba, incluyendo casos con ciclos y sin solución."""
    ini = problema.estado_inicial()
    frontera = deque([ini])
    padre = {ini: None}
    gen, exp, mf, explorados = 1, 0, 1, []
    while frontera:
        s = frontera.popleft()
        if problema.es_objetivo(s):
            return _exito("BFS", padre, s, gen, exp, mf, explorados)
        exp += 1
        explorados.append(s)
        for _, s2, costo in problema.sucesores(s):
            if s2 not in padre:          # visitado se marca al GENERAR
                padre[s2] = (s, costo)
                frontera.append(s2)
                gen += 1
        mf = max(mf, len(frontera))
    return ResultadoBusqueda("BFS", False, [], None, gen, exp, mf, explorados=explorados)


@registrar("DFS")
def dfs(problema, **params):
    """Purpose: hallar ALGÚN camino explorando en profundidad (no garantiza el más corto ni el más barato).
    Preconditions: igual que bfs.
    Postconditions: camino válido si existe; usa conjunto de visitados para evitar ciclos.
      Se marca visitado al EXPANDIR (pueden existir duplicados en la pila, que se descartan al sacarlos).
    Complexity: tiempo O(V+E), espacio O(V).
    AI usage: Yes. AI intervention: generó la implementación base.
    Student validation: Se ha validado la función con varios escenarios de prueba, incluyendo casos con ciclos y sin solución."""
    ini = problema.estado_inicial()
    pila = [(ini, None, 0)]
    padre = {}
    gen, exp, mf, explorados = 1, 0, 1, []
    while pila:
        s, ant, costo = pila.pop()
        if s in padre:
            continue
        padre[s] = None if ant is None else (ant, costo)
        if problema.es_objetivo(s):
            return _exito("DFS", padre, s, gen, exp, mf, explorados)
        exp += 1
        explorados.append(s)
        for _, s2, c in reversed(problema.sucesores(s)):   # reversed: el 1.er vecino se explora primero
            if s2 not in padre:
                pila.append((s2, s, c))
                gen += 1
        mf = max(mf, len(pila))
    return ResultadoBusqueda("DFS", False, [], None, gen, exp, mf, explorados=explorados)
