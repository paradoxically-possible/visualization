import pygame
import math
import random
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import colorsys

# Inisialisasi
pygame.init()
width, height = 1280, 720
pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)
clock = pygame.time.Clock()

# Konfigurasi OpenGL
gluPerspective(45, (width/height), 0.1, 500.0)
glTranslatef(0.0, 0.0, -40)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Parameter sistem partikel
PARTICLE_COUNT = 2000
particles = []
stars = []

class Particle:
    def __init__(self):
        self.pos = np.array([0.0, 0.0, 0.0])
        self.vel = np.array([
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ]) * 0.1
        self.color = colorsys.hsv_to_rgb(random.random(), 1, 1)

class Star:
    def __init__(self):
        self.pos = np.array([
            random.uniform(-50, 50),
            random.uniform(-50, 50),
            random.uniform(-50, 50)
        ])
        self.brightness = random.random()

for _ in range(PARTICLE_COUNT):
    particles.append(Particle())

for _ in range(500):
    stars.append(Star())

# Fungsi fractal icosahedron
def icosahedron():
    t = (1.0 + math.sqrt(5.0)) / 2.0
    verts = [
        [-1,  t,  0], [1,  t,  0], [-1, -t,  0], [1, -t,  0],
        [0, -1,  t], [0,  1,  t], [0, -1, -t], [0,  1, -t],
        [ t, 0, -1], [ t, 0,  1], [-t, 0, -1], [-t, 0,  1]
    ]
    faces = [
        (0,11,5), (0,5,1), (0,1,7), (0,7,10), (0,10,11),
        (1,5,9), (5,11,4), (11,10,2), (10,7,6), (7,1,8),
        (3,9,4), (3,4,2), (3,2,6), (3,6,8), (3,8,9),
        (4,9,5), (2,4,11), (6,2,10), (8,6,7), (9,8,1)
    ]
    return verts, faces

# Rotasi 3D
def rotate(matrix, angle, axis):
    c = math.cos(angle)
    s = math.sin(angle)
    t = 1 - c
    x, y, z = axis
    return np.array([
        [t*x*x + c,   t*x*y - z*s, t*x*z + y*s],
        [t*x*y + z*s, t*y*y + c,   t*y*z - x*s],
        [t*x*z - y*s, t*y*z + x*s, t*z*z + c  ]
    ]) @ matrix

angle = 0
matrix = np.identity(3)

# Main loop
running = True
while running:
    dt = clock.tick(60)/1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Bersihkan layar
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    # Gambar bintang latar belakang
    glBegin(GL_POINTS)
    for star in stars:
        glColor4f(1, 1, 1, star.brightness)
        glVertex3fv(star.pos)
        star.pos += np.array([0, 0, 0.3])
        if star.pos[2] > 50:
            star.pos = [random.uniform(-50, 50), random.uniform(-50, 50), -50]
    glEnd()
    
    # Update partikel
    glBegin(GL_POINTS)
    hue = (angle * 0.5) % 1.0
    for p in particles:
        p.pos += p.vel
        dist = np.linalg.norm(p.pos)
        force = -p.pos / (dist**3 + 1e-5) * 0.01
        p.vel += force
        p.vel *= 0.995
        
        rgb = colorsys.hsv_to_rgb(hue, 1, min(1, 1/(dist*0.3)))
        glColor3f(*rgb)
        glVertex3fv(p.pos)
    glEnd()
    
    # Gambar fractal icosahedron
    verts, faces = icosahedron()
    matrix = rotate(matrix, dt*0.5, [0.7, 1.0, 0.3])
    
    glPushMatrix()
    glScale(3, 3, 3)
    glColor4f(0.2, 0.5, 1.0, 0.8)
    glLineWidth(2)
    
    for face in faces:
        glBegin(GL_LINES)
        for i in face:
            v = np.array(verts[i])
            v_rot = matrix @ v
            glVertex3fv(v_rot)
            glVertex3fv(matrix @ np.array(verts[face[(i+1)%3]]))
        glEnd()
    
    glPopMatrix()
    
    # Update sudut rotasi
    angle += dt
    
    pygame.display.flip()

pygame.quit()