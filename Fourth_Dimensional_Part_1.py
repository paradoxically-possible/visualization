import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Parameter Klein Bottle 4D
a = 2.0
b = 1.0
resolution = 100

# Inisialisasi Pygame
pygame.init()
display = (1280, 720)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -8)
glEnable(GL_DEPTH_TEST)

# Fungsi parametrizasi Klein Bottle 4D
def klein_bottle_4d(u, v):
    x = (a + b*np.cos(v)) * np.cos(u)
    y = (a + b*np.cos(v)) * np.sin(u)
    z = b*np.sin(v) * np.cos(u/2)
    w = b*np.sin(v) * np.sin(u/2)
    return np.array([x, y, z, w])

# Rotasi 4D menggunakan quaternion
def rotate_4d(point, angles):
    theta_xy, theta_zw = angles
    
    # Rotasi XY-plane
    rotation_xy = np.array([
        [np.cos(theta_xy), -np.sin(theta_xy), 0, 0],
        [np.sin(theta_xy), np.cos(theta_xy), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    
    # Rotasi ZW-plane
    rotation_zw = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, np.cos(theta_zw), -np.sin(theta_zw)],
        [0, 0, np.sin(theta_zw), np.cos(theta_zw)]
    ])
    
    return rotation_zw @ rotation_xy @ point

# Proyeksi stereografis 4D → 3D
def stereographic_projection(point_4d, focus=3.0):
    return point_4d[:3] * focus / (focus - point_4d[3])

# Generate vertex grid
u = np.linspace(0, 2*np.pi, resolution)
v = np.linspace(0, 2*np.pi, resolution)
vertices = np.array([klein_bottle_4d(ui, vi) for ui in u for vi in v])

# Variabel kontrol
theta = [0.0, 0.0]
dragging = False
last_pos = (0, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
        # Kontrol mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            last_pos = pygame.mouse.get_pos()
            
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            
        if event.type == pygame.MOUSEMOTION and dragging:
            x, y = pygame.mouse.get_pos()
            dx = x - last_pos[0]
            dy = y - last_pos[1]
            theta[0] += dx * 0.005  # Rotasi XY
            theta[1] += dy * 0.005  # Rotasi ZW
            last_pos = (x, y)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    # Rotasi dan proyeksi semua vertex
    rotated = np.array([rotate_4d(v, theta) for v in vertices])
    projected = np.array([stereographic_projection(p) for p in rotated])
    
    # Gambar sebagai wireframe dengan color coding 4D
    glBegin(GL_LINES)
    for i in range(resolution):
        for j in range(resolution):
            idx = i*resolution + j
            w_value = rotated[idx][3]
            glColor3f((w_value+2)/4, 0.5, (2-w_value)/4)
            
            if j < resolution-1:
                glVertex3fv(projected[idx])
                glVertex3fv(projected[idx+1])
            
            if i < resolution-1:
                glVertex3fv(projected[idx])
                glVertex3fv(projected[idx + resolution])
    glEnd()
    
    pygame.display.flip()
    pygame.time.wait(10)