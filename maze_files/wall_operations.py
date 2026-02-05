"""
Wall operations for the maze.

This module contains helper functions to open and close walls using bitmask
operations, as well as a utility to carve a passage between two adjacent cells
while keeping wall coherence intact.
"""

from enum import Enum
from . import direction_definitions as dirdef
from .maze_definitions import Maze


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


def remove_a_wall(cell: int, direction: int) -> int:
    """
    Remove a wall by clearing its bit in the cell's bitmask.
    A wall bit of 1 means the wall is closed; 0 means open.
    This function sets the bit to 0 to open that wall.

    Example:
        cell=15 (1111, all walls closed)
        remove NORTH (1) -> 14 (1110, north open)
    """
    # Clear the wall bit to open the wall
    new_cell = cell & ~direction
    return new_cell


def add_a_wall(cell: int, direction: int) -> int:
    """
    Close a wall by setting its bit to 1 in the cell's bitmask.
    This is the opposite of remove_a_wall.
    """
    new_cell = cell | direction
    return new_cell


def is_it_solid_wall(cell: int, direction: int) -> bool:
    """
    Return True if the wall in the given direction is closed (bit=1),
    False if the wall is open (bit=0).

    Note:
        Each direction corresponds to one bit (N=1, E=2, S=4, W=8)
    """
    # Check if the wall bit is set in the cell mask
    wall_bit = cell & direction
    if wall_bit != 0:
        return True
    return False


def carve_coordinate(maze: "Maze", coord1: tuple[int, int],
                     coord2: tuple[int, int]) -> None:
    """
    Open the wall between two adjacent cells in the maze. Both cells are
    updated to remove the wall between them.

    Coordinates must be next to each other (adjacent).
    This function changes the maze grid in-place.
    """
    x1, y1 = coord1
    x2, y2 = coord2

    maze.coordinate_validation(coord1, name="coord1")
    maze.coordinate_validation(coord2, name="coord2")

    # Check that the two coordinates are adjacent (one step apart)
    if abs(x1 - x2) + abs(y1 - y2) != 1:
        raise ValueError(f"{C.BG_RED}Error:{C.RESET} For given coordinates "
                         f"{coord1}, {coord2} are not adjacent.")

    cell_A = maze.grid[y1][x1]
    cell_B = maze.grid[y2][x2]

    # Determine direction from coord1 to coord2
    direction = None
    if x2 == x1 + 1 and y2 == y1:
        direction = "E"
    elif x2 == x1 - 1 and y2 == y1:
        direction = "W"
    elif y2 == y1 - 1 and x1 == x2:
        direction = "N"
    elif y2 == y1 + 1 and x1 == x2:
        direction = "S"

    if direction is None:
        raise ValueError(f"{C.BG_RED}Internal error:{C.RESET} adjacent cells "
                         f"but direction could not be determined")

    bit_value = dirdef.walls_to_bits(direction)
    new_cell_A_bitmask = remove_a_wall(cell_A, bit_value)

    opposite_dir = dirdef.opposite_wall(direction)
    opposite_bit = dirdef.walls_to_bits(opposite_dir)
    new_cell_B_bitmask = remove_a_wall(cell_B, opposite_bit)

    # Update both cells to remove the wall between them
    maze.grid[y1][x1] = new_cell_A_bitmask
    maze.grid[y2][x2] = new_cell_B_bitmask

    return None
