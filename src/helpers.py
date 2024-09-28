import numpy as np

from settings import MAP_FILE_PATH


def convert_map_to_grid():
    """
    Converts a map file to a grid representation.
    The map file should have the following format:
    - The first line contains the type information.
    - The second line contains the height of the map.
    - The third line contains the width of the map.
    - The fourth line is the 'map' line which is skipped.
    - The subsequent lines contain the map data where specific characters
      ('@', 'T', 'O', 'S', 'W') are converted to 1 in the grid, and all other
      characters are converted to 0.
    Returns:
        tuple: A tuple containing:
            - grid (numpy.ndarray): A 2D numpy array representing the map grid.
            - width (int): The width of the map.
            - height (int): The height of the map.
    """
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
