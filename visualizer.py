from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


@dataclass(frozen=True)
class AsciiStyle:
    wall_color: str = ""
    reset: str = "\033[0m"


_COLOR_PALETTE = [
    "",             # no color
    "\033[31m",     # red
    "\033[32m",     # green
    "\033[33m",     # yellow
    "\033[34m",     # blue
    "\033[35m",     # magenta
    "\033[36m",     # cyan
]


def _has_wall(cell: int, bit: int) -> bool:
    return (cell & bit) != 0


def _cells_on_path(
    entry: tuple[int, int],
    path: str,
    width: int,
    height: int,
) -> set[tuple[int, int]]:
    x, y = entry
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(f"Entry out of bounds: {entry}")

    visited = {(x, y)}
    for step in path:
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
) -> str:
    grid: list[list[int]] = getattr(maze, "grid")
    height: int = getattr(maze, "height")
    width: int = getattr(maze, "width")

    if len(grid) != height or any(len(row) != width for row in grid):
        raise ValueError("Maze grid dimensions do not match width/height")

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            if not isinstance(cell, int) or not (0 <= cell <= 15):
                raise ValueError(f"Invalid cell value at ({x},{y}): {cell!r}"
                                 f" (expected int 0..15)")

    wall_color = _COLOR_PALETTE[color_mode % len(_COLOR_PALETTE)]
    style = AsciiStyle(wall_color=wall_color)

    path_cells: set[tuple[int, int]] = set()
    if path:
        path_cells = _cells_on_path(entry, path, width, height)

    def cwall(s: str) -> str:
        if not style.wall_color:
            return s
        return f"{style.wall_color}{s}{style.reset}"

    lines: list[str] = []

    for y in range(height):
        top_parts = ["+"]
        for x in range(width):
            cell = grid[y][x]
            top_parts.append(cwall("---") if _has_wall(cell, NORTH) else "   ")
            top_parts.append("+")
        lines.append("".join(top_parts))

        mid_parts: list[str] = []
        for x in range(width):
            cell = grid[y][x]
            mid_parts.append(cwall("|") if _has_wall(cell, WEST) else " ")

            pos = (x, y)
            if pos == entry:
                interior = " E "
            elif pos == exit_pos:
                interior = " X "
            elif pos in path_cells:
                interior = " . "
            else:
                interior = "   "
            mid_parts.append(interior)

        last_cell = grid[y][width - 1]
        mid_parts.append(cwall("|") if _has_wall(last_cell, EAST) else " ")
        lines.append("".join(mid_parts))

    bottom_parts = ["+"]
    y = height - 1
    for x in range(width):
        cell = grid[y][x]
        bottom_parts.append(cwall("---") if _has_wall(cell, SOUTH) else "   ")
        bottom_parts.append("+")
    lines.append("".join(bottom_parts))

    return "\n".join(lines) + "\n"


def _clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def run_ui_loop(
    get_state: Callable[[], tuple[object, str]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
) -> None:
    show_path = False
    color_mode = 0

    maze, path = get_state()

    while True:
        _clear_screen()
        print(render_ascii(maze,
                           entry,
                           exit_pos,
                           path if show_path else None, color_mode))
        print("Commands: [r] regenerate  [p] show/hide path"
              "  [c] change wall color  [q] quit")
        cmd = input("> ").strip().lower()

        if cmd == "q":
            return
        if cmd == "p":
            show_path = not show_path
            continue
        if cmd == "c":
            color_mode += 1
            continue
        if cmd == "r":
            maze, path = get_state()
            continue
