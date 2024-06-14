import os
import numpy as np

def existencia(ruta):
    if not os.path.exists(ruta):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)


def punto_coma(ubicacion):
    with open(ubicacion, 'r') as file:
        data = file.read()
    data = data.replace(',', '.')
    with open(ubicacion, 'w') as file:
        file.write(data)

def coma_punto(ubicacion):
    with open(ubicacion, 'r') as file:
        data = file.read()
    data = data.replace('.', ',')
    with open(ubicacion, 'w') as file:
        file.write(data)
        
def ecuacion_lineal(array_x, array_y):
    "Funcion para calcular los valores m y b para reemplazarlos en la ecuación lineal"
    valor_p= len(array_x)
    valor_xy = np.multiply(array_x, array_y)
    x_squared = np.square(array_x)
    suma_x = np.sum(array_x)
    suma_y = np.sum(array_y)
    suma_xy = np.sum(valor_xy)
    suma_x_squared = np.sum(x_squared)
    valor_m = ((valor_p*suma_xy)-(suma_x*suma_y))/((valor_p*suma_x_squared)-(suma_x)**2)
    valor_b = ((suma_x_squared*suma_y)-(suma_x*suma_xy)) / \
        ((valor_p*suma_x_squared)-(suma_x)**2)
    return valor_m, valor_b

def ecuacion_potencial(array_x, array_y):
    "Funcion para calcular los valores m y b para reemplazarlos en la ecuación potencial"
    valor_p= len(array_x)
    log_x = np.log10(array_x, where=array_x>0)
    log_y = np.log10(array_y, where=array_y>0)
    log_x_log_y = np.multiply(log_x, log_y)
    log_x_squared = np.square(log_x)
    suma_log_x = np.sum(log_x)
    suma_log_y = np.sum(log_y)
    suma_log_x_log_y = np.sum(log_x_log_y)
    suma_log_x_squared = np.sum(log_x_squared)
    valor_m = ((valor_p*suma_log_x_log_y)-(suma_log_x*suma_log_y)) / \
        ((valor_p*suma_log_x_squared)-(suma_log_x)**2)
    valor_b = ((suma_log_x_squared*suma_log_y)-(suma_log_x *
               suma_log_x_log_y))/((valor_p*suma_log_x_squared)-(suma_log_x)**2)
    return valor_m, valor_b

class GeneradorColor:
    def __init__(self):
        self.colores = [
            'black', 'red', 'blue', 'magenta', 'cyan', 'green', 'yellow',
            'darkgray', 'gray', 'lightgray', 'brown', 'lime', 'olive', 'orange', 
            'pink', 'purple', 'teal', 'violet'
        ]
        self.colores_usados = set()
        self.index = 0

    def obtener_color(self):
        if self.index >= len(self.colores):
            raise ValueError("Te quedaste sin colores")
        
        color = self.colores[self.index]
        self.colores_usados.add(color)
        self.index += 1
        
        return color
