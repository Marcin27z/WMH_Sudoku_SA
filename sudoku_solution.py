from __future__ import annotations

import random

import numpy as np

import math

from grid import Grid
from sudoku_grid import SudokuGrid
from random import sample


class SudokuSolution(SudokuGrid):

    def __init__(self, sudoku_grid):
        super().__init__(sudoku_grid)
        self.available = []
        self.counts = []
        self.conflicts = []
        self.empty_in_regions = []
        self.conflicts_counts_in_regions = []
        self.mode_random = False

    @classmethod
    def new(cls, sudoku_grid):
        n = cls(sudoku_grid)
        n.available = [(i, j) for i in range(9) for j in range(9) if n.grid[i][j] == 0]
        if len(n.available) == 1:
            print("cos nie dziala")
        n.counts = [9 for _ in range(10)]
        for _, row in enumerate(n.grid):
            for _, elem in enumerate(row):
                n.counts[elem] -= 1
        n.counts = n.counts[1:]
        return n

    @classmethod
    def copy(cls, sudoku_solution: SudokuSolution):
        cp = cls(SudokuSolution.copy_grid(sudoku_solution.grid))
        cp.available = sudoku_solution.available
        cp.conflicts = cp.conflicts
        cp.counts = sudoku_solution.counts
        cp.empty_in_regions = sudoku_solution.empty_in_regions
        cp.conflicts_counts_in_regions = sudoku_solution.conflicts_counts_in_regions
        return cp

    def __str__(self) -> str:
        return "\n".join([" ".join(map(lambda x: str(x), self.grid[i])) for i in range(9)])

    def fill_random(self):
        available_numbers_set = [i + 1 for i in range(len(self.counts)) for j in range(self.counts[i])]
        for (i, j), number in zip(self.available, available_numbers_set):
            self.grid[i][j] = number
        self.conflicts = self.calculate_conflicts()
        self.mode_random = True

    def fill_regions(self):
        not_available_in_regions = []
        for i in range(3):
            for j in range(3):
                not_available_in_regions.append({self.grid[i * 3 + k][j * 3 + l] for k in range(3) for l in range(3) if self.grid[i * 3 + k][j * 3 + l] != 0})
                self.empty_in_regions.append([(i * 3 + k, j * 3 + l) for k in range(3) for l in range(3) if self.grid[i * 3 + k][j * 3 + l] == 0])

        regions = [{j for j in range(1, 10)} for _ in range(9)]
        available_in_regions = [regions[i].difference(not_available_in_regions[i]) for i in range(9)]
        for i in range(9):
            for (x, y), number in zip(self.empty_in_regions[i], available_in_regions[i]):
                self.grid[x][y] = number
        self.conflicts = self.calculate_conflicts()
        self.mode_random = False

        # sprawdzenie, czy faktycznie każda cyfra występuje 9 razy
        # counts = [0 for _ in range(9)]
        # for _, row in enumerate(self.grid):
        #     for _, elem in enumerate(row):
        #         counts[elem - 1] += 1
        # print(counts)

    def calculate_conflicts(self) -> []:
        def duplicates_in_region(row: int, column: int, number: int) -> int:
            row_region_id = (row % 9 // 3) * 3
            column_region_id = (column % 9 // 3) * 3
            column_region_range = range(column_region_id, column_region_id + 3)
            row_region_range = range(row_region_id, row_region_id + 3)
            return sum([self.grid[i][j] == number for i in row_region_range for j in column_region_range]) - 1

        def duplicates_in_column(column: int, number: int) -> int:
            return sum([self.grid[i][column] == number for i in range(9)]) - 1

        def duplicates_in_row(row: int, number: int) -> int:
            return sum([self.grid[row][i] == number for i in range(9)]) - 1

        if self.mode_random:
            conflicts = [duplicates_in_row(i, self.get(i, j)) + duplicates_in_column(j, self.get(i, j)) + duplicates_in_region(i, j, self.get(i, j)) for (i, j) in self.available]
        else:
            conflicts = [duplicates_in_row(i, self.get(i, j)) + duplicates_in_column(j, self.get(i, j)) for (i, j) in self.available]

        # regions_sizes = [0] + [len(region) for region in self.empty_in_regions]
        #
        # self.conflicts_counts_in_regions = \
        #     [sum(conflicts[regions_sizes[i]:regions_sizes[i + 1]]) for i in range(len(regions_sizes) - 1)]

        return conflicts

    def swap(self, x1, y1, x2, y2):
        self.put(x1, y1, self.get(x1, y1) + self.get(x2, y2))
        self.put(x2, y2, self.get(x1, y1) - self.get(x2, y2))
        self.put(x1, y1, self.get(x1, y1) - self.get(x2, y2))
        self.conflicts = self.calculate_conflicts()
        if self.get(x1, y1) == 0 or self.get(x2, y2) == 0:
            print("tutaj")

    def create_neighbour(self) -> SudokuSolution:
        neighbour = SudokuSolution.copy(self)

        probabilities = list(map(lambda x: 1 - math.exp(-x), self.conflicts))
        sum_of_probabilities = sum(probabilities)
        probabilities = list(map(lambda x: x / sum_of_probabilities, probabilities))
        candidates = np.random.choice(range(len(self.available)), replace=False, p=probabilities, size=2)
        x1 = self.available[candidates[0]][0]
        y1 = self.available[candidates[0]][1]
        x2 = self.available[candidates[1]][0]
        y2 = self.available[candidates[1]][1]

        neighbour.swap(x1, y1, x2, y2)
        neighbour.mode_random = True
        return neighbour

    def create_neighbour_2(self) -> SudokuSolution:
        neighbour = SudokuSolution.copy(self)

        empty = list(self.empty_in_regions)
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

        neighbour.swap(x1, y1, x2, y2)
        return neighbour

    def cost(self) -> int:
        if not self.conflicts:
            self.conflicts = self.calculate_conflicts()
        return sum(self.conflicts)

    def cost2(self) -> int:
        total_cost = 0
        for i, row in enumerate(self.grid):
            for j, elem in enumerate(row):
                backup = elem
                self.grid[i][j] = 0
                total_cost += self.region_contains(i, j, backup) + self.row_contains(j, backup) + self.column_contains(i, backup)
                self.grid[i][j] = backup
        return total_cost

    def is_correct(self) -> bool:
        if not self.is_grid_full:
            return False
        for i in range(9):
            if len(set(self.get_row(i))) != 9 or len(set(self.get_row(i))) != 9:
                return False
        return True
