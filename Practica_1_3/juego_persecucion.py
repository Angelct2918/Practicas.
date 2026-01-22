import pygame
import sys
import math
import csv
import os
from datetime import datetime

pygame.init()

# --- Ventana ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Evasión con Persecución")

# --- Colores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# --- Fuente y reloj ---
font = pygame.font.SysFont("Arial", 22)
clock = pygame.time.Clock()


# ===========================
#     CLASE SENSOR (Jugador)
# ===========================
class Sensor:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 30, 30)
        self.speed = 5
        self.trail = []

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)
        for pos in self.trail[-20:]:
            pygame.draw.circle(screen, (255, 100, 100), pos, 2)

    def move(self, keys):
        old_pos = (self.rect.centerx, self.rect.centery)

        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        new_pos = (self.rect.centerx, self.rect.centery)
        if new_pos != old_pos:
            self.trail.append(new_pos)


# ===========================
#      OBJETO PERSEGUIDOR
# ===========================
class ObjetoPerseguidor:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = 2
        self.color = BLUE

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, target_pos):
        target_x, target_y = target_pos
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = max(1, math.sqrt(dx**2 + dy**2))

        # Movimiento hacia el sensor
        self.rect.x += (dx / distance) * self.speed
        self.rect.y += (dy / distance) * self.speed

        # Cambia color cuando está cerca
        self.color = GREEN if distance < 100 else BLUE


# Crear jugador
sensor = Sensor()

# Crear dos objetos perseguidores
objetos = [
    ObjetoPerseguidor(700, 100),
    ObjetoPerseguidor(600, 400)
]

# Crear CSV
csv_file = "datos_persecucion.csv"
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Player_X', 'Player_Y',
                     'Obj1_X', 'Obj1_Y', 'Obj2_X', 'Obj2_Y'])


# ===========================
#        LOOP PRINCIPAL
# ===========================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    sensor.move(keys)

    for obj in objetos:
        obj.move(sensor.rect.center)

    # Guardar datos cada pocos frames
    if pygame.time.get_ticks() % 5 == 0:
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%H:%M:%S.%f"),
                sensor.rect.centerx, sensor.rect.centery,
                objetos[0].rect.centerx, objetos[0].rect.centery,
                objetos[1].rect.centerx, objetos[1].rect.centery
            ])

    # Dibujar pantalla
    screen.fill(BLACK)
    sensor.draw()

    for obj in objetos:
        obj.draw()

    text = font.render("Usa las flechas para moverte. ¡Los objetos te persiguen!", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print(f"Datos guardados en: {os.path.abspath(csv_file)}")
