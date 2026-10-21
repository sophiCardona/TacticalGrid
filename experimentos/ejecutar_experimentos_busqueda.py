"""Script automatizado para recolectar resultados cuantitativos de búsqueda.

Ejecuta los algoritmos sobre los escenarios de prueba mínimos (casos 1 al 5)
y genera tablas comparativas con:
- Tiempo de ejecución (ms)
- Estados generados
- Estados expandidos
- Máximo en frontera (memoria pico)
- Longitud del camino (movimientos)
- Costo total acumulado
- Verificación del camino
"""
import os
import sys

# Asegurar que el directorio raíz de TacticalGrid esté en sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import algoritmos  # Activa el registro de todos los algoritmos
from algoritmos.base import ejecutar_algoritmo, REGISTRO
from escenario.cargador import cargar_escenario
from juego.problema_navegacion import ProblemaNavegacion
from verificacion.verificador import verificar_camino

CASOS = [
    {
        "archivo": "caso01_bfs_vs_dfs.json",
        "titulo": "Caso 1: BFS vs DFS (Espacio abierto con pocos obstáculos)",
        "configuraciones": [
            ("BFS", {}),
            ("DFS", {}),
            ("UCS", {}),
            ("A_ESTRELLA", {"heuristica": "manhattan"}),
            ("A_ESTRELLA", {"heuristica": "propia"}),
            ("BEAM_SEARCH", {"k": 2, "heuristica": "manhattan"}),
        ]
    },
    {
        "archivo": "caso2_ruta_corta_vs_economica.json",
        "titulo": "Caso 2: Ruta corta vs. ruta económica (BFS vs UCS)",
        "configuraciones": [
            ("BFS", {}),
            ("DFS", {}),
            ("UCS", {}),
            ("A_ESTRELLA", {"heuristica": "manhattan"}),
            ("A_ESTRELLA", {"heuristica": "propia"}),
        ]
    },
    {
        "archivo": "caso3_obstaculo_y_heuristica.json",
        "titulo": "Caso 3: Obstáculo y guía heurística (UCS vs A*)",
        "configuraciones": [
            ("BFS", {}),
            ("UCS", {}),
            ("A_ESTRELLA", {"heuristica": "manhattan"}),
            ("A_ESTRELLA", {"heuristica": "propia"}),
        ]
    },
    {
        "archivo": "caso4_comparacion_heuristicas.json",
        "titulo": "Caso 4: Comparación de heurísticas en A* (Manhattan vs. Propia)",
        "configuraciones": [
            ("UCS", {}),
            ("A_ESTRELLA", {"heuristica": "manhattan"}),
            ("A_ESTRELLA", {"heuristica": "propia"}),
        ]
    },
    {
        "archivo": "caso05_beam_search.json",
        "titulo": "Caso 5: Búsqueda con memoria limitada (Beam Search variando k)",
        "configuraciones": [
            ("BFS", {}),
            ("A_ESTRELLA", {"heuristica": "manhattan"}),
            ("BEAM_SEARCH", {"k": 1, "heuristica": "manhattan"}),
            ("BEAM_SEARCH", {"k": 2, "heuristica": "manhattan"}),
            ("BEAM_SEARCH", {"k": 4, "heuristica": "manhattan"}),
            ("BEAM_SEARCH", {"k": 8, "heuristica": "manhattan"}),
        ]
    }
]


def ejecutar_caso(caso_info):
    ruta_archivo = os.path.join(BASE_DIR, "escenarios", "casos minimos", caso_info["archivo"])
    if not os.path.exists(ruta_archivo):
        print(f"Error: No se encontró {ruta_archivo}")
        return []

    escenario = cargar_escenario(ruta_archivo)
    prueba = escenario.prueba or {}
    uid_inicio = prueba.get("unidad_inicio", "A1")
    unidad_ini = next((u for u in escenario.unidades if u.id == uid_inicio), escenario.unidades[0])
    inicio = (unidad_ini.fila, unidad_ini.columna)
    
    obj_dict = prueba.get("objetivo")
    if obj_dict:
        objetivo = (obj_dict["fila"], obj_dict["columna"])
    else:
        objetivo = escenario.recurso

    problema = ProblemaNavegacion(escenario.mapa, inicio, objetivo)

    filas = []
    for algo_nombre, params in caso_info["configuraciones"]:
        # Repetir varias veces para medir tiempo promedio más representativo
        iteraciones = 5
        tiempos = []
        res = None
        for _ in range(iteraciones):
            r = ejecutar_algoritmo(algo_nombre, problema, **params)
            tiempos.append(r.tiempo_ms)
            res = r
        tiempo_prom_ms = sum(tiempos) / len(tiempos)

        # Verificación del camino
        checks = verificar_camino(escenario.mapa, inicio, objetivo, res)
        todo_ok = all(ok for _, ok, _ in checks)

        # Etiqueta legible
        etiqueta = algo_nombre
        if algo_nombre == "A_ESTRELLA":
            etiqueta = f"A* ({params.get('heuristica', 'manhattan')})"
        elif algo_nombre == "BEAM_SEARCH":
            etiqueta = f"Beam (k={params.get('k', 2)})"

        filas.append({
            "algoritmo": etiqueta,
            "exito": "Sí" if res.exito else "No",
            "longitud": res.longitud if res.longitud is not None else "—",
            "costo": f"{res.costo:.1f}" if res.costo is not None else "—",
            "generados": res.estados_generados,
            "expandidos": res.estados_expandidos,
            "max_frontera": res.maximo_frontera,
            "tiempo_ms": f"{tiempo_prom_ms:.3f}",
            "verificado": "OK" if todo_ok else "FALLO"
        })
    return filas


def formatear_tabla(filas):
    header = "| Algoritmo / Config | Éxito | Longitud | Costo | Generados | Expandidos | Máx Frontera | Tiempo (ms) | Verif. |"
    sep =    "|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|"
    lineas = [header, sep]
    for f in filas:
        lineas.append(
            f"| {f['algoritmo']} | {f['exito']} | {f['longitud']} | {f['costo']} | "
            f"{f['generados']} | {f['expandidos']} | {f['max_frontera']} | {f['tiempo_ms']} | {f['verificado']} |"
        )
    return "\n".join(lineas)


def main():
    print("=" * 80)
    print("EJECUCIÓN DE EXPERIMENTOS DE BÚSQUEDA - TACTICALGRID")
    print("=" * 80)

    reporte_markdown = []
    reporte_markdown.append("# Resultados Experimentales de Algoritmos de Búsqueda\n")
    reporte_markdown.append("Métricas recolectadas automáticamente en los escenarios mínimos de prueba.\n")

    for caso in CASOS:
        print(f"\n>>> Procesando {caso['titulo']}...")
        filas = ejecutar_caso(caso)
        if filas:
            tabla = formatear_tabla(filas)
            print(tabla)
            reporte_markdown.append(f"### {caso['titulo']}\n")
            reporte_markdown.append(f"* **Archivo:** `{caso['archivo']}`\n")
            reporte_markdown.append(tabla + "\n")

    # Guardar reporte en documentacion
    ruta_salida = os.path.join(BASE_DIR, "documentacion", "resultados_experimentos_busqueda.md")
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write("\n".join(reporte_markdown))

    print(f"\n[OK] Resultados guardados exitosamente en:\n  {ruta_salida}")


if __name__ == "__main__":
    main()
