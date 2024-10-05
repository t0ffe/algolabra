from queue import PriorityQueue

import numpy as np
import pygame

from settings import DRAW_IN_PROGRESS, DRAWING_FREQ
from ui import draw_grid

DIRECTIONS = [
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
    (-1, 0),  # up
    (-1, -1),  # up-left
    (-1, 1),  # up-right
    (1, -1),  # down-left
    (1, 1),  # down-right
]


# Manhattan distance heuristic
# def manhattan_heuristic(a, b):
#    return abs(b[0] - a[0]) + abs(b[1] - a[1])


# Euclidean distance heuristic
def euclidean_heuristic(a, b):
    """
    Calculate the Euclidean distance between two points.
    Currently not used in the pathfinding algorithms.
    Args:
        a (tuple): The first point as a tuple of (x, y) coordinates.
        b (tuple): The second point as a tuple of (x, y) coordinates.

    Returns:
        float: The Euclidean distance between points a and b.
    """
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def octile_heuristic(a, b):
    """
    Calculate the Octile distance between two points.

    Args:
        a (tuple): The first point as a tuple of (x, y) coordinates.
        b (tuple): The second point as a tuple of (x, y) coordinates.

    Returns:
        float: The Octile distance between points a and b.
    """
    dx = abs(b[0] - a[0])
    dy = abs(b[1] - a[1])
    return dx + dy + (np.sqrt(2) - 2) * min(dx, dy)


def is_valid(x, y, grid):
    """
    Check if a given cell (x, y) is valid within the grid.

    A cell is considered valid if:
    - It is within the bounds of the grid.
    - The value at the cell is 0.

    Args:
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.
        grid (numpy.ndarray): The grid to check against.

    Returns:
        bool: True if the cell is valid, False otherwise.
    """
    return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1] and grid[x, y] == 0


def astar(grid, start, goal):
    """
    Perform the A* pathfinding algorithm to find the shortest path from start to goal in a grid.
    Args:
        grid (np.array): The grid representing the map where the pathfinding is performed.
        start (tuple of int): The starting position in the grid (x, y).
        goal (tuple of int): The goal position in the grid (x, y).
    Returns:
        tuple: A tuple containing:
            - list of tuple of int: The path from start to goal as a list of positions (x, y).
            - int: The length of the path.
    Notes:
        - The grid is assumed to be a 2D list where each element represents a cell.
        - The function uses a heuristic based on the Euclidean distance to estimate the cost from the current node to the goal.
        - The function draws the grid at intervals if DRAW_IN_PROGRESS is set to True and DRAWING_FREQ is defined.
        - The function returns an empty list and a path length of 0 if no path is found.
    """

    # Get the neighbors of a node
    def get_neighbors(node):
        """
        Given a node, returns a list of valid neighboring nodes.

        Args:
            node (tuple): A tuple representing the coordinates of the current node (x, y).

        Returns:
            list: A list of tuples, each representing the coordinates of a valid neighboring node.

        The function iterates over a predefined set of directions (DIRECTIONS) and calculates
        the coordinates of neighboring nodes. It then checks if each neighboring node is valid
        using the is_valid function. Valid neighbors are added to the result list.
        """
        result = []
        for direction in DIRECTIONS:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if is_valid(neighbor[0], neighbor[1], grid):
                result.append(neighbor)
        return result

    visited_nodes = set()  # Nodes already evaluated
    unexplored_nodes = {start}  # Nodes to be evaluated
    came_from = {}  # Previous node for reconstructing the path

    g_score = {start: 0}  # Cost from start along best path
    f_score = {
        start: octile_heuristic(start, goal)
    }  # Estimated total cost from start to goal
    drawingcounter = 0

    while unexplored_nodes:
        current = min(unexplored_nodes, key=lambda x: f_score[x])
        drawingcounter = drawingcounter + 1
        if current == goal:
            path_lenght = g_score[goal]
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], path_lenght

        if DRAW_IN_PROGRESS and drawingcounter % DRAWING_FREQ == 0:
            draw_grid(
                grid,
                path=list(visited_nodes),
                path_color=(66, 66, 66),
                start=start,
                goal=goal,
            )
            drawingcounter = 0

        unexplored_nodes.remove(current)
        visited_nodes.add(current)

        for neighbor in get_neighbors(current):
            if neighbor in visited_nodes:
                continue

            # The distance from start to a neighbor
            if abs(neighbor[0] - current[0]) + abs(neighbor[1] - current[1]) == 2:
                new_g_score = g_score[current] + np.sqrt(2)
            else:
                new_g_score = g_score[current] + 1

            if neighbor not in unexplored_nodes:
                unexplored_nodes.add(neighbor)
            elif new_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = new_g_score
            f_score[neighbor] = g_score[neighbor] + octile_heuristic(neighbor, goal)

    return [], 0  # No path found


