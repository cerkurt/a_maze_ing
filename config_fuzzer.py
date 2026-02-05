#!/usr/bin/env python3
'''
RUN WITH:

chmod +x config_fuzzer.py
./config_fuzzer.py'''


# Note: this file is not part of the official project submission. created for
# quick testing.
from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass

from config_parser import load_config


@dataclass
class Case:
    name: str
    text: str
    should_pass: bool


BASE = """\
WIDTH=5
HEIGHT=5
ENTRY=0,0
EXIT=4,4
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
"""


def _run_case(case: Case) -> bool:
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
        f.write(case.text)
        path = f.name

    ok = True
    try:
        cfg = load_config(path)
        if not case.should_pass:
            ok = False
    except Exception:
        if case.should_pass:
            ok = False
    finally:
        os.unlink(path)
    return ok


def main() -> int:
    cases: list[Case] = []

    # --- Boolean parsing ---
    for v in ["true", "false", "1", "0", "yes", "no", "y", "n", "True",
              "False"]:
        cases.append(Case(f"bool_ok_{v}", BASE.replace("PERFECT=True",
                                                       f"PERFECT={v}"), True))
    for v in ["maybe", "t", "f", "truthy", "FALSEE"]:
        cases.append(Case(f"bool_bad_{v}",
                          BASE.replace("PERFECT=True", f"PERFECT={v}"), False))

    # --- Seeds ---
    for v in ["0", "42", "-1", "999999999"]:
        cases.append(Case(f"seed_ok_{v}", BASE.replace("SEED=42",
                                                       f"SEED={v}"), True))
    for v in ["abc", "4.2"]:
        cases.append(Case(f"seed_bad_{v}", BASE.replace("SEED=42",
                                                        f"SEED={v}"), False))

    # Optional seed missing / empty
    cases.append(Case("seed_missing", BASE.replace("SEED=42\n", ""), True))
    cases.append(Case("seed_empty", BASE.replace("SEED=42", "SEED="), True))

    # --- Out of bounds ---
    cases.append(Case("entry_x_neg", BASE.replace("ENTRY=0,0", "ENTRY=-1,0"),
                      False))
    cases.append(Case("entry_y_neg", BASE.replace("ENTRY=0,0", "ENTRY=0,-1"),
                      False))
    cases.append(Case("entry_x_eq_w", BASE.replace("ENTRY=0,0", "ENTRY=5,0"),
                      False))
    cases.append(Case("entry_y_eq_h", BASE.replace("ENTRY=0,0", "ENTRY=0,5"),
                      False))

    cases.append(Case("exit_x_neg", BASE.replace("EXIT=4,4", "EXIT=-1,0"),
                      False))
    cases.append(Case("exit_y_neg", BASE.replace("EXIT=4,4", "EXIT=0,-1"),
                      False))
    cases.append(Case("exit_x_eq_w", BASE.replace("EXIT=4,4", "EXIT=5,0"),
                      False))
    cases.append(Case("exit_y_eq_h", BASE.replace("EXIT=4,4", "EXIT=0,5"),
                      False))

    # Entry == Exit
    cases.append(Case("entry_eq_exit", BASE.replace("EXIT=4,4", "EXIT=0,0"),
                      False))

    # --- Bad coordinate syntax ---
    cases.append(Case("entry_missing_y", BASE.replace("ENTRY=0,0", "ENTRY=0"),
                      False))
    cases.append(Case("entry_too_many",
                      BASE.replace("ENTRY=0,0", "ENTRY=0,0,0"), False))
    cases.append(Case("entry_nonint", BASE.replace("ENTRY=0,0", "ENTRY=a,b"),
                      False))
    cases.append(Case("entry_float", BASE.replace("ENTRY=0,0", "ENTRY=0.5,1"),
                      False))

    # --- Missing keys ---
    cases.append(Case("missing_width", BASE.replace("WIDTH=5\n", ""), False))
    cases.append(Case("missing_output",
                      BASE.replace("OUTPUT_FILE=maze.txt\n", ""), False))

    # --- Bad syntax line ---
    cases.append(Case("bad_line_no_equals", BASE + "WIDTH 10\n", False))
    cases.append(Case("bad_empty_key", BASE + "=10\n", False))

    passed = 0
    for c in cases:
        ok = _run_case(c)
        print(f"[{'OK' if ok else 'FAIL'}] {c.name}")
        passed += int(ok)

    total = len(cases)
    print(f"\nResult: {passed}/{total} cases passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
