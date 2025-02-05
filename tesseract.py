#!/usr/bin/env python3
"""
A simulation of a ball bouncing inside a tesseract (4D hypercube)
with a correct 4D-to-3D perspective projection.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # registers the 3D projection

# --- Simulation Parameters ---
L = 1.0       # Half-length of the tesseract along each coordinate (boundaries at -L and L)
r = 0.05      # "Radius" of the ball (used for collision detection)
dt = 0.01     # Time step for simulation updates
d = 3.0       # Projection distance for 4D -> 3D perspective projection

# Initial 4D position and velocity (feel free to adjust)
pos = np.array([0.0, 0.0, 0.0, 0.0])  # (x, y, z, w)
vel = np.array([0.03, 0.02, 0.04, 0.05])  # 4D velocity components

# --- Projection Function ---
def project_point(v, d=3.0):
    """
    Project a 4D point v = (x, y, z, w) into 3D space using a perspective projection.
    The projection "divides" the (x, y, z) coordinates by (d - w), so that as w nears d,
    the point moves far away.
    """
    # Avoid division by zero if w gets too close to d (here d > L so it's safe)
    factor = d / (d - v[3])
    return factor * v[:3]

# --- Build the Tesseract (4D hypercube) edges ---
# Generate all 16 vertices of the tesseract (each coordinate is either -L or L)
vertices = [np.array([x, y, z, w])
            for x in (-L, L)
            for y in (-L, L)
            for z in (-L, L)
            for w in (-L, L)]

# Two vertices form an edge if they differ in exactly one coordinate.
edges = []
for i in range(len(vertices)):
    for j in range(i+1, len(vertices)):
        diff = np.abs(vertices[i] - vertices[j])
        if np.count_nonzero(diff > 1e-5) == 1:  # They differ in exactly one coordinate
            edges.append((i, j))

# --- Set Up the Plot ---
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Draw the tesseract’s projected edges.
for edge in edges:
    p1 = project_point(vertices[edge[0]], d)
    p2 = project_point(vertices[edge[1]], d)
    xs = [p1[0], p2[0]]
    ys = [p1[1], p2[1]]
    zs = [p1[2], p2[2]]
    ax.plot(xs, ys, zs, color='black', linewidth=0.5)

# Prepare a scatter plot for the ball (its projected position)
scat = ax.scatter([], [], [], color='red', s=100)

# Set axis limits – adjust these if needed.
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Ball Bouncing Inside a Tesseract (4D) Projected to 3D')

# --- Animation Update Function ---
def update(frame):
    global pos, vel

    # Update the 4D position
    pos = pos + vel * dt

    # Collision detection for each of the 4 dimensions:
    for i in range(4):
        if pos[i] + r > L:
            pos[i] = L - r  # reposition to be inside the wall
            vel[i] = -vel[i]  # reverse velocity for an elastic bounce
        if pos[i] - r < -L:
            pos[i] = -L + r
            vel[i] = -vel[i]

    # Project the updated 4D position into 3D.
    proj = project_point(pos, d)
    # Update the scatter plot with the new position.
    scat._offsets3d = ([proj[0]], [proj[1]], [proj[2]])
    return scat,

# Create the animation
ani = FuncAnimation(fig, update, frames=1000, interval=10, blit=False)

plt.show()
