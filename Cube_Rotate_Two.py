import turtle
import math
import random
import time

# Konfigurasi sistem
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
STAR_COUNT = 300  # Ditambah menjadi 300 partikel
CUBE_SIZE = 150
ROTATION_SPEED = 0.02
STAR_SPEED = 7
HUE_SPEED = 0.008  # Kecepatan perubahan warna

# Inisialisasi layar
screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen.bgcolor('black')
screen.tracer(0, 0)

# Fungsi konversi HSV ke RGB
def hsv_to_rgb(h):
    r = abs(math.sin(h * math.pi)) * 0.8 + 0.2
    g = abs(math.sin((h + 0.3) * math.pi)) * 0.8 + 0.2
    b = abs(math.sin((h + 0.6) * math.pi)) * 0.8 + 0.2
    return (r, g, b)

# Kelas partikel bintang canggih
class StarParticle:
    def __init__(self):
        self.reset()
        self.hue = random.random()
        
    def reset(self):
        self.z = random.randint(10, SCREEN_WIDTH)
        self.x = random.randint(-SCREEN_WIDTH//2, SCREEN_WIDTH//2)
        self.y = random.randint(-SCREEN_HEIGHT//2, SCREEN_HEIGHT//2)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.uniform(1, 3)
        self.hue_speed = random.uniform(0.002, 0.005)
        
    def update(self):
        self.z -= STAR_SPEED * self.speed
        self.hue = (self.hue + self.hue_speed) % 1.0
        if self.z < 1:
            self.reset()

# Kelas kubus dengan warna dinamis
class ChromaticCube:
    def __init__(self, size):
        self.size = size
        self.vertices = [
            (-size, -size, -size),
            (size, -size, -size),
            (size, size, -size),
            (-size, size, -size),
            (-size, -size, size),
            (size, -size, size),
            (size, size, size),
            (-size, size, size)
        ]
        self.edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.hue_shift = 0.0
        
    def rotate(self):
        self.angle_x += ROTATION_SPEED
        self.angle_y += ROTATION_SPEED * 0.7
        self.angle_z += ROTATION_SPEED * 0.3
        self.hue_shift = (self.hue_shift + HUE_SPEED) % 1.0
        
    def project_3d_to_2d(self, x, y, z):
        fov = SCREEN_WIDTH * 0.8
        scale = fov / (fov + z)
        return x * scale, y * scale
        
    def draw(self, turtle):
        rotated_vertices = []
        for x, y, z in self.vertices:
            # Rotasi 3D
            y, z = y*math.cos(self.angle_x) - z*math.sin(self.angle_x), y*math.sin(self.angle_x) + z*math.cos(self.angle_x)
            x, z = x*math.cos(self.angle_y) + z*math.sin(self.angle_y), -x*math.sin(self.angle_y) + z*math.cos(self.angle_y)
            x, y = x*math.cos(self.angle_z) - y*math.sin(self.angle_z), x*math.sin(self.angle_z) + y*math.cos(self.angle_z)
            
            px, py = self.project_3d_to_2d(x, y, z)
            rotated_vertices.append((px, py))
            
        # Gambar edge dengan warna dinamis
        for i, edge in enumerate(self.edges):
            hue = (self.hue_shift + i*0.02) % 1.0
            color = hsv_to_rgb(hue)
            
            turtle.color(color)
            x1, y1 = rotated_vertices[edge[0]]
            x2, y2 = rotated_vertices[edge[1]]
            turtle.penup()
            turtle.goto(x1, y1)
            turtle.pendown()
            turtle.goto(x2, y2)
            turtle.penup()

# Inisialisasi objek
cube = ChromaticCube(CUBE_SIZE)
stars = [StarParticle() for _ in range(STAR_COUNT)]
cube_turtle = turtle.Turtle()
star_turtle = turtle.Turtle()

# Konfigurasi turtle
for t in [cube_turtle, star_turtle]:
    t.hideturtle()
    t.pensize(2)
    t.speed(0)

# Fungsi gambar bintang
def draw_stars():
    star_turtle.clear()
    for star in stars:
        scale = 100 / star.z
        x = star.x * scale
        y = star.y * scale
        color = hsv_to_rgb(star.hue)
        star_turtle.color(color)
        star_turtle.penup()
        star_turtle.goto(x, y)
        star_turtle.dot(star.size * (1 - star.z/SCREEN_WIDTH))

# Loop animasi utama
try:
    while True:
        screen.update()
        cube_turtle.clear()
        
        # Update dan gambar bintang
        for star in stars:
            star.update()
        draw_stars()
        
        # Update dan gambar kubus
        cube.rotate()
        cube.draw(cube_turtle)
        
        time.sleep(0.016)
        
except turtle.Terminator:
    pass
