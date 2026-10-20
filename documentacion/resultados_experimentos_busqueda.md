# Resultados Experimentales de Algoritmos de Búsqueda

Métricas recolectadas automáticamente en los escenarios mínimos de prueba.

### Caso 1: BFS vs DFS (Espacio abierto con pocos obstáculos)

* **Archivo:** `caso01_bfs_vs_dfs.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 27 | 27.0 | 358 | 350 | 23 | 2.230 | OK |
| DFS | Sí | 235 | 235.0 | 592 | 309 | 263 | 1.436 | OK |
| UCS | Sí | 27 | 27.0 | 358 | 350 | 23 | 2.421 | OK |
| A* (manhattan) | Sí | 27 | 27.0 | 82 | 27 | 55 | 0.244 | OK |
| A* (propia) | Sí | 27 | 27.0 | 82 | 27 | 55 | 0.275 | OK |
| Beam (k=2) | Sí | 27 | 27.0 | 107 | 53 | 2 | 0.386 | OK |

### Caso 2: Ruta corta vs. ruta económica (BFS vs UCS)

* **Archivo:** `caso2_ruta_corta_vs_economica.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 6 | 60.0 | 41 | 33 | 9 | 0.205 | OK |
| DFS | Sí | 142 | 288.0 | 315 | 162 | 153 | 0.772 | OK |
| UCS | Sí | 10 | 19.0 | 85 | 68 | 19 | 0.321 | OK |
| A* (manhattan) | Sí | 10 | 19.0 | 45 | 32 | 14 | 0.198 | OK |
| A* (propia) | Sí | 10 | 19.0 | 19 | 11 | 8 | 0.080 | OK |

### Caso 3: Obstáculo y guía heurística (UCS vs A*)

* **Archivo:** `caso3_obstaculo_y_heuristica.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 18 | 36.0 | 300 | 280 | 20 | 1.357 | OK |
| UCS | Sí | 18 | 36.0 | 300 | 280 | 20 | 1.365 | OK |
| A* (manhattan) | Sí | 18 | 36.0 | 223 | 185 | 40 | 1.158 | OK |
| A* (propia) | Sí | 18 | 36.0 | 206 | 167 | 39 | 1.163 | OK |

### Caso 4: Comparación de heurísticas en A* (Manhattan vs. Propia)

* **Archivo:** `caso4_comparacion_heuristicas.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| UCS | Sí | 22 | 52.0 | 388 | 384 | 22 | 1.913 | OK |
| A* (manhattan) | Sí | 22 | 52.0 | 372 | 353 | 43 | 2.124 | OK |
| A* (propia) | Sí | 22 | 52.0 | 273 | 232 | 43 | 1.563 | OK |

### Caso 5: Búsqueda con memoria limitada (Beam Search variando k)

* **Archivo:** `caso05_beam_search.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 31 | 31.0 | 329 | 321 | 20 | 1.409 | OK |
| A* (manhattan) | Sí | 31 | 31.0 | 219 | 178 | 40 | 1.112 | OK |
| Beam (k=1) | No | — | — | 25 | 9 | 1 | 0.075 | FALLO |
| Beam (k=2) | No | — | — | 31 | 17 | 2 | 0.114 | FALLO |
| Beam (k=4) | Sí | 55 | 55.0 | 266 | 213 | 4 | 1.248 | OK |
| Beam (k=8) | Sí | 31 | 31.0 | 276 | 234 | 8 | 1.325 | OK |
