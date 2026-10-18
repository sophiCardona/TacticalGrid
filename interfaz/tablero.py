"""Widget de tablero: SOLO dibuja lo que le dicen. No contiene lógica de juego ni de búsqueda."""
import tkinter as tk

# ------------------------------------------------------------------ paleta (tema oscuro inmersivo)
FONDO = "#0a0e16"        # fondo profundo del canvas (márgenes del tablero)
MARCOS = "#26304a"       # borde de paneles y marco del tablero
PANEL = "#141b2c"        # superficie de fichas de leyenda y paneles
TEXTO = "#e7edf8"
TEXTO_SUAVE = "#94a3bd"
ORO = "#f5c542"
RUTA = "#ff5fa2"
EXPLORADO = "#4fa8ff"
INICIO = "#3ddc97"
OBJETIVO = "#ff9f43"
RECURSO = "#ffd54a"
COLOR_BANDO = {"A": "#2f6fd0", "B": "#e2574c"}
FUENTE = "Segoe UI"


def _rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in rgb)


def mezclar(c1, c2, k):
    """k=0 -> c1; k=1 -> c2."""
    a, b = _rgb(c1), _rgb(c2)
    return _hex(tuple(a[i] + (b[i] - a[i]) * k for i in range(3)))


def aclarar(c, k):
    return mezclar(c, "#ffffff", k)


def oscurecer(c, k):
    return mezclar(c, "#000000", k)


def contraste(hex_color):
    """Color de texto legible sobre un fondo dado (para etiquetas de leyenda, costos, etc.)."""
    r, g, b = _rgb(hex_color)
    return "#0d1220" if 0.299 * r + 0.587 * g + 0.114 * b > 140 else "#f2f6ff"


COLORES_TERRENO = {"pasto": "#a9e159", "camino": "#66c00b", "bosque": "#419f00"}


def colores_terreno(mapa):
    """Un color por tipo de terreno: paleta fija para pasto/camino/bosque; el resto se
    deriva del COSTO del JSON (verde vivo = barato, tierra cálida = caro, pizarra = obstáculo)."""
    costos = [t["costo"] for t in mapa.tipos.values() if t["transitable"]]
    cmin, cmax = min(costos), max(costos)
    a, b = (111, 178, 105), (176, 120, 74)
    res = {}
    for nombre, t in mapa.tipos.items():
        if not t["transitable"]:
            res[nombre] = "#333c52"
        elif nombre in COLORES_TERRENO:
            res[nombre] = COLORES_TERRENO[nombre]
        else:
            k = 0.0 if cmax == cmin else (t["costo"] - cmin) / (cmax - cmin)
            res[nombre] = _hex(tuple(a[i] + (b[i] - a[i]) * k for i in range(3)))
    return res


def fmt_num(v):
    return f"{v:g}" if isinstance(v, float) else str(v)


