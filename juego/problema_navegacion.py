"""Problema de navegación de UNA unidad (fases de búsqueda: se ignora al adversario)."""


class ProblemaNavegacion:
    """Estado = (fila, columna). Acciones = 4 movimientos a celdas transitables.
    Costo = costo del terreno de la celda destino (leído del escenario)."""

    def __init__(self, mapa, inicio, objetivo):
        self.mapa, self.inicio, self.objetivo = mapa, tuple(inicio), tuple(objetivo)

    def estado_inicial(self):
        return self.inicio

    def es_objetivo(self, s):
        return s == self.objetivo

    def sucesores(self, s):
        """Purpose: generar (nombre_accion, estado_siguiente, costo) en orden determinista.
        Preconditions: s es una celda transitable del mapa.
        Postconditions: solo celdas dentro del mapa y transitables; costo > 0.
        Complexity: O(1).
        AI usage: Yes. AI intervention: estructura del método.
        Student validation: (completar)."""
        return [(n, (f, c), self.mapa.costo(f, c)) for n, f, c in self.mapa.vecinos(*s)]
