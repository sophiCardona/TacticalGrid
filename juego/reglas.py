"""Reglas del juego: acciones legales, transición, costo, fin de partida.

REGLAS DETERMINISTAS (decisiones del equipo):
 R1. Un bando mueve UNA unidad por turno: 1 paso ortogonal o ESPERAR.
 R2. Dos unidades nunca comparten celda, salvo la excepción de R4.
 R3. El recurso se recoge automáticamente al pisar su celda.
 R4. Entrar a la celda del portador ENEMIGO lo intercepta: el portador es eliminado,
     el recurso cae allí y lo recoge quien interceptó.
 R5. Gana el bando cuyo portador está sobre la base de su propio bando.
     También gana un bando si el rival se queda sin unidades.
 R6. El costo de MOVER es el costo del terreno destino (JSON). ESPERAR cuesta 0.
 R7. Siempre existe ESPERAR, así que un bando nunca queda sin acciones.
"""
from escenario.mapa import DIRECCIONES
from juego.estado import Accion, Estado


class Reglas:
    def __init__(self, escenario):
        self.mapa = escenario.mapa
        self.bases = escenario.bases

    def acciones_legales(self, estado):
        """Purpose: listar acciones válidas del bando en turno, en orden determinista.
        Preconditions: estado consistente con el mapa.
        Postconditions: toda acción devuelta puede pasar a aplicar() sin generar estado inválido.
        Complexity: O(U) con U unidades (4 direcciones x búsqueda de ocupante).
        AI usage: Yes. AI intervention: generó el método a partir de las reglas R1-R7.
        Student validation: (completar)."""
        ocupadas = {(u.fila, u.columna): u for u in estado.unidades}
        acciones = []
        for u in estado.unidades_de(estado.turno):
            for _, df, dc in DIRECCIONES:
                dest = (u.fila + df, u.columna + dc)
                if not self.mapa.es_transitable(*dest):
                    continue
                ocupante = ocupadas.get(dest)
                if ocupante is None or (ocupante.id == estado.portador and ocupante.bando != u.bando):
                    acciones.append(Accion(u.id, "MOVER", dest))
            acciones.append(Accion(u.id, "ESPERAR"))
        return acciones

    def costo(self, estado, accion):
        """Purpose: costo de una acción. Preconditions: acción legal. Postconditions: >= 0.
        Complexity: O(1). AI usage: Yes. AI intervention: estructura del método.
        Student validation: (completar)."""
        return 0 if accion.tipo == "ESPERAR" else self.mapa.costo(*accion.destino)

    def aplicar(self, estado, accion):
        """Purpose: función sucesor; devuelve el nuevo Estado sin mutar el anterior.
        Preconditions: accion in acciones_legales(estado).
        Postconditions: turno alterna; recurso y portador consistentes (R3, R4); unidades ordenadas.
        Complexity: O(U).
        AI usage: Yes. AI intervention: generó el método a partir de las reglas.
        Student validation: (completar)."""
        unidades = list(estado.unidades)
        recurso_pos, portador = estado.recurso_pos, estado.portador
        if accion.tipo == "MOVER":
            dest = accion.destino
            # R4: interceptación del portador enemigo
            victima = next((u for u in unidades if (u.fila, u.columna) == dest), None)
            if victima is not None:
                unidades.remove(victima)
                recurso_pos, portador = dest, None
            # mover la unidad (Unidad es inmutable: se reemplaza)
            idx = next(i for i, u in enumerate(unidades) if u.id == accion.unidad_id)
            u = unidades[idx]
            unidades[idx] = type(u)(u.id, u.bando, dest[0], dest[1])
            # R3: recogida automática
            if portador is None and recurso_pos == dest:
                portador, recurso_pos = u.id, None
        nuevo_turno = "B" if estado.turno == "A" else "A"
        return Estado(tuple(sorted(unidades, key=lambda x: x.id)), recurso_pos, portador, nuevo_turno)

    def ganador(self, estado):
        """Purpose: devolver 'A', 'B' o None según R5.
        Preconditions: estado consistente. Postconditions: None si la partida continúa.
        Complexity: O(U). AI usage: Yes. AI intervention: estructura del método.
        Student validation: (completar)."""
        if estado.portador is not None:
            u = estado.unidad(estado.portador)
            if (u.fila, u.columna) == self.bases[u.bando]:
                return u.bando
        for bando, rival in (("A", "B"), ("B", "A")):
            if not estado.unidades_de(bando):
                return rival
        return None

    def es_terminal(self, estado):
        return self.ganador(estado) is not None
