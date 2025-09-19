import os
import json
from tkinter import ttk
import tkinter as tk

def crear_selector(parent, variable, row, label_text, opciones, representacion=None, colores_tk=None):
    tk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=2)
    btn = tk.Button(parent, width=10 if representacion else 3, height=1, relief="raised")
    btn.grid(row=row, column=1, padx=5, pady=2, sticky="w")

    def update_btn():
        if colores_tk:
            btn.config(bg=colores_tk[variable.get()])
        elif representacion:
            btn.config(text=representacion.get(variable.get(), variable.get()))

    def show_palette(event):
        if hasattr(btn, "_palette") and btn._palette.winfo_exists():
            btn._palette.destroy()
        palette = tk.Toplevel(parent)
        palette.overrideredirect(True)
        palette.attributes("-topmost", True)
        x = btn.winfo_rootx()
        y = btn.winfo_rooty() + btn.winfo_height()
        palette.geometry(f"+{x}+{y}")

        def close_palette(event=None):
            if palette.winfo_exists():
                palette.destroy()
        palette.bind("<FocusOut>", close_palette)
        palette.bind("<Escape>", close_palette)
        palette.focus_force()

        cols = 6 if colores_tk else 1
        for idx, op in enumerate(opciones):
            def set_op(val=op):
                variable.set(val)
                update_btn()
                close_palette()
            b = tk.Button(
                palette,
                bg=colores_tk[op] if colores_tk else None,
                text=representacion.get(op, op) if representacion else "",
                width=3 if colores_tk else 10,
                height=1,
                relief="flat",
                command=set_op,
                borderwidth=2,
                highlightthickness=0,
                activebackground=colores_tk[op] if colores_tk else None
            )
            b.grid(row=idx // cols, column=idx % cols, padx=1, pady=1)
        btn._palette = palette

    btn.bind("<Button-1>", show_palette)
    update_btn()
    variable.trace_add("write", lambda *_: update_btn())

def crear_entry(parent, variable, row, label_text):
    tk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=2)
    tk.Entry(parent, textvariable=variable, width=25).grid(row=row, column=1, padx=5, pady=2)

