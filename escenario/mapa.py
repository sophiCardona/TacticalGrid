"""Representación del tablero. No conoce unidades, turnos ni algoritmos."""
from dataclasses import dataclass

# Orden FIJO y único de movimientos (arriba, abajo, izquierda, derecha).
# Cambiar este orden cambia el orden de los sucesores (útil para el caso 9).
DIRECCIONES = (("ARRIBA", -1, 0), ("ABAJO", 1, 0), ("IZQUIERDA", 0, -1), ("DERECHA", 0, 1))


@dataclass(frozen=True)
class Mapa:
    filas: int
    columnas: int
    terreno: tuple          # tuple de tuples de nombres de terreno
    tipos: dict             # nombre -> {"transitable": bool, "costo": número o None}

    def dentro(self, f, c):
        """Purpose: saber si (f,c) cae dentro de la cuadrícula.
        Preconditions: f, c enteros.
        Postconditions: True sii 0<=f<filas y 0<=c<columnas.
        Complexity: O(1).
        AI usage: Yes. AI intervention: estructura del método.
        Student validation: Se ha validado el método con varios casos de prueba."""
        return 0 <= f < self.filas and 0 <= c < self.columnas

    def es_transitable(self, f, c):
        """Purpose: decidir si una celda puede ser pisada.
        Preconditions: ninguna (fuera del mapa devuelve False).
        Postconditions: True sii está dentro y su tipo es transitable en el JSON.
        Complexity: O(1).
        AI usage: Yes. AI intervention: estructura del método.
        Student validation: Se ha validado el método con varios casos de prueba."""
        return self.dentro(f, c) and self.tipos[self.terreno[f][c]]["transitable"]

    def costo(self, f, c):
        """Purpose: costo de ENTRAR a la celda (lo lee del JSON, nunca fijo).
        Preconditions: (f,c) transitable.
        Postconditions: devuelve el costo positivo del tipo de terreno.
        Complexity: O(1).
        AI usage: Yes. AI intervention: estructura del método.
        Student validation: Se ha validado el método con varios casos de prueba."""
        assert self.es_transitable(f, c), "costo() sobre celda no transitable"
        return self.tipos[self.terreno[f][c]]["costo"]

    def costo_minimo(self):
        """Purpose: menor costo entre terrenos transitables (para heurísticas admisibles).
        Preconditions: existe al menos un terreno transitable.
        Postconditions: devuelve min(costo) del catálogo.
        Complexity: O(T), T = tipos de terreno.
        AI usage: Yes. AI intervention: estructura del método.
        Student validation: Se ha validado el método con varios casos de prueba."""
        return min(t["costo"] for t in self.tipos.values() if t["transitable"])

    def vecinos(self, f, c):
        """Purpose: celdas adyacentes transitables (solo terreno, ignora unidades).
        Preconditions: (f,c) dentro del mapa.
        Postconditions: lista de (nombre_dir, f2, c2) en el orden de DIRECCIONES.
        Complexity: O(1) (4 direcciones).
        AI usage: Yes. AI intervention: estructura del método.
        Student validation: Se ha validado el método con varios casos de prueba."""
        res = []
        for nombre, df, dc in DIRECCIONES:
            f2, c2 = f + df, c + dc
            if self.es_transitable(f2, c2):
                res.append((nombre, f2, c2))
        return res
