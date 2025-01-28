import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import colorsys

# Konfigurasi parametrik Klein Bottle 4D
a = 2.0
b = 1.0
resolution = 150

def klein_4d(u, v):
    """Parametrizasi matematis akurat Klein Bottle 4D"""
    x = (a + b*np.cos(v)) * np.cos(u)
    y = (a + b*np.cos(v)) * np.sin(u)
    z = b*np.sin(v) * np.cos(u/2)
    w = b*np.sin(v) * np.sin(u/2)
    return (x, y, z, w)

def rotate_4d(point, angles):
    """Rotasi 4D menggunakan dua bidang ortogonal"""
    xy_angle, zw_angle = angles
    
    # Rotasi XY-plane
    x = point[0]*np.cos(xy_angle) - point[1]*np.sin(xy_angle)
    y = point[0]*np.sin(xy_angle) + point[1]*np.cos(xy_angle)
    z = point[2]
    w = point[3]
    
    # Rotasi ZW-plane
    z_new = z*np.cos(zw_angle) - w*np.sin(zw_angle)
    w_new = z*np.sin(zw_angle) + w*np.cos(zw_angle)
    
    return (x, y, z_new, w_new)

def stereographic_projection(point):
    """Proyeksi stereografis 4D → 3D dengan handling singularitas"""
    if point[3] == 1.0:
        return (0, 0, 0)
    return (point[0]/(1.0 - point[3]),
            point[1]/(1.0 - point[3]),
            point[2]/(1.0 - point[3]))

def create_klein_mesh():
    """Generate mesh parameterisasi"""
    u = np.linspace(0, 2*np.pi, resolution)
    v = np.linspace(0, 2*np.pi, resolution)
    vertices = []
    
    for i in range(resolution):
        for j in range(resolution):
            ui = u[i]
            vj = v[j]
            vertices.append(klein_4d(ui, vj))
    
    return vertices

# Inisialisasi Pygame dan OpenGL
pygame.init()
display = (1280, 720)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -8)
glEnable(GL_DEPTH_TEST)
glLineWidth(1.5)

# Generate mesh
vertices = create_klein_mesh()

# Variabel animasi
time_counter = 0.0
rotation_speed = 0.015

def get_color(w):
    """Color mapping berdasarkan koordinat W"""
    hue = (w + 2.0)/4.0
    return colorsys.hsv_to_rgb(hue, 0.8, 1.0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    # Update rotasi otomatis
    xy_angle = np.sin(time_counter * 0.5) * 2*np.pi
    zw_angle = np.cos(time_counter * 0.3) * 2*np.pi
    time_counter += rotation_speed
    
    # Proses semua vertex
    projected = []
    colors = []
    for v in vertices:
        rotated = rotate_4d(v, (xy_angle, zw_angle))
        proj = stereographic_projection(rotated)
        projected.append(proj)
        colors.append(get_color(rotated[3]))
    
    # Gambar wireframe dengan depth testing
    glBegin(GL_LINES)
    for i in range(resolution):
        for j in range(resolution):
            idx = i*resolution + j
            if j < resolution-1:
                glColor3fv(colors[idx])
                glVertex3fv(projected[idx])
                glVertex3fv(projected[idx+1])
            if i < resolution-1:
                glColor3fv(colors[idx])
                glVertex3fv(projected[idx])
                glVertex3fv(projected[idx + resolution])
    glEnd()
    
    pygame.display.flip()
    pygame.time.wait(10)