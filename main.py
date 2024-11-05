import tkinter as tk
from tkinter import messagebox

def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if arr[row][col] == 0:
                l[0] = row
                l[1] = col
                return True
    return False

def used_in_row(arr, row, num):
    for i in range(9):
        if arr[row][i] == num:
            return True
    return False

def used_in_col(arr, col, num):
    for i in range(9):
        if arr[i][col] == num:
            return True
    return False

def used_in_box(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if arr[i + row][j + col] == num:
                return True
    return False

def check_location_is_safe(arr, row, col, num):
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row % 3, col - col % 3, num)

def solve_sudoku(arr):
    l = [0, 0]
    if not find_empty_location(arr, l):
        return True
    row, col = l[0], l[1]
    for num in range(1, 10):
        if check_location_is_safe(arr, row, col, num):
            arr[row][col] = num
            if solve_sudoku(arr):
                return True
            arr[row][col] = 0
    return False

# GUI functions
def create_sudoku(grid):
    root = tk.Tk()
    root.title("SUDOKU PUZZLE")

    # Initialize the grid entries
    entries = []
    for row in range(9):
        row_entries = []
        for col in range(9):
            cell_value = grid[row][col]
            entry = tk.Entry(root, width=3, font=('Times New Roman', 15), justify='center', bd=3)
            entry.grid(row=row, column=col, padx=5, pady=5)
            if cell_value != 0:
                entry.insert(0, str(cell_value))
                entry.config(state='readonly')
            row_entries.append(entry)
        entries.append(row_entries)

    def solve_and_display():
        puzzle = [[int(entries[i][j].get()) if entries[i][j].get() else 0 for j in range(9)] for i in range(9)]
        if solve_sudoku(puzzle):
            for i in range(9):
                for j in range(9):
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, str(puzzle[i][j]))
                    entries[i][j].config(state='readonly')
        else:
            messagebox.showerror("Error", "No solution.")

    # Solve button
    solve_button = tk.Button(root, text="SOLVE", bd = 5, activebackground="Red", bg="Red", command=solve_and_display)
    solve_button.grid(row=9, column=0, columnspan=9, pady=10)

    root.mainloop()

def main():
    # Sudoku board with zeros as empty cells
    # sudoku_board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
    #                 [5, 2, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 8, 7, 0, 0, 0, 0, 3, 1],
    #                 [0, 0, 3, 0, 1, 0, 0, 8, 0],
    #                 [9, 0, 0, 8, 6, 3, 0, 0, 5],
    #                 [0, 5, 0, 0, 9, 0, 6, 0, 0],
    #                 [1, 3, 0, 0, 0, 0, 2, 5, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 7, 4],
    #                 [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    sudoku_board = [[9, 1, 3, 0, 0, 0, 5, 0, 0],
                    [6, 0, 7, 0, 0, 0, 0, 2, 4],
                    [0, 5, 0, 0, 8, 0, 0, 7, 0],
                    [0, 7, 9, 0, 0, 0, 0, 0, 0],
                    [0, 0, 2, 0, 9, 0, 0, 4, 3],
                    [0, 0, 0, 0, 0, 4, 0, 9, 0],
                    [0, 4, 0, 0, 0, 1, 9, 0, 0],
                    [7, 0, 6, 0, 0, 9, 0, 0, 5],
                    [0, 0, 1, 0, 0, 6, 4, 0, 7]]
    # sudoku_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    create_sudoku(sudoku_board)

if __name__ == "__main__":
    main()