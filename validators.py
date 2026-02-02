"""
Maze validators.

This file contains sanity checks that verify the maze structure:
- wall coherence between neighboring cells
- border walls are closed
- all cells are reachable from the entry (connectivity)

Validators should not modify the maze.
"""

from __future__ import annotations

from enum import Enum
from .maze_files import direction_definitions as dirdef
from .maze_files import wall_operations as wo
from .maze_files.maze_definitions import Maze


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


def wall_validator(maze: Maze) -> None:
    """
    Check that shared walls match between neighbors (E/W and N/S).
    Raises:
        ValueError: if any shared wall is inconsistent between neighbors.
    """

    def check_shared_wall(x: int, y: int, direction: str, neg_x: int,
                          neg_y: int, opposite: str) -> None:
        """Check coherence between (x,y) in `direction` and neighbor
        (neg_x,neg_y) in `opposite`."""

        # Read the wall mask of the current and neighbor cells
        current_cell = maze.grid[y][x]
        neighbor_cell = maze.grid[neg_y][neg_x]

        # Get bit values for direction and opposite direction walls
        dir_bit = dirdef.DIR_BIT_VALUE[direction]
        opp_bit = dirdef.DIR_BIT_VALUE[opposite]

        current_wall_closed = wo.is_it_solid_wall(current_cell, dir_bit)
        neighbor_wall_closed = wo.is_it_solid_wall(neighbor_cell, opp_bit)

        # Coherence means they must match: both closed OR both open.
        if current_wall_closed != neighbor_wall_closed:
            raise ValueError(
                f"{C.BG_RED}Error:{C.RESET} Wall sharing mismatch:\n"
                f"current_cell (x={x}, y={y}):\n"
                f"current_bit_mask={current_cell}\n"
                f"direction={direction}\n"
                f"closed={current_wall_closed}\n\n"
                f"neighbor_cell(x={neg_x}, y={neg_y}):\n"
                f"mask={neighbor_cell}\n"
                f"direction={opposite}\n"
                f"closed={neighbor_wall_closed}"
            )

    for y in range(maze.height):
        for x in range(maze.width):

            # Check East neighbor (x+1, y) if it exists
            if x + 1 < maze.width:
                check_shared_wall(x, y, "E", x + 1, y, "W")

            # Check South neighbor (x, y+1) if it exists
            if y + 1 < maze.height:
                check_shared_wall(x, y, "S", x, y + 1, "N")


def bfs_connection_validator(maze: Maze, forbidden_cells: set) -> None:
    """Check connectivity of the maze using BFS from the entry.

    Raises:
        ValueError: if not all cells are reachable from the entry.

    Assumes that an open wall means movement is allowed between cells.
    """
    # List of visited coordinates to avoid revisiting
    visited_coords = []
    visited_coords.append(maze.entry)

    # Queue of coordinates to visit, starting from entry
    coords_to_visit = []
    coords_to_visit.append(maze.entry)

    while len(coords_to_visit) != 0:
        current_cell = coords_to_visit[0]
        x, y = current_cell
        # Check if walls are solid (True) or open (False)
        north_wall = wo.is_it_solid_wall(maze.grid[y][x], 1)
        east_wall = wo.is_it_solid_wall(maze.grid[y][x], 2)
        south_wall = wo.is_it_solid_wall(maze.grid[y][x], 4)
        west_wall = wo.is_it_solid_wall(maze.grid[y][x], 8)
        if y - 1 >= 0 and north_wall is False:
            nx = x
            ny = y - 1
            north_neighbor = (nx, ny)
            if (north_neighbor not in visited_coords and
                    north_neighbor not in forbidden_cells):
                visited_coords.append(north_neighbor)
                coords_to_visit.append(north_neighbor)
        if x + 1 < maze.width and east_wall is False:
            nx = x + 1
            ny = y
            east_neighbor = (nx, ny)
            if (east_neighbor not in visited_coords and
                    east_neighbor not in forbidden_cells):
                visited_coords.append(east_neighbor)
                coords_to_visit.append(east_neighbor)
        if y + 1 < maze.height and south_wall is False:
            nx = x
            ny = y + 1
            south_neighbor = (nx, ny)
            if (south_neighbor not in visited_coords and
                    south_neighbor not in forbidden_cells):
                visited_coords.append(south_neighbor)
                coords_to_visit.append(south_neighbor)
        if x - 1 >= 0 and west_wall is False:
            nx = x - 1
            ny = y
            west_neighbor = (nx, ny)
            if (west_neighbor not in visited_coords and
                    west_neighbor not in forbidden_cells):
                visited_coords.append(west_neighbor)
                coords_to_visit.append(west_neighbor)
        # Remove the first element to maintain FIFO queue behavior
        # (not a stack)
        coords_to_visit.pop(0)


def closed_borders_validator(maze: Maze) -> None:
    """Check that the outer border walls of the maze are all closed.

    Checks each outer border:
    - top row for North walls
    - left column for West walls
    - bottom row for South walls
    - right column for East walls

    Raises:
        ValueError: on the first found open border wall.
    """
    # Check top border (North walls)
    y = 0
    for x in range(maze.width):
        current_cell_mask = maze.grid[0][x]
        if wo.is_it_solid_wall(current_cell_mask, 1) is False:
            raise ValueError(f"Unclosed border wall on direction N"
                             f"at coord ({x}, {y})")
    # Check left border (West walls)
    x = 0
    for y in range(maze.height):
        current_cell_mask = maze.grid[y][0]
        if wo.is_it_solid_wall(current_cell_mask, 8) is False:
            raise ValueError(f"Unclosed border wall on direction W"
                             f"at coord ({x}, {y})")
    # Check bottom border (South walls)
    y = maze.height - 1
    for x in range(maze.width):
        current_cell_mask = maze.grid[maze.height - 1][x]
        if wo.is_it_solid_wall(current_cell_mask, 4) is False:
            raise ValueError(f"Unclosed border wall on direction S"
                             f"at coord ({x}, {y})")
    # Check right border (East walls)
    x = maze.width - 1
    for y in range(maze.height):
        current_cell_mask = maze.grid[y][maze.width - 1]
        if wo.is_it_solid_wall(current_cell_mask, 2) is False:
            raise ValueError(f"Unclosed border wall on direction E"
                             f"at coord ({x}, {y})")
