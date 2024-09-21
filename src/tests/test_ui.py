from tkinter import W

import numpy as np
import pygame
import pytest

from settings import (
    BUTTON_COLOR,
    BUTTON_HEIGHT,
    BUTTON_HOVER_COLOR,
    GRID_COLOR,
    HEIGHT,
    TILE_SIZE,
    WIDTH,
)
from ui import draw_button, draw_grid, handle_mouse_click, set_screen


@pytest.fixture
def screen():
    pygame.init()
    screen = pygame.display.set_mode(
        ((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE + BUTTON_HEIGHT))
    )
    yield screen
    pygame.quit()


def test_draw_grid(screen):
    grid = np.zeros((10, 10))
    draw_grid(screen, grid, start=None, goal=None, path=None, path_color=None)
    # Check if the grid is drawn correctly
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = screen.get_at((rect.x + TILE_SIZE // 2, rect.y + TILE_SIZE // 2))
            assert color == pygame.Color(*GRID_COLOR)


def test_draw_button(screen):
    screen = pygame.Surface((400, 300))
    button_rect = pygame.Rect(100, 100, 200, 50)

    # Check if the button is drawn correctly
    draw_button(screen, button_rect, is_hovered=False)
    color = screen.get_at((button_rect.x + 1, button_rect.y + 1))
    assert color == pygame.Color(*BUTTON_COLOR)

    # Check if the button is drawn correctly when hovered
    draw_button(screen, button_rect, is_hovered=True)
    color = screen.get_at((button_rect.x + 1, button_rect.y + 1))
    assert color == pygame.Color(*BUTTON_HOVER_COLOR)


def test_handle_mouse_click(screen):
    grid = np.zeros((10, 10))
    button_rect = pygame.Rect(100, 500, 200, 50)
    width, height = 10, 10

    # Click inside the grid
    pos = (50, 50)
    assert not handle_mouse_click(pos, grid, width, height, button_rect, screen)
    assert grid[2, 2] == 1  # Obstacle toggled

    # Click on the button
    pos = (150, 525)
    assert handle_mouse_click(pos, grid, width, height, button_rect, screen)


def test_set_screen():
    width, height = 10, 10
    screen = set_screen(width, height)

    # Check if the screen is correct size
    assert screen.get_size() == (width * TILE_SIZE, height * TILE_SIZE + BUTTON_HEIGHT)

    # Check if the window name is set correctly
    assert pygame.display.get_caption()[0] == "Pathfinding Algorithm Comparison"
