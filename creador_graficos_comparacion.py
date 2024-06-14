from bases import punto_coma, coma_punto, ecuacion_lineal, ecuacion_potencial, GeneradorColor, existencia
import numpy as np
import pyperclip

DATOS = "datos.dat"
GRAFICO = "Resultados/comparacion.txt"
COLUMNA_X = [0,0,0]
COLUMNA_Y = [1,2,3]
TIPO = True
CUADRADO = False
punto_coma(DATOS)

matrix = np.loadtxt(DATOS)

existencia(GRAFICO)

colores = GeneradorColor()

for j in range(len(COLUMNA_X)):
    vector_x = np.concatenate([matrix[:, k] for k in COLUMNA_X])
    vector_y = np.concatenate([matrix[:,k] for k in COLUMNA_Y])
    XMIN = min(vector_x)
    XMAX = max(vector_x)
    YMIN = min(vector_y)
    YMAX = max(vector_y)
    
    if CUADRADO:
        RANGO = max(XMAX - XMIN, YMAX - YMIN)
        XMAX = round(XMIN + RANGO + RANGO/10, 4)
        XMIN = round(XMIN - RANGO/10, 4)
        YMAX = round(YMIN + RANGO + RANGO/10, 4)
        YMIN = round(YMIN - RANGO/10, 4)
    else:
        RANGO = XMAX - XMIN
        XMAX = round(XMIN + RANGO + RANGO/10, 4)
        XMIN = round(XMIN - RANGO/10, 4)
        
        RANGO = YMAX - YMIN
        YMAX = round(YMIN + RANGO + RANGO/10, 4)
        YMIN = round(YMIN - RANGO/10, 4)

def graficar(Eje_x, Eje_y):
    COLOR = colores.obtener_color()
    
    f.write('\\addplot[only marks, color='+f'{COLOR}]'+' coordinates {\n')
    for i in range(len(matrix[:,0])):
        f.write(f'    ({matrix[i,Eje_x]}, {matrix[i,Eje_y]})\n')
    
    f.write('};\n')
    
    if TIPO:
        m, b = ecuacion_lineal(matrix[:,Eje_x],matrix[:,Eje_y])
        if b < 0:
            f.write('\\addplot[domain=' + f'{XMIN}:{XMAX},{COLOR}]' + '{' + f'{round(m, 4)} * x {round(b, 4)}' + '};\n')
        else:
            f.write('\\addplot[domain=' + f'{XMIN}:{XMAX},{COLOR}]' + '{' + f'{round(m, 4)} * x + {round(b, 4)}' + '};\n')
    else:
        m, b = ecuacion_potencial(matrix[:,COLUMNA_X],matrix[:,COLUMNA_Y])
        f.write('\\addplot[domain=' + f'{XMIN}:{XMAX},{COLOR}]' + '{' + f'x^{round(m, 4)} * 10^{round(b, 4)}' + '};\n')
    f.write('\n')

with open(GRAFICO, 'w') as f:
    # Escribir el inicio de la tabla
    f.write('\\begin{figure}[H]\n')
    f.write('\\centering\n')
    f.write('\\begin{tikzpicture}\n')
    
    #Escribir la configuración de los ejes
    f.write('\\begin{axis}[\n')
    f.write('   xlabel={Eje X $(und.)$},\n')
    f.write('   ylabel={Eje Y $(und.)$},\n')
    f.write('    ' + f'xmin={XMIN}, xmax={XMAX},\n')
    f.write('    ' + f'ymin={YMIN}, ymax={YMAX},\n')
    f.write('    grid=both,\n')
    if CUADRADO:
        f.write('    axis equal image,\n')
    f.write(']\n')
    f.write('\n')
    
    for i in range(len(COLUMNA_X)):
        graficar(COLUMNA_X[i], COLUMNA_Y[i])

    f.write('\\end{axis}\n')
    f.write('\\end{tikzpicture}\n')
    f.write('\\caption{}\n')
    f.write('\\label{fig:grafico}\n')
    f.write('\\end{figure}\n')

coma_punto(DATOS)

try:
    with open(GRAFICO, 'r') as archivo:
        contenido = archivo.read()
    pyperclip.copy(contenido)
    print("Grafico copiado al portapapeles.")
except FileNotFoundError:
        print(f"Ocurrio un problema")