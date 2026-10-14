"""Datos del escenario ya validado (objetos internos, independientes del JSON)."""
from dataclasses import dataclass
from typing import Optional

from escenario.mapa import Mapa
from juego.estado import Estado, Unidad


@dataclass(frozen=True)
class Escenario:
    mapa: Mapa
    bases: dict                 # {"A": (f,c), "B": (f,c)}
    recurso: tuple              # posición inicial del recurso (f,c)
    unidades: tuple             # tuple de Unidad
    turno: str
    portador: Optional[str]
    profundidad_minimax: int
    prueba: Optional[dict]

    def estado_inicial(self):
        """Purpose: construir el Estado inicial del juego a partir del escenario.
        Preconditions: escenario validado.
        Postconditions: si hay portador, recurso_pos es None; si no, es la posición del recurso.
        Complexity: O(n log n) por ordenar n unidades.
        AI usage: Yes. AI intervention: estructura del método.
        Student validation: (completar)."""
        recurso_pos = None if self.portador is not None else self.recurso
        return Estado(tuple(sorted(self.unidades, key=lambda u: u.id)),
                      recurso_pos, self.portador, self.turno)
