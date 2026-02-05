"""
maze_files package public interface.

This file defines the public API of the maze_files package by re-exporting
the most commonly used classes, constants, and helper functions from the
internal modules.

The goal is to allow users to import everything they need from a single place
(e.g. `from maze_files import Maze, DIRECTIONS, carve_coordinate`) without
having to know the internal file structure.

Only symbols listed in __all__ are considered part of the stable public API.
"""

# Direction constants and helpers: describe movement, walls, and direction
# logic.
from .direction_definitions import (
    DIRECTIONS,
    DIR_BIT_VALUE,
    DIR_OPPOSITE,
    DIR_MOVE_DELTA,
    walls_to_bits,
    opposite_wall,
    move_delta,
)


# Core maze data structure.
from .maze_definitions import Maze


# Wall operations: low-level helpers for opening/closing walls and checking
# wall state.
from .wall_operations import (
    carve_coordinate,
    add_a_wall,
    remove_a_wall,
    is_it_solid_wall
)

# Explicitly define the public API surface of the package.
__all__ = [
    # direction_definitions
    "DIRECTIONS",
    "DIR_BIT_VALUE",
    "DIR_OPPOSITE",
    "DIR_MOVE_DELTA",
    "walls_to_bits",
    "opposite_wall",
    "move_delta",
    # maze_definitions
    "Maze",
    # wall_operations
    "carve_coordinate",
    "add_a_wall",
    "remove_a_wall",
    "is_it_solid_wall",
]
