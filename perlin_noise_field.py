import numpy as np
import matplotlib.pyplot as plt
import random
import pygame as pg

from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=1)

width, height = 1920, 1080

cell_width = 40

arrow_grid = {}

for x in range(0, width + cell_width, cell_width):
    for y in range(0, height + cell_width, cell_width):
        arrow_grid[(x, y)] = noise([x / height, y / width]) * 2 * np.pi

screen = pg.display.set_mode((width, height))

pg.init()

running = True

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
    pg.draw.line(screen, color, start_pos, end_pos, 3)
    
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
    pg.draw.line(screen, color, end_pos, left_arrowhead, 3)
    pg.draw.line(screen, color, end_pos, right_arrowhead, 3)

clock = pg.time.Clock()
current_frame = 1
octaves = 0



def get_closest_arrow(point):
    x, y = point
    arrow_x = max(0, min(round(x / cell_width) * cell_width, width))
    arrow_y = max(0, min(round(y / cell_width) * cell_width, height))
    return arrow_grid[(arrow_x, arrow_y)]

def move_point_according_to_arrow(point, arrow):
    x_component = np.cos(arrow)
    y_component = np.sin(arrow)
    return (point[0] + x_component, point[1] + y_component)

def connect_points(p1, p2, color="blue", width=4):
    pg.draw.line(screen, pg.Color(204, 204, 255), p1, p2, width)

num_points = 100
points = [
        (random.randrange(width), random.randrange(height))
        for _ in range(num_points)
        ]

screen.fill("black")

#for (x,y), radians in arrow_grid.items():
#    draw_arrow(screen, "white", (x,y), cell_width/2,radians) 
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    for i, point in enumerate(points):
        closest_arrow = get_closest_arrow(point)
        next_point = move_point_according_to_arrow(point, closest_arrow)
        connect_points(point, next_point)
        points[i] = next_point

   
    current_frame += 1
    clock.tick(60)
    pg.display.flip()


