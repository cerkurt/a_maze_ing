"""
Terminal ASCII visualization for maze structures and an optional UI loop.

This module provides functions to render mazes as ASCII art in the terminal,
optionally with color and path highlighting.
It also includes a simple UI loop to interactively display the maze, toggle the
solution path, change colors, nd regenerate the maze.

This module does not contain maze generation or
solving logic; it only visualizes maze data provided to it.
"""


from __future__ import annotations

import os
from enum import Enum
from dataclasses import dataclass
from typing import Callable


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class C(str, Enum):
    """ANSI color codes used to make terminal output easier to read."""

    RESET = "\033[0m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    RED = "\033[31m"
    BG_RED = "\033[41m"
    BG_PURPLE = "\033[45m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BOLD_WHITE = "\033[1;37m"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class AsciiStyle:
    wall_color: str = ""
    reset: str = "\033[0m"


_COLOR_PALETTE = [
    "",  # no color
    "\033[31m",  # red
    "\033[32m",  # green
    "\033[33m",  # yellow
    "\033[34m",  # blue
    "\033[35m",  # magenta
    "\033[36m",  # cyan
]

_BG_42 = "\33[47m"  # white background
_RESET = "\33[0m"


def _has_wall(cell: int, bit: int) -> bool:
    """Check if a given wall exists in a maze cell using bitmask.

    Args:
        cell: Integer representing cell walls as bits.
        bit: Bitmask for a specific wall direction (NORTH, EAST, SOUTH, WEST).

    Returns:
        True if the specified wall is present, False otherwise.
    """
    # Bitwise AND checks if the bit for the wall is set in the cell integer.
    return (cell & bit) != 0


def _cells_on_path(
    entry: tuple[int, int],
    path: str,
    width: int,
    height: int,
) -> set[tuple[int, int]]:
    """Reconstruct the set of cells visited along a path through the maze.

    Args:
        entry: Starting coordinate (x, y) in the maze.
        path: String of directions ('N', 'E', 'S', 'W') representing moves.
        width: Maze width for boundary checks.
        height: Maze height for boundary checks.

    Returns:
        A set of (x, y) tuples representing cells on the path.

    Raises:
        ValueError: If entry or path moves go out of maze bounds or contain
        invalid chars.
    """
    x, y = entry
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(f"Entry out of bounds: {entry}")

    visited = {(x, y)}
    for step in path:
        # Update coordinates according to direction step
        if step == "N":
            y -= 1
        elif step == "E":
            x += 1
        elif step == "S":
            y += 1
        elif step == "W":
            x -= 1
        else:
            raise ValueError(f"Invalid path char: {step!r} (expected N/E/S/W)")
        # Check boundaries after move
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError("Path goes out of bounds (solver/path mismatch)")

        visited.add((x, y))
    return visited


def render_ascii(
    maze: object,
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    path: str | None = None,
    color_mode: int = 0,
    forbidden_cells: set[tuple[int, int]] | None = None,
) -> str:
    """Render the maze as an ASCII string with optional path and color.

    Args:
        maze: Object containing 'grid' (2D list of int), 'height', and 'width'.
        entry: Coordinate (x, y) of maze entry point.
        exit_pos: Coordinate (x, y) of maze exit point.
        path: Optional string of directions representing solution path.
        color_mode: Index to select wall color from predefined palette.
        forbidden_cells: Optional set of coordinates to render differently.

    Returns:
        A string with the ASCII representation of the maze ready for terminal
        output.

    Raises:
        ValueError: If maze grid dimensions or cell values are invalid.
    """
    grid: list[list[int]] = getattr(maze, "grid")
    height: int = getattr(maze, "height")
    width: int = getattr(maze, "width")

    if forbidden_cells is None:
        forbidden_cells = set()
    if len(grid) != height or any(len(row) != width for row in grid):
        raise ValueError("Maze grid dimensions do not match width/height")

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            if not isinstance(cell, int) or not (0 <= cell <= 15):
                raise ValueError(
                    f"Invalid cell value at ({x},{y}): {cell!r}"
                    f" (expected int 0..15)"
                )
    # Select wall color based on color_mode cycling through palette
    wall_color = _COLOR_PALETTE[color_mode % len(_COLOR_PALETTE)]
    style = AsciiStyle(wall_color=wall_color)

    path_cells: set[tuple[int, int]] = set()
    if path:
        # Determine all cells along the solution path for highlighting
        path_cells = _cells_on_path(entry, path, width, height)

    def cwall(s: str) -> str:
        # Apply wall color if specified, otherwise return string unchanged
        if not style.wall_color:
            return s
        return f"{style.wall_color}{s}{style.reset}"

    lines: list[str] = []

    for y in range(height):
        # Construct the top boundary line of cells in this row
        top_parts = ["+"]
        for x in range(width):
            cell = grid[y][x]
            # Add horizontal wall or spaces depending on presence of NORTH wall
            top_parts.append(cwall("---") if _has_wall(cell, NORTH) else "   ")
            top_parts.append("+")
        lines.append("".join(top_parts))

        mid_parts: list[str] = []
        for x in range(width):
            cell = grid[y][x]
            # Add vertical wall or space depending on presence of WEST wall
            mid_parts.append(cwall("|") if _has_wall(cell, WEST) else " ")

            pos = (x, y)
            # Render special markers for entry, exit, forbidden, or path cells
            if pos == entry:
                interior = f"{C.BOLD_WHITE}{C.BG_YELLOW} E {C.RESET}"
            elif pos == exit_pos:
                interior = f"{C.BOLD_WHITE}{C.BG_GREEN} X {C.RESET}"
            elif pos in forbidden_cells:
                # Render forbidden cells with white background for emphasis
                interior = f"{_BG_42}   {_RESET}"
            elif pos in path_cells:
                # Mark cells on the path with a dot
                interior = " • "
            else:
                interior = "   "
            mid_parts.append(interior)

        last_cell = grid[y][width - 1]
    # Add EAST wall for the last cell in the row if present
        mid_parts.append(cwall("|") if _has_wall(last_cell, EAST) else " ")
        lines.append("".join(mid_parts))

    # Construct the bottom boundary line of the maze
    bottom_parts = ["+"]
    y = height - 1
    for x in range(width):
        cell = grid[y][x]
        bottom_parts.append(cwall("---") if _has_wall(cell, SOUTH) else "   ")
        bottom_parts.append("+")
    lines.append("".join(bottom_parts))

    return "\n".join(lines) + "\n"


def _clear_screen() -> None:
    """Clear the terminal screen in a cross-platform way."""
    os.system("cls" if os.name == "nt" else "clear")


def run_ui_loop(
    get_state: Callable[[], tuple[object, str, set[tuple[int, int]]]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
) -> None:
    """Run an interactive terminal UI loop to display and control the maze
    visualization.

    Args:
        get_state: Function returning current maze, path, and forbidden cells.
        entry: Coordinate (x, y) of maze entry point.
        exit_pos: Coordinate (x, y) of maze exit point.

    Behavior:
        - Displays the maze in ASCII with optional path and colors.
        - Accepts user commands to toggle path visibility, change colors,
          regenerate the maze, or quit.
    """
    show_path = False
    color_mode = 0

    maze, path, forbidden_cells = get_state()

    while True:
        _clear_screen()
        print(
            render_ascii(
                maze,
                entry,
                exit_pos,
                path if show_path else None,
                color_mode,
                forbidden_cells=forbidden_cells,
            )
        )
        print(
            f"{C.YELLOW}Commands:{C.RESET}\n"
            f"{C.YELLOW}[r]:{C.RESET} Re-generate a new maze\n"
            f"{C.YELLOW}[p]:{C.RESET} Show/hide path from entry to exit\n"
            f"{C.YELLOW}[c]:{C.RESET} Change maze color\n"
            f"{C.YELLOW}[q]:{C.RESET} Quit the session"
        )
        cmd = input("> ").strip().lower()

        if cmd == "q":
            # Quit the current maze session on terminal
            return
        if cmd == "p":
            # Toggle path visibility on/off
            show_path = not show_path
            continue
        if cmd == "c":
            # Cycle through available color modes for walls
            color_mode += 1
            continue
        if cmd == "r":
            # Reload maze, path, and forbidden cells from get_state
            maze, path, forbidden_cells = get_state()
            continue
