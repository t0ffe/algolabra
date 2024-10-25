from queue import PriorityQueue

import numpy as np

from settings import DRAW_IN_PROGRESS, DRAWING_FREQ
from ui import draw_grid

DIRECTIONS = [
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
    (-1, 0),  # up
    (-1, -1),  # up-left
    (-1, 1),  # up-right
    (1, 1),  # down-right
    (1, -1),  # down-left
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

        if current == goal:
            path_lenght = g_score[goal]
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], len(path)

        drawingcounter += 1
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

    if start == goal:
        return [start], 0
    if not is_valid(start[0], start[1], grid) or not is_valid(goal[0], goal[1], grid):
        return [], 0  # No path found

    class PathFound(Exception):
        pass

    def jump(node):
        if node is not None:
            unexplored_nodes.put((octile_heuristic(node, goal), node))

    def step_cardinal(node, direction, cost):

        current_x, current_y = node
        current_cost = cost

        while True:

            current_x += direction[0]
            current_y += direction[1]
            current_cost += 1

            if (current_x, current_y) == goal:
                came_from[(current_x, current_y)] = node
                g_score[(current_x, current_y)] = current_cost
                raise PathFound()
            else:
                pass
            if not is_valid(current_x, current_y, grid):
                return None
            if (current_x, current_y) in came_from:
                return None
            if (current_x, current_y) not in g_score:
                g_score[(current_x, current_y)] = current_cost
                came_from[(current_x, current_y)] = node

            if direction[0] == 0:
                if not is_valid(current_x + 1, current_y, grid) and is_valid(
                    current_x + 1, current_y + direction[1], grid
                ):
                    return current_x, current_y
                if not is_valid(current_x - 1, current_y, grid) and is_valid(
                    current_x - 1, current_y + direction[1], grid
                ):
                    return current_x, current_y
            elif direction[1] == 0:
                if not is_valid(current_x, current_y + 1, grid) and is_valid(
                    current_x + direction[0], current_y + 1, grid
                ):
                    return current_x, current_y
                if not is_valid(current_x, current_y - 1, grid) and is_valid(
                    current_x + direction[0], current_y - 1, grid
                ):
                    return current_x, current_y

    def step_diagonal(node, direction, cost):

        current_x, current_y = node
        current_cost = cost

        while True:
            current_x += direction[0]
            current_y += direction[1]
            current_cost += 1

            if (current_x, current_y) == goal:
                came_from[(current_x, current_y)] = node
                g_score[(current_x, current_y)] = current_cost
                raise PathFound()
            else:
                pass
            if not is_valid(current_x, current_y, grid):
                return None
            if (current_x, current_y) in came_from:
                return None
            if (current_x, current_y) not in g_score:
                g_score[(current_x, current_y)] = current_cost
                came_from[(current_x, current_y)] = node

            if not is_valid(current_x + direction[0], current_y, grid) and is_valid(
                current_x + direction[0], current_y + direction[1], grid
            ):
                return current_x, current_y
            else:
                jump(
                    step_cardinal(
                        (current_x, current_y), (direction[0], 0), current_cost
                    )
                )

            if not is_valid(current_x, current_y + direction[1], grid) and is_valid(
                current_x + direction[0], current_y + direction[1], grid
            ):
                return current_x, current_y
            else:
                jump(
                    step_cardinal(
                        (current_x, current_y), (0, direction[1]), current_cost
                    )
                )

    unexplored_nodes = PriorityQueue()
    unexplored_nodes.put((octile_heuristic(start, goal), start))
    came_from = {}
    g_score = {start: 0}  # Cost from start along best path

    jump(start)

    while unexplored_nodes:
        cost, current = unexplored_nodes.get()
        if DRAW_IN_PROGRESS:
            draw_grid(
                grid,
                path=came_from,
                path_color=(66, 66, 66),
                start=start,
                goal=goal,
            )
        for direction in range(8):
            try:
                if direction < 4:
                    jump(step_cardinal(current, DIRECTIONS[direction], cost))
                else:
                    jump(step_diagonal(current, DIRECTIONS[direction], cost))
            except PathFound:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return reconstruct_full_jps_path(list(reversed(path))), len(
                    reconstruct_full_jps_path(list(reversed(path)))
                )
        if unexplored_nodes.empty():
            break
    return [], 0  # No path found


def reconstruct_full_jps_path(path):
    if path == []:
        return []

    cur_x, cur_y = path[0]
    result = [(cur_x, cur_y)]
    for i in range(len(path) - 1):
        while cur_x != path[i + 1][0] or cur_y != path[i + 1][1]:
            cur_x += determine_direction(path[i + 1][0] - path[i][0])
            cur_y += determine_direction(path[i + 1][1] - path[i][1])
            result.append((cur_x, cur_y))
    return result


def determine_direction(jump):
    if jump > 0:
        return 1
    elif jump < 0:
        return -1
    else:
        return 0
