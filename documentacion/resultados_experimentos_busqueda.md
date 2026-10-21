# Resultados Experimentales de Algoritmos de Búsqueda

Métricas recolectadas automáticamente por `experimentos/ejecutar_experimentos_busqueda.py` sobre los escenarios de prueba del repositorio. Cada algoritmo se ejecutó 5 veces consecutivas sobre la misma instancia y se reporta el tiempo promedio (`time.perf_counter`); los caminos de búsqueda fueron validados por `verificacion/verificador.py`. Cuando un algoritmo no encuentra ruta, la columna **Verif.** muestra `—` (no hay camino que validar).

## 1. Casos mínimos de búsqueda (1 al 5)

### Caso 1: BFS vs DFS (Espacio abierto con pocos obstáculos)

* **Archivo:** `caso01_bfs_vs_dfs.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 27 | 27.0 | 358 | 350 | 23 | 1.664 | OK |
| DFS | Sí | 235 | 235.0 | 592 | 309 | 263 | 2.185 | OK |
| UCS | Sí | 27 | 27.0 | 358 | 350 | 23 | 2.106 | OK |
| A* (manhattan) | Sí | 27 | 27.0 | 82 | 27 | 55 | 0.517 | OK |
| A* (propia) | Sí | 27 | 27.0 | 82 | 27 | 55 | 0.310 | OK |
| Beam (k=2) | Sí | 27 | 27.0 | 107 | 53 | 2 | 0.329 | OK |

### Caso 2: Ruta corta vs. ruta económica (BFS vs UCS)

* **Archivo:** `caso2_ruta_corta_vs_economica.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 6 | 60.0 | 41 | 33 | 9 | 0.216 | OK |
| DFS | Sí | 142 | 288.0 | 315 | 162 | 153 | 0.921 | OK |
| UCS | Sí | 10 | 19.0 | 85 | 68 | 19 | 0.288 | OK |
| A* (manhattan) | Sí | 10 | 19.0 | 45 | 32 | 14 | 0.165 | OK |
| A* (propia) | Sí | 10 | 19.0 | 19 | 11 | 8 | 0.070 | OK |

### Caso 3: Obstáculo y guía heurística (UCS vs A*)

* **Archivo:** `caso3_obstaculo_y_heuristica.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 18 | 36.0 | 300 | 280 | 20 | 0.959 | OK |
| UCS | Sí | 18 | 36.0 | 300 | 280 | 20 | 1.184 | OK |
| A* (manhattan) | Sí | 18 | 36.0 | 223 | 185 | 40 | 1.112 | OK |
| A* (propia) | Sí | 18 | 36.0 | 206 | 167 | 39 | 1.248 | OK |

### Caso 4: Comparación de heurísticas en A* (Manhattan vs. Propia)

* **Archivo:** `caso4_comparacion_heuristicas.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| UCS | Sí | 22 | 52.0 | 388 | 384 | 22 | 2.026 | OK |
| A* (manhattan) | Sí | 22 | 52.0 | 372 | 353 | 43 | 3.062 | OK |
| A* (propia) | Sí | 22 | 52.0 | 273 | 232 | 43 | 2.218 | OK |

### Caso 5: Búsqueda con memoria limitada (Beam Search variando k)

