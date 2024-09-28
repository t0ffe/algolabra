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
    (1, -1),  # down-left
    (1, 1),  # down-right
]


# Manhattan distance heuristic
# def manhattan_heuristic(a, b):
#    return abs(b[0] - a[0]) + abs(b[1] - a[1])


# Euclidean distance heuristic
def euclidean_heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def is_valid(x, y, grid):
    return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1] and grid[x, y] == 0


def astar(grid, start, goal):

    # Get the neighbors of a node
    def get_neighbors(node):
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
        start: euclidean_heuristic(start, goal)
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
            f_score[neighbor] = g_score[neighbor] + euclidean_heuristic(neighbor, goal)

    return [], 0  # No path found


def jps(grid, start, goal):

    def parent_of_node(node, direction):
        return (node[0] - direction[0], node[1] - direction[1])

    def step(grid, node, direction, goal):
        ns = prune(grid, node, direction)
        jumps = [step(grid, node, (n[0] - node[0], n[1] - node[1]), goal) for n in ns]
        jumps = [j for j in jumps if j is not None]
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
    unexplored_nodes.put((euclidean_heuristic(start, goal), start))
    came_from = {}
    g_score = {start: 0}  # Cost from start along best path

    drawingcounter = 0

    while unexplored_nodes:
        _, current = unexplored_nodes.get()
        # print(f"current: {current}")
        drawingcounter = drawingcounter + 1
        if DRAW_IN_PROGRESS and drawingcounter % DRAWING_FREQ == 0:
            draw_grid(
                grid,
                path=came_from,
                path_color=(66, 66, 66),
                start=start,
                goal=goal,
            )

        if current == goal:
            path = []
            path_lenght = g_score[goal]
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            # print("path found", list(reversed(path)))

            return list(reversed(path)), path_lenght

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

            new_cost = g_score[current] + euclidean_heuristic(current, jump_point)
            if jump_point not in g_score or new_cost < g_score[jump_point]:
                g_score[jump_point] = new_cost
                priority = new_g_score + euclidean_heuristic(jump_point, goal)
                unexplored_nodes.put((priority, jump_point))
                came_from[jump_point] = current

    return [], 0  # No path found
