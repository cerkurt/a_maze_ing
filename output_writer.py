"""
Module responsible for writing the final maze output file.

This file handles only the output writing part of the program. It does not
generate or solve the maze.

The output format strictly follows the subject's requirements to ensure
compatibility.
"""


from __future__ import annotations


def _validate_maze_grid(grid: list[list[int]],
                        width: int,
                        height: int) -> None:
    """
    Validate the maze grid before writing to the output file.

    This function ensures that the maze data is well-formed and consistent.
    It checks the following invariants:
    - The grid height matches the expected maze height.
    - Each row's width matches the expected maze width.
    - Each cell's value is an integer between 0 and 15 inclusive.

    These checks help prevent corrupted or invalid maze data from being
    written, which could cause errors or incorrect output.

    Raises:
        ValueError: If any of the above conditions are not met.
    """
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
    """
    Format a coordinate tuple as a string "x,y".

    Coordinates are formatted this way to match the exact output specification
    required by the subject. This ensures consistent and correct output for
    entry and exit positions in the maze.

    Args:
        coord: A tuple containing the x and y coordinates.

    Returns:
        A string representing the coordinate in "x,y" format.
    """
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
    Write the maze and solution output to a file in the required format.
    The output file contains the following, in order:
    1. The maze grid as hexadecimal digits (0-F), one row per line.
    2. An empty line.
    3. The entry coordinate line formatted as "x,y".
    4. The exit coordinate line formatted as "x,y".
    5. The shortest path string composed of directions (N, E, S, W).

    Parameters:
        filename: The name of the output file to write.
        maze: The maze object containing grid, width, and height attributes.
        entry: The (x, y) coordinates of the maze entry point.
        exit_pos: The (x, y) coordinates of the maze exit point.
        path: A string representing the shortest path using directions.

    The maze grid is written using hexadecimal values to represent each cell,
    which is a compact and subject-specified format.
    """
    # Extract maze grid and dimensions from the maze object
    grid: list[list[int]] = getattr(maze, "grid")
    height: int = getattr(maze, "height")
    width: int = getattr(maze, "width")

    # Validate the maze grid data before writing
    _validate_maze_grid(grid, width, height)

    # Validate that the path string contains only allowed direction characters
    for ch in path:
        if ch not in {"N", "E", "S", "W"}:
            raise ValueError(f"Invalid path character: {ch!r}"
                             " (expected only N/E/S/W)")

    with open(filename, "w", encoding="utf-8") as f:
        # Write the maze rows as hexadecimal digits, one row per line
        for y in range(height):
            line = "".join(format(grid[y][x], "X") for x in range(width))
            f.write(line + "\n")

        # Write an empty line separating the maze from the coordinates
        f.write("\n")

        # Write the entry coordinate line
        f.write(_format_coord(entry) + "\n")
        # Write the exit coordinate line
        f.write(_format_coord(exit_pos) + "\n")
        # Write the shortest path string line
        f.write(path + "\n")
