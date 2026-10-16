# TacticalGrid

Integrantes: (completar con los nombres del equipo)

## Ejecutar
    python3 main.py          # abre la interfaz
    python3 tests/test_paso1_2.py   # pruebas de carga, validación y reglas

Requiere Python 3.9+ con tkinter (Windows y macOS ya lo incluyen; en Ubuntu/Debian: `sudo apt install python3-tk`).

## Modos de la interfaz
- Modo JSON: ejecuta lo que diga el campo `prueba` del archivo (busqueda, partida, adversarial).
- Modo exploración: se elige libremente tarea, algoritmo, unidad y objetivo.

Campos opcionales propios dentro de `prueba` (el enunciado permite campos extra): `algoritmo`, `heuristica`, `k`.
