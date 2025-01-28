import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Rotating Triangle")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Triangle properties
triangle_radius = 200  # Distance from center to vertices
triangle_center = (width//2, height//2)
triangle_rotation = 0  # Degrees
rotation_speed = 0.5   # Degrees per frame

# Ball properties
ball_radius = 15
ball_pos = [width//2, height//2]
ball_vel = [3, 3]  # Initial velocity

def get_triangle_vertices(center, radius, rotation):
    """Generate triangle vertices based on rotation"""
    vertices = []
    for i in range(3):
        angle_deg = 120 * i + rotation
        angle_rad = math.radians(angle_deg)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        vertices.append((x, y))
    return vertices

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update triangle rotation
    triangle_rotation = (triangle_rotation + rotation_speed) % 360

    # Get current triangle vertices
    vertices = get_triangle_vertices(triangle_center, triangle_radius, triangle_rotation)

    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Check collisions with each edge
    for i in range(3):
        # Get current edge points
        A = vertices[i]
        B = vertices[(i+1)%3]
        
        # Calculate edge vector
        edge_vec = (B[0] - A[0], B[1] - A[1])
        
        # Calculate inward-pointing normal (rotated 90 degrees counter-clockwise)
        normal = (-edge_vec[1], edge_vec[0])
        normal_length = math.hypot(normal[0], normal[1])
        
        # Skip zero-length normals (shouldn't happen with proper triangle)
        if normal_length == 0:
            continue
            
        # Normalize normal
        normal = (normal[0]/normal_length, normal[1]/normal_length)
        
        # Calculate distance from ball to edge
        distance = (ball_pos[0] - A[0]) * normal[0] + (ball_pos[1] - A[1]) * normal[1]
        
        # Check for collision
        if distance < ball_radius:
            # Calculate reflection
            dot_product = ball_vel[0] * normal[0] + ball_vel[1] * normal[1]
            ball_vel[0] -= 2 * dot_product * normal[0]
            ball_vel[1] -= 2 * dot_product * normal[1]
            
            # Adjust position to prevent sticking
            penetration = ball_radius - distance
            ball_pos[0] += normal[0] * penetration
            ball_pos[1] += normal[1] * penetration

    # Drawing
    screen.fill(WHITE)
    
    # Draw triangle
    pygame.draw.polygon(screen, BLACK, vertices, 3)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
