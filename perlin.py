import numpy as np
import matplotlib.pyplot as plt
import random

width, height = 190, 100

cell_width = 10

# Define 2-dimensional grid where each grid intersection has
# an associated 2D unit-length gradient vector
g_vecs = {}

for cell_x in range(0, width + cell_width, cell_width):
    for cell_y in range(0, height + cell_width, cell_width):
        theta = random.uniform(0, 2 * np.pi)
        g_vecs[(cell_x, cell_y)] = (np.cos(theta), np.sin(theta))


def get_corners(x, y):
    """Get the corners of the cell (x,y) is in"""
    upper_left_x = int((x // cell_width) * cell_width)
    upper_left_y = int((y // cell_width) * cell_width)
    
    return (
            (upper_left_x, upper_left_y),
            (upper_left_x + cell_width, upper_left_y),
            (upper_left_x, upper_left_y + cell_width),
            (upper_left_x + cell_width, upper_left_y + cell_width)
            )


def smoothstep(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    return a + t * (b - a)


pixel_grid = np.zeros((width, height))

for x in range(width):
    for y in range(height):
        # Identify 4 corners of the cell and their gradient vectors
        corner_g_vecs = np.array([g_vecs[corner] for corner in get_corners(x, y)])

        # Calculate offset vectors for each corner
        offset_vecs = corner_g_vecs - (x, y)

        # Calculate dot products between gradient vectors and offset vectors
        dot_products = np.einsum('ij,ij->i', corner_g_vecs, offset_vecs)
        
        u = smoothstep(0)
        v = smoothstep(0)        

        # Interpolate between dot products and interpolate between these to generate noise
        lerp1 = lerp(dot_products[0], dot_products[1], u)
        lerp2 = lerp(dot_products[2], dot_products[3], u)
        noise = lerp(lerp1, lerp2, v)
        
        pixel_grid[x, y] = noise


cmaps = ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'twilight', 'twilight_shifted', 'hsv', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'viridis', 'plasma', 'inferno', 'magma', 'cividis']



for cmap in cmaps:
    
    fig, ax = plt.subplots()
    inches_scale = 100
    fig.set_size_inches(width / inches_scale, height / inches_scale)
    mat = ax.matshow(np.rot90(pixel_grid), cmap=cmap)
    ax.axis("off")
    plt.show()
    plt.close()

