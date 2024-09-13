import heapq

import numpy as np

from ui import draw_grid

DIRECTIONS = [
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
    (-1, 0),  # up
    # (-1, -1),  # up-left
    # (-1, 1),  # up-right
    # (1, -1),  # down-left
    # (1, 1),  # down-right
]


def create_grid(width, height, obstacles):
    grid = np.zeros((width, height))
    for x, y in obstacles:
        grid[x, y] = 1
    return grid


def astar(grid, start, goal):
    # TODO Implement a* algorithm
    return [(i, i) for i in range(20)]  # Return an empty path if no path is found


def jps(grid, start, goal):
    # TODO Implement the Jump Point Search algorithm
    return []
