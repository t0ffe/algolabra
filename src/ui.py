import pygame

from helpers import convert_map_to_grid
from settings import (
    BUTTON_COLOR,
    BUTTON_HEIGHT,
    BUTTON_HOVER_COLOR,
    BUTTON_TEXT_COLOR,
    BUTTON_WIDTH,
    GOAL_COLOR,
    GRID_COLOR,
    OBSTACLE_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    START_COLOR,
)


def calculate_tile_size(width, height):
    """
    Calculate the optimal tile size for a given grid width and height.

    This function determines the optimal tile size that fits within
    the screen dimensions, taking into account the screen width and height,
    as well as the height of a button area.

    Args:
        width (int): The number of tiles along the width of the grid.
        height (int): The number of tiles along the height of the grid.

    Returns:
        int: The size of each tile in pixels, ensuring that the entire grid
             fits within the screen dimensions.
    """
    max_width_tile_size = SCREEN_WIDTH / width
    max_height_tile_size = (SCREEN_HEIGHT - BUTTON_HEIGHT) / height
    return int(min(max_width_tile_size, max_height_tile_size))


grid, height, width = convert_map_to_grid()
tile_size = calculate_tile_size(width, height)
button_rect = pygame.Rect(
    (height * tile_size - BUTTON_WIDTH) // 2,
    width * tile_size + 10,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)


def set_screen(height, width):
    """
    Initializes and sets up the display screen.

    Args:
        height (int): The height of the grid in tiles.
        width (int): The width of the grid in tiles.

    Returns:
        pygame.Surface: The initialized screen surface with the specified dimensions and background color.
    """
    screen = pygame.display.set_mode(
        (width * tile_size, height * tile_size + BUTTON_HEIGHT)
    )
    pygame.display.set_caption("Pathfinding Algorithm Comparison")
    screen.fill((0, 0, 0))  # Background color
    return screen


screen = set_screen(width, height)


def draw_grid(grid, path=None, path_color=(33, 33, 33), start=(-1, -1), goal=(-1, -1)):
    """
    Draws a grid with optional path, start, and goal points using Pygame.
    Args:
        grid (numpy.ndarray): A 2D array representing the grid where 1 indicates an obstacle and 0 indicates a free space.
        path (list of tuples, optional): A list of (x, y) tuples representing the path to be drawn. Defaults to None.
        path_color (tuple, optional): A tuple representing the RGB color of the path. Defaults to (33, 33, 33).
        start (tuple, optional): A tuple (x, y) representing the start point. Defaults to (-1, -1).
        goal (tuple, optional): A tuple (x, y) representing the goal point. Defaults to (-1, -1).
    Returns:
        None
    """
    # Draw the grid with obstacles
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            rect = pygame.Rect(y * tile_size, x * tile_size, tile_size, tile_size)
            if grid[x, y] == 1:
                pygame.draw.rect(screen, OBSTACLE_COLOR, rect)
            else:
                pygame.draw.rect(screen, GRID_COLOR, rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    # Draw start and goal points
    if start:
        rect = pygame.Rect(
            start[1] * tile_size, start[0] * tile_size, tile_size, tile_size
        )
        pygame.draw.rect(screen, START_COLOR, rect)

    if goal:
        rect = pygame.Rect(
            goal[1] * tile_size, goal[0] * tile_size, tile_size, tile_size
        )
        pygame.draw.rect(screen, GOAL_COLOR, rect)

    # Draw the path
    if path:
        for x, y in path:
            rect = pygame.Rect(y * tile_size, x * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, path_color, rect)

    pygame.display.update()


def draw_button():
    """
    Draws a button on the screen and updates its appearance based on mouse hover state.
    The button's color changes when the mouse hovers over it. The button displays the text "Run Pathfinding".
    Uses the following global variables:
    - screen: The pygame display surface where the button is drawn.
    - button_rect: The pygame Rect object defining the button's position and size.
    - BUTTON_COLOR: The color of the button when not hovered.
    - BUTTON_HOVER_COLOR: The color of the button when hovered.
    - BUTTON_TEXT_COLOR: The color of the text displayed on the button.
    This function does not take any parameters and does not return any values.
    """
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
    """
    Handles mouse click events on the grid and the "Run" button.
    Args:
        pos (tuple): A tuple (x, y) representing the position of the mouse click.
        grid (numpy.ndarray): A 2D array representing the grid where the algorithm operates.
    Returns:
        tuple: A tuple (bool, (int, int)) where the boolean indicates if the "Run" button was clicked,
               and the tuple (int, int) represents the coordinates of the grid cell that was clicked.
               If the click was on the "Run" button, the coordinates will be (-1, -1).
               If the click was outside the grid or on an invalid cell, the coordinates will be (-1, -1).
    """
    # Check if the click is on the "Run" button
    if button_rect.collidepoint(pos):
        return True, (-1, -1)

    # Check if the click is inside the grid
    x, y = pos[1] // tile_size, pos[0] // tile_size
    if 0 <= x < width and 0 <= y < height and grid[x, y] != 1:
        # start and goal points
        print("*click*", x, y)
        return False, (x, y)
    return False, (-1, -1)
