"""Estado del juego: inmutable y hashable (se puede guardar en sets/dicts)."""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Unidad:
    id: str
    bando: str      # "A" o "B"
    fila: int
    columna: int


@dataclass(frozen=True)
class Estado:
    unidades: tuple                 # tuple de Unidad, ordenada por id (forma canónica)
    recurso_pos: Optional[tuple]    # (f,c) si está en el suelo; None si alguien lo lleva
    portador: Optional[str]         # id de la unidad que lo lleva, o None
    turno: str                      # bando que debe actuar

    def unidad(self, uid):
        return next((u for u in self.unidades if u.id == uid), None)

    def unidades_de(self, bando):
        return [u for u in self.unidades if u.bando == bando]

    def posicion_recurso(self):
        """Dónde está el recurso (en el suelo o con su portador)."""
        if self.portador is not None:
            u = self.unidad(self.portador)
            return (u.fila, u.columna)
        return self.recurso_pos


@dataclass(frozen=True)
class Accion:
    unidad_id: str
    tipo: str                       # "MOVER" o "ESPERAR"
    destino: Optional[tuple] = None # (f,c) para MOVER
