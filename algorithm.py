from random import uniform
from math import exp

from full_board import FullBoard
from sudoku_solution import SudokuSolution


def algorithm():
    # full_board = FullBoard()
    # full_board.reduce_fields(55)
    full_board = FullBoard.from_cache(17, 0)
    sudoku_solution = SudokuSolution.new(full_board.grid, False)

    mode = "not random"

    if mode == "random":
        sudoku_solution.fill_random()
    else:
        sudoku_solution.fill_regions()

    cost = sudoku_solution.cost()
    i = 0
    step = 0
    temperature = 20
    old_cost = 1000
    no_improvements = 0

    while cost > 0:
        if mode == "random":
            neighbour = sudoku_solution.create_neighbour()
        else:
            neighbour = sudoku_solution.create_neighbour_2()

        # print(neighbour.difference(sudoku_solution))
        # print(cost)
        if i % 100 == 0:
            print(cost)
            temperature = temperature * 0.999
            no_improvements += 1

            # if no_improvements == 100:
            #     temperature = 0.99
            #     print("resetting")

        i += 1
        step += 1

        if neighbour.cost() <= sudoku_solution.cost() or \
                uniform(0, 1) < exp(-(neighbour.cost() - sudoku_solution.cost()) / temperature):
            sudoku_solution = neighbour
            if cost != neighbour.cost():
                no_improvements = 0
            cost = neighbour.cost()

    print(sudoku_solution.is_correct())

    print('Liczba iteracji:' + str(i))
    print(sudoku_solution)
