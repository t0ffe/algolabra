import heapq

import numpy as np

from ui import draw_grid

DIRECTIONS = [
    (0, 1),  # right
    (0, -1),  # left
    (1, 0),  # down
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

    # Manhattan distance heuristic
    def heuristic(a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    # Get the neighbors of a node
    def get_neighbors(node):
        result = []
        for direction in DIRECTIONS:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if (
                0 <= neighbor[0] < len(grid)
                and 0 <= neighbor[1] < len(grid[0])
                and grid[neighbor[0]][neighbor[1]] != 1
            ):
                result.append(neighbor)
        return result

    visited_nodes = set()  # Nodes already evaluated
    unexplored_nodes = {start}  # Nodes to be evaluated
    came_from = {}  # Previous node for reconstructing the path

    g_score = {start: 0}  # Cost from start along best path
    f_score = {start: heuristic(start, goal)}  # Estimated total cost from start to goal

    while unexplored_nodes:
        current = min(unexplored_nodes, key=lambda x: f_score[x])

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        unexplored_nodes.remove(current)
        visited_nodes.add(current)

        for neighbor in get_neighbors(current):
            if neighbor in visited_nodes:
                continue

            # The distance from start to a neighbor
            new_g_score = g_score[current] + 1

            if neighbor not in unexplored_nodes:
                unexplored_nodes.add(neighbor)
            elif new_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = new_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

    return []  # No path found


def jps(grid, start, goal):
    # TODO Implement the Jump Point Search algorithm
    return []
