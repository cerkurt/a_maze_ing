This project has been created as part of the 42 curriculum
by cerkurt, cmacaroc.
---

## Table of Content
## Index

### A. Description

- [A.1 a-maze-ing](#a1-a-maze-ing)
- [A.2 Project Overview](#a2-project-overview)
- [A.3 Teamwork & Project Organization](#a3-teamwork--project-organization)
- [A.4 Core Concepts](#a4-core-concepts)
  - [A.4.1 What is a Maze?](#a41-what-is-a-maze)
- [A.5 Algorithms Used](#a5-algorithms-used)
  - [A.5.1 Maze Generation — DFS (Depth-First Search)](#a51-maze-generation--dfs-depth-first-search)
    - [A.5.1.a What is DFS in simple words?](#a51a-what-is-dfs-in-simple-words)
  - [A.5.2 Maze Path Solving — BFS (Breadth-First Search)](#a52-maze-path-solving--bfs-breadth-first-search)
    - [A.5.2.a What is BFS in simple words?](#a52a-what-is-bfs-in-simple-words)
    - [A.5.2.b Making the Maze Non-Perfect (Optional)](#a52b-making-the-maze-non-perfect-optional)
- [A.6 Coordinate System](#a6-coordinate-system)
- [A.7 42 Marking Decoration (Conditional)](#a7-42-marking-decoration-conditional)
- [A.8 Direction System as Dictionaries](#a8-direction-system-as-dictionaries)
  - [A.8.1 Direction → Bit Value](#a81-direction--bit-value)
  - [A.8.2 Direction → Movement Delta](#a82-direction--movement-delta)
  - [A.8.3 Direction → Opposite Direction](#a83-direction--opposite-direction)
  - [A.8.4 Benefits of Dictionaries](#a84-benefits-of-dictionaries)
  - [A.8.5 Takeaway](#a85-takeaway)
- [A.9 Public API](#a9-public-api)
  - [A.9.1 Maze structure](#a91-maze-structure)
  - [A.9.2 Maze generation (DFS)](#a92-maze-generation-dfs)
  - [A.9.3 Extra paths (non-perfect maze)](#a93-extra-paths-non-perfect-maze)
  - [A.9.4 Maze solving (BFS)](#a94-maze-solving-bfs)
  - [A.9.5 42 decoration marking](#a95-42-decoration-marking)
- [A.10 Project Structure](#a10-project-structure)
- [A.11 AI Usage](#a11-ai-usage)

### B. Instructions
- [B.1 How to Run](#b1-how-to-run)
  - [B.1.1 Clone the repository](#b11-clone-the-repository)
  - [B.1.2 Run with a config file](#b12-run-with-a-config-file)
  - [B.1.3 Configuration File Example](#b13-configuration-file-example)

### C. Resources
- [C.1 Maze Generation & Graph Traversal](#c1-maze-generation--graph-traversal)
- [C.2 Python & Data Structures](#c2-python--data-structures)

### D. Final Notes
- [Final Notes](#d-final-notes)
---

# A. Description

---

# A.1. a-maze-ing

The goal of the project is to generate and solve mazes programmatically.  
The program is able to:
- generate **perfect** and **non-perfect** mazes,
- guarantee maze validity (bounds, connectivity, wall coherence),
- find the **shortest path** between an entry and an exit,
- optionally decorate the maze with a **42 pattern** when space allows,
- output the result in the required format for evaluation.

The project is written in **Python**, with a strong focus on:
- clean architecture,
- clear separation of responsibilities,
- algorithmic correctness,
- and readability for future students.

The project is designed to be
    **educational**,
    **modular**, and
    **easy to reason about**,
from beginners for beginners.

---

## A.2. Project Overview

This program can:

- Generate a **perfect maze** (only one path between any two cells)
- Optionally turn it into a **non-perfect maze** (multiple paths allowed)
- Solve the maze using **BFS** (shortest path guaranteed)
- Reserve space for a **“42” decoration** inside the maze (conditional)
- Output the maze and the solution path
- Visualize the maze in the terminal with ASCII rendering

---

## A.3. Teamwork & Project Organization

This project was developed by two people, and we intentionally split the
responsibilities by problem domain, not by file size.

The maze project naturally breaks into two big concerns:

1.	Maze logic & algorithms
2.	Input / output, configuration, and display (UI)

We used this natural separation to work in parallel without blocking each
other.

Person A — Maze Logic (Core Algorithms)
Responsible for:

	•	Maze data structure
	•	Wall representation (bitmask logic)
	•	Maze generation (DFS)
	•	Maze solving (BFS)
	•	Validation rules (connectivity, borders, coherence)
	•	Non-perfect maze
    •	42 marking decoration

This work lives mostly inside the maze_files/ package.

Person B — Application Layer & UX
Responsible for:

	•	CLI entrypoint
	•	Config parsing (config.txt)
	•	Output formatting
	•	Visualization
	•	Program flow (when generation, solving, and output happen)

This work lives at the root of the repository and treats the maze logic as a
reusable module.

This separation allowed:

	•	Independent development
	•	Clear ownership
	•	Easy debugging
	•	Minimal merge conflicts

⸻

**A real helper contract: *INTERFACES.md***

Before writing any code, we created a small but strict shared contract as
INTERFACES.md.

This file defines:

	•	What a Maze must expose
	•	How the grid is indexed (maze.grid[y][x])
	•	How coordinates are represented ((x, y))
	•	How walls are encoded (bitmask values)
	•	What functions expect and return

In other words:

We agreed on the rules first, then coded freely.

Because of this:

	•	No one had to guess how the other side works
	•	No refactoring was needed later
	•	Files merged cleanly on the first try
	•	No “but I thought it worked like this” moments

⸻

Why This Made the Merge Easy

When it was time to merge:

	•	Both sides already respected the same data shapes
	•	Function signatures matched exactly
	•	No logic was duplicated
	•	No rewrites were needed

We could simply:

	1.	Import the maze logic
	2.	Plug it into the CLI flow
	3.	Run the program

Everything worked immediately.

This approach turned what is usually a stressful merge into a snap of a finger
time event.

⸻

Takeaway

Using:

	•	a clear interface contract
	•	a clean responsibility split
	•	and early agreement on data structures

allowed us to:

	•	Work faster
	•	Make fewer mistakes
	•	Keep the code readable
	•	Avoid merge conflicts entirely

If this project were extended or reused, the same structure would still scale
cleanly.

---

## A.4. Core Concepts

### A.4.1. What is a Maze?
A maze is a grid of cells.
Each cell has **four possible walls**:

- North (bit value [2^0] = 1)
- East (bit value [2^1] = 2)
- South (bit value [2^2] = 4)
- West (bit value [2^3] = 8)

A wall can be:

- **closed** → you cannot move through it
- **open** → you can move through it

Internally, walls are stored using **bit masks** (numbers from 0–15).

---

## A.5. Algorithms Used

## A.5.1. Maze Generation — DFS (Depth-First Search)

### A.5.1.a. What is DFS in simple words?
DFS explores the maze by:

- Starting from the entry cell.
- Randomly visiting unvisited neighboring cells.
- When moving to a neighbor, removing the wall between the two cells.
- Reaches a cell with no unvisited neighbors, it **backtrack**s.

Think of it as:

> Walk until stuck → step back → try a different direction

This process creates a **perfect maze**, meaning:
- every cell is reachable,
- there is exactly **one unique path** between any two cells.

The DFS is implemented using an **explicit stack** instead of recursion,
to avoid recursion depth limits and keep the logic easier to follow.

**Important rule**
In a perfect maze:

- There is **exactly one path** between any two cells

---

## A.5.2. Maze Path Solving — BFS (Breadth-First Search)

### A.5.2.a. What is BFS in simple words?
BFS is used to **solve the maze** and BFS explores the maze layer by layer.

1. One step away from the start
2. Then two steps away
3. Then three, and so on…

It explores in **layers**.

- BFS guarantees the **shortest path**
- The **first time** BFS reaches the exit → that path is optimal

BFS returns

- A list of coordinates from entry → exit
- This path is later converted into directions like:

```
NNEESWSS
```
---

## A.5.2.b. Making the Maze Non-Perfect (Optional)

If `PERFECT=False` in the config:

- The maze is first generated as perfect (using DFS)
- Then **extra walls are opened**
- This creates **multiple possible paths**

This step does **not break connectivity** — it only adds choices.
---

## A.6. Coordinate System

- Coordinates are always `(x, y)`
- `(0, 0)` is the **top-left** corner
- `x` increases to the right
- `y` increases downward

The maze grid is stored as:

```
maze.grid[y][x]
```

---

## A.7. 42 Marking Decoration (Conditional)

If the maze is large enough both as size also the margin wise:

- A “42” pattern is **reserved in the center**
- These cells are marked as **forbidden** for DFS and BFS search
- DFS will **walk around** them

If the entry or exit would land inside the decoration:

- The decoration is skipped
- A warning is printed
- Maze generation continues normally

This ensures:

- No broken mazes
- No forced paths
- No fixed corridors

---

## A.8. Direction System as Dictionaries

In this project, directions (North, East, South, West) are used everywhere:

    • carving walls
    • checking neighbors
    • DFS generation
    • BFS path finding
    • validators
    • the 42 decoration logic

Instead of handling directions with many if/elif statements, we use direction
dictionaries defined in direction_definitions.py.

This keeps the code simple, consistent, and easier to understand.

⸻

### A.8.1. Direction → Bit Value

Each cell in the maze stores its walls as a bitmask.

Each direction corresponds to one bit:

	•	North → a specific bit (1)
	•	East → a specific bit (2)
	•	South → a specific bit (4)
	•	West → a specific bit (8)

The dictionary maps directions to their bit values:

“Which bit represents this wall?”

This allows us to:
	•	check if a wall exists
	•	open a wall
	•	close a wall

Without this dictionary, we would need to hard-code numbers everywhere.

⸻

### A.8.2. Direction → Movement Delta

When moving in the maze, each direction changes (x, y) differently:

	•	North → (x, y - 1)
	•	East → (x + 1, y)
	•	South → (x, y + 1)
	•	West → (x - 1, y)

This is stored as a dictionary of movement deltas.

Why this matters:
	•	DFS and BFS can loop over directions
	•	no duplicated math
	•	easier bounds checking
	•	fewer bugs

Instead of writing movement logic four times, we write it once.

⸻

### A.8.3. Direction → Opposite Direction

When carving or closing a wall, both cells must be updated.

Example:

	•	If you open East from (x, y)
	•	You must also open West from (x+1, y)

The opposite-direction dictionary answers:

“If I move in this direction, which wall must I update on the neighbor?”

This ensures:

	•	wall coherence
	•	no one-way walls
	•	validators always pass

⸻

### A.8.4. Benefits of Dictionaries

Using direction dictionaries allows the algorithms to be written conceptually:

	•	“For each direction”
	•	instead of “If direction is North, do this… If East, do that…”

This gives us:

	•	cleaner algorithms
	•	fewer special cases
	•	easier debugging
	•	easier future changes

For example:

	•	adding a new validator
	•	changing how walls are stored
	•	adding decorations like the 42 logo

All of that becomes possible without rewriting DFS or BFS.

⸻

#### A.8.5. Takeaway

Dictionaries turn repeated logic into data. Instead of repeating code,
we let the data describe:

	•	how to move
	•	how to check walls
	•	how to update neighbors

This is why DFS, BFS, carving, validation, and decoration can all share the
same direction system.

---

## A.9. Public API

The main reusable entry point of the project is:

- `mazegen.generate_maze(...)`

This function:
1. creates a maze,
2. generates paths,
3. optionally applies the 42 decoration,
4. validates the maze,
5. solves it using BFS,
6. returns the final maze and solution path.

This allows the maze logic to be reused independently from the CLI.

These are the **intended public functions** you can import and use.

### A.9.1. Maze structure

```python
from maze_files.maze_definitions import Maze
```

Create a maze:

```python
maze = Maze(height, width, entry, exit)
```

### A.9.2. Maze generation (DFS)

```python
from maze_files.dfs_maze_generator import dfs_maze_generator

dfs_maze_generator(maze, forbidden_cells, seed)
```

### A.9.3. Extra paths (non-perfect maze)

```python
from maze_files.multiple_path_maze import imperfect_maze

imperfect_maze(maze)
```

### A.9.4. Maze solving (BFS)

```python
from maze_files.bfs_shortest_path_solver import bfs_shortest_path_solver

path = bfs_shortest_path_solver(maze)
```

### A.9.5. 42 decoration marking

```python
from maze_files.forty_two_marking import fourty_two_marking

forbidden_cells = fourty_two_marking(maze)
```

---

## A.10. Project Structure

```
.
├── mazegen.py                          # API wrapper (prepared for reuse)
├── a_maze_ing.py                       # Main entrypoint (CLI)
├── config_parser.py                    # Reads config.txt -> config object
├── output_writer.py                    # Writes output file in required format
├── visualizer.py                       # ASCII/colored terminal display (UI)
├── config.txt                          # Example configuration (input)
├── Makefile                            # Build/run helpers (if you use it)
├── README.md
└── maze_files/                         # Core library (public API lives here)
    ├── __init__.py                     # Marks this folder as a Python package
    ├── maze_definitions.py             # Maze data structure
    ├── direction_definitions.py        # Direction dictionaries
    ├── wall_operations.py              # Helper functions for walls
    ├── dfs_maze_generator.py           # Maze generation using DFS
    ├── multiple_path_maze.py           # Adds extra paths when PERFECT = false
    ├── bfs_shortest_path_solver.py     # Finds the shortest path using BFS
    └── forty_two_marking.py            # Defines and applies the 42 marking
```
---

## A.11. AI Usage

AI tools were used during this project as a **learning aid**, not as a code
generator.

AI assistance was used to:
- clarify algorithm concepts when speficic questions were not answered by the
other recources on the internet.
- discuss design decisions and architecture,
- review logic and reasoning at the end of each working phase,
- improve documentation clarity.

All code was written, tested, and understood by the authors.
No code was copied blindly.

---

# B. Instructions

---

## B.1. How to Run

### B.1.1. Clone the repository

```bash
git clone <repo_url>
cd a-maze-ing
```

### B.1.2. Run with a config file

1. Edit `config.txt` to set maze size, entry, exit, and options.
2. Run the program:

```bash
python3 a_maze_ing.py config.txt
```

---

## B.1.3. Configuration File Example

```
WIDTH=20
HEIGHT=10
ENTRY=0,0
EXIT=19,9
PERFECT=False
SEED=42
```

---

# C. Resources

The following resources were used during the development of this project to
understand algorithms, data structures, and design decisions.

### C.1. Maze Generation & Graph Traversal
- Invent with Python — *Maze generation algorithms*  
  https://inventwithpython.com/recursion/chapter11.html 
  Used to understand common maze generation approaches and the idea of perfect mazes.

- Python Official — *Maze creation in Python*  
  https://discuss.python.org/t/maze-creation-in-python/77030  
  Used to understand how DFS works and how it can be applied to maze generation.

- Wikipedia — *Breadth-First Search (BFS)*  
  https://en.wikipedia.org/wiki/Breadth-first_search  
  Used to understand shortest-path guarantees in unweighted graphs.

### C.2. Python & Data Structures
- Python Official Documentation — *collections.deque*  
  https://docs.python.org/3/library/collections.html#collections.deque  
  Used for efficient queue operations in BFS.

- Python Official Documentation — *set*  
  https://docs.python.org/3/library/stdtypes.html#set  
  Used to efficiently track visited coordinates.

- Python Official Documentation — *random*  
  https://docs.python.org/3/library/random.html  
  Used to create deterministic maze generation via seeding.

---

# D. Final Notes

If you are new to:

- DFS
- BFS
- graph traversal
- grid-based algorithms

You are at the a_maze_ing spot! :)
