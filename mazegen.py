"""Reusable maze generator/solver module.

This module provides a small, reusable API around the core logic of the
**a-maze-ing** project.

Goal
----
Expose the algorithmic parts (generation + solving) behind a clean interface so
other files (CLI / config parser / visualizer / output writer) can reuse them
without needing to know the implementation details.

What this module DOES
---------------------
- Build a grid-based maze using iterative DFS (depth-first search).
- Optionally reserve/forbid cells for the "42" decoration (so DFS will avoid
  carving through those cells).
- Optionally make the maze *non-perfect* by opening a few extra walls (creating
  multiple possible routes).
- Solve the maze using BFS (breadth-first search) to obtain a shortest path.
- Convert a coordinate path to a direction string ("N/E/S/W").

What this module does NOT do
----------------------------
- Parse config files.
- Render/visualize the maze.
- Serialize to hex/output format.

Those concerns live elsewhere (and can call this module).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from maze_files.maze_definitions import Maze
from maze_files.dfs_maze_generator import dfs_maze_generator
from maze_files.bfs_shortest_path_solver import bfs_shortest_path_solver

# Optional features: these modules may not exist in early milestones/tests.
try:
    from maze_files.multiple_path_maze import multiple_path_maze
except Exception:
    multiple_path_maze = None

try:
    from maze_files.forty_two_marking import forty_two_marking
except Exception:
    forty_two_marking = None


@dataclass(slots=True)
class ConfigGen:
    """Configuration container for :class:`MazeGenerator`.

    This mirrors the values you typically get from the config parser, but it is
    kept lightweight so the generator can be reused without depending on file
    parsing code.

    Attributes:
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        entry: Start coordinate as (x, y).
        exit: End coordinate as (x, y).
        seed: RNG seed used for deterministic generation.
        perfect: If True, generate a *perfect* maze (tree; unique path between
            any two reachable cells). If False, add extra openings after DFS.
        marking_42: If True, reserve cells for the "42" decoration when the
            maze is large enough.
    """

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    seed: int = 0
    perfect: bool = True
    marking_42: bool = True


class MazeGenerator:
    """High-level wrapper that owns the maze, forbidden cells, and solution.

    Think of this class as the *orchestrator*:
    - It creates a fresh :class:`~maze_files.maze_definitions.Maze`.
    - It optionally computes the "42" forbidden cells.
    - It runs DFS generation (carving passages).
    - It optionally makes the maze non-perfect.
    - It runs BFS to solve for a shortest path.

    The class stores results internally so other parts of the program can query
    them via properties (maze/grid/path).
    """

    def __init__(self, cfg: ConfigGen) -> None:
        """Create a generator bound to a configuration.

        Args:
            cfg: Generation settings (size, entry/exit, seed,
            perfect/non-perfect).
        """
        self.cfg = cfg
        self._maze: Optional[Maze] = None
        self._path: Optional[list[tuple[int, int]]] = None
        self._forbidden: set[tuple[int, int]] = set()

    @property
    def maze(self) -> Maze:
        """Return the generated maze.

        Raises:
            RuntimeError: If generate() has not been called yet.
        """
        if self._maze is None:
            raise RuntimeError(
                "Maze not generated yer. Please call generate() function"
                "first.")
        return self._maze

    @property
    def grid(self) -> list[list[int]]:
        """Shortcut to access `maze.grid` (2D list of wall masks)."""
        return self.maze.grid

    @property
    def forbidden_cells(self) -> set[tuple[int, int]]:
        """Return a *copy* of the forbidden-cell set.

        Returning a copy prevents callers from accidentally mutating internal
        state.
        """
        return set(self._forbidden)

    @property
    def path(self) -> list[tuple[int, int]]:
        """Return the last solved coordinate path.

        Raises:
            RuntimeError: If solve_maze_path() has not been called yet.
        """
        if self._path is None:
            raise RuntimeError(
                "Maze path is not solved yet. Call solve_maze_path() first "
                "to get the path solution.")

    @property
    def generate(self) -> Maze:
        """Generate the maze and store it internally.

        Generation flow:
            1) Create a fresh maze with all walls closed.
            2) Optionally compute forbidden cells for the "42" decoration.
            3) Run DFS generator, which carves passages while avoiding forbidden cells.
            4) If perfect=False, open extra walls to create loops/multiple routes.

        Returns:
            The generated Maze instance.

        Raises:
            RuntimeError: If perfect=False but `multiple_path_maze` is unavailable.
        """
        cfg = self.cfg

        # Fresh maze: every cell starts with mask=15 (all walls closed).
        self._maze = Maze(cfg.height, cfg.width, cfg.entry, cfg.exit)

        # Reset derived state from any previous run.
        self._path = None
        self._forbidden = set()

        # Compute "42" forbidden cells only when requested and available.
        if cfg.marking_42 and forty_two_marking is not None:
            self._forbidden = set(forty_two_marking(self._maze))

        # DFS generation mutates maze.grid in-place.
        dfs_maze_generator(self._maze, self._forbidden, cfg.seed)
        if not cfg.perfect:
            if multiple_path_maze is None:
                raise RuntimeError(
                    "Config Perfect=False but multiple_path_maze() was not "
                    "found. Expected maze_files/multiple_path_maze.py to "
                    "define multiple_path maze.")
            multiple_path_maze(self._maze)

        return self._maze

    def solve_maze_path(self) -> list[tuple[int, int]]:
        """Solve the maze with BFS and store the resulting coordinate path.

        BFS guarantees the shortest path in an unweighted grid.

        Returns:
            The path as a list of coordinates from entry to exit (inclusive).
        """
        self._path = bfs_shortest_path_solver(self.maze)
        return list(self._path)

    def coords_to_directions(
            self,
            coords: Optional[Iterable[tuple[int, int]]] = None,) -> str:
        """Convert a coordinate path to a direction string.

        The returned string is made of letters:
            - 'N' for (0, -1)
            - 'E' for (+1, 0)
            - 'S' for (0, +1)
            - 'W' for (-1, 0)

        Args:
            coords: Optional coordinate iterable. If omitted, uses `self.path`.

        Returns:
            Direction string such as "NNEESW". For paths shorter than 2, returns "".

        Raises:
            ValueError: If the path contains a non-adjacent step.
        """
        if coords is None:
            coords_list = self.path
        else:
            coords_list = list(coords)

        # Need at least 2 points to produce a move.
        if len(coords_list) < 2:
            return ""

        out: list[str] = []

        # Walk pairwise: (p0,p1), (p1,p2), ...
        for (x1, y1), (x2, y2) in zip(coords_list, coords_list[1:]):
            dx = x2 - x1
            dy = y2 - y1
            if dx == 0 and dy == -1:
                out.append("N")
            elif dx == 1 and dy == 0:
                out.append("E")
            elif dx == 0 and dy == 1:
                out.append("S")
            elif dx == -1 and dy == 0:
                out.append("W")
            else:
                raise ValueError(f"Non-adjacent step in path for coordinates: "
                                 f"{(x1, y1)} and {(x2,  y2)}")
        return "".join(out)
