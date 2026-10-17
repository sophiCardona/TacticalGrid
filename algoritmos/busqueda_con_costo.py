"""Búsqueda basada en costos: Búsqueda de Costo Uniforme (UCS / Dijkstra)."""
import heapq

from algoritmos.base import ResultadoBusqueda, reconstruir_camino, registrar


def _exito(nombre, padre, meta, gen, exp, mf, explorados):
    camino, costo = reconstruir_camino(padre, meta)
    return ResultadoBusqueda(nombre, True, camino, costo, gen, exp, mf, explorados=explorados)


@registrar("UCS")
def ucs(problema, **params):
    """Purpose: encontrar el camino de menor costo acumulado g(n) hacia el objetivo.
    Preconditions: problema expone estado_inicial(), es_objetivo(s), sucesores(s). Costos de paso > 0.
    Postconditions: devuelve ResultadoBusqueda con el camino óptimo en costo si existe solución.
      Métricas registradas: estados_generados, estados_expandidos, maximo_frontera, tiempo, camino, costo.
    Complexity: tiempo O(b^(1 + floor(C*/eps))), espacio O(b^(1 + floor(C*/eps))) donde C* es el costo óptimo
      y eps el costo mínimo de acción.
    AI usage: Yes. AI intervention: implementación de la cola de prioridad y estructura de búsqueda por costo.
    Student validation: verificado en pruebas unitarias y comparado contra BFS en escenario de ruta corta vs. económica."""
    ini = problema.estado_inicial()
    contador = 0
    frontera = [(0, contador, ini)]
    padre = {ini: None}
    mejor_g = {ini: 0}
    expandidos_set = set()
    explorados = []
    gen, exp, mf = 1, 0, 1

    while frontera:
        g, _, s = heapq.heappop(frontera)

        if s in expandidos_set:
            continue

        if problema.es_objetivo(s):
            return _exito("UCS", padre, s, gen, exp, mf, explorados)

        expandidos_set.add(s)
        exp += 1
        explorados.append(s)

        for _, s2, costo_paso in problema.sucesores(s):
            nuevo_g = g + costo_paso
            if s2 not in mejor_g or nuevo_g < mejor_g[s2]:
                mejor_g[s2] = nuevo_g
                padre[s2] = (s, costo_paso)
                contador += 1
                heapq.heappush(frontera, (nuevo_g, contador, s2))
                gen += 1

        mf = max(mf, len(frontera))

    return ResultadoBusqueda("UCS", False, [], None, gen, exp, mf, explorados=explorados)
