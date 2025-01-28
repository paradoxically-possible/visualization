import turtle
import math
import random
import time

# Konfigurasi sistem
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
STAR_COUNT = 100
ROTATION_SPEED = 0.02
STAR_SPEED = 7
CUBE_SIZE = 150

# Inisialisasi layar
screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen.bgcolor('black')
screen.tracer(0, 0)

# Kelas untuk partikel bintang
class StarParticle:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.z = random.randint(10, SCREEN_WIDTH)
        self.x = random.randint(-SCREEN_WIDTH//2, SCREEN_WIDTH//2)
        self.y = random.randint(-SCREEN_HEIGHT//2, SCREEN_HEIGHT//2)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.uniform(1, 3)
        
    def update(self):
        self.z -= STAR_SPEED * self.speed
        if self.z < 1:
            self.reset()

# Kelas untuk kubus 3D
class RotatingCube:
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
        
    def rotate(self):
        self.angle_x += ROTATION_SPEED
        self.angle_y += ROTATION_SPEED * 0.7
        self.angle_z += ROTATION_SPEED * 0.3
        
    def project_3d_to_2d(self, x, y, z):
        # Proyeksi orthografik dengan sudut pandang
        fov = SCREEN_WIDTH * 0.8
        scale = fov / (fov + z)
        return x * scale, y * scale
        
    def draw(self, turtle):
        rotated_vertices = []
        for x, y, z in self.vertices:
            # Rotasi X
            y, z = y*math.cos(self.angle_x) - z*math.sin(self.angle_x), y*math.sin(self.angle_x) + z*math.cos(self.angle_x)
            # Rotasi Y
            x, z = x*math.cos(self.angle_y) + z*math.sin(self.angle_y), -x*math.sin(self.angle_y) + z*math.cos(self.angle_y)
            # Rotasi Z
            x, y = x*math.cos(self.angle_z) - y*math.sin(self.angle_z), x*math.sin(self.angle_z) + y*math.cos(self.angle_z)
            
            # Proyeksi ke 2D
            px, py = self.project_3d_to_2d(x, y, z)
            rotated_vertices.append((px, py))
            
        # Gambar edge kubus
        turtle.color('cyan')
        for edge in self.edges:
            x1, y1 = rotated_vertices[edge[0]]
            x2, y2 = rotated_vertices[edge[1]]
            turtle.penup()
            turtle.goto(x1, y1)
            turtle.pendown()
            turtle.goto(x2, y2)
            turtle.penup()

# Inisialisasi objek
cube = RotatingCube(CUBE_SIZE)
stars = [StarParticle() for _ in range(STAR_COUNT)]
cube_turtle = turtle.Turtle()
star_turtle = turtle.Turtle()

# Konfigurasi turtle
for t in [cube_turtle, star_turtle]:
    t.hideturtle()
    t.pensize(2)
    t.speed(0)

# Fungsi untuk menggambar partikel bintang
def draw_stars():
    star_turtle.clear()
    for star in stars:
        scale = 100 / star.z
        x = star.x * scale
        y = star.y * scale
        star_turtle.color(1.0 - (star.z/SCREEN_WIDTH), 0.8, 0.9)
        star_turtle.penup()
        star_turtle.goto(x, y)
        star_turtle.dot(star.size * (1 - star.z/SCREEN_WIDTH))

# Loop animasi utama
running = True

def close_window():
    global running
    running = False

# Daftarkan handler untuk window close
screen._root.protocol("WM_DELETE_WINDOW", close_window)

try:
    while running:
        screen.update()
        cube_turtle.clear()
        star_turtle.clear()
        
        # Update posisi bintang
        for star in stars:
            star.update()
            
        # Gambar bintang
        draw_stars()
        
        # Update dan gambar kubus
        cube.rotate()
        cube.draw(cube_turtle)
        
        time.sleep(0.016)

except turtle.Terminator:
    pass  # Handle kasus ketika window ditutup tiba-tiba
finally:
    try:
        screen.bye()  # Coba cleanup yang aman
    except:
        pass  # Jika window sudah dihancurkan, abaikan error