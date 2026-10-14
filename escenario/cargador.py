"""Lectura de archivos JSON: valida primero, construye después (todo o nada)."""
import json

from escenario.mapa import Mapa
from escenario.modelos import Escenario
from escenario.validador import validar_datos
from juego.estado import Unidad

PROFUNDIDAD_POR_DEFECTO = 3


class ErrorEscenario(Exception):
    """Escenario inválido; `errores` contiene la lista completa de problemas."""
    def __init__(self, errores):
        self.errores = errores
        super().__init__("Escenario inválido:\n- " + "\n- ".join(errores))


def construir_escenario(datos):
    """Purpose: convertir un dict JSON en un Escenario interno.
    Preconditions: ninguna.
    Postconditions: devuelve Escenario completo o lanza ErrorEscenario sin devolver nada parcial.
    Complexity: O(filas*columnas + unidades).
    AI usage: Yes. AI intervention: generó la estructura; la conversión de campos fue revisada.
    Student validation: (completar)."""
    errores = validar_datos(datos)
    if errores:
        raise ErrorEscenario(errores)
    tipos = {n: {"transitable": t["transitable"], "costo": t.get("costo")}
             for n, t in datos["tipos_terreno"].items()}
    mapa = Mapa(datos["mapa"]["filas"], datos["mapa"]["columnas"],
                tuple(tuple(fila) for fila in datos["terreno"]), tipos)
    pos = lambda p: (p["fila"], p["columna"])
    unidades = tuple(Unidad(u["id"], str(u["bando"]).upper(), u["fila"], u["columna"])
                     for u in datos["unidades"])
    juego = datos["juego"]
    return Escenario(
        mapa=mapa,
        bases={"A": pos(datos["bases"]["A"]), "B": pos(datos["bases"]["B"])},
        recurso=pos(datos["recurso"]),
        unidades=unidades,
        turno=str(datos["turno"]).upper(),
        portador=juego["portador_recurso"],
        profundidad_minimax=juego.get("profundidad_maxima_minimax", PROFUNDIDAD_POR_DEFECTO),
        prueba=datos.get("prueba"),
    )


def cargar_escenario(ruta):
    """Purpose: leer un archivo JSON y devolver un Escenario válido.
    Preconditions: `ruta` apunta a un archivo legible.
    Postconditions: Escenario válido, o ErrorEscenario con mensaje claro (JSON mal formado incluido).
    Complexity: O(tamaño del archivo).
    AI usage: Yes. AI intervention: estructura del método.
    Student validation: (completar)."""
    try:
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
    except json.JSONDecodeError as ex:
        raise ErrorEscenario([f"JSON mal formado: {ex}"])
    except OSError as ex:
        raise ErrorEscenario([f"No se pudo leer el archivo: {ex}"])
    return construir_escenario(datos)
