"""config_parser.py

Read and validate the project configuration file.

This module turns a plain text config file (KEY=VALUE lines) into a validated
`Config` object that the rest of the program can safely rely on.

Responsibilities
- Parse KEY=VALUE lines (ignore blank lines and comments starting with '#').
- Validate types and constraints (sizes, coordinates, booleans, etc.).
- Provide clear `ValueError` messages when the config is invalid.

Non-responsibilities
- This module does NOT generate or solve mazes.
- It does NOT print UI output.

Public API
- `load_config(path: str) -> Config`

Internal helpers start with '_' and are not meant to be imported elsewhere.
"""


from __future__ import annotations

from dataclasses import dataclass


# same as def __init__(self, width: int, ...)
@dataclass(frozen=True)
class Config:
    """Immutable configuration values loaded from the config file.

    Using `frozen=True` prevents accidental mutation after parsing.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


# Keys that must exist in the config file for the program to run.
_REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


def _parse_bool(value: str) -> bool:
    """Parse a boolean-like string from the config file.

    Accepted truthy values: true, 1, yes, y
    Accepted falsy values:  false, 0, no, n

    Raises:
        ValueError: If the value cannot be interpreted as a boolean.
    """
    v = value.strip().lower()
    if v in {"true", "1", "yes", "y"}:
        return True
    if v in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Invalid boolean: {value!r} (expected True/False).")


def _parse_coord(value: str) -> tuple[int, int]:
    """Parse a coordinate written as 'x,y' into a tuple (x, y).

    Whitespace around numbers is allowed (e.g. ' 3, 4 ').

    Raises:
        ValueError: If the format is wrong or x/y are not integers.
    """
    parts = [p.strip() for p in value.split(",")]
    if len(parts) != 2:
        raise ValueError(f"Invalid coordinate: {value!r} (expected x, y).")
    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError as e:
        raise ValueError(f"Invalid coordinate: {value!r} "
                         f"(x, y must be integers).") from e
    return x, y


def load_config(path: str) -> Config:
    """Load a configuration file and return a validated `Config` object.

    The config file is a simple text file with one KEY=VALUE pair per line.
    - Blank lines are ignored.
    - Lines starting with '#' are treated as comments and ignored.
    - Keys are case-insensitive (they are normalized to uppercase).

    Validation performed here (fail fast):
    - Required keys exist.
    - WIDTH and HEIGHT are positive integers.
    - ENTRY and EXIT are valid '(x,y)' coordinates and inside bounds.
    - ENTRY and EXIT are not the same coordinate.
    - OUTPUT_FILE is a non-empty string.
    - PERFECT is a valid boolean string.
    - SEED is optional; if present it must be an integer.

    Raises:
        ValueError: If the file content is invalid (with a clear message).
    """
    # Collect raw string values first, then parse/validate in a second step.
    data: dict[str, str] = {}

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            # Skip empty lines and comments.
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            # Split only on the first '=' so values may contain '=' later.
            if "=" not in line:
                raise ValueError(f"Bad syntax: {line!r} (expected KEY=VALUE)")
            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()
            if not key:
                raise ValueError(f"Bad syntax: {line!r} (empty key)")
            data[key] = value
    # Ensure the config contains every required key.
    missing = [k for k in sorted(_REQUIRED_KEYS) if k not in data]
    if missing:
        raise ValueError(f"Missing required key(s): {', '.join(missing)}")

    try:
        width = int(data["WIDTH"])
        height = int(data["HEIGHT"])
    except ValueError as e:
        raise ValueError("WIDTH and HEIGHT must be integers.") from e

    if width <= 0 or height <= 0:
        raise ValueError("WIDTH and HEIGHT must be > 0.")

    entry = _parse_coord(data["ENTRY"])
    exit_ = _parse_coord(data["EXIT"])

    # Bounds check: coordinates must fit inside [0..width-1] x [0..height-1].
    ex, ey = entry
    xx, xy = exit_

    if not (0 <= ex < width and 0 <= ey < height):
        raise ValueError(f"ENTRY out of bounds: {entry} "
                         f"for maze {width} x {height}.")
    if not (0 <= xx < width and 0 <= xy < height):
        raise ValueError(f"EXIT out of bounds: {exit_} "
                         f"for maze {width} x {height}.")
    if entry == exit_:
        raise ValueError("ENTRY and EXIT must be different.")

    output_file = data["OUTPUT_FILE"].strip()
    if not output_file:
        raise ValueError("OUTPUT_FILE must be a non-empty string.")

    perfect = _parse_bool(data["PERFECT"])

    # SEED is optional. If omitted, the caller may choose a default.
    seed: int | None = None
    if "SEED" in data and data["SEED"].strip() != "":
        try:
            seed = int(data["SEED"])
        except ValueError as e:
            raise ValueError("SEED must be an integer if provided.") from e

    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit_,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )
