import pygame

from helpers import convert_map_to_grid
from settings import (
    BUTTON_COLOR,
    BUTTON_HEIGHT,
    BUTTON_HOVER_COLOR,
    BUTTON_TEXT_COLOR,
    BUTTON_WIDTH,
    GOAL,
    GOAL_COLOR,
    GRID_COLOR,
    OBSTACLE_COLOR,
    START,
    START_COLOR,
)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


def calculate_tile_size(width, height):
    max_width_tile_size = SCREEN_WIDTH / width
    max_height_tile_size = (SCREEN_HEIGHT - BUTTON_HEIGHT) / height
    return int(min(max_width_tile_size, max_height_tile_size))


grid, height, width = convert_map_to_grid()
TILE_SIZE = calculate_tile_size(width, height)
button_rect = pygame.Rect(
    (width * TILE_SIZE - BUTTON_WIDTH) // 2,
    height * TILE_SIZE + 10,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)


def set_screen(height, width):
    screen = pygame.display.set_mode(
        (width * TILE_SIZE, height * TILE_SIZE + BUTTON_HEIGHT)
    )
    pygame.display.set_caption("Pathfinding Algorithm Comparison")
    screen.fill((0, 0, 0))  # Background color
    return screen


screen = set_screen(width, height)


def draw_grid(grid, path=None, path_color=(33, 33, 33), start=START, goal=GOAL):
    # Draw the grid with obstacles
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            rect = pygame.Rect(y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if grid[x, y] == 1:
                pygame.draw.rect(screen, OBSTACLE_COLOR, rect)
            else:
                pygame.draw.rect(screen, GRID_COLOR, rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    # Draw start and goal points
    if start:
        rect = pygame.Rect(
            start[1] * TILE_SIZE, start[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE
        )
        pygame.draw.rect(screen, START_COLOR, rect)

    if goal:
        rect = pygame.Rect(
            goal[1] * TILE_SIZE, goal[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE
        )
        pygame.draw.rect(screen, GOAL_COLOR, rect)

    # Draw the path
    if path:
        for x, y in path:
            rect = pygame.Rect(y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, path_color, rect)

    pygame.display.update()


def draw_button():
    button_rect = pygame.Rect(
        (width * TILE_SIZE - BUTTON_WIDTH) // 2,
        height * TILE_SIZE + 10,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
    )
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = button_rect.collidepoint(mouse_pos)

    color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR

    pygame.draw.rect(screen, color, button_rect)

    font = pygame.font.Font(None, 36)
    text = font.render("Run Pathfinding", True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    pygame.display.update()


def handle_mouse_click(pos, grid):
    # Check if the click is on the "Run" button
    if button_rect.collidepoint(pos):
        return True, (0, 0)

    # Check if the click is inside the grid
    x, y = pos[1] // TILE_SIZE, pos[0] // TILE_SIZE
    if 0 <= x < width and 0 <= y < height:
        # start and goal points
        print("*click*", x, y)
        draw_grid(grid)
        return False, (x, y)
    return False, (0, 0)
