from __future__ import annotations
from enum import Enum
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


def forty_two_marking(maze: Maze) -> set[tuple[int, int]]:
    stamp_height = 5
    stamp_width = 7
    border_margin = 4

    forbidden_cells = set()
    if (maze.height < stamp_height + (2 * border_margin)
            or maze.width < stamp_width + (2 * border_margin)):
        return forbidden_cells

    x_center = maze.width // 2
    y_center = maze.height // 2
    top_left_x_pos = x_center - (stamp_width // 2)
    top_left_y_pos = y_center - (stamp_height // 2)
    sx = 0
    sy = 0
    celss_to_be_blocked = [
        (sx, sy),
        (sx + 4, sy),
        (sx + 5, sy),
        (sx + 6, sy),
        (sx, sy + 1),
        (sx + 6, sy + 1),
        (sx, sy + 2),
        (sx + 1, sy + 2),
        (sx + 2, sy + 2),
        (sx + 4, sy + 2),
        (sx + 5, sy + 2),
        (sx + 6, sy + 2),
        (sx + 2, sy + 3),
        (sx + 4, sy + 3),
        (sx + 2, sy + 4),
        (sx + 4, sy + 4),
        (sx + 5, sy + 4),
        (sx + 6, sy + 4),
    ]
    for maze_cell in celss_to_be_blocked:
        sx, sy = maze_cell
        maze_x = top_left_x_pos + sx
        maze_y = top_left_y_pos + sy
        maze_cell = (maze_x, maze_y)
        forbidden_cells.add(maze_cell)

    error = False
    if maze.entry in forbidden_cells and maze.exit in forbidden_cells:
        print(
            f"{C.BG_RED}Warning:{C.RESET} Maze generated but cannot display "
            f"42 decorator.\nEntry {maze.entry} and exit {maze.exit} "
            f"coordinates are both in blocked cells by 42 decoration.\n"
            f"Display is skipped. Please try different entry and exit values."
        )
        error = True
    elif maze.entry in forbidden_cells:
        print(
            f"{C.BG_RED}Warning:{C.RESET} Maze generated but cannot display "
            f"42 decorator. \nEntry coordinate {maze.entry} is in blocked "
            f"cells by 42 decoration. Display is skipped. Please try a "
            f"different entry value."
        )
        error = True
    elif maze.exit in forbidden_cells:
        print(
            f"{C.BG_RED}Warning:{C.RESET} Maze generated but cannot display "
            f"42 decorator. \nExit coordinate {maze.exit} is in blocked "
            f"cells by 42 decoration. Display is skipped. Please try a "
            f"different exit value."
        )
        error = True
    if error:
        forbidden_cells = set()
        return forbidden_cells
    return forbidden_cells
