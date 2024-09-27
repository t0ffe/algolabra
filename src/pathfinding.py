import numpy as np

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
DRAW_IN_PROGRESS = True


# Manhattan distance heuristic
def manhattan_heuristic(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


# Euclidean distance heuristic
def euclidean_heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def astar(grid, start, goal):

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

        if DRAW_IN_PROGRESS and drawingcounter % 2000 == 0:
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
    # TODO Implement the Jump Point Search algorithm
    return [], 0
