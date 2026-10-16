"""Contrato común de los algoritmos de búsqueda + registro (plug-ins).

La interfaz NUNCA importa un algoritmo concreto: le pregunta a este registro
cuáles existen. Para sumar UCS, A* o Beam basta con escribir la función con el
decorador @registrar y añadir su import en algoritmos/__init__.py.
"""
import time
from dataclasses import dataclass, field
from typing import Optional

# Algoritmos previstos que aún no existen (la interfaz los muestra como pendientes).
PLANIFICADOS = (("UCS", "Costo uniforme"), ("A_ESTRELLA", "A*"), ("BEAM_SEARCH", "Beam Search"))

REGISTRO = {}


@dataclass
class ResultadoBusqueda:
    """Métricas de una ejecución (las que exige el enunciado + extras para visualizar)."""
    algoritmo: str
    exito: bool
    camino: list = field(default_factory=list)      # lista de (fila, columna)
    costo: Optional[float] = None
    estados_generados: int = 0
    estados_expandidos: int = 0
    maximo_frontera: int = 0
    tiempo_ms: float = 0.0
    explorados: list = field(default_factory=list)  # estados expandidos, en orden
    parametros: dict = field(default_factory=dict)

    @property
    def longitud(self):
        """Número de movimientos del camino (None si no hubo solución)."""
        return len(self.camino) - 1 if self.exito and self.camino else None

    def a_dict(self):
        """Formato equivalente al JSON de resultados del enunciado."""
        return {"algoritmo": self.algoritmo, "exito": self.exito,
                "camino": [list(p) for p in self.camino], "costo": self.costo,
                "estados_generados": self.estados_generados,
                "estados_expandidos": self.estados_expandidos,
                "maximo_frontera": self.maximo_frontera,
                "tiempo_ms": round(self.tiempo_ms, 4)}


def registrar(nombre):
    """Decorador: añade una función de búsqueda al registro bajo `nombre`."""
    def deco(fn):
        REGISTRO[nombre] = fn
        return fn
    return deco


def disponibles():
    """Nombres de los algoritmos implementados, en orden de registro."""
    return list(REGISTRO)


def normalizar_nombre(texto):
    """'a*' -> 'A_ESTRELLA', 'beam search' -> 'BEAM_SEARCH' (para leer nombres del JSON)."""
    t = str(texto).strip().upper().replace("*", "_ESTRELLA").replace(" ", "_").replace("-", "_")
    return t


def reconstruir_camino(padre, meta):
    """Purpose: recorrer los punteros `padre` desde la meta hasta el inicio.
    Preconditions: padre[inicio] is None; padre[s] = (anterior, costo_del_paso).
    Postconditions: devuelve (camino inicio->meta, costo acumulado).
    Complexity: O(longitud del camino).
    AI usage: Yes. AI intervention: estructura del método.
    Student validation: (completar)."""
    camino, costo, s = [], 0, meta
    while s is not None:
        camino.append(s)
        p = padre[s]
        if p is None:
            break
        costo += p[1]
        s = p[0]
    camino.reverse()
    return camino, costo


def ejecutar_algoritmo(nombre, problema, **params):
    """Purpose: ejecutar un algoritmo registrado midiendo el tiempo AQUÍ (no en cada algoritmo).
    Preconditions: nombre in REGISTRO; problema cumple la interfaz de ProblemaNavegacion.
    Postconditions: ResultadoBusqueda con tiempo_ms y parametros completados.
    Complexity: la del algoritmo ejecutado.
    AI usage: Yes. AI intervention: estructura del método.
    Student validation: (completar)."""
    t0 = time.perf_counter()
    res = REGISTRO[nombre](problema, **params)
    res.tiempo_ms = (time.perf_counter() - t0) * 1000
    res.parametros = dict(params)
    return res
