This project has been created as part of the 42 curriculum
by **cerkurt** and **cmacaroc**.

---

## Index

## A. Description

- [A.1. a-maze-ing](#a1-a-maze-ing)
- [A.2. Project Overview](#a2-project-overview)
- [A.3. Teamwork & Project Organization](#a3-teamwork--project-organization)
  - [A.3.1. A Real Helper Contract: INTERFACES.md](#a31-a-real-helper-contract-interfacesmd)
- [A.4. Configuration Parsing & Validation](#a4-configuration-parsing--validation)
- [A.5. Core Concepts](#a5-core-concepts)
  - [A.5.1. What is a Maze?](#a51-what-is-a-maze)
- [A.6. Algorithms Used](#a6-algorithms-used)
  - [A.6.1. Maze Generation — DFS (Depth-First Search)](#a61-maze-generation--dfs-depth-first-search)
    - [A.6.1.a. What is DFS in simple words?](#a61a-what-is-dfs-in-simple-words)
  - [A.6.2. Maze Path Solving — BFS (Breadth-First Search)](#a62-maze-path-solving--bfs-breadth-first-search)
    - [A.6.2.a. What is BFS in simple words?](#a62a-what-is-bfs-in-simple-words)
    - [A.6.2.b. Making the Maze Non-Perfect (Optional)](#a62b-making-the-maze-non-perfect-optional)
- [A.7. Coordinate System](#a7-coordinate-system)
- [A.8. 42 Marking Decoration (Conditional)](#a8-42-marking-decoration-conditional)
- [A.9. Direction System as Dictionaries](#a9-direction-system-as-dictionaries)
  - [A.9.1. Direction → Bit Value](#a91-direction--bit-value)
  - [A.9.2. Direction → Movement Delta](#a92-direction--movement-delta)
  - [A.9.3. Direction → Opposite Direction](#a93-direction--opposite-direction)
  - [A.9.4. Benefits of Dictionaries](#a94-benefits-of-dictionaries)
  - [A.9.5. Takeaway](#a95-takeaway)
- [A.10. Project Structure](#a10-project-structure)
- [A.11. AI Usage](#a11-ai-usage)

## B. Instructions

- [B.1. How to Run](#b1-how-to-run)
  - [B.1.1. Clone the Repository](#b11-clone-the-repository)
  - [B.1.2. Run with a Config File](#b12-run-with-a-config-file)
  - [B.1.3. Run with the Makefile](#b13-run-with-the-makefile)
    - [B.1.3.a. Default Usage](#b13a-default-usage)
    - [B.1.3.b. Cleanup](#b13b-cleanup)
- [B.2. Public API and Usage](#b2-public-api-and-usage)
  - [B.2.1. Sections of the Public API](#b21-sections-of-the-public-api)
  - [B.2.2. Install as a Package](#b22-install-as-a-package)
  - [B.2.3. Quick API Example](#b23-quick-api-example)

## C. Resources

- [C.1. Maze Generation & Graph Traversal](#c1-maze-generation--graph-traversal)
- [C.2. Python & Data Structures](#c2-python--data-structures)

## D. Future improvements

- [D. Future Improvements](#d-future-improvements)

## E. Final notes

- [E. Final Notes](#e-final-notes)


---

# A. Description

---

# A.1. a-maze-ing

The goal of the project is to generate and solve mazes programmatically.

The program can:
- generate **perfect** and **non-perfect** mazes,
- guarantee maze validity (bounds, connectivity, wall coherence),
- find the **shortest path** between an entry and an exit,
- optionally decorate the maze with a **42 pattern** when space allows,
- output the result in the required format for evaluation.

The project is written in **Python**, with a strong focus on:
- clean architecture,
- clear separation of responsibilities,
- algorithmic correctness,
- readability for future students.

This project is designed to be **educational**, **modular**, and **easy to reason about**, from beginners for beginners.

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

This project was developed by two people, and we intentionally split
responsibilities by **problem domain**, not by file size.

The maze project naturally breaks into two big concerns:

1. Maze logic & algorithms
2. Input/output, configuration, and display (UI)

We used this natural separation to work in parallel without blocking each other.

Person A — Maze Logic (Core Algorithms)
Responsible for:

- Maze data structure
- Wall representation (bitmask logic)
- Maze generation (DFS)
- Maze solving (BFS)
- Validation rules (connectivity, borders, coherence)
- Non-perfect maze (extra openings)
- 42 marking decoration

This work lives mostly inside the `maze_files/` package.

Person B — Application Layer & UX/UI
Responsible for:

- CLI entrypoint
- Config parsing (`config.txt`)
- Output formatting
- Visualization
- Program flow (when generation, solving, and output happen)

This work lives at the root of the repository and treats the maze logic as a
reusable module.

Before writing any code, we created a small but strict shared contract:
`INTERFACES.md`.

### A.3.1 A real helper contract: *INTERFACES.md*

This file defines:

- what a `Maze` must expose,
- how the grid is indexed (`maze.grid[y][x]`),
- how coordinates are represented (`(x, y)`),
- how walls are encoded (bitmask values),
- what functions expect and return.

In other words:

We agreed on the rules first, then coded freely.

Thanks to this:

- nobody had to guess how the other side works,
- no refactoring was needed later,
- files merged cleanly on the first try,
- no “but I thought it worked like this” moments.

---

## A.4. Configuration Parsing & Validation

All user input for the CLI is provided through a simple configuration file
(`config.txt`). Parsing and validation are handled by `config_parser.py`.

This design ensures:
- Maze logic never deals with raw strings,
- Invalid inputs are rejected early,
- The rest of the program works with **trusted, typed data**.


The configuration file follows a strict `KEY=VALUE` format.

Example:

```
WIDTH=20
HEIGHT=10
ENTRY=0,0
EXIT=19,9
PERFECT=True
SEED=42
```
⸻

#### Parsing Steps

Parsing is performed in three clear phases:

1. Lexical parsing
   - Read the file line by line
   - Strip whitespace
   - Ignore empty lines and comments starting with `#`
   - Require `KEY=VALUE` syntax (a missing `=` triggers an error)

2. Validation and type conversion
   - Required keys must be present: `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`,
     `OUTPUT_FILE`, `PERFECT`
   - Values are converted into typed Python data:
     - `WIDTH`, `HEIGHT` → integers
     - `ENTRY`, `EXIT` → `(x, y)` integer tuples parsed from `"x,y"`
     - `PERFECT` → boolean (accepts values like `true/false`, `1/0`, `yes/no`)
     - `SEED` → optional integer (if provided)
   - Bounds checks are enforced:
     - `0 <= entry.x < width` and `0 <= entry.y < height`
     - same validation for `exit`
   - Entry and exit cannot be the same coordinates

3. Configuration object creation
   - Once validated, values are stored in an immutable dataclass:

```python
@dataclass(frozen=True)
class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None
```
⸻

---

## A.5. Core Concepts

### A.5.1. What is a Maze?
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

## A.6. Algorithms Used

### A.6.1. Maze Generation — DFS (Depth-First Search)

#### A.6.1.a. What is DFS in simple words?

DFS explores the maze by:

- Starting from the entry cell.
- Randomly visiting unvisited neighboring cells.
- When moving to a neighbor, remove the wall between the two cells.
- Reaches a cell with no unvisited neighbors, it **backtracks**.

Think of it as:

> Walk until stuck → step back → try a different direction

This process creates a **perfect maze**, meaning:
- Every cell is reachable,
- There is exactly **one unique path** between any two cells.

The DFS is implemented using an **explicit stack** instead of recursion,
to avoid recursion depth limits and keep the logic easier to follow.

**Important rule**
In a perfect maze:

- There is **exactly one path** between any two cells

---

### A.6.2. Maze Path Solving — BFS (Breadth-First Search)

#### A.6.2.a. What is BFS in simple words?
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

#### A.6.2.b. Making the Maze Non-Perfect (Optional)

If `PERFECT=False` in the config:

- The maze is first generated as perfect (DFS)
- then **extra walls are opened**
- this creates **multiple possible paths**

This step does not break connectivity — it only adds choices.

---

## A.7. Coordinate System

- Coordinates are always `(x, y)`
- `(0, 0)` is the **top-left** corner
- `x` increases to the right
- `y` increases downward

The maze grid is stored as:

```
maze.grid[y][x]
```

---

## A.8. 42 Marking Decoration (Conditional)

If the maze is large enough:

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

## A.9. Direction System as Dictionaries

Directions (N/E/S/W) are used everywhere (carving, DFS, BFS, validators,
decoration). Instead of many `if/elif` statements, we keep direction logic in dictionaries:

- direction → bit value (which wall bit?)
- direction → movement delta (how `(x, y)` changes?)
- direction → opposite direction (which wall to update on the neighbor?)

---

### A.9.1. Direction → Bit Value

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

### A.9.2. Direction → Movement Delta

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

### A.9.3. Direction → Opposite Direction

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

### A.9.4. Benefits of Dictionaries

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

### A.9.5. Takeaway

Dictionaries turn repeated logic into data. Instead of repeating code, we let the data describe:

	•	how to move
	•	how to check walls
	•	how to update neighbors

This is why DFS, BFS, carving, validation, and decoration can all share the
same direction system.

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
├── Makefile                            # Build/run helpers
├── README.md
├── pyproject.toml
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
- clarify algorithm concepts when specific questions were not answered by the
other resources on the internet.
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
git clone https://github.com/cerkurt/a_maze_ing/
cd a_maze_ing
```

### B.1.2. Run with a Config File

1. Edit `config.txt`.
2. Run:

```bash
python3 a_maze_ing.py config.txt
```

### B.1.3. Run with the Makefile
This repository includes a `Makefile` to run the program with short commands.

#### B.1.3.a. Default usage

```bash
make run
```

Show all available commands:
```bash
make help
```

Run with a different config file:
```bash
make run CFG=your_config.txt
```

Generate output and print it:
```bash
make output
```

#### B.1.3.b. Cleanup

Remove Python cache files:
```bash
make clean
```

Remove cache files and the output file:
```bash
make distclean
```

---

## B.2. Public API and Usage

This repository can be used in two ways:

1) **As a CLI program** (run `a_maze_ing.py` with a config file)
2) **As a reusable Python package** (import `mazegen` and `maze_files`)

The **main public API** is `mazegen.py` at the repository root.

### B.2.1. Sections of the Public API

`mazegen.py` exposes two main pieces:

- `ConfigGen`: a small dataclass holding generation options
- `MazeGenerator`: a high-level wrapper that runs generation + solving

Key methods:
- `MazeGenerator.generate` (property): builds and generates the maze
- `MazeGenerator.solve_maze_path()`: runs BFS and returns a coordinate path
- `MazeGenerator.coords_to_directions(coords)`: converts a coordinate path to a `"NESW..."` string

### B.2.2. Install as a package

From the root of the repository:

Toggle to virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the pubic API:
```bash
python3 -m pip install .
```

Confirm the installation was successful:
```python
python3 -c "from mazegen import ConfigGen, MazeGenerator; print('API import OK')"
```

### B.2.3. Quick API example

Toggle to Python interactive shell:
```bash
python
```

Test with example cfg demo:
```python
from mazegen import ConfigGen, MazeGenerator

cfg = ConfigGen(
    width=10,
    height=5,
    entry=(0, 0),
    exit=(9, 4),
    seed=42,
    perfect=True,
    marking_42=True,
)

gen = MazeGenerator(cfg)
maze = gen.generate()
coords = gen.solve_maze_path()
path_str = gen.coords_to_directions(coords)

print("coords:", coords[:5], "...")   # first few append as demo display
print("path:", path_str)
```

Notes:
- `coords_path` is a list of `(x, y)` coordinates from entry → exit.
- `path_str` is the same path encoded as directions (`N`, `E`, `S`, `W`).

---

# C. Resources

The following resources were used during the development of this project to
understand algorithms, data structures, and design decisions.

### C.1. Maze generation & graph traversal
- Invent with Python — *Maze generation algorithms*  
  https://inventwithpython.com/recursion/chapter11.html 
  Common maze generation approaches and the idea of perfect mazes.

- Python Official — *Maze creation in Python*  
  https://discuss.python.org/t/maze-creation-in-python/77030  
  How DFS works and how it can be applied to maze generation.

- Wikipedia — *Breadth-First Search (BFS)*  
  https://en.wikipedia.org/wiki/Breadth-first_search  
  Shortest-path guarantees in unweighted graphs.

### C.2. Python & Data Structures
- Python Official Documentation — *collections.deque*  
  https://docs.python.org/3/library/collections.html#collections.deque  
  Efficient queue operations in BFS.

- Python Official Documentation — *set*  
  https://docs.python.org/3/library/stdtypes.html#set  
  Efficiently track visited coordinates.

- Python Official Documentation — *random*  
  https://docs.python.org/3/library/random.html  
  Create deterministic maze generation via seeding.

- Python Official Documentation — *Stacks and Queues*  
  https://realpython.com/queue-in-python/  
  Understand the process of abstract data structures.

- W3 Schools — *Queues with Python*  
  https://realpython.com/queue-in-python/  
  Understand the process of abstract data structures.

- Medium article — *Stack and Queue Implementations*  
  https://medium.com/codex/understanding-stack-and-queue-implementations-in-python-a-theoretical-approach-e345e9c1362d  
  Understand stacks and queues.

- Datacamp — *Recursion in Python*  
  https://www.datacamp.com/tutorial/recursion-in-python  
  Understand the general concept of recursion in Python and the limitations.

- Real Python — *Recursion in Python*  
  https://realpython.com/python-recursion/  
  Understand the general concept of recursion in Python and the limitations.

---

# D. Future improvements

- Add generation/solving animations (DFS/BFS as generators + terminal rendering)
- Improve visualization (colors, optional UI modes)

---

# E. Final Notes

If you are new to DFS/BFS/graph traversal, this project is a nice place to practice.
