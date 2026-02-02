#!/usr/bin/env python3
from __future__ import annotations

import sys

from config_parser import load_config
from output_writer import write_output
from visualizer import run_ui_loop
from enum import Enum
from maze_files.maze_definitions import Maze
from maze_files.dfs_maze_generator import dfs_maze_generator
from maze_files.multiple_path_maze import multiple_path_maze
from maze_files.bfs_shortest_path_solver import bfs_shortest_path_solver
from maze_files.forty_two_marking import forty_two_marking


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


def _coords_to_path(coords: list[tuple[int, int]]) -> str:
    """Convert a coordinate path [(x,y), ...] into a 'NESW...' step string."""
    if not coords:
        return ""
    steps: list[str] = []
    for (x1, y1), (x2, y2) in zip(coords, coords[1:]):
        dx = x2 - x1
        dy = y2 - y1
        if dx == 1 and dy == 0:
            steps.append("E")
        elif dx == -1 and dy == 0:
            steps.append("W")
        elif dx == 0 and dy == -1:
            steps.append("N")
        elif dx == 0 and dy == 1:
            steps.append("S")
        else:
            raise ValueError(f"Non-adjacent steps in path: "
                             f"{(x1, y1)} -> {(x2, y2)}")
    return "".join(steps)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 a_maze_ing.py <config.txt>")
        return 2

    config_path = argv[1]
    try:
        cfg = load_config(config_path)
    except (OSError, ValueError) as e:
        print(f"{C.BG_RED}Error:{C.RESET} {e}")
        return 1

    # TEMPORARY state provider (replace with real generator/solver)
    def get_state() -> tuple[Maze, str]:
        # Build a fresh maze (all walls closed initially).
        maze = Maze(cfg.height, cfg.width, cfg.entry, cfg.exit)

        # Use seed if provided in config; otherwise fall back to a stable
        # default.
        seed = getattr(cfg, "seed", None)
        if seed is None:
            seed = 0

        # 1) Mark the cells of 42 as forbidden on map so DFS wont try to enter
        # that area.
        forty_two_cells = forty_two_marking(maze)
        for cell in forty_two_cells:
            x, y = cell
            maze.grid[y][x] = 15

        # 2) Generate a perfect maze (DFS backtracker).
        try:
            dfs_maze_generator(maze, seed, forty_two_cells)
        except ValueError as e:
            print(f"{e}")

        # 3) If PERFECT=False, open a few extra walls to create multiple
        # routes.
        if not cfg.perfect:
            multiple_path_maze(maze, forty_two_cells)

        # 4) Solve shortest path (BFS) and convert it to "NESW..." string.
        try:
            coords_path = bfs_shortest_path_solver(maze, forty_two_cells)
            path_str = _coords_to_path(coords_path)
        except ValueError as e:
            print(f"{e}")

        # 5) Write output file (grid in hex + entry/exit + path string).
        write_output(cfg.output_file, maze, cfg.entry, cfg.exit, path_str)

        return maze, path_str

    try:
        run_ui_loop(get_state, cfg.entry, cfg.exit)
    except (OSError, ValueError) as e:
        print(f"{C.BG_RED}Error:{C.RESET} {e}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