class Tablero(tk.Canvas):
    def __init__(self, master, al_clic, al_hover=None):
        super().__init__(master, bg=FONDO, highlightthickness=1, highlightbackground=MARCOS,
                         width=560, height=560, bd=0, cursor="hand2")
        self.al_clic, self.al_hover = al_clic, al_hover
        self.vista, self._geom, self._hover = None, None, None
        self.bind("<Configure>", lambda e: self.redibujar())
        self.bind("<Button-1>", self._clic)
        self.bind("<Motion>", self._movimiento)
        self.bind("<Leave>", lambda e: self._poner_hover(None))

    def mostrar(self, escenario, estado, **capas):
        """capas opcionales: camino, explorados, inicio, objetivo, seleccion, destinos, turno_marcador."""
        self.vista = (escenario, estado, capas)
        self.redibujar()

    def limpiar(self):
        self.vista, self._hover = None, None
        self.delete("all")

    # ------------------------------------------------------------------ geometría y utilidades de dibujo
    def _rect(self, f, c, inset=0):
        ox, oy, t = self._geom[:3]
        return (ox + c * t + inset, oy + f * t + inset, ox + (c + 1) * t - inset, oy + (f + 1) * t - inset)

    def _centro(self, f, c):
        x0, y0, x1, y1 = self._rect(f, c)
        return (x0 + x1) / 2, (y0 + y1) / 2

    def _esquina(self, x0, y0, x1, y1, r, **kw):
        """Rectángulo de celda/panel. Se usan esquinas rectas a propósito: en Tk 8.6
        (Windows) los polígonos suavizados creados en el tablero no rellenan de forma fiable,
        mientras que create_rectangle/oval sí lo hacen."""
        return self.create_rectangle(x0, y0, x1, y1, **kw)

    def _corchetes(self, f, c, color, grosor=3):
        """Cuatro escuadras de esquina (marcas de inicio/objetivo)."""
        x0, y0, x1, y1 = self._rect(f, c, 3)
        L = max(6, (x1 - x0) * 0.3)
        for pts in (((x0, y0 + L), (x0, y0), (x0 + L, y0)),
                    ((x1 - L, y0), (x1, y0), (x1, y0 + L)),
                    ((x1, y1 - L), (x1, y1), (x1 - L, y1)),
                    ((x0 + L, y1), (x0, y1), (x0, y1 - L))):
            self.create_line(*pts, fill=color, width=grosor, capstyle="round", joinstyle="round")

    def _placa(self, x_cx, y_base, texto, color, fs):
        """Placa oscura con texto de color (etiquetas tipo videojuego), medida con bbox."""
        tid = self.create_text(x_cx, y_base - 2, text=texto, anchor="s",
                               font=(FUENTE, fs, "bold"), fill=color)
        bx0, by0, bx1, by1 = self.bbox(tid)
        self.delete(tid)
        self._esquina(bx0 - 6, by0 - 5, bx1 + 6, by1 + 5, 3, fill="#0d1220", outline=color, width=1)
        self.create_text(x_cx, y_base - 2, text=texto, anchor="s",
                         font=(FUENTE, fs, "bold"), fill=color)

    # ------------------------------------------------------------------ dibujo principal
    def redibujar(self):
        self.delete("all")
        if not self.vista:
            return
        esc, est, capas = self.vista
        m = esc.mapa
        w, h = max(self.winfo_width(), 50), max(self.winfo_height(), 50)
        t = max(10, min(w // m.columnas, h // m.filas, 96))
        self._geom = ((w - t * m.columnas) // 2, (h - t * m.filas) // 2, t, m.filas, m.columnas)
        ox, oy = self._geom[:2]
        colores = colores_terreno(m)
        fs = max(7, t // 6)
        bases = {pos: b for b, pos in esc.bases.items()}

        # sombra del tablero y celdas
        self.create_rectangle(ox + 5, oy + 6, ox + t * m.columnas + 5, oy + t * m.filas + 6,
                              fill="#000000", outline="")
        for f in range(m.filas):
            for c in range(m.columnas):
                nombre = m.terreno[f][c]
                tipo = m.tipos[nombre]
                color = colores[nombre]
                x0, y0, x1, y1 = self._rect(f, c)
                self._esquina(x0, y0, x1, y1, max(1.0, t * 0.08), fill=color, outline="#1a2135", width=1)
                if t >= 16:  # bisel: luz arriba, sombra abajo
                    self.create_line(x0 + 2, y0 + 1, x1 - 2, y0 + 1, fill=aclarar(color, 0.18), width=1)
                    self.create_line(x0 + 2, y1 - 1, x1 - 2, y1 - 1, fill=oscurecer(color, 0.22), width=1)
                if not tipo["transitable"]:  # obstáculo: rayado diagonal
                    paso = max(6, t // 3)
                    d = int(x1 - x0)
                    for k in range(-d, d, paso):
                        self.create_line(x0 + max(0, k), y0 + max(0, -k),
                                         x0 + min(d, k + d), y0 + min(d, d - k),
                                         fill="#55618a", width=1)
                    if t >= 30:
                        self.create_text((x0 + x1) / 2, (y0 + y1) / 2, text="✕",
                                         font=(FUENTE, max(8, t // 3), "bold"), fill="#8792ad")
                elif t >= 26:  # costo del terreno en la esquina inferior derecha
                    self.create_text(x1 - 3, y1 - 3, text=fmt_num(tipo["costo"]), anchor="se",
                                     font=(FUENTE, fs), fill=contraste(color))

        # marco del tablero
        self._esquina(ox - 2, oy - 2, ox + t * m.columnas + 2, oy + t * m.filas + 2, 6,
                      outline=MARCOS, width=2)

        # reglas de coordenadas (fila/columna)
        if oy >= 14 and t >= 12:
            fsr = max(7, min(10, t // 3))
            for c in range(m.columnas):
                self.create_text(ox + c * t + t / 2, oy - 5, text=str(c), anchor="s",
                                 font=(FUENTE, fsr), fill=TEXTO_SUAVE)
        if ox >= 16 and t >= 12:
            fsr = max(7, min(10, t // 3))
            for f in range(m.filas):
                self.create_text(ox - 5, oy + f * t + t / 2, text=str(f), anchor="e",
                                 font=(FUENTE, fsr), fill=TEXTO_SUAVE)

        # bases: placas con bandera del bando
        for (f, c), bando in bases.items():
            col = COLOR_BANDO[bando]
            x0, y0, x1, y1 = self._rect(f, c, 2)
            self._esquina(x0, y0, x1, y1, 4, outline=col, width=3)
            px, py = x0 + 7, y0 + 6
            alto = max(7, t * 0.42)
            self.create_line(px, py, px, py + alto, fill="#e7edf8", width=2)
            self.create_polygon(px, py, px, py + max(6, t * 0.16), px + max(7, t * 0.2),
                                py + max(3, t * 0.08), fill=col, outline="")
            if t >= 40:
                cx, _ = self._centro(f, c)
                self._placa(cx, y1 - 2, f"BASE {bando}", col, max(7, t // 6))

        # capa: estados explorados (puntos azules)
        for (f, c) in (capas.get("explorados") or []):
            cx, cy = self._centro(f, c)
            r = max(2, t * 0.12)
            self.create_oval(cx - r, cy - r, cx + r, cy + r, fill=EXPLORADO, outline="#0d1220", width=1)
            r2 = r * 0.45
            self.create_oval(cx - r2, cy - r2, cx + r2, cy + r2, fill="#cfe6ff", outline="")

        # capa: destinos posibles (celdas con borde punteado)
        for (f, c) in (capas.get("destinos") or []):
            x0, y0, x1, y1 = self._rect(f, c, 4)
            self._esquina(x0, y0, x1, y1, 3, outline="#7dd3fc", width=2, dash=(4, 3))
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            r = max(2, t * 0.06)
            self.create_polygon(cx, cy - r, cx + r, cy, cx, cy + r, cx - r, cy,
                                fill="#7dd3fc", outline="")

        # capa: camino (brillo + trazo + flechas de dirección + nodos)
        camino = capas.get("camino")
        if camino and len(camino) > 1:
            pts = [v for p in camino for v in self._centro(*p)]
            grosor = max(3, t // 9)
            self.create_line(*pts, width=grosor + 6, fill="#6e2148", capstyle="round", joinstyle="round")
            self.create_line(*pts, width=grosor, fill=RUTA, capstyle="round", joinstyle="round")
            for (f, c) in camino[1:-1]:
                cx, cy = self._centro(f, c)
                r = max(2, grosor)
                self.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#ffd9ea", outline=RUTA, width=1)
            s = max(3, t * 0.1)
            for (f1, c1), (f2, c2) in zip(camino, camino[1:]):
                xa, ya = self._centro(f1, c1)
                xb, yb = self._centro(f2, c2)
                dx, dy = xb - xa, yb - ya
                n = (dx * dx + dy * dy) ** 0.5
                if n < 10:
                    continue
                ux, uy = dx / n, dy / n
                px, py = -uy, ux
                mx, my = (xa + xb) / 2, (ya + yb) / 2
                self.create_polygon(mx + ux * s, my + uy * s,
                                    mx - ux * s * 0.5 + px * s * 0.8, my - uy * s * 0.5 + py * s * 0.8,
                                    mx - ux * s * 0.5 - px * s * 0.8, my - uy * s * 0.5 - py * s * 0.8,
                                    fill="#ffd9ea", outline="")

        # capa: inicio y objetivo de la búsqueda
        if capas.get("inicio"):
            self._corchetes(*capas["inicio"], INICIO)
        if capas.get("objetivo"):
            f, c = capas["objetivo"]
            self._corchetes(f, c, OBJETIVO)
            x0, y0, x1, y1 = self._rect(f, c, 6)
            self.create_line(x0, y0, x1, y1, fill=OBJETIVO, width=2)
            self.create_line(x0, y1, x1, y0, fill=OBJETIVO, width=2)

        # recurso suelto en el mapa
        if est.recurso_pos is not None:
            cx, cy = self._centro(*est.recurso_pos)
            r = t * 0.24
            self.create_oval(cx - r * 1.7, cy - r * 1.7, cx + r * 1.7, cy + r * 1.7,
                             outline="#8a6b12", width=2)
            self.create_polygon(cx, cy - r, cx + r, cy, cx, cy + r, cx - r, cy,
                                fill=RECURSO, outline="#9a7b12", width=2)
            r2 = r * 0.45
            self.create_polygon(cx, cy - r2, cx + r2, cy, cx, cy + r2, cx - r2, cy,
                                fill="#fff3b8", outline="")

        # unidades: fichas con sombra, brillo, aro de selección y distintivo de portador
        for u in est.unidades:
            cx, cy = self._centro(u.fila, u.columna)
            r = t * 0.32
            col = COLOR_BANDO[u.bando]
            sel = capas.get("seleccion") == u.id
            self.create_oval(cx - r + 2, cy - r + 3, cx + r + 2, cy + r + 3, fill="#000000", outline="")
            self.create_oval(cx - r, cy - r, cx + r, cy + r, fill=col, outline="#0d1220", width=2)
            self.create_oval(cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7,
                             outline=aclarar(col, 0.35), width=1)
            br = r * 0.2
            self.create_oval(cx - r * 0.42 - br, cy - r * 0.45 - br, cx - r * 0.42 + br, cy - r * 0.45 + br,
                             fill="#ffffff", outline="")
            if sel:
                self.create_oval(cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4, outline=ORO, width=3)
                self.create_oval(cx - r - 9, cy - r - 9, cx + r + 9, cy + r + 9,
                                 outline="#ffffff", width=1, dash=(3, 3))
            if capas.get("turno_marcador") and u.bando == est.turno:
                s = max(4, t * 0.13)
                y = cy - r - (8 if sel else 4)
                self.create_polygon(cx, y - s, cx - s * 0.8, y + s * 0.6, cx + s * 0.8, y + s * 0.6,
                                    fill=ORO, outline="#0d1220")
            fu = max(8, int(t * 0.32))
            self.create_text(cx + 1, cy + 1, text=u.id, fill="#000000", font=(FUENTE, fu, "bold"))
            self.create_text(cx, cy, text=u.id, fill="#ffffff", font=(FUENTE, fu, "bold"))
            if est.portador == u.id:
                d = t * 0.14
                px, py = cx + r * 0.85, cy - r * 0.85
                self.create_polygon(px, py - d, px + d, py, px, py + d, px - d, py,
                                    fill=RECURSO, outline="#9a7b12", width=2)

        self._dibujar_hover()

    # ------------------------------------------------------------------ resaltado bajo el cursor
    def _dibujar_hover(self):
        self.delete("hover")
        if not (self._hover and self._geom):
            return
        f, c = self._hover
        x0, y0, x1, y1 = self._rect(f, c, 2)
        self._esquina(x0, y0, x1, y1, 4, outline="#ffffff", width=2, tags=("hover",))

    def _poner_hover(self, celda):
        if celda == self._hover:
            return
        self._hover = celda
        self._dibujar_hover()
        if self.al_hover:
            self.al_hover(*celda) if celda else self.al_hover(None, None)

    def _celda_en(self, ev):
        if not self._geom:
            return None
        ox, oy, t, filas, cols = self._geom
        c, f = (ev.x - ox) // t, (ev.y - oy) // t
        if 0 <= f < filas and 0 <= c < cols:
            return int(f), int(c)
        return None

    def _movimiento(self, ev):
        self._poner_hover(self._celda_en(ev))

    def _clic(self, ev):
        celda = self._celda_en(ev)
        if celda:
            self.al_clic(*celda)
