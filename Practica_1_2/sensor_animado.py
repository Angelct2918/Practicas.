import numpy as np  # Para cálculos matemáticos
import matplotlib.pyplot as plt  # Para gráficos
import matplotlib.animation as animation  # Para animaciones
from matplotlib.patches import Rectangle  # Para dibujar los objetos
import csv  # Para guardar datos en un archivo CSV
import os  # Para manejar rutas de archivos

class SensorAnimado:
    def __init__(self):
        # Crear la figura
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)

        # Cuadrado sensor (fijo)
        self.sensor = Rectangle((1, 1), 1, 1, color='r')
        self.ax.add_patch(self.sensor)

        # Cuadrado objeto (móvil)
        self.objeto = Rectangle((8, 7), 1, 1, color='b')
        self.ax.add_patch(self.objeto)

        # Texto de distancia
        self.dist_text = self.ax.text(0.5, 9.5, "Distancia: 0.00", fontsize=12)

        # Archivo CSV
        self.csv_file = "datos_sensor.csv"

        # Crear archivo CSV con encabezados
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Frame', 'Pos_X', 'Pos_Y', 'Distancia'])

        # Iniciar animación
        self.anim = animation.FuncAnimation(
            self.fig, self.actualizar, frames=60, interval=100, blit=False
        )

    def actualizar(self, frame):
        # Mover el objeto en círculos
        angle = frame * 0.1
        x = 5 + 3 * np.cos(angle)
        y = 5 + 3 * np.sin(angle)
        self.objeto.set_xy((x, y))

        # Calcular distancia al centro del sensor (1.5, 1.5)
        distancia = np.sqrt((x - 1.5)**2 + (y - 1.5)**2)
        self.dist_text.set_text(f"Distancia: {distancia:.2f}")

        # Guardar datos en CSV
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([frame, x, y, distancia])

        return self.objeto, self.dist_text


# Ejecutar simulación
sensor = SensorAnimado()
plt.show()

print(f"Datos guardados en: {os.path.abspath(sensor.csv_file)}")
