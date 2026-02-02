"""
Breadth-First Search (BFS) solver for the maze.
This module finds the shortest path from the maze entry to the maze exit using
BFS. The maze is treated as an unweighted graph where each cell is a node.
"""

from __future__ import annotations
from enum import Enum
from . import direction_definitions as dirdef
from . import wall_operations as wo
from .maze_definitions import Maze
from collections import deque


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


def bfs_shortest_path_solver(maze: Maze,
                             forbidden_cells: set) -> list[tuple[int, int]]:
    """
    Compute the shortest path from the maze entry to the exit using BFS.

    This function performs a breadth-first search to find the shortest path
    from the maze's entry point to its exit. BFS guarantees the shortest path
    in an unweighted graph like the maze grid.

    Returns:
        A list of (x, y) coordinates representing the shortest path.

    Raises:
        ValueError: If the exit is not reachable from the entry.
    """
    x, y = maze.entry

    # Set to keep track of visited coordinates to avoid revisiting
    visited_coords = set()
    visited_coords.add(maze.entry)

    # Queue for BFS traversal, stores coordinates to visit next
    coords_to_visit = deque()
    coords_to_visit.append(maze.entry)

    # Dictionary mapping each cell to its parent cell in the BFS tree
    # (child -> parent)
    path_family_tree = {}
    path_family_tree[maze.entry] = None

    while len(coords_to_visit) != 0:
        current_coord = coords_to_visit.popleft()
        x, y = current_coord
        current_cell_mask = maze.grid[y][x]

        # Stop BFS if we've reached the exit
        if current_coord == maze.exit:
            break

        # Explore neighbors in all possible directions
        for direction in dirdef.DIRECTIONS:
            dx, dy = dirdef.DIR_MOVE_DELTA[direction]
            nx = x + dx
            ny = y + dy

            # Check if neighbor is inside maze bounds
            if 0 <= nx < maze.width and 0 <= ny < maze.height:
                # Check if there is no solid wall blocking movement in this
                # direction
                if (wo.is_it_solid_wall(
                    current_cell_mask,
                    dirdef.DIR_BIT_VALUE[direction])
                        is False):
                    neighbor = nx, ny
                    # If neighbor not visited yet, add it to queue and record
                    # path
                    if (neighbor not in visited_coords and
                            neighbor not in forbidden_cells):
                        visited_coords.add(neighbor)
                        coords_to_visit.append(neighbor)
                        path_family_tree[neighbor] = current_coord

    if maze.exit not in path_family_tree:
        raise ValueError(f"{C.BG_RED}Error:{C.RESET} Exit is not reachable "
                         f"from the maze entry point.")

    # Reconstruct path by following parent links from exit back to entry
    else:
        last_spot = maze.exit
        backtrace = []
        while last_spot is not None:
            backtrace.append(last_spot)
            last_spot = path_family_tree[last_spot]

    # reverse because we collected it exit→entry
    result_path = list(reversed(backtrace))
    return result_path
