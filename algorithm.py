from full_board import FullBoard
from sudoku_solution import SudokuSolution


def algorithm():
    full_board = FullBoard()
    full_board.reduce_fields(15)
    sudoku_solution = SudokuSolution(full_board.grid)
    print(sudoku_solution)
    print()
    # print(sudoku_solution.create_neighbour())

    cost = sudoku_solution.cost()
    i = 0
    while cost != 0:
        neighbour = sudoku_solution.create_neighbour()
        # print(sudoku_solution)
        # print(sudoku_solution.difference(neighbour))
        if i % 10 == 0:
            print(cost)
        i += 1
        if neighbour.cost() < sudoku_solution.cost():
            sudoku_solution = neighbour

    print(sudoku_solution)
