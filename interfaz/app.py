"""Ventana principal. Orquesta: no contiene reglas del juego ni algoritmos, solo los invoca."""
import csv
import json
import os
import random
import tkinter as tk
from tkinter import filedialog, font as tkfont, messagebox, ttk

import algoritmos  # noqa: F401  (registra los algoritmos disponibles)
from algoritmos.base import PLANIFICADOS, disponibles, ejecutar_algoritmo, normalizar_nombre
from escenario.cargador import ErrorEscenario, cargar_escenario
from interfaz.graficas import barras
from interfaz.tablero import (COLOR_BANDO, FONDO, MARCOS, OBJETIVO, ORO, PANEL, RECURSO, RUTA,
                              EXPLORADO, INICIO, TEXTO, TEXTO_SUAVE, Tablero, aclarar, colores_terreno,
                              contraste, fmt_num)
from juego.problema_navegacion import ProblemaNavegacion
from juego.reglas import Reglas
from verificacion.verificador import verificar_camino

TAREAS = {"Búsqueda de ruta": "busqueda", "Partida por turnos": "partida", "Decisión adversarial": "adversarial"}
MODO_A_TAREA = {v: k for k, v in TAREAS.items()}
METRICAS = {"Estados expandidos": "estados_expandidos", "Estados generados": "estados_generados",
            "Costo": "costo", "Longitud": "longitud", "Máx. frontera": "maximo_frontera",
            "Tiempo (ms)": "tiempo_ms"}
HEURISTICAS = ("manhattan", "propia", "euclidiana")
MAX_JUGADAS_AUTO = 300
EJEMPLO = os.path.join(os.path.dirname(__file__), "..", "escenarios", "ejemplo.json")


