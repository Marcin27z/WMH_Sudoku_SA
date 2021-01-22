from algorithm import algorithm
from sudoku_grid import SudokuGrid
import argparse

if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    ap.add_argument("-fc", "--fromcache",   required=True,  help="'1' if file from cache ")
    ap.add_argument("-b",  "--board",       required=False, help="board number")
    ap.add_argument("-r",  "--reducefield", required=True,  help="number of reduced fields on board")
    ap.add_argument("-m",  "--mode",        required=False, help="random or not random")
    ap.add_argument("-t",  "--temperature", required=True,  help="starting temperature")
    ap.add_argument("-f",  "--frequency",   required=True,  help="frequency of temperature changes")

    args = vars(ap.parse_args())
    print(args)
    algorithm(args)
