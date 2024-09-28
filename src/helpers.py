import numpy as np

from settings import MAP_FILE_PATH


def convert_map_to_grid():
    with open(MAP_FILE_PATH, "r") as file:
        # Read header information
        type_line = file.readline().strip()
        height = int(file.readline().split()[1])
        width = int(file.readline().split()[1])
        file.readline()  # Skip 'map' line

        # Initialize grid with zeros
        grid = np.zeros((height, width), dtype=int)

        # Process the map
        for y, line in enumerate(file):
            for x, char in enumerate(line.strip()):
                if (
                    char == "@"
                    or char == "T"
                    or char == "O"
                    or char == "S"
                    or char == "W"
                ):
                    grid[y, x] = 1

    return grid, width, height
