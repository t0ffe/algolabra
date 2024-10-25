import time

import pygame

from helpers import convert_map_to_grid
from pathfinding import astar, jps
from settings import A_STAR_COLOR, JPS_COLOR
from ui import draw_button, draw_grid, handle_mouse_click


class App:
    def run(self):
        """
        Initializes the Pygame environment, sets up the grid, and handles the main event loop for the application.
        The method listens for mouse clicks to set the start and goal positions on the grid.
        It also initiates the comparison of the A* and JPS pathfinding algorithms when a button on the screen is clicked.
        The results of the comparison, including path lengths and execution times, are printed to the console.
        The paths found by both algorithms are then drawn on the grid.

        Events handled:
            - Pygame QUIT event to exit the application.
            - Left mouse click to set the start position or initiate the comparison.
            - Right mouse click to set the goal position.
        The method also continuously updates the grid and button states.
        """
        pygame.init()
        grid, _, _ = convert_map_to_grid()
        comparison_started = False
        goal, start = None, None

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
                if goal is None or start is None:
                    print("Please set the start and goal positions on the grid.")
                    comparison_started = False
                    continue
                astar_path, astar_time, astar_length = self.run_algorithm(
                    astar, grid, start, goal
                )
                jps_path, jps_time, jps_length = self.run_algorithm(
                    jps, grid, start, goal
                )

                print("Comparison Results:")
                print(f"A* Path Length: {astar_length}")
                print(f"A* Time: {astar_time:.4f} seconds")
                # print(f"A* Path: {astar_path}")
                print(f"JPS Path Length: {jps_length}")
                print(f"JPS Time: {jps_time:.4f} seconds")
                # print(f"JPS Path: {jps_path}")
                print("JPS is faster" if jps_time < astar_time else "A* is faster")

                comparison_started = False
                self.draw_paths(grid, astar_path, jps_path)

            draw_button()

    def run_algorithm(self, algorithm, grid, start, goal):
        """
        Executes the given pathfinding algorithm on the provided grid.

        Args:
            algorithm (callable): The pathfinding algorithm to execute. It should take three arguments: grid, start, and goal.
            grid (list): The grid on which the pathfinding algorithm will be executed.
            start (tuple): The starting point coordinates (x, y) on the grid.
            goal (tuple): The goal point coordinates (x, y) on the grid.

        Returns:
            tuple: A tuple containing:
                - path (list): The path found by the algorithm from start to goal.
                - elapsed_time (float): The time taken to execute the algorithm.
                - path_length (int): The length of the path found by the algorithm.
        """
        start_time = time.process_time()
        path, path_length = algorithm(grid, start, goal)
        elapsed_time = time.process_time() - start_time
        return path, elapsed_time, path_length

    def draw_paths(self, grid, astar_path, jps_path):
        """
        Draws the paths on the grid.
        This function continuously listens for Pygame events and draws the given
        A* and JPS paths on the grid. It alternates between drawing the JPS path
        and the A* path with a delay of 500 milliseconds between each draw. The
        function stops drawing when the left mouse button is clicked or when the
        Pygame window is closed.
        Args:
            grid (list): The grid on which the paths will be drawn.
            astar_path (list): The path generated by the A* algorithm.
            jps_path (list): The path generated by the JPS algorithm.
        """
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
