import numpy as np
import matplotlib.pyplot as plt
import random

width, height = 1920, 1080

cell_width = 500

# Define 2-dimensional grid where each grid intersection has
# an associated 2D unit-length gradient vector
g_vecs = {}

def generate_random_g_vec():
    theta = random.uniform(0, 2 * np.pi)
    return (np.cos(theta), np.sin(theta))


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


def noise(x, y):
    # Identify 4 corners of the cell and their gradient vectors
    corners = get_corners(x, y)
    corner_g_vecs = []
    for corner in corners:
        if corner not in g_vecs.keys():
            g_vecs[corner] = generate_random_g_vec()
        corner_g_vecs.append(g_vecs[corner])

    corner_g_vecs = np.array(corner_g_vecs)

    # Normalize x and y to the cell size
    local_x = (x % cell_width) / cell_width
    local_y = (y % cell_width) / cell_width

    # Calculate offset vectors for each corner
    offset_vecs = ((np.array(corners) + corner_g_vecs) - (x , y))

    # Calculate dot products between gradient vectors and offset vectors
    dot_products = np.einsum('ij,ij->i', corner_g_vecs, offset_vecs)  
    
    u = smoothstep(local_x)
    v = smoothstep(local_y)

    # Interpolate between dot products and interpolate between these to generate noise
    lerp_x = lerp(dot_products[0], dot_products[1], u)
    lerp_y = lerp(dot_products[2], dot_products[3], u)
    noise = lerp(lerp_x, lerp_y, v)
    
    return noise

def show_random_noise():
    pixel_grid = np.zeros((width, height))

    for x in range(pixel_grid.shape[0]):
        for y in range(pixel_grid.shape[1]):
            pixel_grid[x, y] = noise(x, y)
    print(pixel_grid)
    print(f"min: {pixel_grid.min()}, max: {pixel_grid.max()}")

    cmaps = ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'twilight', 'twilight_shifted', 'hsv', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'viridis', 'plasma', 'inferno', 'magma', 'cividis']

    fig, ax = plt.subplots()
    inches_scale = 100
    fig.set_size_inches(width / inches_scale, height / inches_scale)
    mat = ax.matshow(np.rot90(pixel_grid), cmap=random.choice(cmaps))
    ax.axis("off")
    plt.show()
    plt.close()

for _ in range(3):
    show_random_noise()