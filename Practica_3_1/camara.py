import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detección en tiempo real - Actividad 1")
        self.root.geometry("900x700")

        self.cap = None
        self.running = False

        # Frame de video
        self.video_label = tk.Label(root)
        self.video_label.pack(pady=10)

        # Sliders
        self.brillo_slider = tk.Scale(root, from_=0, to=100, orient="horizontal",
                                      label="Brillo")
        self.brillo_slider.set(50)
        self.brillo_slider.pack(fill="x", padx=20)

        self.contraste_slider = tk.Scale(root, from_=0, to=100, orient="horizontal",
                                         label="Contraste")
        self.contraste_slider.set(50)
        self.contraste_slider.pack(fill="x", padx=20)

        # Botones
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="Iniciar", command=self.start_video)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = ttk.Button(btn_frame, text="Detener", command=self.stop_video)
        self.stop_btn.grid(row=0, column=1, padx=10)

        self.capture_btn = ttk.Button(btn_frame, text="Capturar Imagen",
                                      command=self.capture_image)
        self.capture_btn.grid(row=0, column=2, padx=10)

        # Mensaje
        self.msg_label = tk.Label(root, text="", fg="blue")
        self.msg_label.pack()

    def start_video(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.update_frame()
            self.msg_label.config(text="Video iniciado")

    def stop_video(self):
        if self.running:
            self.running = False
            self.cap.release()
            self.video_label.config(image="")
            self.msg_label.config(text="Video detenido")

    def update_frame(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)

                # Ajustar brillo y contraste
                brillo = self.brillo_slider.get() - 50      # -50 a +50
                contraste = self.contraste_slider.get() / 50  # 0 a 2
                frame = cv2.convertScaleAbs(frame, alpha=contraste, beta=brillo)

                # Convertir a imagen para tkinter
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = img.resize((800, 500))
                imgtk = ImageTk.PhotoImage(image=img)

                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

            self.root.after(10, self.update_frame)

    def capture_image(self):
        if self.cap and self.running:
            ret, frame = self.cap.read()
            if ret:
                filename = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All Files", "*.*")]
                )
                if filename:
                    cv2.imwrite(filename, frame)
                    self.msg_label.config(text=f"Imagen guardada: {filename}")


# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.mainloop()
