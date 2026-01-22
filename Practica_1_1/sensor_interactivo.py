import tkinter as tk   # Para la interfaz gráfica
import math            # Para cálculos matemáticos (distancia)

class SensorInteractivo:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sensor")  # Título de la ventana

        # Canvas (área de dibujo)
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        # Sensor (cuadrado rojo fijo)
        self.sensor = self.canvas.create_rectangle(50, 50, 100, 100, fill="red", tags="sensor")

        # Objeto (cuadrado azul movible)
        self.objeto = self.canvas.create_rectangle(300, 300, 350, 350, fill="blue", tags="objeto")

        # Etiqueta de distancia
        self.label_distancia = tk.Label(root, text="Distancia: 0 píxeles", font=("Arial", 14))
        self.label_distancia.pack()

        # Vincular teclas
        self.root.bind("<Key>", self.mover_objeto)

        # Calcular distancia inicial
        self.actualizar_distancia()

    def mover_objeto(self, event):
        x, y = 0, 0

        if event.keysym == "Up":
            y = -10
        elif event.keysym == "Down":
            y = 10
        elif event.keysym == "Left":
            x = -10
        elif event.keysym == "Right":
            x = 10

        self.canvas.move("objeto", x, y)
        self.actualizar_distancia()

    def actualizar_distancia(self):
        # Obtener coordenadas de ambos cuadros
        x1, y1, _, _ = self.canvas.coords("sensor")
        x2, y2, _, _ = self.canvas.coords("objeto")

        # Distancia entre centros (más precisa)
        distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        # Mostrar
        self.label_distancia.config(text=f"Distancia: {int(distancia)} píxeles")


# Crear ventana principal
root = tk.Tk()
app = SensorInteractivo(root)
root.mainloop()
