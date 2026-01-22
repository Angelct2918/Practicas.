import tkinter as tk
from tkinter import messagebox
import csv
import time

ruta = []  # Lista de movimientos
archivo_csv = "ruta_carrito.csv"  # Archivo donde se guardan los movimientos


# ------------------ INICIAR APRENDIZAJE ------------------
def iniciar_aprendizaje(event):
    messagebox.showinfo("Instrucciones", "Vamos a enseñarle a la IA a caminar.\nPresiona las flechas para mover el carrito.")
    ruta.clear()

    # Crear archivo CSV nuevo con cabecera
    with open(archivo_csv, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Movimiento", "X", "Y"])


# ------------------ MOVER CARRITO ------------------
def mover_carrito(event):
    global ruta
    movimiento = event.keysym  # Tecla presionada

    x1, y1, x2, y2 = canvas.coords(carrito)

    # Movimiento del carrito
    if movimiento == "Up":
        canvas.move(carrito, 0, -10)
    elif movimiento == "Down":
        canvas.move(carrito, 0, 10)
    elif movimiento == "Left":
        canvas.move(carrito, -10, 0)
    elif movimiento == "Right":
        canvas.move(carrito, 10, 0)

    # Nuevas coordenadas
    x1, y1, x2, y2 = canvas.coords(carrito)
    ruta.append((movimiento, x1, y1))

    # Guardar en el CSV
    with open(archivo_csv, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([movimiento, x1, y1])


# ------------------ REPRODUCIR MOVIMIENTOS ------------------
def repetir_movimientos(event):
    global ruta

    if not ruta:
        messagebox.showerror("Error", "No hay movimientos guardados.")
        return

    respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de que ya terminó el aprendizaje?")
    if not respuesta:
        return

    # Cargar movimientos del CSV
    try:
        with open(archivo_csv, "r") as file:
            reader = csv.reader(file)
            next(reader)
            ruta_reproducir = [(row[0], int(float(row[1])), int(float(row[2]))) for row in reader]

        # Reiniciar posición del carrito
        canvas.coords(carrito, 230, 230, 270, 270)
        root.update()

        # Reproducir movimientos
        for mov, _, _ in ruta_reproducir:
            time.sleep(0.05)
            root.update()

            if mov == "Up":
                canvas.move(carrito, 0, -10)
            elif mov == "Down":
                canvas.move(carrito, 0, 10)
            elif mov == "Left":
                canvas.move(carrito, -10, 0)
            elif mov == "Right":
                canvas.move(carrito, 10, 0)

    except FileNotFoundError:
        messagebox.showerror("Error", "No hay ruta guardada para reproducir.")


# ------------------ INTERFAZ GRÁFICA ------------------
root = tk.Tk()
root.title("Simulación de Carrito IA")

canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()

# Carrito
carrito = canvas.create_rectangle(230, 230, 270, 270, fill="blue")

# Controles
root.bind("a", iniciar_aprendizaje)
root.bind("<Up>", mover_carrito)
root.bind("<Down>", mover_carrito)
root.bind("<Left>", mover_carrito)
root.bind("<Right>", mover_carrito)
root.bind("i", repetir_movimientos)

# Ejecutar ventana
root.mainloop()
