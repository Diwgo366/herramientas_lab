import tkinter as tk
from tkinter import messagebox, ttk
import os

def crear_pestana_datos(notebook, base_dir):
    carpeta_temporales = os.path.join(base_dir, "temporales")
    os.makedirs(carpeta_temporales, exist_ok=True)
    RUTA_DATOS = os.path.join(carpeta_temporales, "datos.dat")
    NUM_COLUMNAS = 5
    ANCHO_CELDA = 64
    ANCHO_LABEL = 32

    def cargar_datos():
        filas = []
        try:
            with open(RUTA_DATOS, "r", encoding="utf-8") as f:
                for linea in f:
                    if linea.strip():
                        partes = [x for x in linea.strip().replace('\t', ' ').split() if x]
                        partes = [p.replace(',', '.') for p in partes]
                        while len(partes) < NUM_COLUMNAS:
                            partes.append("0")
                        filas.append(partes[:NUM_COLUMNAS])
        except FileNotFoundError:
            pass
        return filas

    def guardar():
        filas = []
        for fila in celdas:
            valores = []
            for celda in fila[1:]:
                if isinstance(celda, tk.Entry):
                    v = celda.get().strip().replace(',', '.')
                    try:
                        v = str(float(v))
                    except ValueError:
                        v = "0"
                    valores.append(v)
            if any(float(v) != 0 for v in valores):
                filas.append('\t'.join(valores))
        with open(RUTA_DATOS, "w", encoding="utf-8") as f:
            f.write('\n'.join(filas) + '\n')
        messagebox.showinfo("Guardado", "Datos guardados correctamente.")

    def validar_celda(valor):
        if not valor or valor == "-":
            return True
        valor = valor.replace(',', '.')
        if valor.count('.') > 1 or valor.count('-') > 1 or (valor.startswith('-') is False and '-' in valor):
            return False
        try:
            float(valor)
            return True
        except ValueError:
            return False

    def bind_celda(entry, i, j):
        vcmd = (tab_edicion.register(lambda P: validar_celda(P)), "%P")
        entry.config(validate="key", validatecommand=vcmd)
        entry.bind("<KeyPress>", lambda event, x=i, y=j: mover(event, x, y) if event.keysym in ("Up", "Down", "Left", "Right") else None)
        entry.bind("<Return>", lambda event: guardar())
        entry.bind("<Button-1>", lambda event: entry.after(1, lambda: entry.selection_range(0, tk.END)))

    def enfocar_celda(i, j):
        if 0 <= i < len(celdas) and 0 <= j+1 < len(celdas[i]):
            celda = celdas[i][j+1]
            if isinstance(celda, tk.Entry):
                celda.focus_set()
                celda.selection_range(0, tk.END)

    def mover(event, i, j):
        ni, nj = i, j
        if event.keysym == "Up":
            ni -= 1
        elif event.keysym == "Down":
            ni += 1
        elif event.keysym == "Left":
            nj -= 1
        elif event.keysym == "Right":
            nj += 1
        ni = max(0, min(ni, len(celdas) - 1))
        nj = max(0, min(nj, NUM_COLUMNAS - 1))
        enfocar_celda(ni, nj)

    def agregar_fila(valores=None):
        i = len(celdas)
        fila_celdas = []
        lbl = tk.Label(frame_celdas, text=str(i), width=4, relief="ridge", bg="#e0e0e0")
        lbl.grid(row=i+1, column=0, sticky="nsew")
        fila_celdas.append(lbl)
        for j in range(NUM_COLUMNAS):
            e = tk.Entry(frame_celdas, width=8, justify="center")
            e.grid(row=i+1, column=j+1, sticky="nsew")
            valor = valores[j] if valores and j < len(valores) else "0"
            e.insert(0, valor.replace(',', '.'))
            bind_celda(e, i, j)
            fila_celdas.append(e)
        celdas.append(fila_celdas)
        actualizar_scrollregion()

    def vaciar_todo():
        for fila in celdas:
            for celda in fila:
                celda.grid_forget()
        celdas.clear()
        agregar_fila()
        actualizar_scrollregion()

    def actualizar_scrollregion():
        tab_edicion.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def restablecer():
        for widget in frame_celdas.winfo_children():
            widget.destroy()
        celdas.clear()
        crear_encabezado()
        for fila in cargar_datos():
            agregar_fila(fila)
        if not celdas:
            agregar_fila()
        actualizar_scrollregion()

    def crear_encabezado():
        headers = [f"X{j}" for j in range(NUM_COLUMNAS+1)]
        for j, text in enumerate(headers):
            tk.Label(frame_celdas, text=text, width=8 if j else 4, relief="ridge", bg="#e0e0e0").grid(row=0, column=j, sticky="nsew")

    tab_edicion = ttk.Frame(notebook)
    notebook.add(tab_edicion, text="Edición de datos")
    
    frame_principal = tk.Frame(tab_edicion)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    ancho_canvas = ANCHO_LABEL + NUM_COLUMNAS * ANCHO_CELDA
    canvas = tk.Canvas(frame_principal, width=ancho_canvas, height=250)
    canvas.pack(side=tk.LEFT, fill=tk.Y, expand=False)

    scrollbar_y = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
    scrollbar_y.pack(side=tk.LEFT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar_y.set)

    frame_celdas = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_celdas, anchor="nw")

    frame_botones = tk.Frame(frame_principal)
    frame_botones.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    celdas = []
    crear_encabezado()
    for fila in cargar_datos():
        agregar_fila(fila)
    if not celdas:
        agregar_fila()

    tk.Button(frame_botones, text="Guardar", command=guardar, width=10).pack(pady=5)
    tk.Button(frame_botones, text="Restablecer", command=restablecer, width=10).pack(pady=5)
    tk.Button(frame_botones, text="Vaciar", command=vaciar_todo, width=10).pack(pady=5)
    tk.Button(frame_botones, text="Agregar Fila", command=agregar_fila, width=10).pack(pady=5)

    actualizar_scrollregion()