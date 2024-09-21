import time

import pygame

from pathfinding import astar, create_grid, jps
from settings import (
    A_STAR_COLOR,
    BUTTON_HEIGHT,
    BUTTON_WIDTH,
    GOAL,
    HEIGHT,
    JPS_COLOR,
    START,
    TILE_SIZE,
    WIDTH,
)
from ui import draw_button, draw_grid, handle_mouse_click, set_screen


class App:
    def run(self):
        pygame.init()
        grid = create_grid(WIDTH, HEIGHT, [])
        comparison_started = False

        button_rect = pygame.Rect(
            (WIDTH * TILE_SIZE - BUTTON_WIDTH) // 2,
            HEIGHT * TILE_SIZE + 10,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
        )

        draw_grid(grid)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if handle_mouse_click(pygame.mouse.get_pos(), grid, button_rect):
                        comparison_started = True

            if comparison_started:
                astar_path, astar_time = self.run_algorithm(astar, grid)
                jps_path, jps_time = self.run_algorithm(jps, grid)

                print("Comparison Results:")
                print(f"A* Path Length: {len(astar_path)}")
                print(f"A* Time: {astar_time:.4f} seconds")
                print(f"JPS Path Length: {len(jps_path)}")
                print(f"JPS Time: {jps_time:.4f} seconds")
                print("JPS is faster" if jps_time < astar_time else "A* is faster")

                comparison_started = False
                self.draw_paths(grid, astar_path, jps_path)

            mouse_pos = pygame.mouse.get_pos()
            is_hovering_button = button_rect.collidepoint(mouse_pos)

            draw_button(button_rect, is_hovering_button)

    def run_algorithm(self, algorithm, grid):
        start_time = time.process_time()
        path = algorithm(grid, START, GOAL)
        elapsed_time = time.process_time() - start_time
        return path, elapsed_time

    def draw_paths(self, grid, astar_path, jps_path):
        if jps_path:
            draw_grid(grid, jps_path, JPS_COLOR)
        if astar_path:
            draw_grid(grid, astar_path, A_STAR_COLOR)
