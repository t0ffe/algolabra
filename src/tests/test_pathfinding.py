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


def test_astar():
    # TODO: Implement the test for A* algorithm
    assert 1 == 1


def test_jps():
    # TODO: Implement the test for JPS algorithm
    assert 1 == 1
