from bases import punto_coma, coma_punto
import numpy as np

DATOS = "datos.dat"
GRAFICO = "Resultados/grafico.txt"

punto_coma(DATOS)

matrix = np.loadtxt(DATOS)

print(max(matrix[:,0]))