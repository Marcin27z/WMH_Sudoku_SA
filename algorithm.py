from random import uniform
from math import exp

from full_board import FullBoard
from mode import Mode
from sudoku_solution import SudokuSolution

## Funkcja algorytmu symulowanego wyżarzania
#
#  @param args Przeparsowane argumenty z lini poleceń.
def algorithm(args):
    from_cache = bool(args["from_cache"])
    reduce_fields = int(args["reduce_fields"])
    mode = args["mode"]
    initial_temperature = int(args["temperature"])
    frequency = int(args["frequency"])
    cooling_factor = float(args["cooling_factor"])

    if from_cache:
        full_board = FullBoard.from_cache(81 - reduce_fields, int(args["board"]))
    else:
        full_board = FullBoard()
        full_board.reduce_fields(reduce_fields, save_to_cache=not bool(args["disable_cache"]))

    sudoku_solution = SudokuSolution.new(full_board)

    if mode == Mode.RANDOM:
        sudoku_solution.fill_random()
    else:
        sudoku_solution.fill_regions()

    cost = sudoku_solution.cost()
    i = 0
    step = 0

    old_cost = 1000
    no_improvements = 0

    temperature = initial_temperature
    accepted = 0
    all_time_best = sudoku_solution
    while cost > 0:
        if mode == Mode.RANDOM:
            neighbour = sudoku_solution.create_neighbour()
        else:
            neighbour = sudoku_solution.create_neighbour_2()

        # print(neighbour.difference(sudoku_solution))
        # print(cost)
        if i % frequency == 0:
            #print(f"Cost: {cost} Temperature: {temperature} Acceptance_ratio: {round(accepted/frequency * 100, ndigits=2)}%")
            temperature = temperature * cooling_factor
            accepted = 0
            no_improvements += 1

            if no_improvements == 500:
                temperature = initial_temperature
                #print("resetting")

        i += 1
        step += 1

        if neighbour.cost() <= sudoku_solution.cost() or \
                uniform(0, 1) < exp(-(neighbour.cost() - sudoku_solution.cost()) / temperature):
            accepted += 1
            sudoku_solution = neighbour
            if cost != neighbour.cost():
                no_improvements = 0
            cost = neighbour.cost()
            if sudoku_solution.cost() < all_time_best.cost():
                all_time_best = sudoku_solution

    print(sudoku_solution.is_correct())

    print('Liczba iteracji:' + str(i))
    print(sudoku_solution)
    return i
