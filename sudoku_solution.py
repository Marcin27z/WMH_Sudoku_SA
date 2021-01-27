from __future__ import annotations

import random

import numpy as np

import math

from grid import Grid
from sudoku_grid import SudokuGrid
from random import sample


## Klasa przechowująca pojedyncze rozwiązanie sudoku.
#
#  Obiekt klasy tworzy oraz przechowuje pojedyncze rozwiązanie sudoku używane w algorytmie symulowanego wyżarzania.
#  Udostępnia metody używane przez algorytm symulowanego wyżarzania do liczenia kosztu i znajdowania sąsiada.
#  Proces tworzenia polega na stworzniu nowego obiektu z planszy z brakującymi polami,
#  a następnie wypełnieniu ich w sposób losowy.
class SudokuSolution(SudokuGrid):

    def __init__(self, sudoku_grid):
        super().__init__(sudoku_grid)
        self._available = []
        self._counts = []
        self._conflicts = []
        self._empty_in_regions = []
        self._conflicts_counts_in_regions = []
        self._mode_random = False

    ## Tworzenie obiektu reprezentującego rozwiązanie na podstawie SudokuGrid.
    #
    #  Funkcja pomocnicza do tworzenia nowego rozwiązania na podstawie istniejącej planszy sudoku w klasie SudokuGrid.
    #  Zapewnia poprawne ustawienie potrzebnych zmiennych prywatnych.
    @classmethod
    def new(cls, sudoku_grid: SudokuGrid):
        n = cls(sudoku_grid._grid)
        n._available = [(i, j) for i in range(9) for j in range(9) if n._grid[i][j] == 0]
        if len(n._available) == 1:
            print("cos nie dziala")
        n._counts = [9 for _ in range(10)]
        for _, row in enumerate(n._grid):
            for _, elem in enumerate(row):
                n._counts[elem] -= 1
        n._counts = n._counts[1:]
        return n

    ## Tworzenie obiektu reprezentujacego rozwiązanie jako kopia innego obiektu.
    #
    #  Funkcja pomocnicza do tworzenia nowego rozwiązania jako idealna kopia podanego rozwiązania.
    @classmethod
    def copy(cls, sudoku_solution: SudokuSolution):
        cp = cls(SudokuSolution.copy_grid(sudoku_solution._grid))
        cp._available = sudoku_solution._available
        cp._conflicts = cp._conflicts
        cp._counts = sudoku_solution._counts
        cp._empty_in_regions = sudoku_solution._empty_in_regions
        cp._conflicts_counts_in_regions = sudoku_solution._conflicts_counts_in_regions
        return cp

    ## Funkcja tworząca reprezentację tekstową rozwiązania.
    #
    #  Funkcja tworząca reprezentację tekstową rozwiązania jako liczby podzielone na 9 wierszy oddzielone spacjami.
    def __str__(self) -> str:
        return "\n".join([" ".join(map(lambda x: str(x), self._grid[i])) for i in range(9)])

    ## Funkcja wypełniająca puste pola w sposób całkowicie losowy.
    #
    #  Funkcja wypełniająca puste pola w sposób całkowicie losowy.
    #  Otrzymanie poprawnej planszy z takiego rozwiązania może nastąpić tylko w procesie generacji sąsiada o charakterze globalnym.
    def fill_random(self):
        available_numbers_set = [i + 1 for i in range(len(self._counts)) for j in range(self._counts[i])]
        for (i, j), number in zip(self._available, available_numbers_set):
            self._grid[i][j] = number
        self._mode_random = True
        self._conflicts = self._calculate_conflicts()

    ## Funkcja wypełniająca puste pola w sposób losowy, ale z zachowaniem poprawności w ramach jednego kwadratu 3x3.
    #
    #  Funkcja wypełniająca puste pola w sposób losowy, ale z zachowaniem poprawności w ramach jednego kwadratu 3x3.
    #  Otrzymanie poprawnej planszy z takiego rozwiązania może nastąpić w procesie generacji sąsiada o charakterze lokalnym - wystarczą zamiany w ramach pojedynczych kwadratów.
    def fill_regions(self):
        not_available_in_regions = []
        for i in range(3):
            for j in range(3):
                not_available_in_regions.append({self._grid[i * 3 + k][j * 3 + l] for k in range(3) for l in range(3) if
                                                 self._grid[i * 3 + k][j * 3 + l] != 0})
                self._empty_in_regions.append([(i * 3 + k, j * 3 + l) for k in range(3) for l in range(3) if
                                               self._grid[i * 3 + k][j * 3 + l] == 0])

        regions = [{j for j in range(1, 10)} for _ in range(9)]
        available_in_regions = [regions[i].difference(not_available_in_regions[i]) for i in range(9)]
        for i in range(9):
            for (x, y), number in zip(self._empty_in_regions[i], available_in_regions[i]):
                self._grid[x][y] = number
        self._mode_random = True
        self._conflicts = self._calculate_conflicts()

        # sprawdzenie, czy faktycznie każda cyfra występuje 9 razy
        # counts = [0 for _ in range(9)]
        # for _, row in enumerate(self.grid):
        #     for _, elem in enumerate(row):
        #         counts[elem - 1] += 1
        # print(counts)

    ## Funkcja licząca konflity w rozwiązaniu.
    #
    #  Funkcja dla każdego pola sprawdza, czy występująca w nim wartość występuje ponownie w tym samym wierszu lub tej
    #  samej kolumnie, lub tym samym kwadracie 3x3 i zlicza te wystąpnia. Trzeci warunek jest pomijany, gdy rozwiązanie
    #  zostało wygenerowane z zachowaniem poprawności kwadratów 3x3.
    def _calculate_conflicts(self) -> []:
        def duplicates_in_region(row: int, column: int, number: int) -> int:
            row_region_id = (row % 9 // 3) * 3
            column_region_id = (column % 9 // 3) * 3
            column_region_range = range(column_region_id, column_region_id + 3)
            row_region_range = range(row_region_id, row_region_id + 3)
            return sum([self._grid[i][j] == number for i in row_region_range for j in column_region_range]) - 1

        def duplicates_in_column(column: int, number: int) -> int:
            return sum([self._grid[i][column] == number for i in range(9)]) - 1

        def duplicates_in_row(row: int, number: int) -> int:
            return sum([self._grid[row][i] == number for i in range(9)]) - 1

        if self._mode_random:
            conflicts = [duplicates_in_row(i, self.get(i, j)) + duplicates_in_column(j, self.get(i, j)) + duplicates_in_region(i, j, self.get(i, j)) for (i, j) in self._available]
        else:
            conflicts = [duplicates_in_row(i, self.get(i, j)) + duplicates_in_column(j, self.get(i, j)) for (i, j) in
                         self._available]

        # regions_sizes = [0] + [len(region) for region in self.empty_in_regions]
        #
        # self.conflicts_counts_in_regions = \
        #     [sum(conflicts[regions_sizes[i]:regions_sizes[i + 1]]) for i in range(len(regions_sizes) - 1)]

        return conflicts

    def _swap(self, x1: int, y1: int, x2: int, y2: int):
        self.put(x1, y1, self.get(x1, y1) + self.get(x2, y2))
        self.put(x2, y2, self.get(x1, y1) - self.get(x2, y2))
        self.put(x1, y1, self.get(x1, y1) - self.get(x2, y2))
        self._conflicts = self._calculate_conflicts()
        if self.get(x1, y1) == 0 or self.get(x2, y2) == 0:
            print("tutaj")

    ## Funkcja tworząca sąsiada rozwiązania, które było wypełnione całkowicie losowe.
    #
    #  Charakter tworzenia sąsiada jest globalny.
    def create_neighbour(self) -> SudokuSolution:
        neighbour = SudokuSolution.copy(self)

        probabilities = list(map(lambda x: 1 - math.exp(-x), self._conflicts))
        sum_of_probabilities = sum(probabilities)
        probabilities = list(map(lambda x: x / sum_of_probabilities, probabilities))
        candidates = np.random.choice(range(len(self._available)), replace=False, p=probabilities, size=2)
        x1 = self._available[candidates[0]][0]
        y1 = self._available[candidates[0]][1]
        x2 = self._available[candidates[1]][0]
        y2 = self._available[candidates[1]][1]

        neighbour._swap(x1, y1, x2, y2)
        neighbour._mode_random = True
        return neighbour

    ## Funkcja tworząca sąsiada rozwiązania, które było stworzone z zachowaniem poprawności kwadratów 3x3.
    #
    #   Charakter tworzenia sąsiada jest lokalny.
    def create_neighbour_2(self) -> SudokuSolution:
        neighbour = SudokuSolution.copy(self)

        empty = list(self._empty_in_regions)
        # probabilities = list(map(lambda x: 1 - math.exp(-x), self.conflicts_counts_in_regions))
        # sum_of_probabilities = sum(probabilities)
        # probabilities = list(map(lambda x: x / sum_of_probabilities, probabilities))

        # empty, probabilities = zip(*(filter(lambda e: len(e[0]) >= 2, zip(empty, probabilities))))
        # empty = list(empty)
        empty = list(filter(lambda x: len(x) >= 2, empty))
        random.shuffle(empty)
        if len(empty) == 0:
            return neighbour
        candidates = empty[0]
        # candidates = np.random.choice(empty, replace=False, p=probabilities, size=1)[0]
        candidates = random.sample(candidates, k=2)
        x1 = candidates[0][0]
        y1 = candidates[0][1]
        x2 = candidates[1][0]
        y2 = candidates[1][1]

        neighbour._swap(x1, y1, x2, y2)
        return neighbour

    ## Funkcja licząca koszt rozwiązania.
    #
    #  Funkcja licząca koszt rozwiązania poprzez zsumowanie wszystkich wyliczonych konfliiktów. Wyliczone konflikty nie
    #  są liczone ponownie, jeżeli rozwiązanie się nie zmieniło.
    def cost(self) -> int:
        if not self._conflicts:
            self._conflicts = self._calculate_conflicts()
        return sum(self._conflicts)

    ## Alternatywan funkcja licząca koszt rozwiązania.
    #
    #  Funkcja licząca koszt rozwiązania poprzez zsumowanie wszystkich wyliczonych konfliiktów.
    def cost2(self) -> int:
        total_cost = 0
        for i, row in enumerate(self._grid):
            for j, elem in enumerate(row):
                backup = elem
                self._grid[i][j] = 0
                total_cost += self.region_contains(i, j, backup) + self.row_contains(j, backup) + self.column_contains(
                    i, backup)
                self._grid[i][j] = backup
        return total_cost

    ## Funkcja sprawdzająca poprawność rozwiązania.
    #
    #  Funkcja sprawdzająca poprawność rozwiązania.
    def is_correct(self) -> bool:
        if not self.is_grid_full:
            return False
        for i in range(9):
            if len(set(self.get_row(i))) != 9 or len(set(self.get_row(i))) != 9:
                return False
        return True
