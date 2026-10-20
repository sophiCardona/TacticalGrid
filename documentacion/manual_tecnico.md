# MANUAL TÉCNICO — TACTICALGRID

## 1. Portada

| Campo | Valor |
|---|---|
| Nombre del proyecto | TacticalGrid |
| Descripción corta | Escaramuza táctica 2D por turnos — Sistemas Inteligentes I |
| Versión del proyecto | **No identificada** en el repositorio (no existen etiquetas Git ni campo de versión del proyecto) |
| Versión del formato de escenario | `1.0` (campo `version` de los archivos JSON; no es la versión del software) |
| Rama Git analizada | `main` |
| Último commit analizado | `36782b9` — «Modificacion seccion de Compacion en heuristicas, interfaz» — 2026-10-19 11:29:20 -0500 |
| Fecha de elaboración del manual | 2026-10-19 |
| Elaboración | Generado a partir del código fuente, archivos JSON, pruebas y documentación existentes |
| Interprete verificado en el entorno de elaboración | Python 3.12.0 |

> Este documento se basa exclusivamente en los archivos presentes en el repositorio. Todo dato no verificable se marca expresamente. No se modificó código fuente durante su elaboración.

---

## 2. Tabla de contenido

1. [Portada](#1-portada)
2. [Tabla de contenido](#2-tabla-de-contenido)
3. [Introducción, objetivo y alcance técnico](#3-introducción-objetivo-y-alcance-técnico)
4. [Tecnologías, lenguajes, frameworks, bibliotecas y herramientas](#4-tecnologías-lenguajes-frameworks-bibliotecas-y-herramientas)
5. [Estructura de carpetas y responsabilidad de archivos](#5-estructura-de-carpetas-y-responsabilidad-de-archivos)
6. [Arquitectura del sistema](#6-arquitectura-del-sistema)
7. [Modelo de datos](#7-modelo-de-datos)
8. [Descripción técnica de clases, funciones y métodos](#8-descripción-técnica-de-clases-funciones-y-métodos)
9. [Parámetros, tipos, retornos, excepciones y efectos secundarios](#9-parámetros-tipos-retornos-excepciones-y-efectos-secundarios)
10. [Configuración, instalación y ejecución](#10-configuración-instalación-y-ejecución)
11. [Pruebas existentes y mecanismos de validación](#11-pruebas-existentes-y-mecanismos-de-validación)
12. [Limitaciones técnicas, deuda técnica y funcionalidades pendientes](#12-limitaciones-técnicas-deuda-técnica-y-funcionalidades-pendientes)
13. [Anexos](#13-anexos)

---

## 3. Introducción, objetivo y alcance técnico

### 3.1 Introducción

TacticalGrid es una aplicación de escritorio desarrollada en Python que integra, en una misma interfaz gráfica basada en `tkinter`:

- la **carga y validación** de escenarios de juego definidos en JSON;
- la **simulación por turnos** de una escaramuza táctica 2D sobre una cuadrícula;
- la **resolución de problemas de navegación** mediante algoritmos de búsqueda;
- la **verificación** de los caminos producidos por dichos algoritmos;
- la **comparación** de métricas de algoritmos y heurísticas.

El sistema está organizado en capas: modelo de escenario, modelo de juego y reglas, algoritmos de búsqueda, verificación e interfaz. La interfaz no contiene reglas del juego ni algoritmos; los invoca a través de módulos especializados (véase `interfaz/app.py`, línea 1).

### 3.2 Objetivo

Proveer una herramienta académica para:

1. Modelar un escenario táctico en una cuadrícula con terrenos de distinto costo.
2. Ejecutar y comparar algoritmos de búsqueda (BFS, DFS, UCS, A*).
3. Verificar automáticamente que un camino hallado cumple las propiedades exigidas.
4. Simular una partida por turnos con reglas deterministas (movimiento, recogida e interceptación de un recurso, condición de victoria).

### 3.3 Alcance técnico verificado

| Funcionalidad | Estado observado en el código |
|---|---|
| Carga de escenarios JSON con validación completa | Implementada |
| Modelo de estado inmutable y hashable | Implementada |
| Reglas de movimiento, recogida e interceptación | Implementadas |
| Condición de victoria | Implementada |
| BFS, DFS | Implementados |
| UCS (Dijkstra) | Implementado |
| A* con heurísticas `manhattan` y `propia` | Implementado |
| Verificación de caminos | Implementada |
| Interfaz gráfica con cinco pestañas | Implementada |
| Comparación de todos los algoritmos | Implementada |
| Comparación de heurísticas de A* en Estadísticas | Implementada |
| Exportación del historial a CSV | Implementada |
| Partida por turnos con control humano y control «Azar» | Parcial (el único controlador automático es aleatorio) |
| Tarea adversarial (Minimax / alfa-beta) | **Pendiente**: solo lista acciones legales |
| Beam Search (`k`) | **Pendiente**: aparece como planificado y hay un escenario que lo referencia, pero no está registrado |

La aplicación no utiliza servicios de red, bases de datos ni almacenamiento persistente más allá de la lectura de archivos JSON y la escritura opcional de un CSV.

---

## 4. Tecnologías, lenguajes, frameworks, bibliotecas y herramientas

### 4.1 Lenguaje y versión

| Elemento | Evidencia |
|---|---|
| Lenguaje | Python |
| Versión mínima declarada | 3.9+ (`README.md`, línea 9) |
| Versión verificada en el entorno | 3.12.0 (`python --version` durante la elaboración) |

No existe archivo `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`, `environment.yml` ni configuración equivalente en el repositorio (verificado por búsqueda de archivos).

### 4.2 Bibliotecas utilizadas

Todas las importaciones corresponden a la biblioteca estándar de Python. No se detectaron dependencias de terceros.

| Módulo estándar | Uso | Archivos donde se importa |
|---|---|---|
| `tkinter` (`tk`, `ttk`, `filedialog`, `font`, `messagebox`) | Interfaz gráfica | `interfaz/app.py`, `interfaz/tablero.py` |
| `json` | Lectura de escenarios y serialización de resultados | `escenario/cargador.py`, `interfaz/app.py` |
| `heapq` | Colas de prioridad de UCS y A* | `algoritmos/busqueda_con_costo.py`, `algoritmos/a_estrella.py` |
| `collections.deque` | Frontera FIFO de BFS | `algoritmos/busqueda_no_informada.py` |
| `dataclasses` | Entidades inmutables y resultado de búsqueda | `escenario/mapa.py`, `escenario/modelos.py`, `juego/estado.py`, `algoritmos/base.py` |
| `typing.Optional` | Anotaciones de tipo | `escenario/modelos.py`, `juego/estado.py`, `algoritmos/base.py` |
| `time` | Medición de tiempo con `perf_counter` | `algoritmos/base.py` |
| `random` | Controlador «Azar» de la partida y generación de casos | `interfaz/app.py`, `experimentos/generar_casos_minimos.py` |
| `csv` | Exportación del historial | `interfaz/app.py` |
| `os`, `sys` | Rutas y ajuste de `sys.path` en scripts y pruebas | `interfaz/app.py`, `tests/*.py`, `experimentos/*.py` |
| `unittest` | Pruebas automatizadas | `tests/*.py` |

### 4.3 Herramientas y convenciones

| Herramienta / convención | Observación |
|---|---|
| Git | Repositorio con rama `main`; sin etiquetas (`git tag` vacío) |
| `.gitignore` | Ignora `__pycache__/`, `*.py[cod]`, `*$py.class`, `.vscode/`, `.idea/` |
| Documentación de funciones | Docstrings con campos `Purpose`, `Preconditions`, `Postconditions`, `Complexity`, `AI usage`, `Student validation` |
| Empaquetado | No hay archivos `__init__.py` salvo `algoritmos/__init__.py`; el resto de carpetas funciona como paquetes de espacio de nombres implícitos (Python 3.3+) |
| Linter / formateador / CI | No se encontró configuración de ninguno |
| Cobertura de pruebas | No se encontró configuración de cobertura |

### 4.4 Directorios sin contenido

- `docs/`: existe en el sistema de archivos, sin archivos.
- `heuristicas/`: existe en el sistema de archivos, sin archivos.

> Al estar vacíos, Git no los versiona. Su contenido es `[PENDIENTE DE IMPLEMENTACIÓN]`.

---

## 5. Estructura de carpetas y responsabilidad de archivos

```
TacticalGrid/
├── main.py
├── README.md
├── .gitignore
├── algoritmos/
│   ├── __init__.py
│   ├── base.py
│   ├── busqueda_no_informada.py
│   ├── busqueda_con_costo.py
│   └── a_estrella.py
├── escenario/
│   ├── mapa.py
│   ├── modelos.py
│   ├── cargador.py
│   └── validador.py
├── juego/
│   ├── estado.py
│   ├── reglas.py
│   └── problema_navegacion.py
├── interfaz/
│   ├── app.py
│   ├── tablero.py
│   └── graficas.py
├── verificacion/
│   └── verificador.py
├── tests/
│   ├── test_paso1_2.py
│   ├── test_paso3_ucs.py
│   └── test_paso4_a_estrella.py
├── experimentos/
│   ├── generar_casos_minimos.py
│   └── caso06_estado_compuesto.py
├── escenarios/
│   ├── ejemplo.json
│   ├── prueba_busqueda_dfs.json
│   ├── prueba_partida.json
│   ├── prueba_adversarial.json
│   ├── invalido_a_proposito.json
│   └── casos minimos/
│       ├── caso01_bfs_vs_dfs.json
│       ├── caso2_ruta_corta_vs_economica.json
│       ├── caso3_obstaculo_y_heuristica.json
│       ├── caso4_comparacion_heuristicas.json
│       ├── caso05_beam_search.json
│       ├── caso06a_sin_recurso.json
│       └── caso06b_con_recurso.json
├── docs/              (vacío)
└── heuristicas/       (vacío)
```

### 5.1 Responsabilidad por archivo

| Archivo | Responsabilidad | Estado |
|---|---|---|
| `main.py` | Punto de entrada: instancia `App` y arranca `mainloop()` | Implementado |
| `README.md` | Instrucciones básicas de ejecución y modos | Implementado (integrantes sin completar) |
| `.gitignore` | Exclusiones de control de versiones | Implementado |
| `algoritmos/__init__.py` | Importa los módulos de algoritmos para activar su registro | Implementado |
| `algoritmos/base.py` | Contrato común, registro de algoritmos, métricas (`ResultadoBusqueda`), reconstrucción de caminos y medición de tiempo | Implementado |
| `algoritmos/busqueda_no_informada.py` | BFS y DFS | Implementados |
| `algoritmos/busqueda_con_costo.py` | UCS / Dijkstra | Implementado |
| `algoritmos/a_estrella.py` | A*, heurísticas `manhattan` y `propia`, selector de heurística | Implementado |
| `escenario/mapa.py` | Representación de la cuadrícula y consultas de terreno | Implementado |
| `escenario/modelos.py` | `Escenario` validado y construcción del estado inicial | Implementado |
| `escenario/cargador.py` | Lectura JSON, validación y construcción «todo o nada» | Implementado |
| `escenario/validador.py` | Reglas de validación del JSON | Implementado |
| `juego/estado.py` | Entidades inmutables `Unidad`, `Estado`, `Accion` | Implementado |
| `juego/reglas.py` | Acciones legales, costo, transición, ganador y terminalidad | Implementado |
| `juego/problema_navegacion.py` | Formulación del problema de navegación de un agente | Implementado |
| `interfaz/app.py` | Ventana principal, orquestación de tareas, resultados, estadísticas y comparación | Implementado |
| `interfaz/tablero.py` | Widget de dibujo del tablero y paleta de colores | Implementado |
| `interfaz/graficas.py` | Gráfico de barras simple sobre un `Canvas` | Implementado |
| `verificacion/verificador.py` | Comprobaciones de validez de un camino | Implementado |
| `tests/*.py` | Pruebas unitarias con `unittest` | Implementado |
| `experimentos/generar_casos_minimos.py` | Generación reproducible de los casos mínimos 1, 5 y 6 | Implementado |
| `experimentos/caso06_estado_compuesto.py` | Demostración por consola del caso 6 | Implementado |
| `escenarios/*.json` | Datos de escenario y pruebas declarativas | Implementado |

---

## 6. Arquitectura del sistema

### 6.1 Vista de capas

```
┌──────────────────────────────────────────────────────────────┐
│ Interfaz (tkinter)                                           │
│   interfaz/app.py   interfaz/tablero.py   interfaz/graficas.py│
└───────────────┬──────────────────────────────────────────────┘
                │ invoca
┌───────────────▼──────────────┐   ┌─────────────────────────┐
│ Juego                        │   │ Algoritmos de búsqueda  │
│   juego/estado.py            │   │   algoritmos/base.py    │
│   juego/reglas.py            │   │   busqueda_no_informada  │
│   juego/problema_navegacion  │   │   busqueda_con_costo     │
└───────────────┬──────────────┘   │   a_estrella             │
                │                  └───────────┬─────────────┘
                │ usa                          │ usa
┌───────────────▼──────────────┐   ┌───────────▼─────────────┐
│ Escenario                    │   │ Verificación            │
│   escenario/mapa.py          │   │   verificacion/         │
│   escenario/modelos.py       │   │     verificador.py      │
│   escenario/cargador.py      │   └─────────────────────────┘
│   escenario/validador.py     │
└──────────────────────────────┘
```

### 6.2 Dependencias entre módulos (importaciones verificadas)

| Módulo | Importa de |
|---|---|
| `main.py` | `interfaz.app` |
| `interfaz/app.py` | `algoritmos`, `algoritmos.base`, `escenario.cargador`, `interfaz.graficas`, `interfaz.tablero`, `juego.problema_navegacion`, `juego.reglas`, `verificacion.verificador` |
| `interfaz/graficas.py` | `interfaz.tablero` |
| `interfaz/tablero.py` | Solo `tkinter` |
| `algoritmos/*` | `algoritmos.base` |
| `escenario/cargador.py` | `escenario.mapa`, `escenario.modelos`, `escenario.validador`, `juego.estado` |
| `escenario/modelos.py` | `escenario.mapa`, `juego.estado` |
| `juego/reglas.py` | `escenario.mapa` (`DIRECCIONES`), `juego.estado` |
| `juego/problema_navegacion.py` | Ninguno |
| `verificacion/verificador.py` | Ninguno |
| `tests/*` | módulos del proyecto, ajustando `sys.path` |

No se detectaron dependencias circulares a nivel de importación. `escenario.modelos` importa `juego.estado`, y `juego.estado` no importa nada del proyecto.

### 6.3 Flujo de ejecución principal

1. **Arranque**: `main.py` → `App()` → `_construir()` crea barra superior, tablero y pestañas → `_mostrar_frame_tarea()` → mensaje de estado inicial.
2. **Carga de escenario** (`App.cargar_dialogo` / `App.cargar_ruta`):
   - `cargar_escenario(ruta)` lee el JSON.
   - `construir_escenario(datos)` llama a `validar_datos(datos)`.
   - Si hay errores → `ErrorEscenario` con lista completa; la interfaz los muestra y **no reemplaza** el escenario anterior.
   - Si es válido → se construyen `Mapa`, `Unidad` y `Escenario`.
3. **Aplicación del escenario** (`App._aplicar_escenario`): se crean `Reglas`, el estado inicial, se ajustan controles y se llama a `cambiar_modo(auto_ejecutar=True)`.
4. **Modo JSON**: `_aplicar_prueba()` lee `prueba` y ajusta tarea, unidad, objetivo, algoritmo, heurística y `k`; `_bloquear(True)` deshabilita controles. Si existe `prueba`, se ejecuta automáticamente.
5. **Modo exploración**: el usuario elige tarea, algoritmo, unidad y objetivo; los controles permanecen habilitados.
6. **Búsqueda**:
   - `_problema()` construye un `ProblemaNavegacion(mapa, inicio, objetivo)`.
   - `_correr()` invoca `ejecutar_algoritmo(nombre, problema, k=..., heuristica=...)`.
   - El algoritmo registrado se ejecuta y devuelve `ResultadoBusqueda`.
   - `verificar_camino(...)` produce las comprobaciones.
   - Se agrega un registro al historial y se muestran resultados y métricas.
   - Si el algoritmo es A*, además se ejecuta la comparación entre heurísticas.
7. **Comparación de algoritmos**: `comparar_todos()` ejecuta todos los algoritmos registrados sobre el mismo problema.
8. **Partida**: clics en el tablero → `Reglas.acciones_legales` / `Reglas.aplicar`; el bando «Azar» elige una acción aleatoria.
9. **Adversarial**: `_ejecutar_adversarial()` solo registra en el log las acciones legales del estado; el cálculo Minimax/alfa-beta no está implementado.

### 6.4 Componentes y relaciones

| Componente | Rol | Relación principal |
|---|---|---|
| `Mapa` | Cuadrícula y costos de terreno | Usado por `ProblemaNavegacion`, `Reglas`, `Escenario`, `Tablero` |
| `Escenario` | Datos validados del escenario | Produce `Estado` inicial; usado por `Reglas` y la interfaz |
| `Unidad`, `Estado`, `Accion` | Modelo inmutable del juego | Entradas/salidas de `Reglas` |
| `Reglas` | Legalidad, transición, costo, victoria | Orquesta el estado del juego |
| `ProblemaNavegacion` | Interfaz del problema para búsqueda | Consumida por todos los algoritmos |
| `ResultadoBusqueda` | Resultado y métricas | Producida por algoritmos, consumida por interfaz y verificador |
| Registro de algoritmos (`REGISTRO`) | Descubrimiento de algoritmos | Poblado por decorador `@registrar` al importar `algoritmos` |
| `Tablero` | Dibujo | Recibe escenario, estado y capas visuales |
| `verificar_camino` | Validación independiente | Recibe mapa, inicio, objetivo y resultado |

---

## 7. Modelo de datos

### 7.1 Entidades internas (código)

#### 7.1.1 `Mapa` — `escenario/mapa.py`

`@dataclass(frozen=True)`

| Atributo | Tipo declarado (anotación) | Descripción verificable |
|---|---|---|
| `filas` | `int` (por uso) | Número de filas |
| `columnas` | `int` (por uso) | Número de columnas |
| `terreno` | `tuple` | Tupla de tuplas con nombres de tipo de terreno |
| `tipos` | `dict` | `nombre → {"transitable": bool, "costo": número o None}` |

Observación: aunque la clase es `frozen`, contiene un `dict` (`tipos`), por lo que no es hashable. En el código no se usa como clave de diccionario ni en conjuntos.

Constante del módulo:

```python
DIRECCIONES = (("ARRIBA", -1, 0), ("ABAJO", 1, 0), ("IZQUIERDA", 0, -1), ("DERECHA", 0, 1))
```

El orden es determinista y afecta el orden de generación de sucesores.

#### 7.1.2 `Unidad` — `juego/estado.py`

`@dataclass(frozen=True)`

| Atributo | Tipo | Descripción |
|---|---|---|
| `id` | `str` | Identificador único dentro del escenario |
| `bando` | `str` | `"A"` o `"B"` |
| `fila` | `int` | Fila actual |
| `columna` | `int` | Columna actual |

El campo `tipo` presente en el JSON **no se traslada** a `Unidad` (véase `escenario/cargador.py`, línea 34).

#### 7.1.3 `Estado` — `juego/estado.py`

`@dataclass(frozen=True)`

| Atributo | Tipo | Descripción |
|---|---|---|
| `unidades` | `tuple[Unidad]` | Ordenada por `id` (forma canónica) |
| `recurso_pos` | `Optional[tuple]` | `(f, c)` si el recurso está en el suelo; `None` si alguien lo lleva |
| `portador` | `Optional[str]` | `id` de la unidad que lleva el recurso, o `None` |
| `turno` | `str` | Bando que debe actuar (`"A"` o `"B"`) |

Al ser `frozen` y contener solo tuplas y cadenas, es hashable. La prueba `test_hashable_e_inmutable` lo comprueba.

#### 7.1.4 `Accion` — `juego/estado.py`

`@dataclass(frozen=True)`

| Atributo | Tipo | Descripción |
|---|---|---|
| `unidad_id` | `str` | Unidad que actúa |
| `tipo` | `str` | `"MOVER"` o `"ESPERAR"` |
| `destino` | `Optional[tuple]` | `(f, c)` para `"MOVER"`; valor por defecto `None` |

#### 7.1.5 `Escenario` — `escenario/modelos.py`

`@dataclass(frozen=True)`

| Atributo | Tipo | Descripción |
|---|---|---|
| `mapa` | `Mapa` | Cuadrícula |
| `bases` | `dict` | `{"A": (f,c), "B": (f,c)}` |
| `recurso` | `tuple` | Posición inicial del recurso |
| `unidades` | `tuple` | Tupla de `Unidad` |
| `turno` | `str` | Bando inicial |
| `portador` | `Optional[str]` | Portador inicial del recurso |
| `profundidad_minimax` | `int` | Profundidad máxima declarada |
| `prueba` | `Optional[dict]` | Bloque `prueba` del JSON, sin transformar |

#### 7.1.6 `ResultadoBusqueda` — `algoritmos/base.py`

`@dataclass` (mutable; no `frozen`)

| Atributo | Tipo / valor por defecto | Descripción |
|---|---|---|
| `algoritmo` | `str` | Nombre del algoritmo |
| `exito` | `bool` | Si encontró solución |
| `camino` | `list` (`[]`) | Lista de `(fila, columna)` |
| `costo` | `Optional[float]` | Costo acumulado o `None` |
| `estados_generados` | `int` (`0`) | Estados insertados en la frontera |
| `estados_expandidos` | `int` (`0`) | Estados cuyos sucesores se analizaron |
| `maximo_frontera` | `int` (`0`) | Tamaño máximo observado de la frontera |
| `tiempo_ms` | `float` (`0.0`) | Tiempo medido por `ejecutar_algoritmo` |
| `explorados` | `list` (`[]`) | Estados expandidos en orden |
| `parametros` | `dict` (`{}`) | Parámetros con los que se ejecutó |

Propiedad `longitud`: `len(camino) - 1` si `exito` y hay camino; en caso contrario `None`.

### 7.2 Formato JSON del escenario

Estructura observada en `escenarios/ejemplo.json`:

| Clave | Tipo JSON | Obligatoria | Validación verificada |
|---|---|---|---|
| `version` | cadena | Sí | Solo se exige su presencia; el valor no se compara |
| `mapa.filas` | entero | Sí | Entero positivo; no booleano |
| `mapa.columnas` | entero | Sí | Entero positivo; no booleano |
| `tipos_terreno` | objeto | Sí | No vacío; cada tipo debe tener `transitable` booleano; si es transitable, `costo` numérico > 0 |
| `terreno` | matriz | Sí | Lista de listas con dimensiones coherentes; cada nombre debe existir en `tipos_terreno` |
| `bases.A`, `bases.B` | objeto `{fila, columna}` | Sí | Enteros y dentro del mapa |
| `recurso` | objeto `{fila, columna}` | Sí | Enteros y dentro del mapa |
| `unidades` | lista | Sí | No vacía; cada elemento con `id`; ids únicos; `bando` A/B; posición entera, dentro del mapa y transitable |
| `turno` | cadena | Sí | A/B (se normaliza a mayúsculas) |
| `juego.portador_recurso` | cadena o `null` | Sí | Si no es `null`, debe corresponder a un `id` existente |
| `juego.profundidad_maxima_minimax` | entero | No | Valor por defecto: `3` (`PROFUNDIDAD_POR_DEFECTO`) |
| `prueba` | objeto | No | No se valida al cargar; la interfaz valida `modo` al ejecutar |

Campos opcionales dentro de `prueba` (leídos por `App._aplicar_prueba`): `modo`, `unidad_inicio`, `objetivo{fila,columna}`, `algoritmo`, `heuristica`, `k`.

Observaciones verificables:

- `recurso` y `bases` se validan dentro del mapa, pero **no** se valida que estén sobre terreno transitable.
- El campo `tipo` de cada unidad se acepta en el JSON pero no se modela internamente.
- `version` se exige como clave, pero su contenido no se valida.
- `prueba.modo` debe ser `busqueda`, `partida` o `adversarial` para que `App.ejecutar` no la rechace.

### 7.3 Relaciones

```
Escenario 1 ─── 1 Mapa
Escenario 1 ─── * Unidad        (tupla ordenada)
Escenario 1 ─── 1 Estado        (mediante estado_inicial)
Estado    1 ─── * Unidad        (tupla ordenada por id)
Estado    1 ─── 0..1 portador   (referencia a Unidad.id)
Reglas    1 ─── 1 Escenario
ProblemaNavegacion 1 ─── 1 Mapa
ResultadoBusqueda 1 ─── * celdas (camino)
```

---

## 8. Descripción técnica de clases, funciones y métodos

Convención de estado: **Implementado** = funcionalidad conectada y con lógica verificable en el código; **Parcial** = existe parte de la funcionalidad; **Pendiente** = declarada o prevista pero sin implementación; **Informativo** = constante, dato o utilidad.

### 8.1 `main.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| Bloque `if __name__ == "__main__"` | 4 | Crea `App()` y llama a `mainloop()` | Implementado |

### 8.2 `algoritmos/base.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| Constante `PLANIFICADOS` | 12 | Tupla de pares `(clave, nombre visible)` de algoritmos previstos: `("UCS", "Costo uniforme")`, `("A_ESTRELLA", "A*")`, `("BEAM_SEARCH", "Beam Search")` | Informativo |
| `REGISTRO` | 14 | Diccionario global `nombre → función` | Implementado |
| `ResultadoBusqueda` | 18 | Contenedor de resultados y métricas | Implementado |
| `ResultadoBusqueda.longitud` | 32 | Propiedad calculada del número de movimientos | Implementado |
| `ResultadoBusqueda.a_dict` | 36 | Serialización a diccionario con tiempo redondeado a 4 decimales | Implementado |
| `registrar(nombre)` | 46 | Decorador que inserta la función en `REGISTRO` | Implementado |
| `disponibles()` | 54 | Lista de nombres registrados en orden de inserción | Implementado |
| `normalizar_nombre(texto)` | 59 | Normaliza `a*` → `A_ESTRELLA`, espacios/guiones → `_` | Implementado |
| `reconstruir_camino(padre, meta)` | 65 | Reconstruye el camino y suma costos siguiendo `padre` | Implementado |
| `ejecutar_algoritmo(nombre, problema, **params)` | 84 | Invoca el algoritmo registrado, mide tiempo y adjunta parámetros | Implementado |

Orden de registro efectivo al importar `algoritmos`: `BFS`, `DFS`, `UCS`, `A_ESTRELLA` (determinado por el orden de importación en `algoritmos/__init__.py` y por el orden de las funciones decoradas).

### 8.3 `algoritmos/busqueda_no_informada.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `_exito(...)` | 7 | Construye un `ResultadoBusqueda` exitoso reconstruyendo el camino | Implementado |
| `bfs(problema, **params)` | 13 | Búsqueda en anchura; marca visitados al generar | Implementado |
| `dfs(problema, **params)` | 42 | Búsqueda en profundidad con pila; marca visitados al expandir | Implementado |

Observación verificable: BFS y DFS **no** usan los costos para elegir el camino, pero `reconstruir_camino` sí suma los costos del camino hallado, por lo que `ResultadoBusqueda.costo` refleja el costo del camino encontrado, no necesariamente el mínimo.

### 8.4 `algoritmos/busqueda_con_costo.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `_exito(...)` | 7 | Construye resultado exitoso | Implementado |
| `ucs(problema, **params)` | 13 | Búsqueda de costo uniforme con `heapq` y diccionario `mejor_g` | Implementado |

### 8.5 `algoritmos/a_estrella.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `_exito(...)` | 7 | Construye resultado exitoso | Implementado |
| `h_manhattan(s, problema)` | 12 | Distancia Manhattan multiplicada por `mapa.costo_minimo()` | Implementado |
| `h_propia(s, problema)` | 24 | `(d - 1) * c_min + costo(objetivo)`, con `0` en la meta | Implementado |
| `HEURISTICAS` | 39 | Diccionario `{"manhattan": h_manhattan, "propia": h_propia}` | Implementado |
| `obtener_heuristica(nombre)` | 45 | Devuelve la función pedida; si no existe, `h_manhattan` | Implementado |
| `a_estrella(problema, **params)` | 51 | A* con cola de prioridad, desempate por `h` y contador | Implementado |

Observaciones verificables:

- Los parámetros leídos son `params.get("heuristica", "manhattan")`.
- La frontera almacena `(f, h, contador, estado)`; al extraer se descartan estados ya expandidos.
- La meta se comprueba al extraer de la frontera.
- El diccionario `mejor_g` evita reinsertar un estado con costo mayor o igual.
- `h_propia` presupone que el objetivo es transitable; `ProblemaNavegacion`/interfaz validan esa condición antes de ejecutar.
- La heurística euclidiana **no existe** en la versión analizada; `git log -S "h_euclidiana"` muestra su introducción en el commit `05c4f4f` y su eliminación en el commit `e3561f5`. En el estado actual no hay referencias a `h_euclidiana`.

### 8.6 `escenario/mapa.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `DIRECCIONES` | 6 | Orden fijo de movimientos: ARRIBA, ABAJO, IZQUIERDA, DERECHA | Informativo |
| `Mapa` | 10 | Cuadrícula y catálogo de terrenos | Implementado |
| `Mapa.dentro(f, c)` | 16 | Comprueba límites de la cuadrícula | Implementado |
| `Mapa.es_transitable(f, c)` | 25 | `dentro` y `tipos[terreno]["transitable"]` | Implementado |
| `Mapa.costo(f, c)` | 34 | Costo de entrar a la celda; incluye `assert` de transitabilidad | Implementado |
| `Mapa.costo_minimo()` | 44 | Mínimo costo entre terrenos transitables | Implementado |
| `Mapa.vecinos(f, c)` | 53 | Lista de `(nombre_dir, f2, c2)` transitables en el orden de `DIRECCIONES` | Implementado |

### 8.7 `escenario/modelos.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `Escenario` | 10 | Datos validados del escenario | Implementado |
| `Escenario.estado_inicial()` | 20 | Construye `Estado`; si hay portador, `recurso_pos = None`; ordena unidades por `id` | Implementado |

### 8.8 `escenario/cargador.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `PROFUNDIDAD_POR_DEFECTO` | 9 | Valor `3` | Informativo |
| `ErrorEscenario` | 12 | Excepción con lista `errores` | Implementado |
| `ErrorEscenario.__init__(errores)` | 14 | Guarda la lista y compone el mensaje | Implementado |
| `construir_escenario(datos)` | 19 | Valida y convierte el dict en `Escenario` | Implementado |
| `cargar_escenario(ruta)` | 49 | Lee JSON y delega en `construir_escenario` | Implementado |

### 8.9 `escenario/validador.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `OBLIGATORIOS` | 3 | Claves obligatorias de la raíz | Informativo |
| `_es_entero(x)` | 7 | Entero y no booleano | Implementado |
| `_es_numero(x)` | 11 | Número y no booleano | Implementado |
| `validar_datos(d)` | 15 | Devuelve lista de errores; lista vacía si es válido | Implementado |

Comportamiento verificado: si la raíz no es `dict` o faltan claves obligatorias, retorna de inmediato. En caso contrario acumula todos los errores detectados. La función auxiliar interna `transitable(p)` devuelve `True` ante `KeyError`/`IndexError`/`TypeError` para no duplicar errores ya reportados.

### 8.10 `juego/estado.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `Unidad` | 7 | Entidad inmutable de unidad | Implementado |
| `Estado` | 15 | Estado inmutable del juego | Implementado |
| `Estado.unidad(uid)` | 21 | Busca una unidad por id; `None` si no existe | Implementado |
| `Estado.unidades_de(bando)` | 24 | Lista de unidades del bando | Implementado |
| `Estado.posicion_recurso()` | 27 | Posición del recurso en suelo o con el portador | Implementado |
| `Accion` | 36 | Acción inmutable | Implementado |

`Estado.posicion_recurso()` no se invoca desde los módulos revisados (solo se define). No se encontró uso en `app.py`, `reglas.py`, `tablero.py` ni en las pruebas.

### 8.11 `juego/reglas.py`

Reglas declaradas en el docstring del módulo: R1–R7 (una unidad por turno; no compartir celda salvo interceptación; recogida automática; interceptación del portador enemigo; victoria por base propia o por dejar al rival sin unidades; costo de movimiento = costo del terreno destino, esperar cuesta 0; siempre existe ESPERAR).

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `Reglas.__init__(escenario)` | 19 | Guarda `mapa` y `bases` | Implementado |
| `Reglas.acciones_legales(estado)` | 23 | Acciones del bando en turno, en orden determinista | Implementado |
| `Reglas.costo(estado, accion)` | 43 | `0` si ESPERAR; costo del destino si MOVER | Implementado |
| `Reglas.aplicar(estado, accion)` | 49 | Función de transición sin mutar el estado anterior | Implementado |
| `Reglas.ganador(estado)` | 75 | Devuelve `"A"`, `"B"` o `None` | Implementado |
| `Reglas.es_terminal(estado)` | 89 | `ganador(estado) is not None` | Implementado |

Detalles verificables de `acciones_legales`:

- Construye `ocupadas` como `{(fila, columna): unidad}`.
- Recorre las unidades del bando en turno.
- Para cada dirección: descarta destinos no transitables; descarta destinos ocupados, salvo que el ocupante sea el portador enemigo (excepción de interceptación).
- Agrega `Accion(u.id, "ESPERAR")` por cada unidad.

Detalles verificables de `aplicar`:

- Copia la lista de unidades, `recurso_pos` y `portador`.
- Si es MOVER y hay una víctima en el destino, la elimina y deja el recurso en el destino con `portador = None`.
- Reemplaza la unidad por una nueva instancia (las entidades son inmutables).
- Aplica recogida automática si el recurso está en el destino.
- Alterna el turno y devuelve un `Estado` con unidades ordenadas por `id`.

Condiciones previas declaradas: `accion in acciones_legales(estado)`. Si se violan, el uso de `next(...)` sin valor por defecto puede producir `StopIteration` al buscar la unidad.

### 8.12 `juego/problema_navegacion.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `ProblemaNavegacion` | 4 | Problema de un agente; estado `(fila, columna)` | Implementado |
| `ProblemaNavegacion.__init__(mapa, inicio, objetivo)` | 8 | Convierte `inicio` y `objetivo` a tuplas | Implementado |
| `ProblemaNavegacion.estado_inicial()` | 11 | Devuelve `inicio` | Implementado |
| `ProblemaNavegacion.es_objetivo(s)` | 14 | Igualdad con `objetivo` | Implementado |
| `ProblemaNavegacion.sucesores(s)` | 17 | `(nombre_accion, estado, costo)` desde `Mapa.vecinos` | Implementado |

Ejemplo real de `sucesores` (código íntegro):

```python
return [(n, (f, c), self.mapa.costo(f, c)) for n, f, c in self.mapa.vecinos(*s)]
```

### 8.13 `verificacion/verificador.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `verificar_camino(mapa, inicio, objetivo, resultado)` | 4 | Devuelve lista de `(descripción, ok, detalle)` | Implementado |

Comprobaciones realizadas (seis):

1. El camino comienza en la celda inicial.
2. Todas las celdas están dentro del mapa.
3. Ninguna celda es obstáculo (todas transitables).
4. Cada movimiento es un paso ortogonal de distancia Manhattan 1.
5. El costo reportado coincide con la suma de costos de las transiciones (tolerancia `1e-9`).
6. La última celda es el objetivo.

### 8.14 `interfaz/app.py`

Constantes del módulo:

| Constante | Valor | Uso |
|---|---|---|
| `TAREAS` | `{"Búsqueda de ruta": "busqueda", "Partida por turnos": "partida", "Decisión adversarial": "adversarial"}` | Mapeo nombre visible → clave interna |
| `MODO_A_TAREA` | Inverso de `TAREAS` | Mapeo clave → nombre visible |
| `METRICAS` | Seis métricas | Opciones de los desplegables de métricas |
| `HEURISTICAS` | `("manhattan", "propia")` | Heurísticas de A* |
| `MAX_JUGADAS_AUTO` | `300` | Tope de jugadas del auto-juego |
| `EJEMPLO` | Ruta a `escenarios/ejemplo.json` | Escenario de ejemplo |

Función de módulo:

| Elemento | Línea | Responsabilidad |
|---|---|---|
| `fmt(v)` | 30 | Formatea `None` como `—`, booleanos como `Sí`/`No`, flotantes redondeados a 3 decimales |

Clase `App(tk.Tk)`:

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `__init__` | 41 | Inicializa atributos, tema, construcción de UI, frame de tarea y estado | Implementado |
| `_tema` | 59 | Configura estilos `ttk` (tema oscuro) | Implementado |
| `_texto` | 145 | Crea caja de texto con etiquetas de color | Implementado |
| `_construir` | 157 | Barra superior, panel dividido, tablero y pestañas | Implementado |
| `_tab_control` | 215 | Pestaña Control con misión y formularios | Implementado |
| `_f_busqueda` | 240 | Formulario de búsqueda (algoritmo, unidad, objetivo, heurística, `k`, opciones) | Implementado |
| `_f_partida` | 291 | Formulario de partida (control por bando, botones) | Implementado |
| `_f_adversarial` | 321 | Formulario adversarial (algoritmo, profundidad) | Parcial |
| `_tab_resultados` | 340 | Tabla de métricas y texto de resultados | Implementado |
| `_tab_estadisticas` | 352 | Resumen, historial, gráfico, comparación de heurísticas | Implementado |
| `_tab_comparacion` | 398 | Comparación de algoritmos, selector de heurística de A* | Implementado |
| `_tab_escenario` | 426 | Resumen del escenario y log | Implementado |
| `_poner_estado` | 436 | Escribe la barra de estado | Implementado |
| `log` | 439 | Agrega línea al log | Implementado |
| `_tarea` | 443 | Clave interna de la tarea seleccionada | Implementado |
| `_modo_json` | 446 | `True` si el modo es JSON | Implementado |
| `_es_astar` | 449 | `True` si el algoritmo seleccionado normaliza a `A_ESTRELLA` | Implementado |
| `_actualizar_visibles` | 452 | Muestra heurística y comparación solo con A*; `k` solo con Beam Search | Implementado |
| `cargar_dialogo` | 469 | Diálogo de selección de JSON | Implementado |
| `cargar_ruta` | 475 | Carga validando primero; conserva el escenario anterior ante error | Implementado |
| `_mostrar_errores` | 488 | Muestra errores de validación | Implementado |
| `_aplicar_escenario` | 496 | Crea `Reglas`, estado, ajusta controles, limpia y redibuja | Implementado |
| `_resumen_escenario` | 519 | Texto con detalles del escenario | Implementado |
| `_dibujar_leyenda` | 533 | Leyenda de terrenos y símbolos | Implementado |
| `cambiar_modo` | 562 | Aplica modo JSON/exploración, bloqueo y ejecución automática | Implementado |
| `_aplicar_prueba` | 578 | Lee `prueba` y ajusta controles | Implementado |
| `_bloquear` | 607 | Habilita/deshabilita controles | Implementado |
| `_elegir_tarea` | 615 | Cambia la tarea activa | Implementado |
| `_cambio_tarea` | 622 | Redibuja tras cambio de tarea | Implementado |
| `_mostrar_frame_tarea` | 626 | Muestra el formulario de la tarea activa | Implementado |
| `_cambio_parametros` | 633 | Limpia capas y redibuja ante cambios de parámetros | Implementado |
| `_inicio_busqueda` | 639 | Posición de la unidad de inicio | Implementado |
| `_objetivo_busqueda` | 645 | Objetivo si está dentro del mapa | Implementado |
| `refrescar_tablero` | 652 | Compone capas y actualiza tablero, turno y costos | Implementado |
| `_limpiar_vista` | 678 | Limpia capas visuales | Implementado |
| `_hover_celda` | 682 | Información de la celda bajo el cursor | Implementado |
| `clic_tablero` | 707 | Despacha clics según tarea | Implementado |
| `_es_humano` | 727 | Indica si el bando es humano | Implementado |
| `_clic_partida` | 730 | Selección de unidad y movimiento en partida | Implementado |
| `_reiniciar_partida` | 751 | Restaura el estado inicial y contadores | Implementado |
| `_aplicar_accion` | 760 | Aplica una acción, acumula costo, registra y comprueba victoria | Implementado |
| `esperar` | 779 | Acción ESPERAR para la unidad seleccionada | Implementado |
| `turno_ia` | 788 | Elige una acción aleatoria para el bando no humano | Parcial (controlador aleatorio) |
| `auto_jugar` | 796 | Alterna el auto-juego | Implementado |
| `_auto_tick` | 804 | Avanza el auto-juego cada 250 ms, con tope de 300 jugadas | Implementado |
| `ejecutar` | 823 | Despacha según tarea | Implementado |
| `_problema` | 844 | Construye y valida `ProblemaNavegacion` | Implementado |
| `_parametros` | 863 | Devuelve `{"k": int, "heuristica": str}` | Implementado |
| `_correr` | 870 | Ejecuta, verifica, agrega al historial y devuelve `(res, checks)` | Implementado |
| `_ejecutar_busqueda` | 882 | Ejecuta búsqueda, muestra resultados; si es A*, compara heurísticas | Implementado |
| `comparar_todos` | 902 | Ejecuta todos los algoritmos registrados | Implementado |
| `verificar` | 919 | Re-verifica la última ejecución | Implementado |
| `_ejecutar_adversarial` | 933 | Lista acciones legales; no calcula Minimax | Pendiente (solo listado) |
| `_limpiar_resultados` | 944 | Limpia resultados, comparación e historial de heurísticas | Implementado |
| `_mostrar_resultado` | 955 | Rellena métricas, camino, verificación y JSON | Implementado |
| `_mostrar_comparacion` | 979 | Rellena tabla de comparación y resumen | Implementado |
| `_seleccion_comparacion` | 1002 | Muestra el camino del algoritmo seleccionado en el tablero | Implementado |
| `_graficar_comparacion` | 1011 | Gráfico de barras por algoritmo | Implementado |
| `_refrescar_estadisticas` | 1017 | Historial, resumen y gráfico | Implementado |
| `_agrupar` | 1034 | Agrupa historial por algoritmo | Implementado |
| `_graficar_estadisticas` | 1040 | Barras por heurística si A* está activo; si no, promedio por algoritmo | Implementado |
| `_comparar_heuristicas` | 1053 | Ejecuta A* con cada heurística y guarda resultados | Implementado |
| `_refrescar_comparacion_heur` | 1064 | Rellena tabla de heurísticas y redibuja | Implementado |
| `exportar_csv` | 1078 | Exporta el historial a CSV | Implementado |
| `borrar_historial` | 1091 | Vacía historial y comparación de heurísticas | Implementado |

Comportamientos verificables de la interfaz:

- La heurística (`cb_heur`) y la tabla/checkboxes de comparación de heurísticas se muestran solo cuando el algoritmo seleccionado normaliza a `A_ESTRELLA`.
- El control `k` se muestra solo cuando el algoritmo seleccionado es `BEAM_SEARCH`.
- Al ejecutar A* se comparan ambas heurísticas: se reutiliza el resultado de la heurística seleccionada y se ejecuta A* con la otra.
- La pestaña Comparación conserva la ejecución de todos los algoritmos y permite elegir la heurística usada por A* (`var_heur_cmp`).
- Cada llamada a `_correr` agrega una entrada al historial; por tanto, una ejecución de A* con comparación de heurísticas agrega una entrada por cada heurística ejecutada (la seleccionada se reutiliza, la otra se ejecuta y registra).

### 8.15 `interfaz/tablero.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| Constantes de paleta | 5–17 | Colores del tema oscuro | Informativo |
| `_rgb`, `_hex`, `mezclar`, `aclarar`, `oscurecer` | 20–40 | Utilidades de color | Implementado |
| `contraste(hex_color)` | 43 | Color de texto legible sobre un fondo | Implementado |
| `colores_terreno(mapa)` | 52 | Color por tipo; derivado del costo para tipos no fijos | Implementado |
| `fmt_num(v)` | 70 | Formato numérico compacto | Implementado |
| `Tablero` | 74 | `tk.Canvas` que dibuja el estado | Implementado |
| `Tablero.__init__` | 75 | Enlaza eventos y callbacks | Implementado |
| `Tablero.mostrar` | 85 | Guarda escenario, estado y capas; redibuja | Implementado |
| `Tablero.limpiar` | 90 | Borra la vista | Implementado |
| `_rect`, `_centro`, `_esquina`, `_corchetes`, `_placa` | 95–119 | Geometría y elementos visuales | Implementado |
| `redibujar` | 130 | Dibuja terreno, bases, capas, recurso y unidades | Implementado |
| `_dibujar_hover`, `_poner_hover` | 301, 309 | Resaltado bajo el cursor | Implementado |
| `_celda_en`, `_movimiento`, `_clic` | 317–330 | Conversión de píxeles a celda y despacho de eventos | Implementado |

Capas aceptadas por `mostrar`: `camino`, `explorados`, `inicio`, `objetivo`, `seleccion`, `destinos`, `turno_marcador`.

### 8.16 `interfaz/graficas.py`

| Elemento | Línea | Responsabilidad | Estado |
|---|---|---|---|
| `_fmt`, `_rect` | 8, 12 | Utilidades de formato y rectángulos | Implementado |
| `barras(canvas, datos, titulo="")` | 18 | Dibuja barras y rejilla; ignora valores `None`; si el canvas es menor a 40×60 no dibuja | Implementado |

### 8.17 `experimentos/`

| Archivo / elemento | Responsabilidad | Estado |
|---|---|---|
| `generar_casos_minimos.py` | Genera `caso01`, `caso05`, `caso06a`, `caso06b` en `escenarios/casos_minimos` | Implementado |
| `generar_casos_minimos.matriz`, `poner`, `rect`, `unidad`, `escenario`, `guardar` | Utilidades de construcción | Implementado |
| `generar_casos_minimos.caso1`, `caso5`, `caso6` | Definición de los casos | Implementado |
| `caso06_estado_compuesto.py` | Imprime comparación de estados de los casos 6a y 6b | Implementado |

Observación verificable: `generar_casos_minimos.py` escribe en `escenarios/casos_minimos` (guion bajo), mientras que la carpeta versionada es `escenarios/casos minimos` (espacio). Ejecutar el generador crearía/actualizaría una carpeta distinta de la usada por las pruebas y los escenarios existentes.

---

## 9. Parámetros, tipos, retornos, excepciones y efectos secundarios

Solo se documentan datos verificables en el código. Las anotaciones de tipo son las declaradas; cuando el código no anota, se indica «por uso».

### 9.1 Funciones del cargador

| Función | Parámetros | Retorno | Excepciones | Efectos secundarios |
|---|---|---|---|---|
| `validar_datos(d)` | `d`: cualquier objeto | `list[str]` (vacía si válido) | No declaradas; maneja internamente tipos inesperados | Ninguno; no modifica `d` |
| `construir_escenario(datos)` | `datos`: `dict` | `Escenario` | `ErrorEscenario` si hay errores de validación | Ninguno |
| `cargar_escenario(ruta)` | `ruta`: ruta de archivo | `Escenario` | `ErrorEscenario` ante JSON mal formado o error de E/S | Lectura de archivo |

### 9.2 Funciones de reglas

| Función | Parámetros | Retorno | Excepciones | Efectos secundarios |
|---|---|---|---|---|
| `Reglas.__init__(escenario)` | `escenario`: `Escenario` | instancia | No | Guarda referencias |
| `Reglas.acciones_legales(estado)` | `estado`: `Estado` | `list[Accion]` | No | Ninguno |
| `Reglas.costo(estado, accion)` | `estado`, `accion` | número (`0` o costo del destino) | Precondición: acción legal | Ninguno |
| `Reglas.aplicar(estado, accion)` | `estado`, `accion` | `Estado` nuevo | Potencial `StopIteration` si la acción no corresponde a una unidad existente (precondición) | Ninguno; no muta el estado anterior |
| `Reglas.ganador(estado)` | `estado` | `"A"`, `"B"` o `None` | Precondición: estado consistente; un `portador` inexistente produciría `AttributeError` | Ninguno |
| `Reglas.es_terminal(estado)` | `estado` | `bool` | Las de `ganador` | Ninguno |

### 9.3 Funciones de búsqueda

| Función | Parámetros | Retorno | Excepciones | Efectos secundarios |
|---|---|---|---|---|
| `ejecutar_algoritmo(nombre, problema, **params)` | `nombre`: clave del registro; `problema`: objeto con `estado_inicial`, `es_objetivo`, `sucesores`; `params`: arbitrarios | `ResultadoBusqueda` | `KeyError` si `nombre` no está en `REGISTRO` | Mide tiempo; asigna `tiempo_ms` y `parametros` al resultado |
| `bfs(problema, **params)` | `problema` | `ResultadoBusqueda` | Las de la interfaz del problema | Ninguno |
| `dfs(problema, **params)` | `problema` | `ResultadoBusqueda` | Ídem | Ninguno |
| `ucs(problema, **params)` | `problema` | `ResultadoBusqueda` | Ídem | Ninguno |
| `a_estrella(problema, **params)` | `problema`; `params["heuristica"]` opcional (`"manhattan"` por defecto) | `ResultadoBusqueda` | Ídem | Ninguno |
| `h_manhattan(s, problema)` | `s`: celda; `problema` | número | `mapa` debe exponer `costo_minimo()` | Ninguno |
| `h_propia(s, problema)` | `s`: celda; `problema` | número | `mapa` debe exponer `costo_minimo()` y `costo()` | Ninguno |
| `obtener_heuristica(nombre)` | `nombre`: cualquier valor convertible a cadena | función de heurística | No | Ninguno |
| `reconstruir_camino(padre, meta)` | `padre`: dict; `meta`: estado | `(list, número)` | `KeyError` si `padre` es inconsistente (precondición) | Ninguno |

### 9.4 Funciones de mapa y modelo

| Función | Parámetros | Retorno | Excepciones | Efectos secundarios |
|---|---|---|---|---|
| `Mapa.dentro(f, c)` | enteros | `bool` | No | Ninguno |
| `Mapa.es_transitable(f, c)` | enteros | `bool` | `KeyError` si el nombre de terreno no está en `tipos` (escenario inconsistente) | Ninguno |
| `Mapa.costo(f, c)` | enteros | número | `AssertionError` si la celda no es transitable | Ninguno |
| `Mapa.costo_minimo()` | — | número | `ValueError` si no hay terrenos transitables (`min` sobre vacío) | Ninguno |
| `Mapa.vecinos(f, c)` | enteros | `list[(str, int, int)]` | Las de `es_transitable` | Ninguno |
| `Escenario.estado_inicial()` | — | `Estado` | No | Ninguno |
| `Estado.unidad(uid)` | `str` | `Unidad` o `None` | No | Ninguno |
| `Estado.unidades_de(bando)` | `str` | `list[Unidad]` | No | Ninguno |
| `Estado.posicion_recurso()` | — | tupla o `None` | `AttributeError` si `portador` no corresponde a una unidad | Ninguno |

### 9.5 Verificación

| Función | Parámetros | Retorno | Excepciones | Efectos secundarios |
|---|---|---|---|---|
| `verificar_camino(mapa, inicio, objetivo, resultado)` | `mapa`; `inicio`, `objetivo`: tuplas; `resultado`: `ResultadoBusqueda` con `exito=True` | `list[(str, bool, str)]` | Las de `mapa.dentro`, `mapa.es_transitable`, `mapa.costo` si el camino es inválido | Ninguno |

### 9.6 Interfaz

| Elemento | Entradas verificables | Salidas / efectos |
|---|---|---|
| `App()` | — | Abre ventana; crea widgets y atributos de estado |
| `App.cargar_ruta(ruta)` | ruta de archivo | Carga escenario o muestra errores; actualiza controles, leyenda y log; puede ejecutar automáticamente |
| `App.ejecutar()` | estado de la UI | Ejecuta búsqueda, partida o adversarial; puede mostrar diálogos |
| `App.comparar_todos()` | escenario y objetivo actuales | Ejecuta todos los algoritmos; agrega entradas al historial; muestra comparación |
| `App.exportar_csv()` | historial en memoria | Abre diálogo de guardado; escribe el CSV en la ruta elegida con las claves del primer registro del historial |
| `App.borrar_historial()` | — | Vacía historial, comparación de heurísticas y refresca vistas |

Diálogos observables: `messagebox.showinfo`, `showerror`, `showwarning` y `filedialog.asksaveasfilename`/`askopenfilename`.

---

## 10. Configuración, instalación y ejecución

### 10.1 Requisitos

| Requisito | Evidencia |
|---|---|
| Python 3.9 o superior | `README.md`, línea 9 |
| `tkinter` incluido en la instalación de Python | `README.md`, línea 9 |
| En Ubuntu/Debian: `sudo apt install python3-tk` | `README.md`, línea 9 |
| Sin dependencias de terceros | No hay archivo de dependencias; todas las importaciones son de la biblioteca estándar |

### 10.2 Variables de entorno

No se detectó lectura de variables de entorno (`os.environ`, `os.getenv`, `dotenv`) ni uso de argumentos de línea de comandos (`argparse`, `sys.argv`) en el código del proyecto. La configuración se realiza mediante:

- el archivo JSON de escenario cargado desde la interfaz;
- los controles de la interfaz (algoritmo, heurística, `k`, unidad, objetivo, tarea, modo).

### 10.3 Instalación

No se requiere instalación de paquetes. Basta con disponer de Python y `tkinter`. No hay instalador, empaquetado ni script de configuración.

### 10.4 Ejecución (respaldada por archivos existentes)

Desde la raíz del repositorio:

```bash
python3 main.py
```

En el entorno Windows de elaboración se verificó que el intérprete disponible responde a `python` (versión 3.12.0). La forma equivalente es:

```bash
python main.py
```

> No se ejecutó la interfaz gráfica durante la elaboración de este manual; la instrucción se deriva de `main.py` y del `README.md`.

### 10.5 Ejecución de pruebas

```bash
python3 tests/test_paso1_2.py
```

Forma equivalente verificada durante la elaboración:

```bash
python -m unittest discover -s tests -v
```

### 10.6 Generación de escenarios de ejemplo

```bash
python3 experimentos/generar_casos_minimos.py
```

Advertencia verificable: el script escribe en `escenarios/casos_minimos`, mientras que los escenarios versionados están en `escenarios/casos minimos`.

### 10.7 Ejecución del experimento del caso 6

```bash
python3 experimentos/caso06_estado_compuesto.py
```

Este script imprime por consola posiciones, igualdad/hash de estados, portador, recurso y acciones legales de los casos 6a y 6b.

### 10.8 Modos de la interfaz

| Modo | Comportamiento verificado |
|---|---|
| Modo JSON (por defecto, `var_modo = "json"`) | Aplica `prueba` y bloquea controles; si hay `prueba`, ejecuta automáticamente la tarea |
| Modo exploración | Permite elegir libremente tarea, algoritmo, unidad y objetivo |

---

## 11. Pruebas existentes y mecanismos de validación

### 11.1 Pruebas automatizadas

Se ejecutó la suite completa durante la elaboración con:

```bash
python -m unittest discover -s tests -v
```

**Resultado obtenido: 17 pruebas ejecutadas, 17 correctas (`OK`), en 0.029 s, con Python 3.12.0.**

| Archivo | Clase | Prueba | Qué comprueba (según el código) | Resultado observado |
|---|---|---|---|---|
| `tests/test_paso1_2.py` | `TestCarga` | `test_valido` | Dimensiones, costo `(2,2)=7`, costo mínimo `1`, profundidad `4` | OK |
| `tests/test_paso1_2.py` | `TestCarga` | `test_errores_multiples` | Al menos 5 errores ante varias inconsistencias | OK |
| `tests/test_paso1_2.py` | `TestCarga` | `test_unidad_sobre_muro` | Error «no transitable» | OK |
| `tests/test_paso1_2.py` | `TestCarga` | `test_costo_no_positivo` | Error «costo positivo» | OK |
| `tests/test_paso1_2.py` | `TestCarga` | `test_dimensiones_inconsistentes` | Error por filas incoherentes | OK |
| `tests/test_paso1_2.py` | `TestJuego` | `test_hashable_e_inmutable` | `Estado` igual y hashable | OK |
| `tests/test_paso1_2.py` | `TestJuego` | `test_acciones_y_sucesor` | Acciones del bando en turno y alternancia de turno | OK |
| `tests/test_paso1_2.py` | `TestJuego` | `test_estado_compuesto` | Misma posición de unidad, estados distintos según portador | OK |
| `tests/test_paso1_2.py` | `TestJuego` | `test_recoger_recurso` | Recogida automática al pisar el recurso | OK |
| `tests/test_paso1_2.py` | `TestJuego` | `test_victoria` | Victoria al portador en base propia | OK |
| `tests/test_paso1_2.py` | `TestJuego` | `test_interceptar` | Interceptación del portador enemigo | OK |
| `tests/test_paso1_2.py` | `TestJuego` | `test_no_atraviesa_muro_ni_ocupadas` | Destinos legales transitables y no ocupados | OK |
| `tests/test_paso3_ucs.py` | `TestUCS` | `test_ucs_ejecucion_y_verificacion` | Éxito, métricas positivas y verificación del camino | OK |
| `tests/test_paso3_ucs.py` | `TestUCS` | `test_caso2_bfs_vs_ucs_diferencia` | Caminos distintos; BFS menos movimientos; UCS menor costo | OK |
| `tests/test_paso4_a_estrella.py` | `TestAEstrella` | `test_admisibilidad_heuristicas` | Heurísticas `0` en meta y `h_propia >= h_manhattan` en inicio | OK |
| `tests/test_paso4_a_estrella.py` | `TestAEstrella` | `test_caso3_obstaculo_y_heuristica` | Camino verificado y rodeo del muro | OK |
| `tests/test_paso4_a_estrella.py` | `TestAEstrella` | `test_caso4_comparacion_heuristicas` | Mismo costo óptimo; `propia` expande menos que `manhattan` | OK |

Nota: la prueba `test_admisibilidad_heuristicas` no comprueba numéricamente la admisibilidad global de las heurísticas; comprueba los valores en la meta y una relación de orden en el inicio, según el código de la prueba.

### 11.2 Mecanismos de validación en producción

| Mecanismo | Ubicación | Función |
|---|---|---|
| Validación de escenarios | `escenario/validador.py` | Acumula errores de estructura, dimensiones, terrenos, bases, recurso, unidades, turno y portador |
| Carga «todo o nada» | `escenario/cargador.py`, `App.cargar_ruta` | No reemplaza el escenario anterior si el nuevo es inválido |
| Aserción de costo | `Mapa.costo` | `assert` de transitabilidad antes de leer el costo |
| Verificación de caminos | `verificacion/verificador.py` | Seis comprobaciones independientes del algoritmo |
| Verificación en interfaz | `App._correr`, `App.verificar` | Ejecuta `verificar_camino` y muestra el resultado |
| Comprobación de algoritmo implementado | `App._ejecutar_busqueda` | Rechaza algoritmos no registrados |

### 11.3 Pruebas no existentes

- No hay pruebas automatizadas de la interfaz gráfica.
- No hay pruebas de `interfaz/tablero.py`, `interfaz/graficas.py` ni de los flujos de `App` (aunque parte de la lógica se ejerce indirectamente desde los tests de algoritmos y reglas).
- En la versión inicial documentada no había pruebas de Beam Search ni de Minimax/alfa-beta. Para el componente adversarial se añadieron pruebas en `tests/test_minimax.py`; Beam Search aún requiere una matriz de pruebas específica para k=1,2,4,8.
- No hay medición de cobertura.
- No hay integración continua configurada.

---

## 12. Limitaciones técnicas, deuda técnica y funcionalidades pendientes

### 12.1 Funcionalidades pendientes

| Elemento | Evidencia | Estado |
|---|---|---|
| Beam Search | `algoritmos/beam_search.py` registra el algoritmo | Implementado; falta completar pruebas comparativas para k=1,2,4,8 |
| Comparación con `k` | `algoritmos/beam_search.py` acepta el ancho de haz | Parcial: falta ejecutar y registrar todos los valores exigidos |
| Minimax | `algoritmos/minimax.py`, interfaz y `tests/test_minimax.py` | Implementado y probado en los escenarios 7–10 |
| Alfa-beta | `algoritmos/minimax.py`, interfaz y reporte experimental | Implementado y probado en los escenarios 7–10 |
| Controlador de partida por IA | El único controlador no humano es «Azar (provisional)» (`turno_ia` elige aleatoriamente) | Parcial |
| Contenido de `docs/` y `heuristicas/` | Directorios vacíos | **Pendiente** |

### 12.2 Deuda técnica y limitaciones verificables

| Aspecto | Observación |
|---|---|
| Ausencia de archivo de dependencias | No hay `requirements.txt` ni equivalente; no se fijan versiones |
| Ausencia de empaquetado | No hay `__init__.py` en `escenario`, `juego`, `interfaz`, `verificacion`, `tests` ni `experimentos`; se depende de paquetes de espacio de nombres |
| Sin linter/formateador/CI | No se encontró configuración |
| Docstrings con validación incompleta | Varios métodos contienen `Student validation: (completar)` — `[COMPLETAR CUANDO SE IMPLEMENTE]` |
| Campo `tipo` de unidades | Se acepta en el JSON pero no se modela en `Unidad` ni se usa en reglas |
| `version` sin validación de valor | Solo se exige la clave |
| Bases y recurso sobre obstáculos | El validador no comprueba transitabilidad de bases ni del recurso; solo de unidades |
| Generador de casos y carpeta de salida | `generar_casos_minimos.py` usa `casos_minimos`; la carpeta versionada es `casos minimos` |
| Crecimiento del historial | El historial se mantiene en memoria y crece con cada ejecución; cada ejecución de A* agrega una entrada por heurística ejecutada |
| Costo en BFS/DFS | El costo reportado corresponde al camino hallado; no se optimiza por costo |
| Condiciones previas no verificadas en tiempo de ejecución | Varias funciones asumen precondiciones (`Reglas.aplicar`, `reconstruir_camino`, `Mapa.costo`) y pueden lanzar excepciones si se violan |
| Mediciones de tiempo | `tiempo_ms` mide solo la llamada al algoritmo, no la verificación ni la interfaz |
| Escenario `caso05_beam_search.json` | No ejecutable con los algoritmos registrados; la interfaz informaría «Algoritmo pendiente» |
| Rutas absolutas en el manual | Las rutas citadas son relativas a la raíz del repositorio |
| Heurística euclidiana | Ausente en la versión actual; `git log -S "h_euclidiana"` registra su eliminación en el commit `e3561f5` y no hay referencias actuales |

### 12.3 Aspectos no verificados

- No se verificó el comportamiento visual de la interfaz en ejecución (no se abrió la ventana durante esta elaboración).
- No se verificó el rendimiento en escenarios de gran tamaño más allá de lo que miden las pruebas.
- No se verificó la ejecución de `experimentos/generar_casos_minimos.py` ni `experimentos/caso06_estado_compuesto.py` durante esta elaboración.
- No se verificó compatibilidad real con Python 3.9, 3.10 u 3.11; solo se ejecutó con 3.12.0.
- No se pudo determinar la versión del proyecto: no hay etiquetas ni metadatos.
- No se verificó el contenido de `docs/` ni `heuristicas/` porque están vacíos.

---

## 13. Anexos

### 13.1 Anexo A — Diagramas solicitados

#### A.1 Diagrama de clases

```
[PENDIENTE DE IMPLEMENTACIÓN: insertar diagrama de clases]
Elementos a representar:
- Mapa (frozen) — filas, columnas, terreno, tipos
- Escenario (frozen) — mapa, bases, recurso, unidades, turno, portador,
  profundidad_minimax, prueba
- Unidad (frozen), Estado (frozen), Accion (frozen)
- Reglas — acciones_legales, costo, aplicar, ganador, es_terminal
- ProblemaNavegacion — estado_inicial, es_objetivo, sucesores
- ResultadoBusqueda (mutable)
- App(tk.Tk), Tablero(tk.Canvas)
```

#### A.2 Diagrama de dependencias

```
[PENDIENTE DE IMPLEMENTACIÓN: insertar diagrama de dependencias]
Fuente verificable: tabla de la sección 6.2.
```

#### A.3 Diagrama de secuencia de una búsqueda

```
[PENDIENTE DE IMPLEMENTACIÓN: insertar diagrama de secuencia]
Secuencia verificable:
App._ejecutar_busqueda
  -> App._problema
  -> App._correr
     -> ejecutar_algoritmo
        -> algoritmo registrado (BFS/DFS/UCS/A*)
           -> ProblemaNavegacion.sucesores
              -> Mapa.vecinos / Mapa.costo
     -> verificar_camino
     -> historial.append
  -> App._mostrar_resultado
  -> (si A*) App._comparar_heuristicas
  -> App._refrescar_estadisticas
```

#### A.4 Diagrama de estados del juego

```
[PENDIENTE DE IMPLEMENTACIÓN: insertar diagrama de estados]
Transiciones verificables: Reglas.aplicar sobre Estado
Acciones: MOVER (4 direcciones ortogonales) y ESPERAR
Condiciones terminales: Reglas.ganador
```

### 13.2 Anexo B — Ejemplo real de escenario JSON

Tomado de `escenarios/ejemplo.json` (contenido íntegro):

```json
{
  "version": "1.0",
  "mapa": {"filas": 4, "columnas": 4},
  "tipos_terreno": {
    "camino":  {"costo": 1, "transitable": true},
    "pasto":   {"costo": 2, "transitable": true},
    "bosque":  {"costo": 4, "transitable": true},
    "pantano": {"costo": 7, "transitable": true},
    "muro":    {"transitable": false}
  },
  "terreno": [
    ["camino", "camino", "pasto", "pasto"],
    ["camino", "muro", "bosque", "pasto"],
    ["camino", "camino", "pantano", "pasto"],
    ["pasto", "pasto", "camino", "camino"]
  ],
  "bases": {"A": {"fila": 0, "columna": 0}, "B": {"fila": 3, "columna": 3}},
  "recurso": {"fila": 2, "columna": 2},
  "unidades": [
    {"id": "A1", "bando": "A", "tipo": "estandar", "fila": 0, "columna": 1},
    {"id": "A2", "bando": "A", "tipo": "estandar", "fila": 1, "columna": 0},
    {"id": "B1", "bando": "B", "tipo": "estandar", "fila": 3, "columna": 2},
    {"id": "B2", "bando": "B", "tipo": "estandar", "fila": 2, "columna": 3}
  ],
  "turno": "A",
  "juego": {"portador_recurso": null, "profundidad_maxima_minimax": 4},
  "prueba": {"modo": "busqueda", "unidad_inicio": "A1", "objetivo": {"fila": 3, "columna": 2}}
}
```

### 13.3 Anexo C — Ejemplo real de resultado serializado

Esquema producido por `ResultadoBusqueda.a_dict` (tipos, no valores concretos):

```
{
  "algoritmo": str,
  "exito": bool,
  "camino": list[list[int]],
  "costo": número | null,
  "estados_generados": int,
  "estados_expandidos": int,
  "maximo_frontera": int,
  "tiempo_ms": float
}
```

> `a_dict` redondea `tiempo_ms` a 4 decimales y convierte cada celda del camino a lista. Los valores concretos dependen del escenario y del algoritmo; no se transcriben resultados no reproducidos en esta elaboración.

### 13.4 Anexo D — Ejemplo real de código

Función de sucesores (`juego/problema_navegacion.py`, líneas 17–24):

```python
def sucesores(self, s):
    """Purpose: generar (nombre_accion, estado_siguiente, costo) en orden determinista.
    Preconditions: s es una celda transitable del mapa.
    Postconditions: solo celdas dentro del mapa y transitables; costo > 0.
    Complexity: O(1).
    AI usage: Yes. AI intervention: estructura del método.
    Student validation: (completar)."""
    return [(n, (f, c), self.mapa.costo(f, c)) for n, f, c in self.mapa.vecinos(*s)]
```

### 13.5 Anexo E — Evidencias de ejecución

```
[AGREGAR EVIDENCIA]
Sugerencia de evidencia a incorporar:
- Captura de la salida de `python -m unittest discover -s tests -v`.
  Resultado obtenido en esta elaboración:
  "Ran 17 tests in 0.029s — OK" (Python 3.12.0, 2026-10-19).
- Captura de la ventana principal con un escenario cargado.
- Captura de la pestaña Resultados tras una búsqueda.
- Captura de la pestaña Estadísticas con la comparación de heurísticas de A*.
- Captura de la pestaña Comparación con todos los algoritmos.
```

### 13.6 Anexo F — Inventario de escenarios

| Archivo | Contenido verificable | `prueba.modo` |
|---|---|---|
| `escenarios/ejemplo.json` | Mapa 4×4; 4 unidades; recurso en `(2,2)` | `busqueda` |
| `escenarios/prueba_busqueda_dfs.json` | Mapa 4×4; algoritmo DFS; objetivo `(3,0)` | `busqueda` |
| `escenarios/prueba_partida.json` | Mapa 4×4; sin portador inicial | `partida` |
| `escenarios/prueba_adversarial.json` | Mapa 4×4; portador `B1` | `adversarial` |
| `escenarios/invalido_a_proposito.json` | Costo `0` en `pasto` y tipo `lava` inexistente | No aplica (inválido) |
| `escenarios/casos minimos/caso01_bfs_vs_dfs.json` | Mapa 20×20; BFS vs DFS | `busqueda` |
| `escenarios/casos minimos/caso2_ruta_corta_vs_economica.json` | Mapa para BFS vs UCS | `busqueda` |
| `escenarios/casos minimos/caso3_obstaculo_y_heuristica.json` | Mapa con obstáculo | `busqueda` |
| `escenarios/casos minimos/caso4_comparacion_heuristicas.json` | Mapa para comparar heurísticas | `busqueda` |
| `escenarios/casos minimos/caso05_beam_search.json` | Referencia `BEAM_SEARCH`, `k=1` | `busqueda` |
| `escenarios/casos minimos/caso06a_sin_recurso.json` | Estado compuesto sin portador | `adversarial` |
| `escenarios/casos minimos/caso06b_con_recurso.json` | Estado compuesto con portador `A1` | `adversarial` |

### 13.7 Anexo G — Glosario

| Término | Definición en el contexto del proyecto |
|---|---|
| Estado | Tupla inmutable `(unidades, recurso_pos, portador, turno)` |
| Acción | `MOVER` a una celda ortogonal o `ESPERAR` |
| Sucesor | Celda adyacente transitable con su acción y costo |
| Frontera | Colección de estados pendientes de expandir |
| Expandido | Estado cuyos sucesores fueron analizados |
| Generado | Estado insertado en la frontera |
| c_min | Menor costo entre terrenos transitables (`Mapa.costo_minimo`) |
| Portador | Unidad que lleva el recurso |
| Interceptación | Entrada a la celda del portador enemigo, que lo elimina |
| Escenario válido | JSON que supera `validar_datos` sin errores |

---

### Nota final de alcance documental

Este manual describe el estado del repositorio en el commit `36782b9` de la rama `main`. Cualquier cambio posterior en el código puede invalidar total o parcialmente las referencias de línea y los comportamientos aquí descritos. Las secciones marcadas con `[PENDIENTE DE IMPLEMENTACIÓN]`, `[COMPLETAR CUANDO SE IMPLEMENTE]` o `[AGREGAR EVIDENCIA]` requieren completarse con información o artefactos que no existen en el repositorio al momento de la elaboración.
