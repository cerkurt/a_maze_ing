"""
Direction and movement definitions for the maze.

This module defines:
- Direction letters (N, E, S, W)
- Bit values used for wall masks
- Opposite direction mappings
- Movement deltas for grid navigation

This file is intentionally independent of the Maze class
and contains only static direction-related utilities.
"""

from enum import Enum


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


# capital letters are used for the values that should never change! in this
# case, the dictionaries below are not variables THEY ARE CONSTANTS.

# Canonical order of directions used throughout the project.
DIRECTIONS: tuple[str, ...] = ("N", "E", "S", "W")

# Bitmask values representing walls in each direction.
DIR_BIT_VALUE: dict[str, int] = {
    "N": 1,
    "E": 2,
    "S": 4,
    "W": 8
}

# Mapping each direction to its opposite wall direction.
DIR_OPPOSITE: dict[str, str] = {
    "N": "S",
    "E": "W",
    "S": "N",
    "W": "E"
}

# Movement deltas for grid navigation: x increases to the right, y increases
# downward.
DIR_MOVE_DELTA: dict[str, tuple[int, int]] = {
    "N": (0, -1),
    "E": (+1, 0),
    "S": (0, +1),
    "W": (-1, 0)
}


def walls_to_bits(direction: str) -> int:
    """
    Get the bit value representing a wall in the given direction.

    Args:
        One of "N", "E", "S", or "W".

    Returns:
        The integer bitmask for that direction.

    Raises:
        ValueError: If direction is invalid.
    """
    if direction not in DIR_BIT_VALUE:
        raise ValueError(f"{C.BG_RED}Invalid direction:{C.RESET}"
                         f" {direction!r}. "
                         f"Expected directions are one of: N, E, S, W.")
    return DIR_BIT_VALUE[direction]


def opposite_wall(direction: str) -> str:
    """
    Return the opposite wall direction of the given direction.

    Args:
        One of "N", "E", "S", or "W".

    Retuns:
        Opposite direction letter.

    Raises:
        ValueError: If direction is invalid.
    """
    if direction not in DIR_OPPOSITE:
        raise ValueError(f"{C.BG_RED}Invalid direction:{C.RESET}"
                         f" {direction!r}. "
                         f"Expected directions are one of: N, E, S, W.")
    return DIR_OPPOSITE[direction]


def move_delta(direction: str) -> tuple[int, int]:
    """
    Return the (dx, dy) movement delta for a step in the given direction on
    the grid.

    Args:
        One of "N", "E", "S", or "W".

    Returns:
        Tuple (dx, dy) representing the movement offset.

    Raises:
        ValueError: If direction is invalid.
    """
    if direction not in DIR_MOVE_DELTA:
        raise ValueError(f"{C.BG_RED}Invalid direction:{C.RESET}"
                         f" {direction!r}. "
                         f"Expected directions are one of: N, E, S, W.")
    return DIR_MOVE_DELTA[direction]
