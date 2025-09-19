import tkinter as tk
from tkinter import ttk
import os
import sys
from mod.pestana_datos import crear_pestana_datos
from mod.pestana_grafica import crear_pestana_grafica
from mod.pestana_configuracion import crear_pestana_configuracion

APP_TITLE = "Graficador"

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(__file__))

def main():
    BASE_DIR = get_base_dir()

    root = tk.Tk()
    root.title(APP_TITLE)
    root.resizable(False, False)

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    crear_pestana_datos(notebook, BASE_DIR)
    crear_pestana_grafica(notebook, BASE_DIR)
    crear_pestana_configuracion(notebook, BASE_DIR)

    root.mainloop()

if __name__ == "__main__":
    main()
