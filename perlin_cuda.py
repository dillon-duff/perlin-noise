import numpy as np
import matplotlib.pyplot as plt
import random
from numba import cuda, float32

width, height = 1920, 1080
cell_width = 250

# Define 2-dimensional grid where each grid intersection has an associated 2D unit-length gradient vector
def generate_gradient_vectors(width, height, cell_width):
    g_vecs = np.zeros((width // cell_width + 1, height // cell_width + 1, 2), dtype=np.float32)
    for i in range(g_vecs.shape[0]):
        for j in range(g_vecs.shape[1]):
            theta = random.uniform(0, 2 * np.pi)
            g_vecs[i, j, 0] = np.cos(theta)
            g_vecs[i, j, 1] = np.sin(theta)
    return g_vecs

g_vecs = generate_gradient_vectors(width, height, cell_width)

@cuda.jit(device=True)
def smoothstep(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

@cuda.jit(device=True)
def lerp(a, b, t):
    return a + t * (b - a)

@cuda.jit
def generate_noise(pixel_grid, g_vecs, width, height, cell_width):
    x, y = cuda.grid(2)
    if x < width and y < height:
        # Identify 4 corners of the cell and their gradient vectors
        cell_x = x // cell_width
        cell_y = y // cell_width

        corners = (
            (cell_x, cell_y),
            (cell_x + 1, cell_y),
            (cell_x, cell_y + 1),
            (cell_x + 1, cell_y + 1)
        )

        # Calculate offset vectors and dot products
        dot_products = cuda.local.array(4, dtype=float32)
        for i, (cx, cy) in enumerate(corners):
            gradient = g_vecs[cx, cy]
            offset = (x - cx * cell_width, y - cy * cell_width)
            dot_products[i] = gradient[0] * offset[0] + gradient[1] * offset[1]

        # Normalize x and y to the cell size
        local_x = (x % cell_width) / cell_width
        local_y = (y % cell_width) / cell_width

        u = smoothstep(local_x)
        v = smoothstep(local_y)

        # Interpolate between dot products and interpolate between these to generate noise
        lerp1 = lerp(dot_products[0], dot_products[1], u)
        lerp2 = lerp(dot_products[2], dot_products[3], u)
        noise = lerp(lerp1, lerp2, v)

        pixel_grid[y, x] = noise


# Prepare data for GPU
pixel_grid_device = cuda.device_array((height, width), dtype=np.float32)
g_vecs_device = cuda.to_device(g_vecs)

# Define threads per block and number of blocks
threads_per_block = (16, 16)
blocks_per_grid_x = int(np.ceil(width / threads_per_block[0]))
blocks_per_grid_y = int(np.ceil(height / threads_per_block[1]))
blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

# Generate noise on GPU
generate_noise[blocks_per_grid, threads_per_block](pixel_grid_device, g_vecs_device, width, height, cell_width)

# Copy the result back to host
pixel_grid = pixel_grid_device.copy_to_host()

cmaps = ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'twilight', 'twilight_shifted', 'hsv', 'PiYG', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'viridis', 'plasma', 'inferno', 'cividis']

for cmap in cmaps:
    fig, ax = plt.subplots()
    inches_scale = 100
    fig.set_size_inches(width / inches_scale, height / inches_scale)
    mat = ax.matshow(pixel_grid, cmap=cmap)
    ax.axis("off")
    plt.show()
    plt.close()
