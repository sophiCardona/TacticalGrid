"""Validación COMPLETA de un escenario JSON (ya convertido a dict)."""

OBLIGATORIOS = ("version", "mapa", "tipos_terreno", "terreno", "bases", "recurso",
                "unidades", "turno", "juego")


def _es_entero(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _es_numero(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validar_datos(d):
    """Purpose: revisar todas las reglas del enunciado y devolver TODOS los errores.
    Preconditions: ninguna (acepta cualquier objeto; si no es dict, reporta error).
    Postconditions: lista vacía si el escenario es válido. No modifica `d`.
    Complexity: O(filas*columnas + unidades).
    AI usage: Yes. AI intervention: generó la estructura y las reglas de validación.
    Student validation: Se han aprobado las reglas de validacion."""
    e = []
    if not isinstance(d, dict):
        return ["El archivo debe contener un objeto JSON en la raíz."]
    faltan = [k for k in OBLIGATORIOS if k not in d]
    if faltan:
        return [f"Faltan campos obligatorios: {', '.join(faltan)}."]

    # --- mapa y dimensiones ---
    m = d["mapa"]
    filas = m.get("filas") if isinstance(m, dict) else None
    cols = m.get("columnas") if isinstance(m, dict) else None
    dims_ok = _es_entero(filas) and _es_entero(cols) and filas > 0 and cols > 0
    if not dims_ok:
        e.append("mapa.filas y mapa.columnas deben ser enteros positivos.")

    # --- catálogo de terrenos ---
    tipos = d["tipos_terreno"]
    if not isinstance(tipos, dict) or not tipos:
        e.append("tipos_terreno debe ser un objeto no vacío.")
        tipos = {}
    for nombre, t in tipos.items():
        if not isinstance(t, dict) or not isinstance(t.get("transitable"), bool):
            e.append(f"Terreno '{nombre}': 'transitable' debe ser true/false.")
        elif t["transitable"] and not (_es_numero(t.get("costo")) and t["costo"] > 0):
            e.append(f"Terreno '{nombre}': un terreno transitable necesita costo positivo.")
    if tipos and not any(isinstance(t, dict) and t.get("transitable") is True for t in tipos.values()):
        e.append("Debe existir al menos un terreno transitable.")

    # --- matriz ---
    mat = d["terreno"]
    if not isinstance(mat, list):
        e.append("terreno debe ser una matriz (lista de listas).")
        mat = []
    elif dims_ok:
        if len(mat) != filas:
            e.append(f"terreno tiene {len(mat)} filas pero mapa.filas es {filas}.")
        for i, fila in enumerate(mat):
            if not isinstance(fila, list) or len(fila) != cols:
                e.append(f"terreno fila {i}: debe tener {cols} columnas.")
                continue
            for j, nombre in enumerate(fila):
                if nombre not in tipos:
                    e.append(f"terreno[{i}][{j}]: tipo '{nombre}' no existe en tipos_terreno.")

    def pos_ok(p):
        return isinstance(p, dict) and _es_entero(p.get("fila")) and _es_entero(p.get("columna"))

    def dentro(p):
        return dims_ok and 0 <= p["fila"] < filas and 0 <= p["columna"] < cols

    def transitable(p):
        try:
            return tipos[mat[p["fila"]][p["columna"]]]["transitable"] is True
        except (KeyError, IndexError, TypeError):
            return True  # el error de terreno ya se reportó arriba

    # --- bases y recurso ---
    bases = d["bases"]
    for b in ("A", "B"):
        p = bases.get(b) if isinstance(bases, dict) else None
        if not pos_ok(p):
            e.append(f"bases.{b} debe tener 'fila' y 'columna' enteras.")
        elif not dentro(p):
            e.append(f"bases.{b} está fuera del mapa.")
    if not pos_ok(d["recurso"]):
        e.append("recurso debe tener 'fila' y 'columna' enteras.")
    elif not dentro(d["recurso"]):
        e.append("recurso está fuera del mapa.")

    # --- unidades ---
    ids = set()
    unidades = d["unidades"]
    if not isinstance(unidades, list) or not unidades:
        e.append("unidades debe ser una lista no vacía.")
        unidades = []
    for u in unidades:
        if not isinstance(u, dict) or "id" not in u:
            e.append("Cada unidad debe ser un objeto con 'id'.")
            continue
        uid = u["id"]
        if uid in ids:
            e.append(f"Identificador de unidad repetido: '{uid}'.")
        ids.add(uid)
        if str(u.get("bando", "")).upper() not in ("A", "B"):
            e.append(f"Unidad '{uid}': bando debe ser A o B.")
        if not pos_ok(u):
            e.append(f"Unidad '{uid}': posición inválida.")
        elif not dentro(u):
            e.append(f"Unidad '{uid}': fuera del mapa.")
        elif not transitable(u):
            e.append(f"Unidad '{uid}': está sobre una celda no transitable.")

    # --- turno y portador ---
    if str(d["turno"]).upper() not in ("A", "B"):
        e.append("turno debe ser A o B.")
    juego = d["juego"]
    if not isinstance(juego, dict) or "portador_recurso" not in juego:
        e.append("juego.portador_recurso es obligatorio (puede ser null).")
    elif juego["portador_recurso"] is not None and juego["portador_recurso"] not in ids:
        e.append(f"juego.portador_recurso '{juego['portador_recurso']}' no es una unidad existente.")
    return e
