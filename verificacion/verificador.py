"""Verificación de soluciones: comprueba propiedades del camino, no solo lo produce."""


def verificar_camino(mapa, inicio, objetivo, resultado):
    """Purpose: comprobar que un camino devuelto por una búsqueda es correcto.
    Preconditions: resultado.exito es True.
    Postconditions: lista de (descripción, ok, detalle); el camino es válido sii todos los ok son True.
    Complexity: O(longitud del camino).
    AI usage: Yes. AI intervention: generó la lista de comprobaciones a partir del enunciado.
    Student validation: (completar: caminos corruptos a mano que probaron)."""
    cam = [tuple(p) for p in resultado.camino]
    checks = []
    checks.append(("El camino comienza en la celda inicial", bool(cam) and cam[0] == tuple(inicio),
                   f"primera celda = {cam[0] if cam else None}"))
    dentro = bool(cam) and all(mapa.dentro(*p) for p in cam)
    checks.append(("Todas las celdas están dentro del mapa", dentro, ""))
    libre = dentro and all(mapa.es_transitable(*p) for p in cam)
    checks.append(("Ninguna celda es un obstáculo", libre, ""))
    pasos = all(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 for a, b in zip(cam, cam[1:]))
    checks.append(("Cada movimiento es válido (un paso ortogonal)", pasos, ""))
    recalculado = sum(mapa.costo(*p) for p in cam[1:]) if libre else None
    coincide = recalculado is not None and resultado.costo is not None and abs(recalculado - resultado.costo) < 1e-9
    checks.append(("El costo reportado coincide con las transiciones", coincide,
                   f"reportado = {resultado.costo}, recalculado = {recalculado}"))
    checks.append(("El estado final cumple la condición objetivo", bool(cam) and cam[-1] == tuple(objetivo),
                   f"última celda = {cam[-1] if cam else None}, objetivo = {tuple(objetivo)}"))
    return checks
