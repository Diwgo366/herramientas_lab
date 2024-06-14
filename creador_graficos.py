from bases import punto_coma, coma_punto, ecuacion_lineal, ecuacion_potencial, existencia
import numpy as np
import pyperclip

DATOS = "datos.dat"
GRAFICO = "Resultados/grafico.txt"
COLUMNA_X = 0
COLUMNA_Y = 3
COLOR_PUNTOS = "black"
COLOR_RECTA = "red"
TIPO = True
CUADRADO = False

punto_coma(DATOS)

existencia(GRAFICO)

matrix = np.loadtxt(DATOS)

with open(GRAFICO, 'w') as f:
    # Escribir el inicio de la tabla
    f.write('\\begin{figure}[H]\n')
    f.write('\\centering\n')
    f.write('\\begin{tikzpicture}\n')
    
    #Escribir la configuración de los ejes
    f.write('\\begin{axis}[\n')
    f.write('   xlabel={Eje X $(und.)$},\n')
    f.write('   ylabel={Eje Y $(und.)$},\n')
    XMIN = min(matrix[:,COLUMNA_X])
    XMAX = max(matrix[:,COLUMNA_X])
    YMIN = min(matrix[:,COLUMNA_Y])
    YMAX = max(matrix[:,COLUMNA_Y])
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
    
    f.write('    ' + f'xmin={XMIN}, xmax={XMAX},\n')
    f.write('    ' + f'ymin={YMIN}, ymax={YMAX},\n')
    f.write('    grid=both,\n')
    if CUADRADO:
        f.write('    axis equal image,\n')
    f.write(']\n')
    f.write('\\addplot[only marks, color='+f'{COLOR_PUNTOS}]'+' coordinates {\n')
    
    # Escribir el listado de puntos
    for i in range(len(matrix[:,0])):
        f.write(f'    ({matrix[i,COLUMNA_X]}, {matrix[i,COLUMNA_Y]})\n')
    
    f.write('};\n')
    
    if TIPO:
        m, b = ecuacion_lineal(matrix[:,COLUMNA_X],matrix[:,COLUMNA_Y])
        if b < 0:
            f.write('\\addplot[domain=' + f'{XMIN}:{XMAX},{COLOR_RECTA}]' + '{' + f'{round(m, 4)} * x {round(b, 4)}' + '};\n')
        else:
            f.write('\\addplot[domain=' + f'{XMIN}:{XMAX},{COLOR_RECTA}]' + '{' + f'{round(m, 4)} * x + {round(b, 4)}' + '};\n')
    else:
        m, b = ecuacion_potencial(matrix[:,COLUMNA_X],matrix[:,COLUMNA_Y])
        f.write('\\addplot[domain=' + f'{XMIN}:{XMAX},{COLOR_RECTA}]' + '{' + f'x^{round(m, 4)} * 10^{round(b, 4)}' + '};\n')
    
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