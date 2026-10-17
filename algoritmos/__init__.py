"""Registro de algoritmos de búsqueda (plug-ins).

Cada import aquí abajo activa un algoritmo para la interfaz: al importarse el módulo,
sus decoradores @registrar lo añaden a algoritmos.base.REGISTRO.
"""
from algoritmos import busqueda_no_informada  # noqa: F401  (BFS y DFS)
from algoritmos import busqueda_con_costo     # noqa: F401  (UCS)
from algoritmos import a_estrella             # noqa: F401  (A*)

