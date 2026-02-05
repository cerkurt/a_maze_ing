PY  := python3
CFG ?= config.txt
OUT ?= maze.txt

.PHONY: help run ui output check imports clean distclean

help:
	@echo ""
	@echo "a-maze-ing Makefile"
	@echo "------------------"
	@echo "make run        Run program with CFG=$(CFG)"
	@echo "make ui         Run interactive visualizer"
	@echo "make output     Run and print output file ($(OUT))"
	@echo "make check      Compile + import checks"
	@echo "make clean      Remove __pycache__ and *.pyc"
	@echo "make distclean  Clean + remove output file"
	@echo ""

run:
	$(PY) a_maze_ing.py $(CFG)

ui: run

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

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

distclean: clean
	rm -f $(OUT)
