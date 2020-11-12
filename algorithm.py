from full_board import FullBoard
from sudoku_solution import SudokuSolution


def algorithm():
    full_board = FullBoard()
    full_board.reduce_fields(15)
    sudoku_solution = SudokuSolution(full_board.grid)
    print(sudoku_solution)
    print()
    print(sudoku_solution.create_neighbour())