def crear_pestana_configuracion(notebook, base_dir):
    carpeta_temporales = os.path.join(base_dir, "temporales")
    os.makedirs(carpeta_temporales, exist_ok=True)
    archivo_config = os.path.join(carpeta_temporales, "configuracion_grafica.json")

    # --- Definición de colores y tipos de línea ---
    colores_pgf = [
        "black", "red", "blue", "green", "yellow", "orange", "purple",
        "brown", "cyan", "magenta", "gray", "white"
    ]
    colores_tk = {
        "black": "#000000", "red": "#ff0000", "blue": "#0000ff", "green": "#008000",
        "yellow": "#ffff00", "orange": "#ffa500", "purple": "#800080", "brown": "#a52a2a",
        "cyan": "#00ffff", "magenta": "#ff00ff", "gray": "#808080", "white": "#ffffff"
    }
    tipos_linea = ["solid", "dashed", "dotted", "dashdotted"]
    tipo_linea_repr = {
        "solid": "───", "dashed": "-------", "dotted": "············", "dashdotted": "–·–·–·–·–"
    }

    valores_default = {
        "fondo": "white", "linea": "orange", "tipo_linea": "solid", "color_ajuste": "black",
        "mostrar_ajuste": True, "colores_x": ["red", "blue", "green", "purple", "brown"],
        "label_grafica": "", "nombre_eje_x": "", "nombre_eje_y": "",
        "nombre_x": [ "Y1", "Y2", "Y3", "Y4", "Y5"],
        "mostrar_leyenda": True
    }
    if not os.path.exists(archivo_config):
        with open(archivo_config, "w", encoding="utf-8") as f:
            json.dump(valores_default, f, indent=2)
    with open(archivo_config, "r", encoding="utf-8") as f:
        config_actual = json.load(f)

    tab_configuracion = ttk.Frame(notebook)
    notebook.add(tab_configuracion, text="Configuración")
    frame_principal = tk.Frame(tab_configuracion)
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
    frame_izq = tk.Frame(frame_principal)
    frame_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    frame_der = tk.Frame(frame_principal)
    frame_der.grid(row=0, column=1, sticky="nsew")
    frame_principal.grid_columnconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)

    # --- Etiquetas ---
    frame_nombres = tk.LabelFrame(frame_izq, text="  Etiquetas  ")
    frame_nombres.pack(fill=tk.X, padx=0, pady=5)
    label_grafica_var = tk.StringVar(value=config_actual.get("label_grafica", ""))
    nombre_eje_x_var = tk.StringVar(value=config_actual.get("nombre_eje_x", ""))
    nombre_eje_y_var = tk.StringVar(value=config_actual.get("nombre_eje_y", ""))
    crear_entry(frame_nombres, label_grafica_var, 0, "Label:")
    crear_entry(frame_nombres, nombre_eje_x_var, 1, "Nombre del eje X:")
    crear_entry(frame_nombres, nombre_eje_y_var, 2, "Nombre del eje Y:")

    # Agregar entradas para el nombre de cada X
    nombre_x_vars = []
    for i in range(5):
        var = tk.StringVar(value=config_actual.get("nombre_x", [""]*5)[i] if "nombre_x" in config_actual else "")
        crear_entry(frame_nombres, var, 3 + i, f"Nombre X{i+1}:")
        nombre_x_vars.append(var)

    # --- Línea de ajuste ---
    frame_ajuste = tk.LabelFrame(frame_izq, text="  Línea de ajuste  ")
    frame_ajuste.pack(fill=tk.X, padx=0, pady=5)
    mostrar_ajuste_var = tk.BooleanVar(value=config_actual.get("mostrar_ajuste", True))
    tk.Checkbutton(
        frame_ajuste, text="Mostrar", variable=mostrar_ajuste_var, onvalue=True, offvalue=False
    ).grid(row=0, column=0, padx=5, pady=2, sticky="w", columnspan=2)
    tipo_linea_var = tk.StringVar(value=config_actual.get("tipo_linea", "solid"))
    ajuste_var = tk.StringVar(value=config_actual.get("color_ajuste", "black"))
    crear_selector(frame_ajuste, tipo_linea_var, 1, "Tipo de línea:", tipos_linea, tipo_linea_repr)
    crear_selector(frame_ajuste, ajuste_var, 2, "Color de línea:", colores_pgf, colores_tk=colores_tk)

    # --- Colores de la gráfica ---
    frame_grafica = tk.LabelFrame(frame_der, text="  Configuración del Fondo  ")
    frame_grafica.pack(fill=tk.X, padx=0, pady=5)
    fondo_var = tk.StringVar(value=config_actual.get("fondo", "white"))
    crear_selector(frame_grafica, fondo_var, 0, "Color de Fondo:", colores_pgf, colores_tk=colores_tk)
    linea_var = tk.StringVar(value=config_actual.get("linea", "orange"))
    crear_selector(frame_grafica, linea_var, 1, "Color de Líneas:", colores_pgf, colores_tk=colores_tk)

    # --- Mostrar leyenda ---
    mostrar_leyenda_var = tk.BooleanVar(value=config_actual.get("mostrar_leyenda", True))
    tk.Checkbutton(
        frame_grafica, text="Mostrar leyenda", variable=mostrar_leyenda_var, onvalue=True, offvalue=False
    ).grid(row=2, column=0, columnspan=2, padx=5, pady=2, sticky="w")

    # --- Colores de las series X ---
    frame_colores_x = tk.LabelFrame(frame_der, text="  Colores de las variables  ")
    frame_colores_x.pack(fill=tk.X, padx=0, pady=5)
    colores_x_vars = []
    colores_x_config = config_actual.get("colores_x", valores_default["colores_x"])
    for i in range(1, 6):
        color_default = colores_x_config[i-1] if i-1 < len(colores_x_config) else colores_pgf[(i-1) % len(colores_pgf)]
        var = tk.StringVar(value=color_default)
        crear_selector(frame_colores_x, var, i-1, f"Color X{i}:", colores_pgf, colores_tk=colores_tk)
        colores_x_vars.append(var)

    # --- Guardar configuración en JSON ---
    def guardar_configuracion():
        datos = {
            "fondo": fondo_var.get(),
            "linea": linea_var.get(),
            "tipo_linea": tipo_linea_var.get(),
            "color_ajuste": ajuste_var.get(),
            "mostrar_ajuste": mostrar_ajuste_var.get(),
            "colores_x": [v.get() for v in colores_x_vars],
            "label_grafica": label_grafica_var.get(),
            "nombre_eje_x": nombre_eje_x_var.get(),
            "nombre_eje_y": nombre_eje_y_var.get(),
            "nombre_x": [v.get() for v in nombre_x_vars],
            "mostrar_leyenda": mostrar_leyenda_var.get()
        }
        with open(archivo_config, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2)
        nonlocal config_actual
        config_actual = datos

    # --- Botón de guardar configuración ---
    tk.Button(frame_principal, text="Guardar configuración", command=guardar_configuracion)\
        .grid(row=1, column=0, columnspan=2, pady=5)

    # --- Almacenar referencias a las variables de configuración ---
    tab_configuracion.config_vars = {
        "fondo": fondo_var,
        "linea": linea_var,
        "tipo_linea": tipo_linea_var,
        "colores_x": colores_x_vars,
        "color_ajuste": ajuste_var,
        "mostrar_ajuste": mostrar_ajuste_var,
        "label_grafica": label_grafica_var,
        "nombre_eje_x": nombre_eje_x_var,
        "nombre_eje_y": nombre_eje_y_var,
        "nombre_x": nombre_x_vars,
        "mostrar_leyenda": mostrar_leyenda_var,
    }