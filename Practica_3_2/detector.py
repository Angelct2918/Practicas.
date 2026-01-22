import cv2
import numpy as np
import tkinter as tk
from tkinter import Scale
from PIL import Image, ImageTk

# -----------------------------------------------------------
# FUNCIÓN PRINCIPAL DE DETECCIÓN DE COLORES Y FORMAS
# -----------------------------------------------------------
def detect_color_and_shapes(frame, lower_hsv, upper_hsv):

    # Convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Máscara para detectar color
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Convertir a gris para detectar contornos
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Obtener contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Clasificación y dibujo de formas
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Filtrar ruido pequeño

            # Aproximación del contorno
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Determinar forma según número de vértices
            if len(approx) == 3:
                shape = "Triangulo"
            elif len(approx) == 4:
                shape = "Cuadrado"
            elif len(approx) > 4:
                shape = "Circulo"
            else:
                shape = "Figura"

            # Dibujar contorno
            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)

            # Posición de texto
            x = approx.ravel()[0]
            y = approx.ravel()[1] - 10

            cv2.putText(frame, shape, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)

    return frame

# -----------------------------------------------------------
# FUNCIÓN PARA ACTUALIZAR EL VIDEO
# -----------------------------------------------------------
def update_frame():
    ret, frame = cap.read()
    if ret:

        # Leer sliders
        h_min = scale_h_min.get()
        h_max = scale_h_max.get()
        s_min = scale_s_min.get()
        s_max = scale_s_max.get()
        v_min = scale_v_min.get()
        v_max = scale_v_max.get()

        # Construir rangos HSV
        lower_hsv = np.array([h_min, s_min, v_min])
        upper_hsv = np.array([h_max, s_max, v_max])

        # Procesar frame
        frame = detect_color_and_shapes(frame, lower_hsv, upper_hsv)

        # Convertir para Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(frame_pil)

        # Mostrar en interfaz
        label_video.config(image=frame_tk)
        label_video.image = frame_tk

    # Llamar de nuevo en 10 ms
    window.after(10, update_frame)

# -----------------------------------------------------------
# CONFIGURACIÓN DE TKINTER
# -----------------------------------------------------------
cap = cv2.VideoCapture(0)

window = tk.Tk()
window.title("Detección de Color y Formas")

# Área de video
label_video = tk.Label(window)
label_video.pack()

# Sliders HSV
scale_h_min = Scale(window, from_=0, to=179, orient="horizontal", label="H Min")
scale_h_min.set(0)
scale_h_min.pack()

scale_h_max = Scale(window, from_=0, to=179, orient="horizontal", label="H Max")
scale_h_max.set(179)
scale_h_max.pack()

scale_s_min = Scale(window, from_=0, to=255, orient="horizontal", label="S Min")
scale_s_min.set(0)
scale_s_min.pack()

scale_s_max = Scale(window, from_=0, to=255, orient="horizontal", label="S Max")
scale_s_max.set(255)
scale_s_max.pack()

scale_v_min = Scale(window, from_=0, to=255, orient="horizontal", label="V Min")
scale_v_min.set(0)
scale_v_min.pack()

scale_v_max = Scale(window, from_=0, to=255, orient="horizontal", label="V Max")
scale_v_max.set(255)
scale_v_max.pack()

# Iniciar video
update_frame()

window.mainloop()

# Cerrar cámara correctamente
cap.release()
cv2.destroyAllWindows()
