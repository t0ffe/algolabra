import numpy as np

from ui import button_rect, handle_mouse_click, height, tile_size, width


def test_handle_mouse_click_inside_grid():
    pos = (tile_size // 2, tile_size // 2)
    grid = np.zeros((height, width))
    result = handle_mouse_click(pos, grid)
    assert result == (False, (0, 0))


def test_handle_mouse_click_on_obstacle():
    pos = (tile_size // 2, tile_size // 2)
    grid = np.zeros((height, width))
    grid[0, 0] = 1  # Set an obstacle at (0, 0)
    result = handle_mouse_click(pos, grid)
    assert result == (False, (-1, -1))


def test_handle_mouse_click_outside_grid():
    pos = (width * tile_size + 10, height * tile_size + 10)
    grid = np.zeros((height, width))
    result = handle_mouse_click(pos, grid)
    assert result == (False, (-1, -1))


def test_handle_mouse_click_on_valid_cell():
    pos = (tile_size * 2, tile_size * 2)
    grid = np.zeros((height, width))
    result = handle_mouse_click(pos, grid)
    assert result == (False, (2, 2))
