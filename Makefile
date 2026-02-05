PY  := python3
PIP := $(PY) -m pip
CFG ?= config.txt
OUT ?= maze.txt

.PHONY: help install run debug ui output check imports clean distclean lint lint-strict

help:
	@echo ""
	@echo "a-maze-ing Makefile"
	@echo "------------------"
	@echo "make install     Install project dependencies"
	@echo "make run         Run program with CFG=$(CFG)"
	@echo "make debug       Run program in pdb with CFG=$(CFG)"
	@echo "make output      Run and print output file ($(OUT))"
	@echo "make check       Compile + import checks"
	@echo "make lint        flake8 + mypy"
	@echo "make lint-strict flake8 + mypy --strict"
	@echo "make clean       Remove caches/temp files"
	@echo "make distclean   Clean + remove output file"
	@echo ""

install:
	$(PIP) install -r requirements.txt

run:
	$(PY) a_maze_ing.py $(CFG)

debug:
	$(PY) -m pdb a_maze_ing.py $(CFG)

output:
	$(PY) a_maze_ing.py $(CFG)
	@echo
	@echo "----- $(OUT) -----"
	@cat $(OUT)

check: imports
	$(PY) -m compileall -q .

imports:
	$(PY) -c "import maze_files"
	$(PY) -c "from maze_files.maze_definitions import Maze"
	$(PY) -c "from maze_files.dfs_maze_generator import dfs_maze_generator"
	$(PY) -c "from maze_files.bfs_shortest_path_solver import bfs_shortest_path_solver"
	$(PY) -c "from maze_files.wall_operations import carve_coordinate"
	@echo "All imports OK"

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache .pytest_cache .ruff_cache .coverage htmlcov

distclean: clean
	rm -f $(OUT)
