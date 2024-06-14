from bases import punto_coma, coma_punto, existencia
import numpy as np
import pyperclip

DATOS = "datos.dat"
TABLA = "Resultados/tabla.txt"

punto_coma(DATOS)

matrix = np.loadtxt(DATOS)

existencia(TABLA)

with open(TABLA, 'w') as f:
    # Escribir el inicio de la tabla
    f.write('\\begin{table}[H]\n')
    f.write('\\centering\n')
    f.write('\\begin{tabular}{|')
    for _ in range(matrix.shape[1]):
        f.write('c|')
    f.write('}\n')
    f.write('\\hline\n')
    
    # Escribir los datos de la matriz en la tabla
    for row in matrix:
        row_str = ' & '.join(map(lambda x: f'${x}$', row)) + '\\\\\n'
        f.write(row_str)
        f.write('\\hline\n')
    
    # Escribir el final de la tabla
    f.write('\\end{tabular}\n')
    f.write('\\caption{}\n')
    f.write('\\label{tab:tabla}\n')
    f.write('\\end{table}\n')

coma_punto(DATOS)

try:
    with open(TABLA, 'r') as archivo:
        contenido = archivo.read()
    pyperclip.copy(contenido)
    print("Tabla copiada al portapapeles.")
except FileNotFoundError:
        print(f"Ocurrio un problema")