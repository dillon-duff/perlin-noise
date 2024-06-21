import numpy as np
import matplotlib.pyplot as plt
import random
import pygame as pg

from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=1)

width, height = 960, 540

cell_width = height

arrow_grid = {}

for x in range(0, width + cell_width, cell_width):
    for y in range(0, height + cell_width, cell_width):
        arrow_grid[(x, y)] = noise([x / height, y / width]) * 2 * np.pi


display = pg.display.set_mode((width, height))

pg.init()

running = True

import pygame
import math

def draw_arrow(screen, color, start_pos, length, angle):
    """
    Draw an arrow in Pygame.
    
    Parameters:
        screen (pygame.Surface): The Pygame surface to draw on.
        color (tuple): The color of the arrow (R, G, B).
        start_pos (tuple): The (x, y) position to center the arrow.
        length (int): The length of the arrow.
        angle (float): The angle of the arrow in radians.
    """
    # Calculate the end position of the arrow
    end_pos = (
        start_pos[0] + length * math.cos(angle),
        start_pos[1] + length * math.sin(angle)
    )
    
    # Draw the main line of the arrow
    pygame.draw.line(screen, color, start_pos, end_pos, 3)
    
    # Calculate the two points of the arrowhead
    arrowhead_length = length * 0.2
    arrowhead_angle = math.pi / 6  # 30 degrees for the arrowhead

    left_arrowhead = (
        end_pos[0] - arrowhead_length * math.cos(angle - arrowhead_angle),
        end_pos[1] - arrowhead_length * math.sin(angle - arrowhead_angle)
    )
    
    right_arrowhead = (
        end_pos[0] - arrowhead_length * math.cos(angle + arrowhead_angle),
        end_pos[1] - arrowhead_length * math.sin(angle + arrowhead_angle)
    )
    
    # Draw the arrowhead
    pygame.draw.line(screen, color, end_pos, left_arrowhead, 3)
    pygame.draw.line(screen, color, end_pos, right_arrowhead, 3)

clock = pg.time.Clock()
current_frame = 1
octaves = 0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    display.fill(pg.Color(255,255,255))

    if cell_width < 150:
        if current_frame % 3 == 0:
            cell_width -= 1
    else:
        cell_width -= 1
    print(cell_width)
    if cell_width < 10:
        running = False

    arrow_grid = {}
    for x in range(0, width + cell_width, cell_width):
        for y in range(0, height + cell_width, cell_width):
            arrow_grid[(x, y)] = noise([x / height, y / width]) * 2 * np.pi

    for (x,y), radians in arrow_grid.items():
        draw_arrow(display, pg.Color(0,0,0), (x,y), cell_width/2,radians) 
    
    current_frame += 1
    clock.tick(30)
    pg.display.flip()

