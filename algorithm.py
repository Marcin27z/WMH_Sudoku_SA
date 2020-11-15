from random import uniform
from math import exp

from full_board import FullBoard
from sudoku_solution import SudokuSolution


def algorithm():
    full_board = FullBoard()
    full_board.reduce_fields(20)
    #full_board = FullBoard.from_cache(67, 0)
    sudoku_solution = SudokuSolution.new(full_board.grid, True)

    mode = "random"

    if mode == "not random":
        sudoku_solution.fill_random()
    else:
        sudoku_solution.fill_regions()

    cost = sudoku_solution.cost()
    i = 0
    step = 0
    temperature = 0.99

    while cost > 0:
        if mode == "random":
            neighbour = sudoku_solution.create_neighbour()
        else:
            neighbour = sudoku_solution.create_neighbour_2()
        print(cost)
        if i % 100 == 0:
            print(cost)
        i += 1
        step += 1
        #zmiana temperatury co pewien krok lub bez pętli w każdym kroku
        if step == 2:
            temperature = uniform(0, 1) * temperature
            step = 0
        if neighbour.cost() < sudoku_solution.cost() or uniform(0,1) < exp(-(neighbour.cost()-sudoku_solution.cost())/temperature):
            sudoku_solution = neighbour
            cost = neighbour.cost()

    print('Liczba iteracji:' + str(i))
    print(sudoku_solution)
