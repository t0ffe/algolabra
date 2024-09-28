import time

import pygame

from helpers import convert_map_to_grid
from pathfinding import astar, jps
from settings import A_STAR_COLOR, JPS_COLOR
from ui import draw_button, draw_grid, handle_mouse_click


class App:
    def run(self):
        pygame.init()
        grid, _, _ = convert_map_to_grid()
        comparison_started = False

        draw_grid(grid)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif pygame.mouse.get_pressed()[0]:
                    on_button, start_pos = handle_mouse_click(
                        pygame.mouse.get_pos(), grid
                    )
                    if on_button:
                        comparison_started = True
                    else:
                        start = start_pos
                        draw_grid(grid, start=start)
                elif pygame.mouse.get_pressed()[2]:
                    on_button, goal = handle_mouse_click(pygame.mouse.get_pos(), grid)
                    draw_grid(grid, goal=goal)

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

            draw_button()

    def run_algorithm(self, algorithm, grid, start, goal):
        start_time = time.process_time()
        path, path_length = algorithm(grid, start, goal)
        elapsed_time = time.process_time() - start_time
        return path, elapsed_time, path_length

    def draw_paths(self, grid, astar_path, jps_path):
        comparing = True

        while comparing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif pygame.mouse.get_pressed()[0]:
                    comparing = False
            if not len(jps_path) == 0:
                draw_grid(grid, jps_path, JPS_COLOR)
            pygame.time.wait(500)
            if not len(astar_path) == 0:
                draw_grid(grid, astar_path, A_STAR_COLOR)
            pygame.time.wait(500)
