"""Búsqueda adversarial Minimax y poda alfa-beta para TacticalGrid.

La utilidad se calcula desde la perspectiva del bando que inicia la evaluación.
La profundidad cuenta acciones individuales (plies), no rondas completas.
"""
from dataclasses import dataclass
import time


@dataclass
class ResultadoAdversarial:
    algoritmo: str
    accion: object
    valor: float
    profundidad_maxima: int
    nodos_generados: int
    nodos_evaluados: int
    nodos_podados: int
    tiempo_ms: float
    orden_acciones: str

    def a_dict(self):
        return {
            "algoritmo": self.algoritmo,
            "accion": None if self.accion is None else {
                "unidad_id": self.accion.unidad_id,
                "tipo": self.accion.tipo,
                "destino": self.accion.destino,
            },
            "valor": self.valor,
            "profundidad_maxima": self.profundidad_maxima,
            "nodos_generados": self.nodos_generados,
            "nodos_evaluados": self.nodos_evaluados,
            "nodos_podados": self.nodos_podados,
            "tiempo_ms": round(self.tiempo_ms, 4),
            "orden_acciones": self.orden_acciones,
        }


def _distancia(a, b):
    if a is None or b is None:
        return 0
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _utilidad(estado, reglas, escenario, perspectiva):
    """Evalúa material, posesión y distancias; valores terminales dominan heurística."""
    ganador = reglas.ganador(estado)
    if ganador is not None:
        return 100000.0 if ganador == perspectiva else -100000.0
    rival = "B" if perspectiva == "A" else "A"
    propios, enemigos = estado.unidades_de(perspectiva), estado.unidades_de(rival)
    valor = 35.0 * (len(propios) - len(enemigos))
    portador = estado.unidad(estado.portador) if estado.portador else None
    if portador:
        pos = (portador.fila, portador.columna)
        if portador.bando == perspectiva:
            valor += 180.0 - 8.0 * _distancia(pos, escenario.bases[perspectiva])
            # Premia la presión rival sobre el portador propio: una amenaza cercana reduce utilidad.
            dist_rival = min((_distancia(pos, (u.fila, u.columna)) for u in enemigos), default=20)
            valor -= max(0, 5 - dist_rival) * 12.0
        else:
            valor -= 180.0 - 8.0 * _distancia(pos, escenario.bases[rival])
            dist_propio = min((_distancia(pos, (u.fila, u.columna)) for u in propios), default=20)
            valor += max(0, 5 - dist_propio) * 12.0
    else:
        objetivo = estado.recurso_pos
        if objetivo is not None:
            dp = min((_distancia((u.fila, u.columna), objetivo) for u in propios), default=20)
            de = min((_distancia((u.fila, u.columna), objetivo) for u in enemigos), default=20)
            valor += 5.0 * (de - dp)
    return valor


def _clave_accion(accion):
    return (accion.unidad_id, accion.tipo, accion.destino or (-1, -1))


def _acciones_ordenadas(estado, reglas, escenario, perspectiva, orden, maximiza):
    acciones = reglas.acciones_legales(estado)
    if orden == "inverso":
        return list(reversed(acciones))
    if orden == "heuristico":
        # Ordenar por la evaluación del sucesor mejora la probabilidad de poda sin cambiar reglas.
        evaluadas = [( _utilidad(reglas.aplicar(estado, a), reglas, escenario, perspectiva), a)
                     for a in acciones]
        evaluadas.sort(key=lambda par: (par[0], _clave_accion(par[1])), reverse=maximiza)
        return [a for _, a in evaluadas]
    return acciones


def _buscar(estado, reglas, escenario, profundidad_maxima, orden_acciones, con_poda):
    if not isinstance(profundidad_maxima, int) or profundidad_maxima < 1:
        raise ValueError("La profundidad máxima debe ser un entero mayor o igual a 1.")
    if orden_acciones not in ("estandar", "inverso", "heuristico"):
        raise ValueError("orden_acciones debe ser 'estandar', 'inverso' o 'heuristico'.")
    inicio = time.perf_counter()
    perspectiva = estado.turno
    cont = {"generados": 1, "evaluados": 0, "podados": 0}

    def rec(s, profundidad, alpha, beta):
        if profundidad == 0 or reglas.es_terminal(s):
            cont["evaluados"] += 1
            return _utilidad(s, reglas, escenario, perspectiva), None
        maximiza = s.turno == perspectiva
        acciones = _acciones_ordenadas(s, reglas, escenario, perspectiva, orden_acciones, maximiza)
        if not acciones:
            cont["evaluados"] += 1
            return _utilidad(s, reglas, escenario, perspectiva), None
        mejor_accion = None
        mejor_valor = float("-inf") if maximiza else float("inf")
        for i, accion in enumerate(acciones):
            sucesor = reglas.aplicar(s, accion)
            cont["generados"] += 1
            valor, _ = rec(sucesor, profundidad - 1, alpha, beta)
            if (maximiza and valor > mejor_valor) or (not maximiza and valor < mejor_valor):
                mejor_valor, mejor_accion = valor, accion
            if con_poda:
                if maximiza:
                    alpha = max(alpha, mejor_valor)
                else:
                    beta = min(beta, mejor_valor)
                if alpha >= beta:
                    cont["podados"] += len(acciones) - i - 1
                    break
        return mejor_valor, mejor_accion

    valor, accion = rec(estado, profundidad_maxima, float("-inf"), float("inf"))
    ms = (time.perf_counter() - inicio) * 1000.0
    return ResultadoAdversarial(
        "ALFA_BETA" if con_poda else "MINIMAX", accion, valor, profundidad_maxima,
        cont["generados"], cont["evaluados"], cont["podados"], ms, orden_acciones)


def minimax(estado, reglas, escenario, profundidad_maxima=3, orden_acciones="estandar"):
    """Purpose: hallar la mejor acción suponiendo respuesta óptima del rival.
    Preconditions: estado válido y reglas/escenario compatibles.
    Postconditions: resultado con acción, utilidad y métricas reproducibles.
    Complexity: temporal O(b^d), espacial O(d) por la recursión (b: ramificación, d: profundidad).
    AI usage: Yes. AI intervention: implementación inicial del algoritmo.
    Student validation: comparar valor/acción con alfa_beta y pruebas de regresión."""
    return _buscar(estado, reglas, escenario, profundidad_maxima, orden_acciones, False)


def alfa_beta(estado, reglas, escenario, profundidad_maxima=3, orden_acciones="estandar"):
    """Purpose: calcular la decisión Minimax evitando ramas con límites alfa/beta.
    Preconditions: las mismas de minimax.
    Postconditions: mismo valor óptimo que Minimax con profundidad y utilidad iguales.
    Complexity: temporal O(b^d) peor caso y hasta O(b^(d/2)) con orden ideal; espacial O(d).
    AI usage: Yes. AI intervention: implementación inicial de la poda alfa-beta.
    Student validation: comprobar equivalencia con Minimax y medir nodos para varios órdenes."""
    return _buscar(estado, reglas, escenario, profundidad_maxima, orden_acciones, True)
