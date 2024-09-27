import time

import pygame

from helpers import convert_map_to_grid
from pathfinding import astar, create_grid, jps
from settings import A_STAR_COLOR, BUTTON_HEIGHT, BUTTON_WIDTH, JPS_COLOR, TILE_SIZE
from ui import draw_button, draw_grid, handle_mouse_click, set_screen


class App:
    def run(self):
        pygame.init()
        grid, width, height = convert_map_to_grid()
        comparison_started = False

        button_rect = pygame.Rect(
            (width * TILE_SIZE - BUTTON_WIDTH) // 2,
            height * TILE_SIZE + 10,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
        )

        draw_grid(grid)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif pygame.mouse.get_pressed()[0]:
                    on_button, start_pos = handle_mouse_click(
                        pygame.mouse.get_pos(), grid, button_rect, 0
                    )
                    if on_button:
                        comparison_started = True
                    else:
                        start = start_pos
                        print(start)
                elif pygame.mouse.get_pressed()[2]:
                    on_button, goal = handle_mouse_click(
                        pygame.mouse.get_pos(), grid, button_rect, 1
                    )
                    print(goal)

            if comparison_started:
                astar_path, astar_time, astar_length = self.run_algorithm(
                    astar, grid, start, goal
                )
                jps_path, jps_time, jps_length = self.run_algorithm(
                    jps, grid, start, goal
                )

                print("Comparison Results:")
                print(f"A* Path Length: {astar_length}")
                print(f"A* Time: {astar_time:.4f} seconds")
                print(f"JPS Path Length: {jps_length}")
                print(f"JPS Time: {jps_time:.4f} seconds")
                print("JPS is faster" if jps_time < astar_time else "A* is faster")

                comparison_started = False
                self.draw_paths(grid, astar_path, jps_path)

            mouse_pos = pygame.mouse.get_pos()
            is_hovering_button = button_rect.collidepoint(mouse_pos)

            draw_button(button_rect, is_hovering_button)

    def run_algorithm(self, algorithm, grid, start, goal):
        start_time = time.process_time()
        path, path_length = algorithm(grid, start, goal)
        elapsed_time = time.process_time() - start_time
        return path, elapsed_time, path_length

    def draw_paths(self, grid, astar_path, jps_path):
        if jps_path:
            draw_grid(grid, jps_path, JPS_COLOR)
        if astar_path:
            draw_grid(grid, astar_path, A_STAR_COLOR)
