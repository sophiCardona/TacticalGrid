"""Búsqueda con memoria limitada: Beam Search (Búsqueda en Haz)."""
from algoritmos.base import ResultadoBusqueda, reconstruir_camino, registrar
from algoritmos.a_estrella import obtener_heuristica


def _exito(nombre, padre, meta, gen, exp, mf, explorados):
    camino, costo = reconstruir_camino(padre, meta)
    return ResultadoBusqueda(
        nombre,
        True,
        camino,
        costo,
        gen,
        exp,
        mf,
        explorados=explorados,
    )


@registrar("BEAM_SEARCH")
def beam_search(problema, **params):
    """Purpose: Búsqueda con memoria limitada (Haz / Beam Search) con tamaño de haz k.
    Preconditions: problema es una instancia válida de Problema; params contiene opcionalmente 'k' y 'heuristica'.
    Postconditions: ResultadoBusqueda con el camino hallado (si existe) y métricas.
    Complexity: O(profundidad * k * b) en tiempo; O(k * profundidad) en espacio.
    AI usage: Yes. AI intervention: estructuración del haz por niveles.
    Student validation: verificado sobre caso05_beam_search con k = 1, 2, 4, 8."""
    try:
        k = max(1, int(params.get("k", 2)))
    except (ValueError, TypeError):
        k = 2

    h_nombre = params.get("heuristica", "manhattan")
    h_fn = obtener_heuristica(h_nombre)

    ini = problema.estado_inicial()
    haz = [ini]
    padre = {ini: None}
    explorados = []
    gen, exp, mf = 1, 0, 1

    while haz:
        for s in haz:
            if problema.es_objetivo(s):
                return _exito("BEAM_SEARCH", padre, s, gen, exp, mf, explorados)

        candidatos = []
        for s in haz:
            exp += 1
            explorados.append(s)
            for _, s2, costo in problema.sucesores(s):
                if s2 not in padre:
                    padre[s2] = (s, costo)
                    h_val = h_fn(s2, problema)
                    candidatos.append((h_val, s2))
                    gen += 1

        if not candidatos:
            break

        candidatos.sort(key=lambda x: (x[0], x[1]))

        nuevo_haz = []
        vistos_nivel = set()
        for h_val, s2 in candidatos:
            if s2 not in vistos_nivel:
                vistos_nivel.add(s2)
                nuevo_haz.append(s2)
                if len(nuevo_haz) == k:
                    break

        haz = nuevo_haz
        mf = max(mf, len(haz))

    return ResultadoBusqueda("BEAM_SEARCH", False, [], None, gen, exp, mf, explorados=explorados)
