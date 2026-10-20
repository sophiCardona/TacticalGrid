# TacticalGrid

Integrantes:
- Sophia Cardona
- Danna Alexandra Madrid Roa
- Michel Dahiana Arenas López

## Documentación
- [Manual de Usuario](documentacion/manual_de_usuario.md)
- [Manual Técnico](documentacion/manual_tecnico.md)

## Ejecutar
```bash
python main.py                 # Abre la interfaz gráfica
python -m unittest discover -s tests -p "test_*.py" -v  # Pruebas unitarias
```

Requiere Python 3.9+ con tkinter (Windows y macOS ya lo incluyen; en Ubuntu/Debian: `sudo apt install python3-tk`).

## Modos de la interfaz
- **Modo JSON:** Ejecuta estrictamente lo que indica el campo `prueba` del archivo JSON (búsqueda, partida, adversarial).
- **Modo Exploración:** Permite interactuar libremente seleccionando tarea, algoritmo, heurística, unidad de inicio y objetivo mediante clics en el tablero.

