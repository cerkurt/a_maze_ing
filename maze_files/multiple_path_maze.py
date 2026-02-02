"""
Imperfect maze helper (PERFECT=False).

This module modifies an already-generated perfect maze by opening a small
number of extra walls. This creates multiple possible routes (loops)
while keeping the maze connected.
"""

from __future__ import annotations
from enum import Enum
from . import wall_operations as wo
from . import direction_definitions as dirdef
from .maze_definitions import Maze
import random


class C(str, Enum):
    """ANSI color codes used to make terminal output easier to read."""
    RESET = "\033[0m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    RED = "\033[31m"
    BG_RED = "\033[41m"

    def __str__(self) -> str:
        return self.value


def check_neighbor_pair(maze, coord1: tuple, direction: str) -> bool:
    """
    Check if the wall in the given direction from coord1 is closed.

    Args:
        maze: The maze object containing the grid.
        coord1: Tuple (x, y) coordinates of the first cell.
        direction: Direction string ('N', 'E', 'S', 'W') to check.

    Returns:
        True if the wall in the specified direction from coord1 is closed
        (candidate for opening), False otherwise.
    """
    x1, y1 = coord1

    # Read the mask value from the maze grid at position (y, x)
    coord1_mask = maze.grid[y1][x1]
    # Check if the wall bit for the given direction is set (wall is closed)
    if wo.is_it_solid_wall(coord1_mask, dirdef.DIR_BIT_VALUE[direction]):
        return True
    else:
        return False


def multiple_path_maze(maze: Maze, forbidden_cells: set):
    """
    Modify a perfect maze to create an imperfect maze by opening extra walls.

    This implements the PERFECT=False option by opening K extra walls, where
    K is chosen as max(1, (width * height) // 25), scaling with maze size.
    It scans east and south neighbor pairs only to avoid duplicates.
    The maze.grid is mutated in-place to open walls and create loops.
    Randomness is used to pick which walls to open; callers should seed
    the random module for reproducibility.

    Args:
        maze: Maze object to be modified.
    """
    # Number of extra walls to open, scaling with maze size
    extra_paths = max(1, (maze.width * maze.height) // 25)

    # List of candidate cells to open walls between:
    # ((x, y), (nx, ny), direction)
    candidate_cells = []

    # Scan every cell in the maze
    for y in range(maze.height):
        for x in range(maze.width):
            # Check east neighbor if within bounds and wall is currently closed
            if x + 1 < maze.width:
                if (check_neighbor_pair(maze, (x, y), "E") is True and
                        (x, y) not in forbidden_cells and
                        (x + 1, y) not in forbidden_cells):
                    candidate_cells.append(((x, y), (x + 1, y), "E"))

            # Check south neighbor if within bounds and wall is currently
            # closed
            if y + 1 < maze.height:
                if (check_neighbor_pair(maze, (x, y), "S") is True and
                        (x, y) not in forbidden_cells and
                        (x, y + 1) not in forbidden_cells):
                    candidate_cells.append(((x, y), (x, y + 1), "S"))

    # Cannot open more walls than available candidates
    extra_paths = min(extra_paths, len(candidate_cells))

    # Open walls randomly from candidates to create multiple paths
    for paths in range(extra_paths):
        # Pick a random candidate index
        random_pick = random.randint(0, len(candidate_cells) - 1)
        carving_pair = candidate_cells[random_pick]

        # Remove the chosen candidate to avoid reopening the same wall
        candidate_cells.remove(carving_pair)
        # Open the wall between the two cells, keeping maze coherence
        wo.carve_coordinate(maze, carving_pair[0], carving_pair[1])