def jps(grid, start, goal):

    def parent_of_node(node, direction):
        return (node[0] - direction[0], node[1] - direction[1])

    def step(grid, node, direction, goal):
        ns = prune(grid, node, direction)
        jumps = []
        stack = [(node, (n[0] - node[0], n[1] - node[1])) for n in ns]
        visited = set()
        while stack:
            current_node, current_direction = stack.pop()
            if current_node in visited:
                continue
            visited.add(current_node)
            jump_point = jump(grid, current_node, current_direction, goal)
            if jump_point is not None:
                jumps.append(jump_point)
                new_ns = prune(grid, jump_point, current_direction)
                stack.extend(
                    [
                        (jump_point, (n[0] - jump_point[0], n[1] - jump_point[1]))
                        for n in new_ns
                    ]
                )
        return jumps

    def prune(grid, node, direction):
        result = {}
        for direction in DIRECTIONS:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if is_valid(neighbor[0], neighbor[1], grid):
                result.update({neighbor: direction})

        if direction is not None:
            result.pop(parent_of_node(node, direction), None)
            return result
        return result

    def jump(grid, from_pos, direction, goal):
        x, y = from_pos
        dx, dy = direction
        next_pos = (x + dx, y + dy)
        while is_valid(next_pos[0], next_pos[1], grid):
            if next_pos == goal:
                return next_pos
            if forced_neighbors(next_pos, direction):
                return next_pos
            if dx != 0 and dy != 0:
                if step(grid, next_pos, (dx, 0), goal) or step(
                    grid, next_pos, (0, dy), goal
                ):
                    return next_pos
            nx, ny = next_pos
            next_pos = (nx + dx, ny + dy)
        return None

    def forced_neighbors(from_pos, direction):
        x, y = from_pos
        dx, dy = direction
        forced = []

        if dy == 0:
            if is_valid(x, y - 1, grid):
                forced.append((x + dx, y - 1))
            if is_valid(x, y + 1, grid):
                forced.append((x + dx, y + 1))
        elif dx == 0:
            if is_valid(x - 1, y, grid):
                forced.append((x - 1, y + dy))
            if is_valid(x + 1, y, grid):
                forced.append((x + 1, y + dy))
        else:
            if is_valid(x - dx, y, grid):
                forced.append((x - dx, y + dy))
            if is_valid(x, y - dy, grid):
                forced.append((x + dx, y - dy))

        return forced

    unexplored_nodes = PriorityQueue()
    unexplored_nodes.put((octile_heuristic(start, goal), start))
    came_from = {}
    g_score = {start: 0}  # Cost from start along best path

    drawingcounter = 0

    while unexplored_nodes:
        _, current = unexplored_nodes.get()
        # print(f"current: {current}")
        drawingcounter += 1
        if DRAW_IN_PROGRESS and drawingcounter % DRAWING_FREQ == 0:
            draw_grid(
                grid,
                path=came_from,
                path_color=(66, 66, 66),
                start=start,
                goal=goal,
            )
            pygame.time.wait(500)

        if current == goal:
            path = []
            path_length = g_score[goal]
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            # print("path found", list(reversed(path)))
            return list(reversed(path)), path_length

        neighbors = prune(grid, current, None)
        for neighbor in neighbors:
            # print(f"neighbor: {neighbor}")
            jump_point = jump(grid, current, neighbors[neighbor], goal)

            if jump_point is None:
                continue
            move = abs(jump_point[0] - current[0]) + abs(jump_point[1] - current[1])
            if move % 2 == 0:
                new_g_score = g_score[current] + np.sqrt(2)
            else:
                new_g_score = g_score[current] + 1

            new_cost = g_score[current] + octile_heuristic(current, jump_point)
            if jump_point not in g_score or new_cost < g_score[jump_point]:
                g_score[jump_point] = new_cost
                priority = new_g_score + octile_heuristic(jump_point, goal)
                unexplored_nodes.put((priority, jump_point))
                came_from[jump_point] = current

    return [], 0  # No path found
