import numpy as np
import pytest

from pathfinding import astar, create_grid, jps


def test_create_grid():
    width, height = 5, 5
    obstacles = [(1, 1), (2, 2), (3, 3)]
    grid = create_grid(width, height, obstacles)
    assert grid.shape == (width, height)
    for x, y in obstacles:
        assert grid[x, y] == 1
    assert grid[0, 0] == 0
    assert grid[0, 1] == 0
    assert grid[4, 4] == 0
    assert grid[2, 2] == 1
    assert grid[3, 3] == 1
    assert grid[1, 1] == 1


def test_astar_simple_path():
    width, height = 5, 5
    obstacles = [(1, 1), (2, 2), (3, 3)]
    grid = create_grid(width, height, obstacles)
    start = (0, 0)
    goal = (4, 4)
    path = astar(grid, start, goal)
    expected_path = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 3),
        (2, 3),
        (2, 4),
        (3, 4),
        (4, 4),
    ]
    assert path == expected_path


def test_astar_with_obstacles():
    width, height = 5, 5
    start = (0, 0)
    goal = (4, 4)
    grid_with_obstacles = create_grid(width, height, [(1, 0), (1, 1), (1, 2), (1, 3)])
    path = astar(grid_with_obstacles, start, goal)
    expected_path = [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (1, 4),
        (2, 4),
        (3, 4),
        (4, 4),
    ]
    assert path == expected_path


def test_astar_no_path():
    width, height = 5, 5
    start = (0, 0)
    goal = (4, 4)
    grid_with_no_path = create_grid(
        width, height, [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (0, 1), (2, 0)]
    )
    path = astar(grid_with_no_path, start, goal)
    assert path == []


def test_astar_start_is_goal():
    width, height = 5, 5
    obstacles = [(1, 1), (2, 2), (3, 3)]
    grid = create_grid(width, height, obstacles)
    start = (2, 2)
    goal = (2, 2)
    path = astar(grid, start, goal)
    expected_path = [(2, 2)]
    assert path == expected_path
