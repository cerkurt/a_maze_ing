"""
Maze data structure and basic validation utilities.
This file defines the Maze class and is intentionally kept free of wall
operations and pathfinding logic.
"""

from enum import Enum
from typing import List


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


class Maze:
    """
    Represents a rectangular grid maze.

    Each cell in the maze stores a wall bitmask (0–15) indicating which walls
    are present. The grid is indexed as grid[y][x], where y is the row and x
    is the column.
    """
    def __init__(self, height: int,
                 width: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int]) -> None:
        # Validate that width is positive; zero or negative widths are
        # invalid.
        if width <= 0:
            raise ValueError(f"{C.BG_RED}Error:{C.RESET} "
                             f"Width value cannot be 0 or negative.")
        # Validate that height is positive; zero or negative heights are
        # invalid.
        if height <= 0:
            raise ValueError(f"{C.BG_RED}Error:{C.RESET} "
                             f"Height value cannot be 0 or negative.")

        self.width = width
        self.height = height

        # Validate entry coordinate is within bounds.
        self.entry = self.coordinate_validation(entry, name="entry")
        # Validate exit coordinate is within bounds.
        self.exit = self.coordinate_validation(exit, name="exit")

        # Entry and exit points must not be the same, as that would invalidate
        # maze traversal.
        if self.entry == self.exit:
            raise ValueError(f"{C.BG_RED}Error:{C.RESET} "
                             f"Entry and exit points cannot be the same.")

        # Initialize the grid as a list of rows, each row is a list of cells.
        # Each cell is initialized to 15, representing all walls present
        # (bitmask 1111).
        self.grid: List[List[int]] = []
        for _ in range(self.height):
            row: List[int] = [15] * self.width
            self.grid.append(row)

    def is_in_bounds(self, coord: tuple[int, int]) -> bool:
        # Coordinates are in the form (x, y), where x is horizontal index and
        # y is vertical index.
        x, y = coord

        # Check horizontal bounds: x must be within [0, width-1].
        if x < 0:
            return False
        if x >= self.width:
            return False

        # Check vertical bounds: y must be within [0, height-1].
        # Height is checked against y because y corresponds to rows.
        if y < 0:
            return False
        if y >= self.height:
            return False

        # If none of the checks failed, the coordinate is valid and within
        # maze bounds.
        return True

    def coordinate_validation(self,
                              coord: tuple[int, int],
                              name: str = "coordinate") -> tuple[int, int]:
        """
        Validate that a coordinate is within the bounds of the maze.

        This function checks whether the given coordinate lies inside the maze
        grid.

        If the coordinate is out of bounds, it raises a ValueError with an
        error message indicating which coordinate (by name) is invalid.

        On success, it returns the validated coordinate unchanged.
        """
        x, y = coord
        if not self.is_in_bounds(coord):
            raise ValueError(f"{C.BG_RED}Error:{C.RESET} for {name} "
                             f"Given values are out of maze bounds.")
        return coord

    def entry_point(self, entry: tuple[int, int]) -> tuple[int, int]:
        # Thin wrapper for semantic clarity: validates and returns the entry
        # point.
        return self.coordinate_validation(entry, name="entry")

    def exit_point(self, exit: tuple[int, int]) -> tuple[int, int]:
        # Thin wrapper for semantic clarity: validates and returns the exit
        # point.
        return self.coordinate_validation(exit, name="exit")
