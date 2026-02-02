from __future__ import annotations


def _validate_maze_grid(grid: list[list[int]],
                        width: int,
                        height: int) -> None:
    if len(grid) != height:
        raise ValueError("Grid height does not match maze.height")
    for y, row in enumerate(grid):
        if len(row) != width:
            raise ValueError(f"Grid width does not match "
                             f"maze.width at row {y}")
        for x, cell in enumerate(row):
            if not isinstance(cell, int) or not (0 <= cell <= 15):
                raise ValueError(f"Invalid cell value at ({x},{y}): {cell!r}"
                                 f" (expected int 0..15)")


def _format_coord(coord: tuple[int, int]) -> str:
    x, y = coord
    return f"{x},{y}"


def write_output(
    filename: str,
    maze: object,
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    path: str,
) -> None:
    """
    Write maze output format required by the subject:

    - Hex digit per cell, row by row, one row per line
    - Empty line
    - Entry coordinates line: "x,y"
    - Exit coordinates line: "x,y"
    - Shortest path string line: "NESW..."
    - All lines end with '\n'
    """
    grid: list[list[int]] = getattr(maze, "grid")
    height: int = getattr(maze, "height")
    width: int = getattr(maze, "width")

    _validate_maze_grid(grid, width, height)

    # Validate path characters (allow empty string)
    for ch in path:
        if ch not in {"N", "E", "S", "W"}:
            raise ValueError(f"Invalid path character: {ch!r}"
                             " (expected only N/E/S/W)")

    with open(filename, "w", encoding="utf-8") as f:
        # Maze rows
        for y in range(height):
            line = "".join(format(grid[y][x], "X") for x in range(width))
            f.write(line + "\n")

        # Empty line
        f.write("\n")

        # Entry, exit, path
        f.write(_format_coord(entry) + "\n")
        f.write(_format_coord(exit_pos) + "\n")
        f.write(path + "\n")