def fmt(v):
    if v is None:
        return "—"
    if isinstance(v, bool):
        return "Sí" if v else "No"
    if isinstance(v, float):
        return f"{round(v, 3):g}"
    return str(v)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TacticalGrid — Sistemas Inteligentes I")
        self.geometry("1240x760")
        self.minsize(1000, 640)
        self._tema()
        self.escenario = self.reglas = self.estado = self.ruta_actual = None
        self.historial, self.comparacion, self.heuristica_cmp, self.capas = [], [], [], {}
        self.sel_unidad, self.auto, self.plies, self._cargando = None, False, 0, False
        self.btns_tarea = {}
        self.costos = {"A": 0, "B": 0}
        self.rng = random.Random()
        self.var_modo = tk.StringVar(value="json")
        self._construir()
        self._mostrar_frame_tarea()
        self._poner_estado("Carga un escenario JSON para empezar.")

    # ------------------------------------------------------------------ tema visual
    def _tema(self):
        """Paleta oscura tipo juego táctico. Solo apariencia: no toca datos ni reglas."""
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        familias = set(tkfont.families(self))
        self.fuente = "Segoe UI" if "Segoe UI" in familias else "Helvetica"
        f, fb = (self.fuente, 9), (self.fuente, 9, "bold")
        boton, boton_act = "#2c6bed", aclarar("#2c6bed", 0.18)
        self.style.configure(".", background=FONDO, foreground=TEXTO, font=f,
                             fieldbackground=PANEL, bordercolor=MARCOS, darkcolor=PANEL,
                             lightcolor=PANEL, troughcolor=PANEL)
        self.style.configure("TFrame", background=FONDO)
        self.style.configure("Barra.TFrame", background="#080b12")
        self.style.configure("TLabel", background=FONDO, foreground=TEXTO)
        self.style.configure("Titulo.TLabel", font=(self.fuente, 18, "bold"), foreground=ORO,
                             background="#080b12")
        self.style.configure("Sub.TLabel", font=(self.fuente, 9), foreground=TEXTO_SUAVE)
        self.style.configure("Barra.TLabel", background="#080b12", foreground=TEXTO_SUAVE,
                             font=(self.fuente, 9))
        self.style.configure("Chip.TLabel", background=PANEL, foreground=TEXTO,
                             font=(self.fuente, 9), padding=(10, 4))
        self.style.configure("Aviso.TLabel", background="#1b2740", foreground="#bcd2ff",
                             font=(self.fuente, 9), padding=(10, 8), wraplength=460, justify="left")
        self.style.configure("Turno.TLabel", background="#1b2740", foreground="#ffffff",
                             font=(self.fuente, 13, "bold"), padding=(12, 8), anchor="center")
        self.style.configure("Estado.TLabel", background="#080b12", foreground=TEXTO_SUAVE,
                             font=(self.fuente, 9), padding=(10, 5))
        self.style.configure("Seccion.TLabel", font=(self.fuente, 10, "bold"), foreground=ORO)
        self.style.configure("TButton", background=boton, foreground="#ffffff", font=fb,
                             padding=(12, 7), borderwidth=0, focusthickness=0)
        self.style.map("TButton", background=[("active", boton_act), ("pressed", boton_act),
                                              ("disabled", "#243050")],
                       foreground=[("disabled", "#6d7a94")])
        self.style.configure("Secundario.TButton", background="#243047")
        self.style.map("Secundario.TButton", background=[("active", "#31405f"), ("pressed", "#31405f"),
                                                         ("disabled", "#1c2536")],
                       foreground=[("disabled", "#6d7a94")])
        self.style.configure("Tarea.TButton", background="#1b2740", font=(self.fuente, 9, "bold"),
                             padding=(8, 10))
        self.style.map("Tarea.TButton", background=[("active", "#25344f")],
                       foreground=[("disabled", "#6d7a94")])
        self.style.configure("TareaActiva.TButton", background=ORO, foreground="#1a1200",
                             font=(self.fuente, 9, "bold"), padding=(8, 10))
        self.style.map("TareaActiva.TButton", background=[("active", aclarar(ORO, 0.15))],
                       foreground=[("disabled", "#6d7a94")])
        self.style.configure("TRadiobutton", background="#080b12", foreground=TEXTO, font=f)
        self.style.map("TRadiobutton", background=[("active", "#080b12")],
                       foreground=[("selected", ORO), ("disabled", "#6d7a94")])
        self.style.configure("TCheckbutton", background=FONDO, foreground=TEXTO)
        self.style.map("TCheckbutton", background=[("active", FONDO)],
                       foreground=[("disabled", "#6d7a94")])
        self.style.configure("TLabelframe", background=FONDO, foreground=TEXTO, bordercolor=MARCOS,
                             borderwidth=1, relief="groove")
        self.style.configure("TLabelframe.Label", background=FONDO, foreground=ORO, font=fb)
        self.style.configure("TNotebook", background=FONDO, borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#141b2c", foreground=TEXTO_SUAVE,
                             font=(self.fuente, 9, "bold"), padding=(14, 8), borderwidth=0)
        self.style.map("TNotebook.Tab", background=[("selected", FONDO), ("active", "#1d2740")],
                       foreground=[("selected", ORO), ("active", TEXTO)])
        self.style.configure("Treeview", background=PANEL, fieldbackground=PANEL, foreground=TEXTO,
                             rowheight=26, borderwidth=0, font=f)
        self.style.configure("Treeview.Heading", background="#1d2740", foreground=TEXTO, font=fb,
                             relief="flat", padding=(6, 6))
        self.style.map("Treeview", background=[("selected", "#2a3d66")], foreground=[("selected", "#ffffff")])
        self.style.map("Treeview.Heading", background=[("active", "#25344f")])
        self.style.configure("TCombobox", background=PANEL, foreground=TEXTO, fieldbackground=PANEL,
                             arrowcolor=TEXTO, bordercolor=MARCOS, lightcolor=MARCOS, darkcolor=MARCOS,
                             padding=5, font=f)
        self.style.map("TCombobox", fieldbackground=[("readonly", PANEL), ("disabled", "#1a2132")],
                       foreground=[("readonly", TEXTO), ("disabled", "#6d7a94")],
                       arrowcolor=[("disabled", "#6d7a94")])
        self.style.configure("TSpinbox", background=PANEL, foreground=TEXTO, fieldbackground=PANEL,
                             arrowcolor=TEXTO, bordercolor=MARCOS, padding=4, font=f)
        self.style.map("TSpinbox", fieldbackground=[("readonly", PANEL), ("disabled", "#1a2132")],
                       foreground=[("disabled", "#6d7a94")])
        self.style.configure("TPanedwindow", background=FONDO)
        self.style.configure("TSeparator", background=MARCOS)
        self.option_add("*TCombobox*Listbox.background", PANEL)
        self.option_add("*TCombobox*Listbox.foreground", TEXTO)
        self.option_add("*TCombobox*Listbox.selectBackground", "#2a3d66")
        self.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
        self.option_add("*TCombobox*Listbox.font", f)

    def _texto(self, parent, altura=12):
        """Caja de texto oscura con tipografía monoespaciada y colores de estado."""
        t = tk.Text(parent, height=altura, wrap="word", font=("Consolas", 9), bg=PANEL, fg=TEXTO,
                    insertbackground=TEXTO, selectbackground="#2a3d66", selectforeground="#ffffff",
                    relief="flat", highlightthickness=1, highlightbackground=MARCOS,
                    highlightcolor=MARCOS, padx=8, pady=6)
        t.tag_config("ok", foreground="#48d597")
        t.tag_config("err", foreground="#ff7b72")
        t.tag_config("h", font=(self.fuente, 9, "bold"), foreground=ORO)
        return t

    # ------------------------------------------------------------------ construcción
    def _construir(self):
        barra = ttk.Frame(self, style="Barra.TFrame", padding=(14, 8))
        barra.pack(side="top", fill="x")
        marca = ttk.Frame(barra, style="Barra.TFrame")
        marca.pack(side="left")
        ttk.Label(marca, text="TACTICALGRID", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(marca, text="Escaramuza táctica 2D por turnos · Sistemas Inteligentes I",
                  style="Barra.TLabel").pack(anchor="w")
        acciones = ttk.Frame(barra, style="Barra.TFrame")
        acciones.pack(side="right")
        ttk.Button(acciones, text="Cargar JSON…", command=self.cargar_dialogo).pack(side="left")
        ttk.Button(acciones, text="Cargar ejemplo", style="Secundario.TButton",
                   command=lambda: self.cargar_ruta(EJEMPLO)).pack(side="left", padx=6)
        self.lbl_archivo = ttk.Label(acciones, text="Sin escenario", style="Chip.TLabel")
        self.lbl_archivo.pack(side="left", padx=(10, 12))
        ttk.Radiobutton(acciones, text="Modo exploración", value="explora", variable=self.var_modo,
                        command=self.cambiar_modo).pack(side="left")
        ttk.Radiobutton(acciones, text="Modo JSON (ejecuta lo que dice «prueba»)", value="json",
                        variable=self.var_modo, command=self.cambiar_modo).pack(side="left", padx=(8, 0))

        self.status = ttk.Label(self, style="Estado.TLabel", anchor="w")
        self.status.pack(side="bottom", fill="x")

        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True)
        izq, der = ttk.Frame(paned), ttk.Frame(paned)
        paned.add(izq, weight=3)
        paned.add(der, weight=2)

        cab = ttk.Frame(izq, padding=(10, 10, 10, 0))
        cab.pack(fill="x")
        self.lbl_turno = ttk.Label(cab, text="", style="Turno.TLabel")
        self.lbl_turno.pack(fill="x")
        self.lbl_celda = ttk.Label(cab, text="Pasa el cursor por el tablero para inspeccionar celdas.",
                                   style="Sub.TLabel")
        self.lbl_celda.pack(fill="x", pady=(4, 0))
        self.leyenda = ttk.Frame(izq, padding=(10, 0, 10, 10))
        self.leyenda.pack(side="bottom", fill="x")
        marco = tk.Frame(izq, bg=MARCOS, padx=1, pady=1)
        marco.pack(fill="both", expand=True, padx=10, pady=8)
        self.tablero = Tablero(marco, self.clic_tablero, self._hover_celda)
        self.tablero.pack(fill="both", expand=True)

        self.nb = ttk.Notebook(der)
        self.nb.pack(fill="both", expand=True, padx=(0, 10), pady=10)
        self.tab_ctrl, self.tab_res, self.tab_est, self.tab_cmp, self.tab_esc = (
            ttk.Frame(self.nb, padding=8) for _ in range(5))
        for tab, nombre in ((self.tab_ctrl, "Control"), (self.tab_res, "Resultados"),
                            (self.tab_est, "Estadísticas"), (self.tab_cmp, "Comparación"),
                            (self.tab_esc, "Escenario")):
            self.nb.add(tab, text=nombre)
        self._tab_control()
        self._tab_resultados()
        self._tab_estadisticas()
        self._tab_comparacion()
        self._tab_escenario()

    def _tab_control(self):
        t = self.tab_ctrl
        t.columnconfigure(0, weight=1)
        self.lbl_info = ttk.Label(t, text="", style="Aviso.TLabel")
        self.lbl_info.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(t, text="MISIÓN", style="Seccion.TLabel").grid(row=1, column=0, sticky="w", pady=(0, 4))
        self.var_tarea = tk.StringVar(value=list(TAREAS)[0])
        tareas = ttk.Frame(t)
        tareas.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        for i, nombre in enumerate(TAREAS):
            tareas.columnconfigure(i, weight=1)
            b = ttk.Button(tareas, text=nombre, style="Tarea.TButton",
                           command=lambda n=nombre: self._elegir_tarea(n))
            b.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 4, 0))
            self.btns_tarea[nombre] = b
        cont = ttk.Frame(t)
        cont.grid(row=3, column=0, sticky="nsew", pady=(4, 0))
        cont.columnconfigure(0, weight=1)
        t.rowconfigure(3, weight=1)
        self.f_busq, self.f_part, self.f_adv = self._f_busqueda(cont), self._f_partida(cont), self._f_adversarial(cont)
        for f in (self.f_busq, self.f_part, self.f_adv):
            f.grid(row=0, column=0, sticky="nsew")
        for v in (self.var_unidad, self.var_of, self.var_oc):
            v.trace_add("write", lambda *a: self._cambio_parametros())

    def _f_busqueda(self, parent):
        f = ttk.Frame(parent)
        f.columnconfigure(0, weight=1)
        lf = ttk.Labelframe(f, text=" Parámetros de búsqueda ", padding=10)
        lf.grid(row=0, column=0, sticky="ew")
        lf.columnconfigure(1, weight=1)
        nombres = disponibles()
        self.var_alg = tk.StringVar(value=nombres[0] if nombres else "")
        self.cb_alg = ttk.Combobox(lf, textvariable=self.var_alg, values=nombres, state="readonly")
        self.var_unidad, self.var_of, self.var_oc = tk.StringVar(), tk.StringVar(value="0"), tk.StringVar(value="0")
        self.cb_unidad = ttk.Combobox(lf, textvariable=self.var_unidad, state="readonly")
        fo = ttk.Frame(lf)
        self.sp_of = ttk.Spinbox(fo, from_=0, to=99, textvariable=self.var_of, width=5)
        self.sp_oc = ttk.Spinbox(fo, from_=0, to=99, textvariable=self.var_oc, width=5)
        self.var_heur, self.var_k = tk.StringVar(value="manhattan"), tk.StringVar(value="2")
        self.cb_heur = ttk.Combobox(lf, textvariable=self.var_heur, values=list(HEURISTICAS), state="readonly")
        self.sp_k = ttk.Spinbox(lf, from_=1, to=64, textvariable=self.var_k, width=5)
        self.var_expl = tk.BooleanVar(value=True)
        ttk.Label(lf, text="Algoritmo").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.cb_alg.grid(row=0, column=1, sticky="ew", pady=2)
        pend = ", ".join(e for _, e in PLANIFICADOS if normalizar_nombre(e) not in disponibles()
                         and _ not in disponibles())
        ttk.Label(lf, text=f"Pendientes de implementar: {pend}", style="Sub.TLabel").grid(
            row=1, column=0, columnspan=2, sticky="w")
        ttk.Label(lf, text="Unidad de inicio").grid(row=2, column=0, sticky="w", padx=(0, 8))
        self.cb_unidad.grid(row=2, column=1, sticky="ew", pady=2)
        ttk.Label(lf, text="Objetivo (fila, col)").grid(row=3, column=0, sticky="w", padx=(0, 8))
        fo.grid(row=3, column=1, sticky="w")
        self.sp_of.pack(side="left")
        self.sp_oc.pack(side="left", padx=4)
        ttk.Label(fo, text="(o haz clic en el mapa)", style="Sub.TLabel").pack(side="left", padx=4)
        ttk.Label(lf, text="Heurística (A*)").grid(row=4, column=0, sticky="w", padx=(0, 8))
        self.cb_heur.grid(row=4, column=1, sticky="ew", pady=2)
        ttk.Label(lf, text="k (Beam Search)").grid(row=5, column=0, sticky="w", padx=(0, 8))
        self.sp_k.grid(row=5, column=1, sticky="w", pady=2)
        ttk.Checkbutton(lf, text="Mostrar estados explorados", variable=self.var_expl,
                        command=self.refrescar_tablero).grid(row=6, column=0, columnspan=2, sticky="w", pady=(4, 0))
        fb = ttk.Frame(f)
        fb.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        for i, (txt, cmd, estilo) in enumerate((("Ejecutar búsqueda", self.ejecutar, "TButton"),
                                                ("Comparar todos", self.comparar_todos, "Secundario.TButton"),
                                                ("Verificar camino", self.verificar, "Secundario.TButton"),
                                                ("Limpiar vista", self._limpiar_vista, "Secundario.TButton"))):
            fb.columnconfigure(i, weight=1)
            ttk.Button(fb, text=txt, command=cmd, style=estilo).grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 4, 0))
        self._lock = [self.cb_unidad, self.sp_of, self.sp_oc, self.cb_heur, self.sp_k]
        return f

    def _f_partida(self, parent):
        f = ttk.Frame(parent)
        f.columnconfigure(0, weight=1)
        lf = ttk.Labelframe(f, text=" Despliegue de bandos ", padding=10)
        lf.grid(row=0, column=0, sticky="ew")
        lf.columnconfigure(1, weight=1)
        self.var_ctrl = {"A": tk.StringVar(value="Humano"), "B": tk.StringVar(value="Azar (provisional)")}
        for i, bando in enumerate("AB"):
            ttk.Label(lf, text=f"Controla el bando {bando}").grid(row=i, column=0, sticky="w", padx=(0, 8))
            ttk.Combobox(lf, textvariable=self.var_ctrl[bando], state="readonly",
                         values=["Humano", "Azar (provisional)"]).grid(row=i, column=1, sticky="ew", pady=2)
        self.lbl_costos = ttk.Label(lf, text="")
        self.lbl_costos.grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))
        ttk.Label(f, text="Clic en una unidad propia y luego en una celda marcada con borde punteado. "
                          "Minimax se añadirá como controlador en el Paso 8.", style="Sub.TLabel",
                  wraplength=460).grid(row=1, column=0, sticky="ew", pady=6)
        fb = ttk.Frame(f)
        fb.grid(row=2, column=0, sticky="ew", pady=(4, 0))
        self.btn_auto = ttk.Button(fb, text="Auto-jugar", command=self.auto_jugar)
        botones = (ttk.Button(fb, text="Turno de la IA", command=self.turno_ia, style="Secundario.TButton"),
                   self.btn_auto,
                   ttk.Button(fb, text="Esperar con la unidad elegida", command=self.esperar,
                              style="Secundario.TButton"),
                   ttk.Button(fb, text="Reiniciar partida", command=self._reiniciar_partida,
                              style="Secundario.TButton"))
        for i, w in enumerate(botones):
            w.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 4, 0))
            fb.columnconfigure(i, weight=1)
        return f

    def _f_adversarial(self, parent):
        f = ttk.Frame(parent)
        f.columnconfigure(0, weight=1)
        lf = ttk.Labelframe(f, text=" Árbol de decisión ", padding=10)
        lf.grid(row=0, column=0, sticky="ew")
        lf.columnconfigure(1, weight=1)
        self.var_prof, self.var_alg_adv = tk.StringVar(value="3"), tk.StringVar(value="MINIMAX")
        ttk.Label(lf, text="Algoritmo").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Combobox(lf, textvariable=self.var_alg_adv, values=["MINIMAX", "ALFA_BETA"],
                     state="readonly").grid(row=0, column=1, sticky="ew", pady=2)
        ttk.Label(lf, text="Profundidad máxima").grid(row=1, column=0, sticky="w", padx=(0, 8))
        ttk.Spinbox(lf, from_=1, to=12, textvariable=self.var_prof, width=5).grid(row=1, column=1, sticky="w")
        ttk.Label(f, text="Minimax y alfa-beta se implementan en el Paso 8. Por ahora se lista cada acción "
                          "legal del estado actual (la base de la verificación de legalidad).",
                  style="Sub.TLabel", wraplength=460).grid(row=1, column=0, sticky="ew", pady=6)
        ttk.Button(f, text="Listar acciones legales", command=self._ejecutar_adversarial).grid(
            row=2, column=0, sticky="ew", pady=(4, 0))
        return f

    def _tab_resultados(self):
        t = self.tab_res
        ttk.Label(t, text="MÉTRICAS DE LA ÚLTIMA EJECUCIÓN", style="Seccion.TLabel").pack(anchor="w", pady=(0, 6))
        self.tree_res = ttk.Treeview(t, columns=("m", "v"), show="headings", height=9)
        self.tree_res.heading("m", text="Métrica")
        self.tree_res.heading("v", text="Valor")
        self.tree_res.column("m", width=190)
        self.tree_res.column("v", width=260)
        self.tree_res.pack(fill="x")
        self.txt_res = self._texto(t, altura=14)
        self.txt_res.pack(fill="both", expand=True, pady=(10, 0))

    def _tab_estadisticas(self):
        t = self.tab_est
        ttk.Label(t, text="Resumen por algoritmo (todas las ejecuciones)", style="Seccion.TLabel").pack(anchor="w")
        cols = ("alg", "n", "exito", "costo", "exp", "tiempo")
        self.tree_resumen = ttk.Treeview(t, columns=cols, show="headings", height=3)
        for c, txt, w in zip(cols, ("Algoritmo", "Ejec.", "Éxito %", "Costo prom.", "Expand. prom.", "ms prom."),
                             (80, 45, 60, 80, 90, 70)):
            self.tree_resumen.heading(c, text=txt)
            self.tree_resumen.column(c, width=w, anchor="center")
        self.tree_resumen.pack(fill="x", pady=(4, 0))
        ttk.Label(t, text="Historial de ejecuciones", style="Seccion.TLabel").pack(anchor="w", pady=(6, 0))
        cols = ("n", "alg", "exito", "long", "costo", "gen", "exp", "fr", "t", "ruta")
        self.tree_hist = ttk.Treeview(t, columns=cols, show="headings", height=3)
        for c, txt, w in zip(cols, ("#", "Alg.", "Éxito", "Long.", "Costo", "Gener.", "Expand.", "Front.", "ms", "Ruta"),
                             (25, 50, 45, 45, 45, 50, 55, 50, 50, 100)):
            self.tree_hist.heading(c, text=txt)
            self.tree_hist.column(c, width=w, anchor="center")
        self.tree_hist.pack(fill="x", pady=(4, 0))
        fb = ttk.Frame(t)
        fb.pack(fill="x", pady=6)
        self.var_met_est = tk.StringVar(value="Estados expandidos")
        cb = ttk.Combobox(fb, textvariable=self.var_met_est, values=list(METRICAS), state="readonly", width=20)
        cb.pack(side="left")
        cb.bind("<<ComboboxSelected>>", lambda e: (self._graficar_estadisticas(), self._graficar_heuristicas()))
        ttk.Button(fb, text="Exportar CSV", style="Secundario.TButton", command=self.exportar_csv).pack(side="right")
        ttk.Button(fb, text="Borrar historial", style="Secundario.TButton",
                   command=self.borrar_historial).pack(side="right", padx=4)
        # Comparación de heurísticas (un mismo algoritmo): empaquetada por abajo ANTES que el
        # gráfico expandible, para que nunca quede sin espacio vertical.
        self.cv_heur = tk.Canvas(t, height=80, bg=PANEL, highlightthickness=1, highlightbackground=MARCOS)
        self.cv_heur.pack(side="bottom", fill="x", pady=(6, 0))
        self.cv_heur.bind("<Configure>", lambda e: self._graficar_heuristicas())
        cols = ("h", "exito", "long", "costo", "gen", "exp", "fr", "t")
        self.tree_heur = ttk.Treeview(t, columns=cols, show="headings", height=2)
        for c, txt, w in zip(cols, ("Heurística", "Éxito", "Long.", "Costo", "Gener.", "Expand.", "Front.", "ms"),
                             (90, 50, 50, 55, 60, 65, 55, 60)):
            self.tree_heur.heading(c, text=txt)
            self.tree_heur.column(c, width=w, anchor="center")
        self.tree_heur.pack(side="bottom", fill="x", pady=(4, 0))
        fh = ttk.Frame(t)
        fh.pack(side="bottom", fill="x", pady=(4, 0))
        self.var_alg_heur = tk.StringVar(value=disponibles()[0] if disponibles() else "")
        ttk.Combobox(fh, textvariable=self.var_alg_heur, values=disponibles(), state="readonly",
                     width=12).pack(side="left")
        ttk.Button(fh, text="Comparar heurísticas", command=self.comparar_heuristicas).pack(side="left", padx=6)
        self.lbl_heur = ttk.Label(fh, text="Elige algoritmo y métrica; cada heurística genera fila y barra.",
                                  style="Sub.TLabel")
        self.lbl_heur.pack(side="left", padx=6)
        ttk.Label(t, text="Comparar heurísticas (un mismo algoritmo)", style="Seccion.TLabel").pack(
            side="bottom", anchor="w")
        self.cv_est = tk.Canvas(t, height=80, bg=PANEL, highlightthickness=1, highlightbackground=MARCOS)
        self.cv_est.pack(fill="both", expand=True)
        self.cv_est.bind("<Configure>", lambda e: self._graficar_estadisticas())

    def _tab_comparacion(self):
        t = self.tab_cmp
        fb = ttk.Frame(t)
        fb.pack(fill="x")
        ttk.Button(fb, text="Comparar todos los algoritmos", command=self.comparar_todos).pack(side="left")
        self.var_met_cmp = tk.StringVar(value="Estados expandidos")
        cb = ttk.Combobox(fb, textvariable=self.var_met_cmp, values=list(METRICAS), state="readonly", width=20)
        cb.pack(side="right")
        cb.bind("<<ComboboxSelected>>", lambda e: self._graficar_comparacion())
        cols = ("alg", "exito", "long", "costo", "gen", "exp", "fr", "t", "ver")
        self.tree_cmp = ttk.Treeview(t, columns=cols, show="headings", height=6)
        for c, txt, w in zip(cols, ("Algoritmo", "Éxito", "Long.", "Costo", "Gener.", "Expand.", "Front.", "ms", "Verif."),
                             (75, 45, 45, 50, 55, 55, 50, 55, 50)):
            self.tree_cmp.heading(c, text=txt)
            self.tree_cmp.column(c, width=w, anchor="center")
        self.tree_cmp.pack(fill="x", pady=8)
        self.tree_cmp.bind("<<TreeviewSelect>>", self._seleccion_comparacion)
        self.lbl_cmp = ttk.Label(t, text="Selecciona una fila para ver su camino en el mapa.",
                                 style="Sub.TLabel", wraplength=460, justify="left")
        self.lbl_cmp.pack(fill="x")
        self.cv_cmp = tk.Canvas(t, height=170, bg=PANEL, highlightthickness=1, highlightbackground=MARCOS)
        self.cv_cmp.pack(fill="both", expand=True, pady=(8, 0))
        self.cv_cmp.bind("<Configure>", lambda e: self._graficar_comparacion())

    def _tab_escenario(self):
        t = self.tab_esc
        ttk.Label(t, text="VALIDACIÓN Y CONTENIDO DEL ESCENARIO", style="Seccion.TLabel").pack(anchor="w")
        self.txt_esc = self._texto(t, altura=14)
        self.txt_esc.pack(fill="both", expand=True, pady=(4, 0))
        ttk.Label(t, text="Registro de partidas y algoritmos", style="Seccion.TLabel").pack(anchor="w", pady=(10, 0))
        self.txt_log = self._texto(t, altura=8)
        self.txt_log.pack(fill="both", expand=True, pady=(4, 0))

    # ------------------------------------------------------------------ utilidades
    def _poner_estado(self, texto):
        self.status.config(text=texto)

    def log(self, texto):
        self.txt_log.insert("end", texto + "\n")
        self.txt_log.see("end")

    def _tarea(self):
        return TAREAS[self.var_tarea.get()]

    def _modo_json(self):
        return self.var_modo.get() == "json"

    # ------------------------------------------------------------------ carga de escenarios
    def cargar_dialogo(self):
        ruta = filedialog.askopenfilename(title="Escenario JSON", filetypes=[("JSON", "*.json"), ("Todos", "*.*")],
                                          initialdir=os.path.dirname(EJEMPLO))
        if ruta:
            self.cargar_ruta(ruta)

    def cargar_ruta(self, ruta):
        """Valida primero; solo si es válido reemplaza el escenario actual (todo o nada)."""
        try:
            esc = cargar_escenario(ruta)
        except ErrorEscenario as ex:
            self._mostrar_errores(ruta, ex.errores)
            self.nb.select(self.tab_esc)
            self._poner_estado(f"Escenario rechazado ({len(ex.errores)} error/es). El escenario anterior no se modificó.")
            messagebox.showerror("Escenario inválido", f"{len(ex.errores)} error(es) en {os.path.basename(ruta)}.\n"
                                 "El escenario anterior no fue modificado. Detalles en la pestaña Escenario.")
            return
        self._aplicar_escenario(esc, ruta)

    def _mostrar_errores(self, ruta, errores):
        self.txt_esc.delete("1.0", "end")
        self.txt_esc.insert("end", f"✘ NO se cargó {os.path.basename(ruta)}\n", "err")
        for i, e in enumerate(errores, 1):
            self.txt_esc.insert("end", f"  {i}. {e}\n", "err")
        if self.escenario:
            self.txt_esc.insert("end", f"\nSigue activo: {os.path.basename(self.ruta_actual)}\n", "h")

    def _aplicar_escenario(self, esc, ruta):
        self._cargando = True
        self.escenario, self.reglas, self.ruta_actual = esc, Reglas(esc), ruta
        self.estado = esc.estado_inicial()
        self.capas, self.comparacion, self.sel_unidad = {}, [], None
        self.auto, self.plies, self.costos = False, 0, {"A": 0, "B": 0}
        self.btn_auto.config(text="Auto-jugar")
        m = esc.mapa
        self.cb_unidad.config(values=sorted(u.id for u in esc.unidades))
        self.var_unidad.set(sorted(u.id for u in esc.unidades)[0])
        self.sp_of.config(to=m.filas - 1)
        self.sp_oc.config(to=m.columnas - 1)
        self.var_of.set(str(esc.recurso[0]))
        self.var_oc.set(str(esc.recurso[1]))
        self.var_prof.set(str(esc.profundidad_minimax))
        self._cargando = False
        self.lbl_archivo.config(text=os.path.basename(ruta))
        self._limpiar_resultados()
        self._dibujar_leyenda()
        self._resumen_escenario()
        self.log(f"Escenario cargado: {os.path.basename(ruta)} ({m.filas}x{m.columnas}, {len(esc.unidades)} unidades)")
        self.cambiar_modo(auto_ejecutar=True)

    def _resumen_escenario(self):
        e, m, t = self.escenario, self.escenario.mapa, self.txt_esc
        t.delete("1.0", "end")
        t.insert("end", f"✔ Escenario válido: {os.path.basename(self.ruta_actual)}\n", "ok")
        t.insert("end", f"Mapa: {m.filas} filas x {m.columnas} columnas\n", "h")
        t.insert("end", "Terrenos (nombre: costo):\n")
        for n, tp in m.tipos.items():
            t.insert("end", f"  {n}: " + (f"costo {fmt_num(tp['costo'])}" if tp["transitable"] else "no transitable") + "\n")
        t.insert("end", f"Bases: A={e.bases['A']}  B={e.bases['B']}\n")
        t.insert("end", f"Recurso: {e.recurso}   Portador: {e.portador}   Turno: {e.turno}\n")
        t.insert("end", "Unidades: " + ", ".join(f"{u.id}({u.bando})@({u.fila},{u.columna})" for u in e.unidades) + "\n")
        t.insert("end", f"Profundidad Minimax: {e.profundidad_minimax}\n")
        t.insert("end", f"Prueba: {json.dumps(e.prueba, ensure_ascii=False) if e.prueba else 'no definida'}\n")

    def _dibujar_leyenda(self):
        for w in self.leyenda.winfo_children():
            w.destroy()
        m = self.escenario.mapa
        fila1 = ttk.Frame(self.leyenda)
        fila1.pack(fill="x")
        ttk.Label(fila1, text="Terreno:", style="Sub.TLabel").pack(side="left", padx=(0, 6))
        for nombre, color in colores_terreno(m).items():
            tp = m.tipos[nombre]
            txt = f" {nombre} · {fmt_num(tp['costo'])} " if tp["transitable"] else f" {nombre} ✕ "
            tk.Label(fila1, text=txt, bg=color, fg=contraste(color),
                     font=(self.fuente, 8, "bold"), padx=6, pady=2).pack(side="left", padx=2)
        fila2 = ttk.Frame(self.leyenda)
        fila2.pack(fill="x", pady=(4, 0))
        ttk.Label(fila2, text="Leyenda:", style="Sub.TLabel").pack(side="left", padx=(0, 6))
        simbolos = ((f"◆ Recurso", RECURSO), (f"● Unidad", TEXTO), (f"━━ Ruta", RUTA),
                    (f"● Explorados", EXPLORADO))
        for txt, color in simbolos:
            tk.Label(fila2, text=f" {txt} ", bg=PANEL, fg=color, font=(self.fuente, 8, "bold"),
                     padx=6, pady=2).pack(side="left", padx=2)
        fila3 = ttk.Frame(self.leyenda)
        fila3.pack(fill="x", pady=(4, 0))
        ttk.Frame(fila3, width=57).pack(side="left")
        for txt, color in ((f"Inicio", INICIO), (f"✕ Objetivo", OBJETIVO),
                           (f"Turno de la IA ▲", ORO)):
            tk.Label(fila3, text=f" {txt} ", bg=PANEL, fg=color, font=(self.fuente, 8, "bold"),
                     padx=6, pady=2).pack(side="left", padx=2)

    # ------------------------------------------------------------------ modos
    def cambiar_modo(self, auto_ejecutar=False):
        json_m = self._modo_json()
        if json_m:
            self.lbl_info.config(text="MODO JSON: el programa ejecuta lo que indica el campo «prueba» del archivo "
                                      "(búsqueda, partida o adversarial). Los controles quedan bloqueados.")
            self._aplicar_prueba()
        else:
            self.lbl_info.config(text="MODO EXPLORACIÓN: usa el mapa cargado para probar cualquier tarea, "
                                      "algoritmo, unidad y objetivo que elijas.")
        self._bloquear(json_m)
        self._mostrar_frame_tarea()
        self.refrescar_tablero()
        if json_m and auto_ejecutar and self.escenario and self.escenario.prueba:
            self.ejecutar()

    def _aplicar_prueba(self):
        if not self.escenario:
            return
        p = self.escenario.prueba or {}
        if not p:
            self.lbl_info.config(text="MODO JSON: este archivo NO trae el campo «prueba». "
                                      "Cambia al modo exploración o agrégalo al JSON.")
            return
        self._cargando = True
        modo = p.get("modo")
        if modo in MODO_A_TAREA:
            self.var_tarea.set(MODO_A_TAREA[modo])
        else:
            self.lbl_info.config(text=f"MODO JSON: «prueba.modo» = {modo!r} no es válido "
                                      f"(use {', '.join(TAREAS.values())}).")
        if p.get("unidad_inicio"):
            self.var_unidad.set(str(p["unidad_inicio"]))
        obj = p.get("objetivo")
        if isinstance(obj, dict) and "fila" in obj and "columna" in obj:
            self.var_of.set(str(obj["fila"]))
            self.var_oc.set(str(obj["columna"]))
        if p.get("algoritmo"):
            self.var_alg.set(normalizar_nombre(p["algoritmo"]))
        if p.get("heuristica"):
            self.var_heur.set(str(p["heuristica"]))
        if p.get("k"):
            self.var_k.set(str(p["k"]))
        self._cargando = False

    def _bloquear(self, bloquear):
        for w in self._lock:
            w.config(state="disabled" if bloquear else ("normal" if isinstance(w, ttk.Spinbox) else "readonly"))
        for b in self.btns_tarea.values():
            b.state(["disabled"] if bloquear else ["!disabled"])
        define_alg = bool(self.escenario and (self.escenario.prueba or {}).get("algoritmo"))
        self.cb_alg.config(state="disabled" if (bloquear and define_alg) else "readonly")

    def _elegir_tarea(self, nombre):
        if self.var_tarea.get() == nombre:
            self._mostrar_frame_tarea()
            return
        self.var_tarea.set(nombre)
        self._cambio_tarea()

    def _cambio_tarea(self):
        self._mostrar_frame_tarea()
        self.refrescar_tablero()

    def _mostrar_frame_tarea(self):
        marcos = {"busqueda": self.f_busq, "partida": self.f_part, "adversarial": self.f_adv}
        for k, f in marcos.items():
            f.grid() if k == self._tarea() else f.grid_remove()
        for nombre, b in self.btns_tarea.items():
            b.configure(style="TareaActiva.TButton" if nombre == self.var_tarea.get() else "Tarea.TButton")

    def _cambio_parametros(self):
        if not self._cargando:
            self.capas = {}
            self.refrescar_tablero()

    # ------------------------------------------------------------------ dibujo
    def _inicio_busqueda(self):
        if not self.estado:
            return None
        u = self.estado.unidad(self.var_unidad.get())
        return (u.fila, u.columna) if u else None

    def _objetivo_busqueda(self):
        try:
            o = (int(self.var_of.get()), int(self.var_oc.get()))
        except ValueError:
            return None
        return o if self.escenario.mapa.dentro(*o) else None

    def refrescar_tablero(self):
        if not self.escenario:
            self.tablero.limpiar()
            return
        capas, tarea = {}, self._tarea()
        if tarea == "busqueda":
            capas.update(self.capas)
            if not self.var_expl.get():
                capas["explorados"] = None
            capas["inicio"], capas["objetivo"] = self._inicio_busqueda(), self._objetivo_busqueda()
        elif tarea == "partida":
            capas["seleccion"] = self.sel_unidad
            capas["turno_marcador"] = True
            if self.sel_unidad and not self.reglas.es_terminal(self.estado):
                capas["destinos"] = [a.destino for a in self.reglas.acciones_legales(self.estado)
                                     if a.unidad_id == self.sel_unidad and a.tipo == "MOVER"]
        self.tablero.mostrar(self.escenario, self.estado, **capas)
        e = self.estado
        rec = f"lo lleva {e.portador}" if e.portador else f"en el suelo {e.recurso_pos}"
        gan = self.reglas.ganador(e)
        texto = (f"GANÓ EL BANDO {gan}   |   " if gan else f"Turno del bando {e.turno}   |   ") + f"Recurso: {rec}"
        fondo = ORO if gan else COLOR_BANDO.get(e.turno, "#1b2740")
        self.lbl_turno.config(text=texto, background=fondo,
                              foreground="#1a1200" if gan else contraste(fondo))
        self.lbl_costos.config(text=f"Costo acumulado — A: {fmt_num(self.costos['A'])}   B: {fmt_num(self.costos['B'])}")

    def _limpiar_vista(self):
        self.capas = {}
        self.refrescar_tablero()

    def _hover_celda(self, f, c):
        """Ficha de información de la celda bajo el cursor (solo lectura)."""
        if not self.escenario:
            return
        if f is None:
            self.lbl_celda.config(text="Pasa el cursor por el tablero para inspeccionar celdas.")
            return
        m, e = self.escenario.mapa, self.estado
        nombre = m.terreno[f][c]
        tp = m.tipos[nombre]
        detalle = f"costo {fmt_num(tp['costo'])}" if tp["transitable"] else "obstáculo · no transitable"
        partes = [f"({f}, {c}) · {nombre} · {detalle}"]
        u = next((x for x in e.unidades if (x.fila, x.columna) == (f, c)), None)
        if u:
            partes.append(f"unidad {u.id} (bando {u.bando})")
        for bando, pos in self.escenario.bases.items():
            if pos == (f, c):
                partes.append(f"base del bando {bando}")
        if e.portador is None and e.recurso_pos == (f, c):
            partes.append("recurso en el suelo")
        elif e.portador and u and u.id == e.portador:
            partes.append("lleva el recurso")
        self.lbl_celda.config(text="   ·   ".join(partes))

    # ------------------------------------------------------------------ clics
    def clic_tablero(self, f, c):
        if not self.escenario:
            return
        if self._tarea() == "partida":
            self._clic_partida(f, c)
        elif self._tarea() == "busqueda":
            if self._modo_json():
                self._poner_estado("En modo JSON el objetivo viene del archivo. Cambia al modo exploración para elegirlo.")
                return
            u = next((x for x in self.estado.unidades if (x.fila, x.columna) == (f, c)), None)
            if u:
                self.var_unidad.set(u.id)
                self._poner_estado(f"Unidad de inicio: {u.id}")
            elif self.escenario.mapa.es_transitable(f, c):
                self.var_of.set(str(f))
                self.var_oc.set(str(c))
                self._poner_estado(f"Objetivo: ({f}, {c})")
            else:
                self._poner_estado("Esa celda es un obstáculo: no puede ser objetivo.")

    def _es_humano(self, bando):
        return self.var_ctrl[bando].get().startswith("Humano")

    def _clic_partida(self, f, c):
        if self.reglas.es_terminal(self.estado):
            self._poner_estado("La partida terminó. Pulsa «Reiniciar partida».")
            return
        bando = self.estado.turno
        if not self._es_humano(bando):
            self._poner_estado(f"Le toca al bando {bando}, controlado por la IA: pulsa «Turno de la IA».")
            return
        u = next((x for x in self.estado.unidades if (x.fila, x.columna) == (f, c)), None)
        if u and u.bando == bando:
            self.sel_unidad = u.id
            self.refrescar_tablero()
            return
        if self.sel_unidad:
            for a in self.reglas.acciones_legales(self.estado):
                if a.unidad_id == self.sel_unidad and a.tipo == "MOVER" and a.destino == (f, c):
                    self._aplicar_accion(a)
                    return
        self._poner_estado("Movimiento no válido: muro, unidad ocupando la celda o fuera de alcance.")

    # ------------------------------------------------------------------ partida
    def _reiniciar_partida(self):
        if not self.escenario:
            return
        self.estado = self.escenario.estado_inicial()
        self.costos, self.sel_unidad, self.plies, self.auto = {"A": 0, "B": 0}, None, 0, False
        self.btn_auto.config(text="Auto-jugar")
        self.log("Partida reiniciada desde el estado inicial del escenario.")
        self.refrescar_tablero()

    def _aplicar_accion(self, a):
        bando = self.estado.turno
        self.costos[bando] += self.reglas.costo(self.estado, a)
        antes = self.estado
        self.estado = self.reglas.aplicar(self.estado, a)
        self.plies += 1
        self.sel_unidad = None
        desc = f"{a.unidad_id} espera" if a.tipo == "ESPERAR" else f"{a.unidad_id} -> {a.destino}"
        extra = ""
        if antes.portador != self.estado.portador:
            extra = f"  [recurso: {antes.portador} -> {self.estado.portador}]"
        self.log(f"Jugada {self.plies} (bando {bando}): {desc}{extra}")
        g = self.reglas.ganador(self.estado)
        if g:
            self.log(f"*** Gana el bando {g} ***")
            self.auto = False
            self.btn_auto.config(text="Auto-jugar")
        self.refrescar_tablero()

    def esperar(self):
        if not (self.escenario and self._tarea() == "partida") or self.reglas.es_terminal(self.estado):
            return
        if self.sel_unidad and self._es_humano(self.estado.turno):
            self._aplicar_accion(next(a for a in self.reglas.acciones_legales(self.estado)
                                      if a.unidad_id == self.sel_unidad and a.tipo == "ESPERAR"))
        else:
            self._poner_estado("Selecciona primero una unidad propia (turno humano).")

    def turno_ia(self):
        if not self.escenario or self.reglas.es_terminal(self.estado):
            return
        if self._es_humano(self.estado.turno):
            self._poner_estado(f"El bando {self.estado.turno} está controlado por un humano.")
            return
        self._aplicar_accion(self.rng.choice(self.reglas.acciones_legales(self.estado)))

    def auto_jugar(self):
        if not self.escenario or self._tarea() != "partida":
            return
        self.auto = not self.auto
        self.btn_auto.config(text="Pausar" if self.auto else "Auto-jugar")
        if self.auto:
            self._auto_tick()

    def _auto_tick(self):
        if not self.auto:
            return
        if self.reglas.es_terminal(self.estado):
            return
        if self._es_humano(self.estado.turno):
            self.auto = False
            self.btn_auto.config(text="Auto-jugar")
            self._poner_estado("Auto-juego en pausa: es turno de un humano.")
            return
        if self.plies >= MAX_JUGADAS_AUTO:
            self.auto = False
            self.btn_auto.config(text="Auto-jugar")
            self.log(f"Tope de {MAX_JUGADAS_AUTO} jugadas en auto-juego (el límite de turnos real se definirá en el Paso 7).")
            return
        self.turno_ia()
        self.after(250, self._auto_tick)

    # ------------------------------------------------------------------ ejecución
    def ejecutar(self):
        if not self.escenario:
            messagebox.showinfo("Sin escenario", "Primero carga un escenario JSON.")
            return
        if self._modo_json():
            if not self.escenario.prueba:
                messagebox.showwarning("Sin prueba", "El JSON no trae el campo «prueba». Cambia al modo exploración.")
                return
            if self.escenario.prueba.get("modo") not in MODO_A_TAREA:
                messagebox.showwarning("Prueba inválida", "«prueba.modo» debe ser busqueda, partida o adversarial.")
                return
        t = self._tarea()
        if t == "busqueda":
            self._ejecutar_busqueda()
        elif t == "partida":
            self._reiniciar_partida()
            self.nb.select(self.tab_ctrl)
            self._poner_estado("Partida lista: continúa por turnos (clic en unidades o «Turno de la IA»).")
        else:
            self._ejecutar_adversarial()

    def _problema(self):
        esc, errores = self.escenario, []
        inicio, obj = self._inicio_busqueda(), None
        if inicio is None:
            errores.append(f"La unidad de inicio «{self.var_unidad.get()}» no existe o fue eliminada.")
        try:
            obj = (int(self.var_of.get()), int(self.var_oc.get()))
        except ValueError:
            errores.append("El objetivo debe tener fila y columna enteras.")
        if obj is not None:
            if not esc.mapa.dentro(*obj):
                errores.append(f"El objetivo {obj} está fuera del mapa.")
            elif not esc.mapa.es_transitable(*obj):
                errores.append(f"El objetivo {obj} es una celda no transitable.")
        if errores:
            messagebox.showerror("Prueba de búsqueda inválida", "\n".join(errores))
            return None
        return ProblemaNavegacion(esc.mapa, inicio, obj)

    def _parametros(self):
        try:
            k = int(self.var_k.get())
        except ValueError:
            k = 2
        return {"k": k, "heuristica": self.var_heur.get()}

    def _correr(self, nombre, p, **extra):
        params = {**self._parametros(), **extra}
        res = ejecutar_algoritmo(nombre, p, **params)
        checks = verificar_camino(self.escenario.mapa, p.inicio, p.objetivo, res) if res.exito else []
        self.historial.append({"escenario": os.path.basename(self.ruta_actual), "algoritmo": res.algoritmo,
                               "exito": res.exito, "longitud": res.longitud, "costo": res.costo,
                               "estados_generados": res.estados_generados,
                               "estados_expandidos": res.estados_expandidos,
                               "maximo_frontera": res.maximo_frontera, "tiempo_ms": round(res.tiempo_ms, 4),
                               "origen": p.inicio, "destino": p.objetivo, "parametros": json.dumps(res.parametros)})
        return res, checks

    def _ejecutar_busqueda(self):
        nombre = normalizar_nombre(self.var_alg.get())
        if nombre not in disponibles():
            messagebox.showinfo("Algoritmo pendiente",
                                f"«{self.var_alg.get()}» todavía no está implementado. Disponibles: {', '.join(disponibles())}.")
            return
        p = self._problema()
        if p is None:
            return
        res, checks = self._correr(nombre, p)
        self.capas = {"camino": res.camino, "explorados": res.explorados}
        self.refrescar_tablero()
        self._mostrar_resultado(res, checks, p)
        self._refrescar_estadisticas()
        self.nb.select(self.tab_res)
        self._poner_estado(f"{nombre}: " + (f"camino de costo {fmt(res.costo)} y {res.longitud} movimientos."
                                            if res.exito else "no se encontró camino."))

    def comparar_todos(self):
        if not self.escenario:
            messagebox.showinfo("Sin escenario", "Primero carga un escenario JSON.")
            return
        if self._tarea() != "busqueda":
            self.var_tarea.set(MODO_A_TAREA["busqueda"])
            self._cambio_tarea()
        p = self._problema()
        if p is None:
            return
        self.comparacion = [self._correr(n, p) for n in disponibles()]
        self._mostrar_comparacion(p)
        self._refrescar_estadisticas()
        self.nb.select(self.tab_cmp)

    def verificar(self):
        if not self.escenario or not getattr(self, "_ultimo", None):
            messagebox.showinfo("Verificar", "Ejecuta primero un algoritmo de búsqueda.")
            return
        res, p = self._ultimo
        if not res.exito:
            messagebox.showinfo("Verificar", "La última ejecución no encontró camino: no hay nada que verificar.")
            return
        checks = verificar_camino(self.escenario.mapa, p.inicio, p.objetivo, res)
        self._mostrar_resultado(res, checks, p)
        self.nb.select(self.tab_res)
        ok = all(c[1] for c in checks)
        messagebox.showinfo("Verificación", "Todas las comprobaciones pasaron." if ok else "Hay comprobaciones que fallaron.")

    def _ejecutar_adversarial(self):
        self.nb.select(self.tab_esc)
        self.log(f"--- Decisión adversarial ({self.var_alg_adv.get()}, profundidad {self.var_prof.get()}) ---")
        self.log(f"Estado: turno {self.estado.turno}, portador {self.estado.portador}.")
        acc = self.reglas.acciones_legales(self.estado)
        for a in acc:
            self.log("  " + (f"{a.unidad_id} espera" if a.tipo == "ESPERAR" else f"{a.unidad_id} -> {a.destino}"))
        self.log(f"{len(acc)} acciones legales. Minimax/alfa-beta se implementarán en el Paso 8.")
        self._poner_estado("Adversarial: listadas las acciones legales (Minimax pendiente).")

    # ------------------------------------------------------------------ resultados
    def _limpiar_resultados(self):
        self._ultimo = None
        self.heuristica_cmp = []
        for t in (self.tree_res, self.tree_cmp):
            t.delete(*t.get_children())
        self.txt_res.delete("1.0", "end")
        self.lbl_cmp.config(text="Selecciona una fila para ver su camino en el mapa.")
        self.tree_heur.delete(*self.tree_heur.get_children())
        self._graficar_comparacion()
        self._graficar_heuristicas()
        self._refrescar_estadisticas()

    def _mostrar_resultado(self, res, checks, p):
        self._ultimo = (res, p)
        self.tree_res.delete(*self.tree_res.get_children())
        filas = [("Algoritmo", res.algoritmo), ("Solución encontrada", fmt(res.exito)),
                 ("Longitud (movimientos)", fmt(res.longitud)), ("Costo total", fmt(res.costo)),
                 ("Estados generados", fmt(res.estados_generados)), ("Estados expandidos", fmt(res.estados_expandidos)),
                 ("Máximo de frontera", fmt(res.maximo_frontera)), ("Tiempo (ms)", fmt(res.tiempo_ms)),
                 ("Origen → destino", f"{p.inicio} → {p.objetivo}")]
        for f in filas:
            self.tree_res.insert("", "end", values=f)
        t = self.txt_res
        t.delete("1.0", "end")
        t.insert("end", "Camino recorrido\n", "h")
        t.insert("end", (" → ".join(f"({f},{c})" for f, c in res.camino) if res.exito else "Sin camino") + "\n\n")
        if checks:
            t.insert("end", "Verificación\n", "h")
            for desc, ok, det in checks:
                t.insert("end", ("✔ " if ok else "✘ ") + desc + (f"  [{det}]" if det and not ok else "") + "\n",
                         "ok" if ok else "err")
            t.insert("end", "\n")
        t.insert("end", "Resultado en formato JSON\n", "h")
        d = res.a_dict()
        t.insert("end", "{\n" + ",\n".join(f'  "{k}": {json.dumps(v, ensure_ascii=False)}' for k, v in d.items()) + "\n}")

    def _mostrar_comparacion(self, p):
        self.tree_cmp.delete(*self.tree_cmp.get_children())
        for i, (r, chk) in enumerate(self.comparacion):
            ver = "—" if not r.exito else ("OK" if all(c[1] for c in chk) else "FALLA")
            self.tree_cmp.insert("", "end", iid=str(i), values=(
                r.algoritmo, fmt(r.exito), fmt(r.longitud), fmt(r.costo), r.estados_generados,
                r.estados_expandidos, r.maximo_frontera, fmt(r.tiempo_ms), ver))
        ok = [r for r, _ in self.comparacion if r.exito]
        if ok:
            def mejores(clave):
                m = min(clave(r) for r in ok)
                return ", ".join(r.algoritmo for r in ok if clave(r) == m)
            distintos = len({tuple(r.camino) for r in ok}) > 1
            self.lbl_cmp.config(text=(f"Menor costo: {mejores(lambda r: r.costo)}.  Menos movimientos: {mejores(lambda r: r.longitud)}.  "
                                      f"Menos expandidos: {mejores(lambda r: r.estados_expandidos)}.  "
                                      f"Más rápido: {mejores(lambda r: r.tiempo_ms)}.\n"
                                      + ("Los algoritmos produjeron CAMINOS DISTINTOS." if distintos else "Todos produjeron el mismo camino.")
                                      + "  Selecciona una fila para verlo en el mapa."))
            self.tree_cmp.selection_set("0")
        else:
            self.lbl_cmp.config(text="Ningún algoritmo encontró camino.")
        self._graficar_comparacion()

    def _seleccion_comparacion(self, _ev):
        sel = self.tree_cmp.selection()
        if not sel or not self.comparacion:
            return
        r, _ = self.comparacion[int(sel[0])]
        self.capas = {"camino": r.camino, "explorados": r.explorados}
        self.refrescar_tablero()
        self._poner_estado(f"Mostrando el camino de {r.algoritmo}.")

    def _graficar_comparacion(self):
        clave = METRICAS[self.var_met_cmp.get()]
        datos = [(r.algoritmo, getattr(r, clave)) for r, _ in self.comparacion]
        barras(self.cv_cmp, datos, f"Comparación: {self.var_met_cmp.get()}")

    # ------------------------------------------------------------------ estadísticas
    def _refrescar_estadisticas(self):
        self.tree_hist.delete(*self.tree_hist.get_children())
        for i, h in enumerate(self.historial, 1):
            self.tree_hist.insert("", "end", values=(i, h["algoritmo"], fmt(h["exito"]), fmt(h["longitud"]),
                                                     fmt(h["costo"]), h["estados_generados"], h["estados_expandidos"],
                                                     h["maximo_frontera"], fmt(h["tiempo_ms"]),
                                                     f"{h['origen']}→{h['destino']}"))
        self.tree_hist.yview_moveto(1)
        self.tree_resumen.delete(*self.tree_resumen.get_children())
        for alg, hs in self._agrupar().items():
            ex = [h for h in hs if h["exito"]]
            prom = lambda k, L: sum(h[k] for h in L) / len(L) if L else None
            self.tree_resumen.insert("", "end", values=(alg, len(hs), fmt(round(100 * len(ex) / len(hs), 1)),
                                                        fmt(prom("costo", ex)), fmt(prom("estados_expandidos", hs)),
                                                        fmt(prom("tiempo_ms", hs))))
        self._graficar_estadisticas()

    def _agrupar(self):
        g = {}
        for h in self.historial:
            g.setdefault(h["algoritmo"], []).append(h)
        return g

    def _graficar_estadisticas(self):
        clave = {"Estados expandidos": "estados_expandidos", "Estados generados": "estados_generados",
                 "Costo": "costo", "Longitud": "longitud", "Máx. frontera": "maximo_frontera",
                 "Tiempo (ms)": "tiempo_ms"}[self.var_met_est.get()]
        datos = []
        for alg, hs in self._agrupar().items():
            vals = [h[clave] for h in hs if h[clave] is not None]
            datos.append((alg, sum(vals) / len(vals) if vals else None))
        barras(self.cv_est, datos, f"Promedio por algoritmo: {self.var_met_est.get()}")

    def comparar_heuristicas(self):
        """Ejecuta el algoritmo seleccionado una vez por heurística y compara sus métricas."""
        if not self.escenario:
            messagebox.showinfo("Sin escenario", "Primero carga un escenario JSON.")
            return
        if self._tarea() != "busqueda":
            self.var_tarea.set(MODO_A_TAREA["busqueda"])
            self._cambio_tarea()
        nombre = normalizar_nombre(self.var_alg_heur.get())
        if nombre not in disponibles():
            messagebox.showinfo("Algoritmo pendiente",
                                f"«{self.var_alg_heur.get()}» todavía no está implementado. "
                                f"Disponibles: {', '.join(disponibles())}.")
            return
        p = self._problema()
        if p is None:
            return
        self.heuristica_cmp = [(h, self._correr(nombre, p, heuristica=h)[0]) for h in HEURISTICAS]
        self._mostrar_heuristicas(nombre)
        self._refrescar_estadisticas()
        self.nb.select(self.tab_est)
        self._poner_estado(f"{nombre}: comparadas las heurísticas {', '.join(HEURISTICAS)}.")

    def _mostrar_heuristicas(self, nombre):
        self.tree_heur.delete(*self.tree_heur.get_children())
        for h, r in self.heuristica_cmp:
            self.tree_heur.insert("", "end", values=(h, fmt(r.exito), fmt(r.longitud), fmt(r.costo),
                                                     r.estados_generados, r.estados_expandidos,
                                                     r.maximo_frontera, fmt(r.tiempo_ms)))
        claves = {(r.exito, r.costo, tuple(r.camino) if r.camino else None, r.estados_expandidos)
                  for _, r in self.heuristica_cmp}
        self.lbl_heur.config(text=(
            f"{nombre} arroja los MISMOS resultados con todas las heurísticas (aún no las usa): "
            "el efecto será visible con A*."
            if len(claves) == 1 else f"{nombre} responde DISTINTO según la heurística."))
        self._graficar_heuristicas()

    def _graficar_heuristicas(self):
        clave = METRICAS[self.var_met_est.get()]
        nombre = self.var_alg_heur.get() or "algoritmo"
        datos = [(h, getattr(r, clave)) for h, r in self.heuristica_cmp]
        barras(self.cv_heur, datos, f"{nombre}: {self.var_met_est.get()} por heurística")

    def exportar_csv(self):
        if not self.historial:
            messagebox.showinfo("Exportar", "Todavía no hay ejecuciones en el historial.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")],
                                            initialfile="resultados.csv")
        if ruta:
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(self.historial[0]))
                w.writeheader()
                w.writerows(self.historial)
            self._poner_estado(f"Historial exportado a {ruta}")

    def borrar_historial(self):
        self.historial = []
        self._refrescar_estadisticas()
