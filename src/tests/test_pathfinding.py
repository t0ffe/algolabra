import random

import pytest

from helpers import convert_map_to_grid
from pathfinding import astar, is_valid, jps, octile_heuristic


# Create a fixture for the grid
@pytest.fixture
def grid():
    grid, _, _ = convert_map_to_grid()
    yield grid


# Create a fixture for the valid start and goal positions
@pytest.fixture
def create_valid_start_goal(grid):
    def _create_valid_start_goal():
        start = random.choice(
            [(x, y) for x in range(len(grid[0])) for y in range(len(grid))]
        )
        while not is_valid(start[0], start[1], grid):
            start = random.choice(
                [(x, y) for x in range(len(grid[0])) for y in range(len(grid))]
            )

        goal = random.choice(
            [(x, y) for x in range(len(grid[0])) for y in range(len(grid))]
        )
        while not is_valid(goal[0], goal[1], grid) or goal == start:
            goal = random.choice(
                [(x, y) for x in range(len(grid[0])) for y in range(len(grid))]
            )
        return start, goal

    yield _create_valid_start_goal


def test_is_valid(grid):
    assert is_valid(0, 0, grid) == False  # Obstacle
    assert is_valid(1, 1, grid) == True  # Valid
    assert is_valid(-1, -1, grid) == False  # Out of bounds


def test_octile_heuristic():
    assert octile_heuristic((0, 0), (1, 1)) == pytest.approx(1.41421356237)
    assert octile_heuristic((0, 0), (2, 2)) == pytest.approx(2.82842712475)
    assert octile_heuristic((0, 0), (1, 0)) == 1
    assert octile_heuristic((0, 0), (0, 1)) == 1


def test_astar_known_length_and_path(grid):
    start = (1, 1)
    goal = (7, 6)
    path, length = astar(grid, start, goal)
    expected_path = [
        (1, 1),
        (1, 2),
        (2, 3),
        (3, 3),
        (4, 3),
        (5, 4),
        (5, 5),
        (6, 6),
        (7, 6),
    ]
    assert path == expected_path
    assert length == pytest.approx(9.242640687119286)


def test_jps_known_length_and_path(grid):
    start = (1, 1)
    goal = (7, 6)
    path, length = jps(grid, start, goal)
    expected_path = [(1, 1), (5, 1), (5, 3), (5, 5), (6, 6), (7, 6)]
    assert path == expected_path
    assert length == pytest.approx(10.414213562373096)


def test_astar_no_path(grid):
    start = (-1, -1)
    goal = (-2, -2)
    path, length = astar(grid, start, goal)
    assert path == []
    assert length == 0


def test_jps_no_path(grid):
    start = (-1, -1)
    goal = (-2, -2)
    path, length = jps(grid, start, goal)
    assert path == []
    assert length == 0


def test_astar_same_start_goal(grid):
    start = (1, 1)
    goal = (1, 1)
    path, length = astar(grid, start, goal)
    assert path == [(1, 1)]
    assert length == 0


def test_jps_same_start_goal(grid):
    start = (1, 1)
    goal = (1, 1)
    path, length = jps(grid, start, goal)
    assert path == [(1, 1)]
    assert length == 0


def test_astar_random_valid_not_same_goal_and_start(grid, create_valid_start_goal):
    start, goal = create_valid_start_goal()
    path, length = astar(grid, start, goal)

    if start == (13, 8) or goal == (13, 8):  # This is a dead end on the test.map
        assert path == []
        assert length == 0
    else:
        assert path != []
        assert length != 0


def test_astar_100_random_valid_not_same_goal_and_start(grid, create_valid_start_goal):
    for _ in range(100):
        start, goal = create_valid_start_goal()
        path, length = astar(grid, start, goal)

        if start == (13, 8) or goal == (13, 8):  # This is a dead end on the test.map
            assert path == []
            assert length == 0
        else:
            assert path != []
            assert length != 0


def test_jps_100_random_valid_not_same_goal_and_start(grid, create_valid_start_goal):
    for _ in range(100):
        start, goal = create_valid_start_goal()
        path, length = jps(grid, start, goal)

        if start == (13, 8) or goal == (13, 8):  # This is a dead end on the test.map
            assert path == []
            assert length == 0
        else:
            assert path != []
            assert length != 0


def test_astar_and_jps_same_length(grid):
    start = (1, 1)
    goal = (7, 6)
    astar_path, astar_length = astar(grid, start, goal)
    jps_path, jps_length = jps(grid, start, goal)
    assert astar_length == jps_length


if __name__ == "__main__":
    pytest.main()
