from random import randint

from full_board import FullBoard
from sudoku_solution import SudokuSolution


def algorithm():
    full_board = FullBoard()
    full_board.reduce_fields(60)
    sudoku_solution = SudokuSolution.new(full_board.grid, False)

    mode = "random"

    if mode == "not random":
        sudoku_solution.fill_random()
    else:
        sudoku_solution.fill_regions()

    cost = sudoku_solution.cost()
    i = 0
    while cost != 0:
        if mode == "random":
            neighbour = sudoku_solution.create_neighbour()
        else:
            neighbour = sudoku_solution.create_neighbour_2()
        print(cost)
        if i % 100 == 0:
            print(cost)
        i += 1
        if neighbour.cost() < sudoku_solution.cost() or randint(0, 1000) < 5:
            sudoku_solution = neighbour
            cost = neighbour.cost()

    print(sudoku_solution)
