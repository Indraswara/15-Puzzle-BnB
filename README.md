# 15-Puzzle-BnB

This Python script solves the classic 15-puzzle using a Branch and Bound algorithm with multiprocessing and a Manhattan distance heuristic. It's designed for simple instances of the 15-puzzle and may not handle highly complex configurations efficiently.
## Requirements
- Python 3.x
- Libraries: heapq, multiprocessing

## Usage
- Input Format: Provide a text file containing the initial configuration of the puzzle. Use numbers 1 through 15 and _ for the empty space (e.g., 1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 _).
- Run: Execute the script and input the path to your puzzle file when prompted.
- Output: The solution steps will be displayed if solvable, along with the time taken to solve the puzzle.

# Notes
- Complexity: This solver is suitable for simple instances of the 15-puzzle where solutions exist within a reasonable time frame. Highly complex configurations may not be handled efficiently.
- Performance: Utilizes multiprocessing for faster solving, leveraging multiple CPU cores.
- Heuristic: Uses Manhattan distance as a heuristic to estimate the distance to the goal state.

# Example
```
$ python puzzle_solver.py
```
```
Enter the path to the matrix file (or 'exit' to quit): ../data/puzzle.txt
Solvable
Generating solution...
1 2 3 4
5 6 _ 8
9 10 7 11
13 14 15 12

1 2 3 4
5 6 7 8
9 10 _ 11
13 14 15 12

1 2 3 4
5 6 7 8
9 10 11 _
13 14 15 12

Execution time: 0.1234 seconds
```
## Limitations
This solver assumes the input puzzles are solvable.
Highly complex or non-standard configurations may lead to unexpected behavior or long computation times.