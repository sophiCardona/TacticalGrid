"""Registro de algoritmos de búsqueda (plug-ins).

Cada import aquí abajo activa un algoritmo para la interfaz: al importarse el módulo,
sus decoradores @registrar lo añaden a algoritmos.base.REGISTRO.
"""
from algoritmos import busqueda_no_informada  # noqa: F401  (BFS y DFS)
