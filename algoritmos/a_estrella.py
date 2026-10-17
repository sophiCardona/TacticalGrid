"""Búsqueda informada: Algoritmo A* con heurísticas admisibles."""
import heapq

from algoritmos.base import ResultadoBusqueda, reconstruir_camino, registrar


def _exito(nombre, padre, meta, gen, exp, mf, explorados):
    camino, costo = reconstruir_camino(padre, meta)
    return ResultadoBusqueda(nombre, True, camino, costo, gen, exp, mf, explorados=explorados)


def h_manhattan(s, problema):
    """Purpose: estimar costo restante usando la distancia Manhattan escalada por c_min.
    Preconditions: s y problema.objetivo son tuplas (fila, columna) válidas.
    Postconditions: devuelve cota inferior admisible h(s) <= h*(s).
    Complexity: O(1).
    AI usage: Yes. AI intervention: formulación de la distancia multiplicada por costo mínimo.
    Student validation: probado en cuadrícula con costos mayores a 1 para asegurar admisibilidad."""
    c_min = problema.mapa.costo_minimo()
    d = abs(s[0] - problema.objetivo[0]) + abs(s[1] - problema.objetivo[1])
    return d * c_min


def h_propia(s, problema):
    """Purpose: heurística propia informada por el terreno objetivo (Goal-Terrain Aware Manhattan).
    Preconditions: s y problema.objetivo son tuplas válidas; objetivo es transitable.
    Postconditions: devuelve cota inferior h(s) <= h*(s); domina a Manhattan si costo(obj) > c_min.
    Complexity: O(1).
    AI usage: Yes. AI intervention: ajuste del costo del último paso con el terreno real del objetivo.
    Student validation: demostrada matemáticamente su admisibilidad y verificada en pruebas unitarias."""
    if s == problema.objetivo:
        return 0
    c_min = problema.mapa.costo_minimo()
    d = abs(s[0] - problema.objetivo[0]) + abs(s[1] - problema.objetivo[1])
    c_obj = problema.mapa.costo(*problema.objetivo)
    return (d - 1) * c_min + c_obj


def h_euclidiana(s, problema):
    """Purpose: heurística euclidiana multiplicada por c_min.
    Preconditions: s y problema.objetivo son tuplas válidas.
    Postconditions: devuelve cota inferior admisible (más relajada que Manhattan en movimientos 4-dir).
    Complexity: O(1).
    AI usage: Yes. AI intervention: implementación matemática.
    Student validation: verificada con distancias euclidianas."""
    c_min = problema.mapa.costo_minimo()
    d = ((s[0] - problema.objetivo[0]) ** 2 + (s[1] - problema.objetivo[1]) ** 2) ** 0.5
    return d * c_min


HEURISTICAS = {
    "manhattan": h_manhattan,
    "propia": h_propia,
    "euclidiana": h_euclidiana,
}


def obtener_heuristica(nombre):
    clave = str(nombre).strip().lower()
    return HEURISTICAS.get(clave, h_manhattan)


@registrar("A_ESTRELLA")
def a_estrella(problema, **params):
    """Purpose: encontrar el camino óptimo hacia el objetivo minimizando f(n) = g(n) + h(n).
    Preconditions: problema expone estado_inicial(), es_objetivo(s), sucesores(s).
      params puede contener 'heuristica' ('manhattan', 'propia', 'euclidiana').
    Postconditions: ResultadoBusqueda con el camino óptimo y métricas registradas.
    Complexity: tiempo O(b^d) en el peor caso, pero fuertemente reducido según la calidad de h(n).
      Espacio O(b^d) para almacenar la frontera y los estados generados.
    AI usage: Yes. AI intervention: estructura del algoritmo A* con desempate por h(n).
    Student validation: verificado contra BFS y UCS, y comparadas ambas heurísticas en escenarios con obstáculos."""
    h_nombre = params.get("heuristica", "manhattan")
    h_fn = obtener_heuristica(h_nombre)

    ini = problema.estado_inicial()
    h_ini = h_fn(ini, problema)

    contador = 0
    # frontera: (f, h, contador, estado)
    frontera = [(h_ini, h_ini, contador, ini)]
    padre = {ini: None}
    mejor_g = {ini: 0}
    expandidos_set = set()
    explorados = []
    gen, exp, mf = 1, 0, 1

    while frontera:
        f, h, _, s = heapq.heappop(frontera)

        if s in expandidos_set:
            continue

        if problema.es_objetivo(s):
            return _exito("A_ESTRELLA", padre, s, gen, exp, mf, explorados)

        expandidos_set.add(s)
        exp += 1
        explorados.append(s)

        g_actual = mejor_g[s]
        for _, s2, costo_paso in problema.sucesores(s):
            nuevo_g = g_actual + costo_paso
            if s2 not in mejor_g or nuevo_g < mejor_g[s2]:
                mejor_g[s2] = nuevo_g
                padre[s2] = (s, costo_paso)
                h2 = h_fn(s2, problema)
                f2 = nuevo_g + h2
                contador += 1
                heapq.heappush(frontera, (f2, h2, contador, s2))
                gen += 1

        mf = max(mf, len(frontera))

    return ResultadoBusqueda("A_ESTRELLA", False, [], None, gen, exp, mf, explorados=explorados)
