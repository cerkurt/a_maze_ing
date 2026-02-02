from __future__ import annotations

from dataclasses import dataclass


# same as def __init__(self, width: int, ...)
@dataclass(frozen=True)
class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


_REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


def _parse_bool(value: str) -> bool:
    v = value.strip().lower()
    if v in {"true", "1", "yes", "y"}:
        return True
    if v in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Invalid boolean: {value!r} (expected True/False).")


def _parse_coord(value: str) -> tuple[int, int]:
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
    """
    Load config file with KEY=VALUE lines.
    Ignores comments starting with '#'.
    Raises ValueError with a clear message on invalid config.
    """
    data: dict[str, str] = {}

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(f"Bad syntax: {line!r} (expected KEY=VALUE)")
            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()
            if not key:
                raise ValueError(f"Bad syntax: {line!r} (empty key)")
            data[key] = value

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