* **Archivo:** `caso05_beam_search.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 31 | 31.0 | 329 | 321 | 20 | 1.324 | OK |
| A* (manhattan) | Sí | 31 | 31.0 | 219 | 178 | 40 | 2.545 | OK |
| Beam (k=1) | No | — | — | 25 | 9 | 1 | 0.206 | — |
| Beam (k=2) | No | — | — | 31 | 17 | 2 | 0.286 | — |
| Beam (k=4) | Sí | 55 | 55.0 | 266 | 213 | 4 | 3.037 | OK |
| Beam (k=8) | Sí | 31 | 31.0 | 276 | 234 | 8 | 2.906 | OK |

## 2. Casos robustos de búsqueda (R01 a R08)

Situaciones límite del cargador y del mapa: metas inalcanzables, origen igual a meta, corredores no cuadrados, unidades encerradas, objetivos sobre muro, costos fraccionarios, terrenos nuevos y mapas de gran escala.

### Robusto R01: meta inalcanzable (rodeada de muros)

* **Archivo:** `r01_meta_inalcanzable.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | No | — | — | 391 | 391 | 23 | 3.431 | — |
| DFS | No | — | — | 737 | 391 | 348 | 2.507 | — |
| UCS | No | — | — | 391 | 391 | 23 | 2.208 | — |
| A* (manhattan) | No | — | — | 543 | 391 | 204 | 2.961 | — |
| A* (propia) | No | — | — | 543 | 391 | 204 | 2.970 | — |
| Beam (k=8) | No | — | — | 377 | 320 | 8 | 2.184 | — |

### Robusto R02: origen igual a la meta

* **Archivo:** `r02_inicio_igual_meta.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 0 | 0.0 | 1 | 0 | 1 | 0.005 | OK |
| UCS | Sí | 0 | 0.0 | 1 | 0 | 1 | 0.003 | OK |
| A* (manhattan) | Sí | 0 | 0.0 | 1 | 0 | 1 | 0.004 | OK |
| Beam (k=2) | Sí | 0 | 0.0 | 1 | 0 | 1 | 0.002 | OK |

### Robusto R03: corredor 1x20 (mapa no cuadrado)

* **Archivo:** `r03_corredor_1x20.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 19 | 29.0 | 20 | 19 | 1 | 0.083 | OK |
| DFS | Sí | 19 | 29.0 | 20 | 19 | 1 | 0.100 | OK |
| UCS | Sí | 19 | 29.0 | 20 | 19 | 1 | 0.089 | OK |
| A* (manhattan) | Sí | 19 | 29.0 | 20 | 19 | 1 | 0.103 | OK |
| Beam (k=1) | Sí | 19 | 29.0 | 20 | 19 | 1 | 0.110 | OK |

### Robusto R04: unidad encerrada por muros

* **Archivo:** `r04_unidad_encerrada.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | No | — | — | 1 | 1 | 1 | 0.005 | — |
| UCS | No | — | — | 1 | 1 | 1 | 0.003 | — |
| A* (manhattan) | No | — | — | 1 | 1 | 1 | 0.005 | — |
| Beam (k=4) | No | — | — | 1 | 1 | 1 | 0.003 | — |

### Robusto R05: objetivo sobre un muro (rechazo previo)

* **Archivo:** `r05_objetivo_en_muro.json`

* **Nota:** El objetivo (10,10) no es transitable: la aplicación rechaza la búsqueda antes de invocar al algoritmo, por lo que no se ejecuta.

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| — | Rechazado | — | — | — | — | — | — | — |

### Robusto R06: costos fraccionarios (autopista 0.5)

* **Archivo:** `r06_costos_fraccionarios.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 21 | 21.0 | 295 | 279 | 20 | 1.222 | OK |
| DFS | Sí | 367 | 357.5 | 746 | 384 | 362 | 2.117 | OK |
| UCS | Sí | 21 | 11.5 | 209 | 189 | 24 | 0.904 | OK |
| A* (manhattan) | Sí | 21 | 11.5 | 80 | 40 | 40 | 0.313 | OK |
| A* (propia) | Sí | 21 | 11.5 | 61 | 21 | 40 | 0.255 | OK |

### Robusto R07: dimensiones 8x12 y terrenos con otros nombres

* **Archivo:** `r07_dimensiones_y_nombres_nuevos.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 11 | 25.0 | 67 | 60 | 10 | 0.200 | OK |
| DFS | Sí | 43 | 107.0 | 88 | 53 | 35 | 0.193 | OK |
| UCS | Sí | 11 | 15.0 | 58 | 44 | 17 | 0.177 | OK |
| A* (manhattan) | Sí | 11 | 15.0 | 34 | 20 | 14 | 0.110 | OK |
| A* (propia) | Sí | 11 | 15.0 | 34 | 20 | 14 | 0.118 | OK |

### Robusto R08: mapa grande 40x40

* **Archivo:** `r08_mapa_grande_40x40.json`

| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BFS | Sí | 70 | 142.0 | 1521 | 1516 | 43 | 6.432 | OK |
| DFS | Sí | 966 | 2028.0 | 2538 | 1230 | 1220 | 6.718 | OK |
| UCS | Sí | 70 | 77.0 | 1519 | 1509 | 69 | 9.332 | OK |
| A* (manhattan) | Sí | 70 | 77.0 | 1064 | 694 | 325 | 5.607 | OK |
| A* (propia) | Sí | 70 | 77.0 | 1064 | 694 | 325 | 6.136 | OK |

## 3. Casos adversariales (7 al 10)

Evaluación del árbol de juego desde el estado inicial del escenario. La **Acción recomendada** es la jugada elegida por el bando en turno, el **Valor** es la utilidad minimax desde su perspectiva, **Evaluados** cuenta las hojas cuya función de evaluación se calculó y **Podados** las ramas descartadas por la poda alfa-beta.

### Caso 7: Decisión adversarial (interceptación táctica)

* **Archivo:** `caso07_decision_adversarial.json`

| Algoritmo / Config | Acción recomendada | Valor | Prof. | Generados | Evaluados | Podados | Tiempo (ms) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| MINIMAX (prof 3, estandar) | A1 -> (8, 9) | 87.00 | 3 | 3234 | 3009 | 0 | 32.710 |
| ALFA_BETA (prof 3, estandar) | A1 -> (8, 9) | 87.00 | 3 | 358 | 300 | 488 | 3.587 |

### Caso 8: Minimax frente a poda alfa-beta

* **Archivo:** `caso08_minimax_vs_alfa_beta.json`

| Algoritmo / Config | Acción recomendada | Valor | Prof. | Generados | Evaluados | Podados | Tiempo (ms) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| MINIMAX (prof 3, estandar) | A1 -> (9, 7) | 5.00 | 3 | 3496 | 3255 | 0 | 33.834 |
| ALFA_BETA (prof 3, estandar) | A1 -> (9, 7) | 5.00 | 3 | 628 | 543 | 600 | 6.169 |

### Caso 9: Impacto del orden de acciones en la poda alfa-beta

* **Archivo:** `caso09_orden_acciones.json`

| Algoritmo / Config | Acción recomendada | Valor | Prof. | Generados | Evaluados | Podados | Tiempo (ms) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| ALFA_BETA (prof 3, estandar) | A1 -> (9, 7) | 5.00 | 3 | 628 | 543 | 600 | 7.290 |
| ALFA_BETA (prof 3, inverso) | A1 -> (9, 7) | 5.00 | 3 | 2008 | 1829 | 622 | 42.203 |
| ALFA_BETA (prof 3, heuristico) | A1 -> (9, 7) | 5.00 | 3 | 276 | 231 | 392 | 10.021 |

### Caso 10: Efecto de la profundidad en Minimax / alfa-beta

* **Archivo:** `caso10_profundidad.json`

| Algoritmo / Config | Acción recomendada | Valor | Prof. | Generados | Evaluados | Podados | Tiempo (ms) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| ALFA_BETA (prof 1, heuristico) | A1 -> (9, 7) | 5.00 | 1 | 16 | 15 | 0 | 0.328 |
| ALFA_BETA (prof 2, heuristico) | A1 -> (9, 7) | 0.00 | 2 | 45 | 29 | 196 | 2.543 |
| ALFA_BETA (prof 3, heuristico) | A1 -> (9, 7) | 5.00 | 3 | 276 | 231 | 392 | 8.264 |
| ALFA_BETA (prof 4, heuristico) | A1 -> (9, 7) | 0.00 | 4 | 709 | 433 | 3416 | 39.421 |
