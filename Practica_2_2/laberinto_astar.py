import tkinter as tk
import heapq

TAM_CELDA = 40

# Laberinto
laberinto = [
 ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
 ["1", "A", "0", "0", "1", "0", "0", "0", "1", "0", "0", "0", "1", "0", "B", "1"],
 ["1", "1", "1", "0", "1", "1", "1", "0", "1", "0", "1", "0", "1", "0", "1", "1"],
 ["1", "0", "1", "0", "0", "0", "1", "0", "0", "0", "1", "0", "0", "0", "0", "1"],
 ["1", "0", "1", "1", "1", "0", "1", "1", "1", "1", "1", "1", "1", "1", "0", "1"],
 ["1", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "1"],
 ["1", "1", "1", "0", "1", "1", "1", "1", "1", "0", "1", "1", "0", "1", "0", "1"],
 ["1", "0", "0", "0", "0", "0", "0", "0", "1", "0", "1", "0", "0", "1", "0", "1"],
 ["1", "0", "1", "1", "1", "1", "1", "0", "1", "0", "1", "0", "1", "1", "0", "1"],
 ["1", "0", "1", "0", "0", "0", "1", "0", "0", "0", "1", "0", "0", "0", "0", "1"],
 ["1", "0", "1", "0", "1", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
 ["1", "0", "1", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"],
 ["1", "0", "1", "0", "1", "1", "1", "1", "1", "0", "1", "1", "1", "1", "0", "1"],
 ["1", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "1", "0", "1"],
 ["1", "1", "1", "1", "1", "1", "1", "0", "1", "1", "1", "1", "0", "1", "0", "1"],
 ["1", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "1", "0", "0", "0", "1"],
 ["1", "0", "1", "1", "1", "0", "1", "1", "1", "1", "0", "1", "1", "1", "1", "1"],
 ["1", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"],
 ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]
]


class LaberintoApp:
    def __init__(self, root, lab):
        self.root = root
        self.laberinto = lab
        self.inicio, self.fin = self.encontrar_puntos()

        self.alto = len(lab)
        self.ancho = len(lab[0])

        self.canvas = tk.Canvas(
            root,
            width=self.ancho * TAM_CELDA,
            height=self.alto * TAM_CELDA
        )
        self.canvas.pack()

        self.dibujar_laberinto()

        # Crear bolita verde
        self.bolita = self.canvas.create_oval(
            self.inicio[1] * TAM_CELDA + 10,
            self.inicio[0] * TAM_CELDA + 10,
            self.inicio[1] * TAM_CELDA + 30,
            self.inicio[0] * TAM_CELDA + 30,
            fill="green"
        )

        self.camino = self.buscar_camino()

        self.explorar()

    def dibujar_laberinto(self):
        for i, fila in enumerate(self.laberinto):
            for j, celda in enumerate(fila):
                x1, y1 = j * TAM_CELDA, i * TAM_CELDA
                x2, y2 = x1 + TAM_CELDA, y1 + TAM_CELDA

                if celda == "1":
                    color = "black"
                elif celda == "A":
                    color = "white"
                elif celda == "B":
                    color = "red"
                else:
                    color = "white"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="gray"
                )

    def encontrar_puntos(self):
        inicio, fin = None, None

        for i, fila in enumerate(self.laberinto):
            for j, celda in enumerate(fila):
                if celda == "A":
                    inicio = (i, j)
                elif celda == "B":
                    fin = (i, j)

        return inicio, fin

    def heuristic(self, a, b):
        """Distancia Manhattan"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def buscar_camino(self):
        """A*"""

        inicio = self.inicio
        fin = self.fin

        cola = []
        heapq.heappush(cola, (0, inicio))

        came_from = {}
        cost = {inicio: 0}

        while cola:
            _, actual = heapq.heappop(cola)

            if actual == fin:
                break

            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = actual[0] + dx, actual[1] + dy

                if self.laberinto[nx][ny] == "1":
                    continue

                nuevo_costo = cost[actual] + 1

                if (nx, ny) not in cost or nuevo_costo < cost[(nx, ny)]:
                    cost[(nx, ny)] = nuevo_costo
                    prioridad = nuevo_costo + self.heuristic((nx, ny), fin)
                    heapq.heappush(cola, (prioridad, (nx, ny)))
                    came_from[(nx, ny)] = actual

        # Reconstruir camino
        camino = []
        actual = fin

        while actual != inicio:
            camino.append(actual)
            actual = came_from.get(actual)

            if actual is None:
                print("NO hay camino")
                return []

        camino.reverse()
        return camino

    def explorar(self, paso=0):
        if paso < len(self.camino):
            x, y = self.camino[paso]
            self.canvas.coords(
                self.bolita,
                y*TAM_CELDA + 10,
                x*TAM_CELDA + 10,
                y*TAM_CELDA + 30,
                x*TAM_CELDA + 30
            )
            self.root.after(150, self.explorar, paso + 1)


# Ejecutar programa
root = tk.Tk()
root.title("Laberinto con A*")
app = LaberintoApp(root, laberinto)
root.mainloop()
