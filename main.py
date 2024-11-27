import tkinter as tk
from collections import deque
import tkinter.messagebox
from tkinter import mainloop

# # Initialize the Sudoku sudoku_board (0 represents an empty cell)
sudoku_board = [
    [9, 1, 3, 0, 0, 0, 5, 0, 0],
    [6, 0, 7, 0, 0, 0, 0, 2, 4],
    [0, 5, 0, 0, 8, 0, 0, 7, 0],
    [0, 7, 9, 0, 0, 2, 0, 0, 0],
    [0, 0, 2, 0, 9, 0, 0, 4, 3],
    [0, 0, 0, 0, 0, 4, 0, 9, 0],
    [0, 4, 0, 0, 0, 1, 9, 0, 0],
    [7, 0, 6, 0, 0, 9, 0, 0, 5],
    [0, 0, 1, 0, 0, 6, 4, 0, 7]
]


# Initialize domains for each cell
domains = {}
for i in range(9):
    for j in range(9):
        if sudoku_board[i][j] != 0:  # If the cell already has a number
            domains[(i, j)] = {sudoku_board[i][j]}
        else:  # If the cell is empty
            domains[(i, j)] = set(range(1, 10))


def get_neighbors(row, col):
    neighbors = set()
    for i in range(9):
        if i != col:
            neighbors.add((row, i))
        if i != row:
            neighbors.add((i, col))
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if (i, j) != (row, col):
                neighbors.add((i, j))
    return neighbors

def ac3():
    queue = deque([(cell, neighbor) for cell in domains for neighbor in get_neighbors(*cell)])
    while queue:
        cell, neighbor = queue.popleft()
        if revise(cell, neighbor):
            if not domains[cell]:
                return False  # No solution possible
            for n in get_neighbors(*cell) - {neighbor}:
                queue.append((n, cell))
    return True


def revise(cell, neighbor):
    revised = False
    for value in domains[cell].copy():
        if not any(value != n_val for n_val in domains[neighbor]):
            domains[cell].remove(value)
            revised = True
    return revised


def backtrack():
    if all(len(domains[cell]) == 1 for cell in domains):
        return True
    cell = min((c for c in domains if len(domains[c]) > 1), key=lambda c: len(domains[c]))
    original_domains = {k: v.copy() for k, v in domains.items()}
    for value in domains[cell]:
        domains[cell] = {value}
        if ac3() and backtrack():
            return True
        domains.update(original_domains)  # Revert domains to original
    return False


def domains_to_sudoku_board():
    return [[next(iter(domains[(i, j)])) for j in range(9)] for i in range(9)]

# Tkinter GUI setup
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.build_grid()
        solve_button = tk.Button(self.root, text="SOLVE", bd=5, activebackground="Red", bg="Red", command=self.solve)
        solve_button.grid(row=10, column=0, columnspan=9, pady=10)

    def validate_sudoku_board(self):
        seen = set()
        for i in range(9):
            for j in range(9):
                value = self.cells[i][j].get()
                if value.isdigit():
                    value = int(value)
                    if value < 1 or value > 9:  # Check for out-of-range numbers
                        return False
                    if (i, value) in seen or (j + 9, value) in seen or (i // 3, j // 3, value) in seen:
                        return False  # Duplicate in row, column, or subgrid
                    seen.add((i, value))
                    seen.add((j + 9, value))
                    seen.add((i // 3, j // 3, value))
                elif value:
                    return False
        return True

    def build_grid(self):
        for i in range(9):
            for j in range(9):
                value = sudoku_board[i][j]
                cell = tk.Entry(self.root, width=3, font=('Times New Roman', 15), justify='center', bd=3)
                cell.grid(row=i, column=j, padx=5, pady=5)
                cell.insert(0, value if value != 0 else "")
                cell.config(state="readonly" if value != 0 else "normal")
                self.cells[i][j] = cell

    def solve(self):
        # Validate initial sudoku_board state
        if not self.validate_sudoku_board():
            tk.messagebox.showinfo("Sudoku Solver", "Invalid sudoku_board: no solution found.")
            return

        # Apply AC-3 and backtracking
        if ac3() and backtrack():
            solved_sudoku_board = domains_to_sudoku_board()
            for i in range(9):
                for j in range(9):
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, solved_sudoku_board[i][j])
                    self.cells[i][j].config(state="readonly")
        else:
            tk.messagebox.showinfo("Sudoku Solver", "No solution found.")


root = tk.Tk()
SudokuGUI(root)
root.mainloop()


