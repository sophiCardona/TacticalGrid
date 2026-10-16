"""Gráfica de barras sencilla sobre un Canvas (sin dependencias externas)."""
from interfaz.tablero import TEXTO, TEXTO_SUAVE, aclarar

COLORES = ["#4f9cf9", "#f5a524", "#38c98d", "#a78bfa", "#f472b6", "#94a3b8"]
REJILLA = "#232c42"


def _fmt(v):
    return f"{round(v, 2):g}" if isinstance(v, float) else str(v)


def _rect(canvas, x0, y0, x1, y1, **kw):
    """Rectángulo de barra (esquinas rectas: en Tk/Windows los polígonos suavizados
    no rellenan de forma fiable)."""
    return canvas.create_rectangle(x0, y0, x1, y1, **kw)


def barras(canvas, datos, titulo=""):
    """datos: lista de (etiqueta, valor numérico o None)."""
    canvas.delete("all")
    w, h = canvas.winfo_width(), canvas.winfo_height()
    if w < 40 or h < 60:
        return
    canvas.create_text(w / 2, 10, text=titulo, font=("Segoe UI", 9, "bold"), fill=TEXTO)
    datos = [(e, v) for e, v in datos if v is not None]
    if not datos:
        canvas.create_text(w / 2, h / 2, text="Sin datos todavía", fill=TEXTO_SUAVE,
                           font=("Segoe UI", 9))
        return
    vmax = max(v for _, v in datos) or 1
    margen, base, techo = 24, h - 26, 38 if h >= 160 else 32
    lineas = 4 if (base - techo) >= 90 else 2
    for i in range(lineas):  # rejilla de referencia (2 líneas si el canvas es bajo)
        y = base - (base - techo) * i / (lineas - 1)
        canvas.create_line(margen, y, w - margen, y, fill=REJILLA, dash=(3, 4))
        canvas.create_text(margen - 4, y, text=_fmt(vmax * i / (lineas - 1)), anchor="e",
                           font=("Segoe UI", 7), fill=TEXTO_SUAVE)
    ancho = (w - 2 * margen) / len(datos)
    for i, (et, v) in enumerate(datos):
        x0, x1 = margen + i * ancho + ancho * 0.18, margen + (i + 1) * ancho - ancho * 0.18
        y0 = base - (v / vmax) * (base - techo)
        color = COLORES[i % len(COLORES)]
        _rect(canvas, x0, min(y0, base - 3), x1, base, fill=color, outline="")
        canvas.create_rectangle(x0, y0, x1, y0 + 4, fill=aclarar(color, 0.35), outline="")
        canvas.create_text((x0 + x1) / 2, y0 - 8, text=_fmt(v), font=("Segoe UI", 8, "bold"), fill=TEXTO)
        canvas.create_text((x0 + x1) / 2, base + 12, text=et, font=("Segoe UI", 8), fill=TEXTO_SUAVE)
