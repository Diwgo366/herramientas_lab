from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import shutil
from mod.crear_latex import crear_archivo_tek
from mod.crear_word import crear_archivo_word

def crear_pestana_grafica(notebook, base_dir):
    tab_grafica = ttk.Frame(notebook)
    notebook.add(tab_grafica, text="Graficar")

    frame_principal = tk.Frame(tab_grafica)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    frame_izquierda = tk.Frame(frame_principal)
    frame_izquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    tk.Label(frame_izquierda, text="Tipo de gráfica:").pack(anchor="w")
    tipo_grafica = ttk.Combobox(frame_izquierda, values=["Lineal", "Exponencial"], state="readonly")
    tipo_grafica.current(0)
    tipo_grafica.pack(fill="x", pady=5)

    tk.Label(frame_izquierda, text="Eje X:").pack(anchor="w", pady=(10,0))
    opciones_x = [f"X{i}" for i in range(0, 5+1)]
    seleccion_x = ttk.Combobox(frame_izquierda, values=opciones_x, state="readonly")
    seleccion_x.current(0)
    seleccion_x.pack(fill="x", pady=5)

    tk.Label(frame_izquierda, text="Eje(s) Y:").pack(anchor="w", pady=(10,0))
    opciones_y = [f"X{i}" for i in range(1, 5+1)]
    seleccion_y = tk.Listbox(frame_izquierda, selectmode=tk.MULTIPLE, exportselection=False, height=5)
    for op in opciones_y:
        seleccion_y.insert(tk.END, op)
    seleccion_y.pack(fill="x", pady=5)

    frame_derecha = tk.Frame(frame_principal)
    frame_derecha.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)

    def obtener_selecciones():
        tipo = tipo_grafica.get()
        x = seleccion_x.get()
        y_indices = seleccion_y.curselection()
        y = [seleccion_y.get(i) for i in y_indices]
        return tipo, x, y

    def verificar_miktex():
        return shutil.which("pdflatex") is not None

    def comando_codigo_latex():
        tipo, x, y = obtener_selecciones()
        if not y:
            messagebox.showwarning("Advertencia", "Debe seleccionar al menos una variable para el eje Y.")
            return
        crear_archivo_tek(tipo, x, y, base_dir, False)

    def comando_documento_pdf():
        tipo, x, y = obtener_selecciones()
        if not y:
            messagebox.showwarning("Advertencia", "Debe seleccionar al menos una variable para el eje Y.")
            return
        if not verificar_miktex():
            messagebox.showerror(
            "Error",
            "No se detectó MiKTeX (pdflatex) en el sistema.\n"
            "Instale MiKTeX para generar PDF.\n\n"
            "Descárguelo desde: https://miktex.org/download"
            )
            return
        crear_archivo_tek(tipo, x, y, base_dir, True)
    
    def comando_documento_word():
        tipo, x, y = obtener_selecciones()
        if not y:
            messagebox.showwarning("Advertencia", "Debe seleccionar al menos una variable para el eje Y.")
            return
        if not verificar_miktex():
            messagebox.showerror(
            "Error",
            "No se pudo generar la gráfica debido a MiKTeX (pdflatex) no encontrado.\n"
            "Instale MiKTeX para generarla.\n\n"
            "Descárguelo desde: https://miktex.org/download"
            )
        crear_archivo_word(tipo, x, y, base_dir)

    btn_tek = tk.Button(frame_derecha, text="Código LaTeX", command=comando_codigo_latex, width=20)
    btn_tek.pack(pady=10)

    btn_pdf = tk.Button(frame_derecha, text="Crear PDF", command=comando_documento_pdf, width=20)
    btn_pdf.pack(pady=10)

    btn_word = tk.Button(frame_derecha, text="Crear Word", command=comando_documento_word, width=20)
    btn_word.pack(pady=10)
