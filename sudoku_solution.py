from __future__ import annotations

from sudoku_grid import SudokuGrid
from random import sample


class SudokuSolution(SudokuGrid):

    def __init__(self, sudoku_grid):
        super().__init__(sudoku_grid)
        self.available = [(i, j) for i in range(9) for j in range(9) if self.grid[i][j] == 0]
        self.counts = [9 for _ in range(10)]
        for _, row in enumerate(self.grid):
            for _, elem in enumerate(row):
                self.counts[elem] -= 1
        self.counts = self.counts[1:]
        self.fill_random()

    def __str__(self) -> str:
        return "\n".join([" ".join(map(lambda x: str(x), self.grid[i])) for i in range(9)])

    def fill_random(self):
        available_numbers_set = [i + 1 for i in range(len(self.counts)) for j in range(self.counts[i])]
        for (i, j), number in zip(self.available, available_numbers_set):
            self.grid[i][j] = number

        # sprawdzenie, czy faktycznie każda cyfra występuje 9 razy
        # counts = [0 for _ in range(9)]
        # for _, row in enumerate(self.grid):
        #     for _, elem in enumerate(row):
        #         counts[elem - 1] += 1
        # print(counts)

    def swap(self, x1, y1, x2, y2):
        self.put(x1, y1, self.get(x1, y1) + self.get(x2, y2))
        self.put(x2, y2, self.get(x1, y1) - self.get(x2, y2))
        self.put(x1, y1, self.get(x1, y1) - self.get(x2, y2))

    def create_neighbour(self) -> SudokuSolution:
        candidates = sample(self.available, 2)
        x1 = candidates[0][0]
        y1 = candidates[0][1]
        x2 = candidates[1][0]
        y2 = candidates[1][1]
        print(candidates)
        neighbour = SudokuSolution(SudokuGrid.copy_grid(self.grid))
        neighbour.swap(x1, y1, x2, y2)
        return neighbour
