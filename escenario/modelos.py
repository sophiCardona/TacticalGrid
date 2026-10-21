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
        Student validation: Se ha validado el método con varios casos de prueba."""
        unidades = tuple(sorted(self.unidades, key=lambda u: u.id))
        portador, recurso_pos = self.portador, (None if self.portador is not None else self.recurso)
        if portador is None:
            # Regla R3 aplicada al estado inicial: una unidad que EMPIEZA sobre el recurso lo recoge.
            sobre = [u for u in unidades if (u.fila, u.columna) == self.recurso]
            if sobre:
                portador, recurso_pos = sobre[0].id, None
        return Estado(unidades, recurso_pos, portador, self.turno)
 
